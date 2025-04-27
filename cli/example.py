from controller.actions.base import BaseAction
from controller.actions.const import ActionKeyword
from tasks import trigger_task

# data
telegram_message = {
    "update_id": 711525474,
    "message": {
        "message_id": 16,
        "from": {
            "id": 415232232,
            "is_bot": False,
            "first_name": "Кирилл",
            "last_name": "Баяндин",
            "username": "kirillbayandin",
            "language_code": "en",
        },
        "chat": {
            "id": 415232232,
            "first_name": "Кирилл",
            "last_name": "Баяндин",
            "username": "kirillbayandin",
            "type": "private",
        },
        "date": 1744909300,
        "text": "Hallo",
    },
}

telegram_message_jsonschema = {
    "type": "object",
    "required": [],
    "properties": {
        "update_id": {"type": "number"},
        "message": {
            "type": "object",
            "required": [],
            "properties": {
                "message_id": {"type": "number"},
                "from": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "id": {"type": "number"},
                        "is_bot": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "username": {"type": "string"},
                        "language_code": {"type": "string"},
                    },
                },
                "chat": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "id": {"type": "number"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "username": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
                "date": {"type": "number"},
                "text": {"type": "string"},
            },
        },
    },
}

# triggers
triggers_types = [
    {
        "id": "tg_bot_new_msg",
        "name": "Telegram new message",
        "output": telegram_message_jsonschema,
    },
]
triggers = [
    {"id": "t1"},
]

interface_tjs = {  # transform jsonschema
    "type": "object",
    "required": [],
    "properties": {
        "text": {"type": "string", "_source": "$.message.text"},
    },
}

api_response_jsonschema = {
    "type": "object",
    "required": [],
    "properties": {
        "result": {
            "type": "object",
            "required": [],
            "properties": {
                "alternatives": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [],
                        "properties": {
                            "message": {
                                "type": "object",
                                "required": [],
                                "properties": {
                                    "role": {"type": "string"},
                                    "text": {"type": "string"},
                                },
                            },
                            "status": {"type": "string"},
                        },
                    },
                },
                "usage": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "inputTextTokens": {"type": "string"},
                        "completionTokens": {"type": "string"},
                        "totalTokens": {"type": "string"},
                        "completionTokensDetails": {
                            "type": "object",
                            "required": [],
                            "properties": {"reasoningTokens": {"type": "string"}},
                        },
                    },
                },
                "modelVersion": {"type": "string"},
            },
        }
    },
}

get_answer_tjs = {  # transform jsonschema
    "type": "object",
    "required": [],
    "properties": {
        "text": {
            "type": "string",
            "_source": "$.result.alternatives[0].message.text",
        },
    },
}

telegram_send_msg_response_jsonschema = {
    "type": "object",
    "required": [],
    "properties": {
        "ok": {"type": "boolean"},
        "result": {
            "type": "object",
            "required": [],
            "properties": {
                "message_id": {"type": "number"},
                "from": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "id": {"type": "number"},
                        "is_bot": {"type": "boolean"},
                        "first_name": {"type": "string"},
                        "username": {"type": "string"},
                    },
                },
                "chat": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "id": {"type": "number"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "username": {"type": "string"},
                        "type": {"type": "string"},
                    },
                },
                "date": {"type": "number"},
                "text": {"type": "string"},
            },
        },
    },
}

# actions
actions = {
    ActionKeyword.INIT_STEP: {
        ActionKeyword.TYPE: "empty",
        ActionKeyword.NEXT: "2",
    },
    "2": {
        "name": "Interface",
        ActionKeyword.TYPE: "transform",
        "input": telegram_message_jsonschema,
        "output": interface_tjs,
        ActionKeyword.NEXT: "3",
    },
    "3": {
        "name": "AI response",
        ActionKeyword.TYPE: "http_request",
        "input": interface_tjs,
        "params": {},
        "output": api_response_jsonschema,
        ActionKeyword.NEXT: "4",
    },
    "4": {
        "name": "Extract answer",
        ActionKeyword.TYPE: "transform",
        "input": api_response_jsonschema,
        "output": get_answer_tjs,
        ActionKeyword.NEXT: "5",
    },
    "5": {
        "name": "Send msg to tg",
        ActionKeyword.TYPE: "http_request",
        "input": get_answer_tjs,
        "params": {},
        "output": telegram_send_msg_response_jsonschema,
    },
}


from database.db import DatabaseStore

DatabaseStore.action.upsert("proc0", actions)

_input_key = "example_only"
BaseAction.save_output_by_key(_input_key, telegram_message)
trigger_task.call_local(_input_key, "proc0", _call_local=True)
