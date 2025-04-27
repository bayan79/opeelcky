from controller.actions.base import BaseAction


class EmptyAction(BaseAction):
    @classmethod
    def action_type(cls) -> str:
        return "empty"

    def execute_task(self, _input: dict):
        return _input
