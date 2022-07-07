import typing

from fastapi.responses import JSONResponse


class CustomJSONResp(JSONResponse):
    _resp_body: dict = {}

    def __init__(self, data: typing.Dict = None, status_code: int = 200, **kwargs):
        status = "success" if status_code == 200 else "error"

        self._resp_body['status'] = status
        self._resp_body['status_code'] = status_code

        if data:
            self._resp_body['data'] = data

        super().__init__(
            content=self._resp_body,
            status_code=status_code,
            **kwargs
        )
