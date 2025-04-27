from controller.actions.base import BaseAction
from controller.transformer import DataTransformer


class TransformAction(BaseAction):
    @classmethod
    def action_type(cls):
        return "transform"

    def execute_task(self, _input: dict) -> dict:
        print("_input:", _input)
        print("_output:", self.action_args.step_config)

        transformer = DataTransformer(_input)
        result = transformer.transform_to(self.output_schema)

        print("_result:", result)
        return result
