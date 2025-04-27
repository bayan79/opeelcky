import pickle
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from database.db import DatabaseStore
from database.redis import redis_store

from .const import ActionKeyword


@dataclass
class ActionArgs:
    run_id: str
    process_id: str
    step_id: str
    step_config: dict

    @property
    def action_type(self):
        return self.step_config[ActionKeyword.TYPE]

    @classmethod
    def load(cls, run_id: str, process_id: str, step_id: str):
        action_process = DatabaseStore.action.get_by_key(process_id)
        if action_process is None:
            raise KeyError(process_id)

        _step = action_process[step_id]
        return cls(
            run_id=run_id, process_id=process_id, step_id=step_id, step_config=_step
        )

    # def encode(self):
    #     return b64encode(pickle.dumps(self)).decode()
    #     # return f"{self.process_id}:{self.step_id}:{self.run_id}"

    # @classmethod
    # def decode(cls, obj: str):
    #     return pickle.loads(b64decode(obj.encode()))

    @property
    def next_step_id(self) -> Optional[str]:
        return self.step_config.get(ActionKeyword.NEXT)

    def get_step_input_key(self, step_id: str) -> str:
        return "|".join(
            [
                "in",
                self.run_id,
                self.process_id,
                step_id,
            ],
        )

    @property
    def current_step_input_key(self):
        return self.get_step_input_key(self.step_id)


class BaseAction:
    __registered: Dict[str, Type["BaseAction"]] = {}

    def __init__(self, action_args: ActionArgs):
        self.action_args = action_args

    # registry

    @classmethod
    def load_action_type(cls, action_type: str):
        return cls.__registered[action_type]

    @classmethod
    def action_type(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def register(cls):
        cls.__registered[cls.action_type()] = cls

    @classmethod
    def __init_subclass__(cls):
        cls.register()

    # action
    @property
    def input_schema(self) -> dict:
        return self.action_args.step_config["input"]

    @property
    def output_schema(self) -> dict:
        return self.action_args.step_config["output"]

    @classmethod
    def load_input_by_key(cls, _input_key: str):
        _input = redis_store.get(_input_key)
        if _input is None:
            raise KeyError(_input_key)
        if not isinstance(_input, bytes):
            raise TypeError
        return pickle.loads(_input)

    def load_input(self):
        return self.load_input_by_key(self.action_args.current_step_input_key)

    def save_output(self, output: dict) -> Optional[str]:
        if self.action_args.next_step_id is None:
            return
        _key = self.action_args.get_step_input_key(self.action_args.next_step_id)
        self.save_output_by_key(_key=_key, output=output)
        return _key

    @classmethod
    def save_output_by_key(cls, _key: str, output: Any):
        redis_store.set(_key, pickle.dumps(output), ex=3600)

    def execute_task(self, _input: dict) -> dict:
        raise NotImplementedError

    def execute(self):  # output key
        _input = self.load_input()

        _output = self.execute_task(_input)
        self.save_output(_output)
