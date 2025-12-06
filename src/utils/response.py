from dataclasses import asdict, is_dataclass
from typing import Any
from fastapi.responses import ORJSONResponse as Response
from fastapi import status as ResponseStatus
from fastapi.encoders import jsonable_encoder

def _normalize_payload(data: Any) -> Any:
    if data is None:
        return {}
    if hasattr(data, "to_py"):
        return data.to_py()
    data = jsonable_encoder(data)
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
