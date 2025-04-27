from uuid import uuid4

from controller.actions import ActionArgs, ActionKeyword, BaseAction
from controller.huey_controller import huey


@huey.task()
def trigger_task(_input_key: str, process_id: str, _call_local: bool = False):
    run_id = uuid4().hex
    action_args = ActionArgs.load(
        run_id,
        "proc0",
        ActionKeyword.INIT_STEP,
    )
    BaseAction.save_output_by_key(
        _key=action_args.current_step_input_key,
        output=BaseAction.load_input_by_key(_input_key),
    )
    if _call_local:
        main_task.call_local(
            run_id,
            process_id,
            ActionKeyword.INIT_STEP,
            _call_local=_call_local,
        )
    else:
        main_task(run_id, process_id, ActionKeyword.INIT_STEP, _call_local=_call_local)


@huey.task()
def main_task(
    run_id: str,
    process_id: str,
    step_id: str = ActionKeyword.INIT_STEP,
    _call_local: bool = False,
):
    action_args = ActionArgs.load(
        run_id=run_id,
        process_id=process_id,
        step_id=step_id,
    )
    action = BaseAction.load_action_type(action_args.action_type)(
        action_args=action_args
    )
    action.execute()

    _next_step = action_args.next_step_id
    if _next_step is not None:
        kwargs = dict(
            run_id=run_id,
            process_id=process_id,
            step_id=_next_step,
            _call_local=_call_local,
        )
        if _call_local:
            main_task.call_local(**kwargs)
        else:
            main_task(**kwargs)
