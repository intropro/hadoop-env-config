from setuptools import setup

setup(
    name='hadoop-env-config',
    version='0.2.2',
    py_modules=['hadoop_env_config'],
    entry_points='''
        [console_scripts]
        hadoop-env-config=hadoop_env_config.main:run
    ''',
)
