import os

import pytest
from pytest_django.live_server_helper import LiveServer

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture
def browser_context_args(live_server: LiveServer):
    return {"base_url": live_server.url}

