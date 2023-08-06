import json

import requests_mock  # type: ignore

from .servicemock import ExpectedRequests


class UnexpectedRequest(requests_mock.NoMockAddress):

    def __str__(self) -> str:
        requests = ExpectedRequests.get_requests_not_made()

        try:
            text_body = None
            json_body = self.request.json()
        except (TypeError, json.JSONDecodeError):
            text_body = self.request.text
            json_body = None

        msg = f"Received unexpected request '{self.request.method} {self.request.url}, headers: {self.request.headers}'"
        if json_body:
            msg = msg + f', json: {json_body}'

        if text_body:
            msg = msg + f', text: {text_body}'

        message = f"{msg}.\nExpected requests are:\n  - "
        return message + "\n  - ".join([str(r) for r in requests])


class Adapter(requests_mock.Adapter):

    def send(self, request, **kwargs):
        try:
            return super().send(request, **kwargs)
        except requests_mock.NoMockAddress as e:
            raise UnexpectedRequest(e.request)


class Mocker(requests_mock.Mocker):

    def __init__(self, *args, **kwargs):
        # TODO: If somebody is giving adapter, raise not possible
        kwargs['adapter'] = Adapter()
        super().__init__(*args, **kwargs)
