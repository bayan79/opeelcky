from jsonpath_ng.ext import parse

from exceptions.crud import NotFound

from .const import Const


class DataTransformer:
    def __init__(self, source_data: dict | list):
        self.data = source_data

    def parse_int(self, _value: dict) -> int:
        _static_value = _value.get(Const.STATIC_VALUE)
        if isinstance(_static_value, int):
            return _static_value

        _default = _value.get(Const.DEFAULT_VALUE)

        _source = _value.get(Const.SOURCE_PATH)
        match _source:
            case None:
                if _default is None:
                    raise ValueError("_default not set")
                return int(_default)
            case str():
                json_expr = parse(_source)
                if res := json_expr.find(self.data):
                    _item = res[0].value
                    return int(_item)
                raise NotFound
            case _:
                raise ValueError(f"unknown int source: {_source}")

    def parse_str(self, _value: dict) -> str:
        _static_value = _value.get(Const.STATIC_VALUE)
        if isinstance(_static_value, str):
            return _static_value

        _default = _value.get(Const.DEFAULT_VALUE)

        _source = _value.get(Const.SOURCE_PATH)
        match _source:
            case None:
                print(_value)
                if _default is None:
                    # import pudb; pudb.set_trace()
                    raise ValueError("_default not set")
                return str(_default)
            case str():
                json_expr = parse(_source)
                if res := json_expr.find(self.data):
                    _item = res[0].value
                    return str(_item)
                raise NotFound
            case _:
                raise ValueError(f"unknown int source: {_source}")

    def parse(self, _item: dict | list | str | int | float | bool | None) -> dict:
        _result = {}
        if isinstance(_item, dict):
            _type: str = _item["type"]
            for _k, _v in _item.get("properties", {}).items():
                if isinstance(_v, dict):
                    _prop_type: str = _v["type"]
                    match _prop_type:
                        case Const.Types.OBJECT:
                            _result[_k] = self.parse(_v)
                        case Const.Types.INT:
                            _result[_k] = self.parse_int(_v)
                        case Const.Types.STR:
                            _result[_k] = self.parse_str(_v)
        return _result

    def transform_to(self, schema: dict):
        return self.parse(schema)
