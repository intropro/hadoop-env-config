import os
import pytest

from hadoop_env_config import common


def get_abspath_test_path():

    return os.path.dirname(os.path.abspath(__file__))

def get_conf_dirs_path():

    return os.path.join(get_abspath_test_path(), 'resources/conf-dirs/')


@pytest.fixture(params=['cdh-with-server.settings', 'cdh-wo-server.settings'])
def settings_path(request):
    path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(path, 'resources/settings/', request.param)


def test_config_builder_init():

    builder = common.ConfigBuilder(get_conf_dirs_path())


def test_config_builder_hdp228_config():

    conf_path = os.path.join(get_conf_dirs_path(), 'hdp-2.2.8')
    config = common.ConfigBuilder(conf_path).config

    assert isinstance(config, dict) and len(config) != 0
