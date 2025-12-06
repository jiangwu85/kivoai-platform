from dataclasses import asdict, is_dataclass
from typing import Any
from fastapi.responses import ORJSONResponse as Response
from fastapi import status as ResponseStatus

def _normalize_payload(data: Any) -> Any:
    if data is None:
        return {}
    if is_dataclass(data):
        return asdict(data)
    if hasattr(data, "model_dump"):
        return data.model_dump()
    if hasattr(data, "dict"):
        return data.dict()
    if isinstance(data, (set, tuple)):
        return list(data)
    return data

class SuccessResponse(Response):
    def __init__(
            self,
            data=None,
            msg="success",
            code=ResponseStatus.HTTP_200_OK,
            status=ResponseStatus.HTTP_200_OK,
            **kwargs
    ):
        payload = _normalize_payload(data)
        body = {
            "code": code,
            "message": msg,
            "data": payload,
        }
        body.update(kwargs)
        super().__init__(content=body, status_code=status)

class ErrorResponse(Response):
    def __init__(
            self,
            msg=None,
            code=ResponseStatus.HTTP_400_BAD_REQUEST,
            status=ResponseStatus.HTTP_200_OK,
            **kwargs
    ):
        body = {
            "code": code,
            "message": msg,
        }
        body.update(kwargs)
        super().__init__(content=body, status_code=status)
