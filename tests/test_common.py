import os
import pytest

from hadoop_env_config.common import create_env_props

@pytest.fixture(params=['cdh-with-server.settings', 'cdh-wo-server.settings'])
def settings_path(request):
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, 'resources/settings/', request.param)
