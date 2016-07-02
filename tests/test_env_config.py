import os
import pytest

from hadoop_env_config import env_config

def get_abspath_test_path():

    return os.path.dirname(os.path.abspath(__file__))

def get_settings_path():

    return os.path.join(get_abspath_test_path(), 'resources/settings/')

def get_configs_path():

    return os.path.join(get_abspath_test_path(), 'resources/conf-dirs/')


@pytest.fixture(params=['hdp-with-server.settings', 'hdp-wo-server.settings'])
def hdp_settings_path(request):

    return os.path.join(get_settings_path(), request.param)


@pytest.fixture(params=['hdp-with-server.settings', 'hdp-wo-server.settings'])
def hdp_settings_path(request):

    return os.path.join(get_settings_path(), request.param)


def test_env_config_undefined_settings():

    with pytest.raises(env_config.UndefinedSettingsFile):
        conf = env_config.HadoopEnvConfig(None)


def test_env_config_empty_settings():

    with pytest.raises(env_config.IncorrectJsonFormat):
        conf = env_config.HadoopEnvConfig(os.path.join(get_settings_path(), 'empty.settings'))

def test_env_config_incorrect_path_to_settings():

    with pytest.raises(env_config.IncorrectJsonFormat):
        conf = env_config.HadoopEnvConfig(os.path.join(get_settings_path(), 'shadow.settings'))


def test_hadoop_env_config(hdp_settings_path):

    conf = env_config.HadoopEnvConfig(hdp_settings_path)
    conf.settings['config-dir'] = os.path.join(get_configs_path(), 'hdp-2.2.8/')
    env_props = conf.parse()

    assert isinstance(env_props, dict) and len(env_props) != 0
    assert 'oozieServer' in env_props and env_props['oozieServer'] == 'http://oozie.bigdata.hosts:11000'
    assert 'jobTracker' in env_props and env_props['jobTracker'] == 'yarn.bigdata.hosts:8050'
    assert 'nameNode' in env_props and env_props['nameNode'] == 'hdfs://nn.bigdata.hosts:8020'

    assert 'sshUserName' in env_props and env_props['sshUserName'] == 'username'
    assert 'sshPassword' in env_props and env_props['sshPassword'] == 'password'
    
