# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2021/10/19 15:47
# @File           : exception.py
# @IDE            : PyCharm
# @desc           : Global exception handling

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
import traceback

class CustomException(Exception):

    def __init__(self, msg: str, code: int = status.HTTP_400_BAD_REQUEST, desc: str = None):
        self.msg = msg
        self.desc = desc
        self.code = code


def register_exception(app: FastAPI):
    """
    Exception interception
    """

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        """
        Custom exception handler
        """
        print("Request URL", request.url.__str__())
        print("Caught overridden CustomException: custom_exception_handler")
        print(exc.desc)
        print(exc.msg)
        return JSONResponse(
            status_code=200,
            content={"message": exc.msg, "code": exc.code},
        )

    @app.exception_handler(StarletteHTTPException)
    async def unicorn_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Override HTTPException handler
        """
        print("Request URL", request.url.__str__())
        print("Caught overridden HTTPException: unicorn_exception_handler")
        print(exc.detail)
        return JSONResponse(
            status_code=200,
            content={
                "code": status.HTTP_400_BAD_REQUEST,
                "message": exc.detail,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Override request validation handler
        """
        print("Request URL", request.url.__str__())
        print("Caught validation exception: validation_exception_handler")
        print(exc.errors())
        msg = exc.errors()[0].get("msg")
        if msg == "field required":
            msg = "Request failed, missing required field!"
        elif msg == "value is not a valid list":
            print(exc.errors())
            msg = "Type error, payload must be a list!"
        elif msg == "value is not a valid int":
            msg = "Type error, payload must be an integer!"
        elif msg == "value could not be parsed to a boolean":
            msg = "Type error, payload must be a boolean!"
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "message": msg,
                    "body": exc.body,
                    "code": status.HTTP_400_BAD_REQUEST
                }
            ),
        )

    @app.exception_handler(ValueError)
    async def value_exception_handler(request: Request, exc: ValueError):
        """
        Capture ValueError
        """
        print("Request URL", request.url.__str__())
        print("Caught ValueError: value_exception_handler")
        print(exc.__str__())
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(
                {
                    "message": exc.__str__(),
                    "code": status.HTTP_400_BAD_REQUEST
                }
            ),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        Capture all remaining exceptions
        """
        print("Request URL", request.url.__str__())
        print("Caught global exception: all_exception_handler")
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {
                    "message":  exc.__str__(),
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            ),
        )
