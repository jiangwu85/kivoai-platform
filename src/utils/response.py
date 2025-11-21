from fastapi.responses import ORJSONResponse as Response
from fastapi import status as ResponseStatus


class SuccessResponse(Response):
    """
    成功响应
    """

    def __init__(
            self,
            data=None,
            msg="success",
            code=ResponseStatus.HTTP_200_OK,
            status=ResponseStatus.HTTP_200_OK,
            **kwargs
    ):
        self.data = {
            "code": code,
            "message": msg,
            "data": data,
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)


class ErrorResponse(Response):
    """
    失败响应
    """

    def __init__(self, msg=None, code=ResponseStatus.HTTP_400_BAD_REQUEST, status=ResponseStatus.HTTP_200_OK, **kwargs):
        self.data = {
            "code": code,
            "message": msg
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)
