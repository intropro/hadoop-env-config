import json
import settings as settings_mod

import cdh
from common import create_env_props


class IncorrectJsonFormat(Exception):
    pass

class UndefinedSettingsFile(Exception):
    pass

class EmptyMappingFile(Exception):
    pass

class EmptyPlatformName(Exception):
    pass

class MissingMandatoryParameter(Exception):
    pass


CDH4X_PLATFORMS = ['CDH46', 'CDH47', ]
CDH5X_PLATFORMS = ['CDH51', 'CDH52', 'CDH53',]
CDH_PLATFORMS = CDH4X_PLATFORMS + CDH5X_PLATFORMS
CDH_MANDATORY_PARAMETERS = [
    'cdh-gateway-http-protocol',
    'cdh-gateway-hostname',
    'cdh-gateway-port',
    'cdh-cluster-name',
    'cdh-gateway-username',
    'cdh-gateway-password',
    'config-dir'
]

HDP2X_PLATFORMS = ['HDP22', 'HDP23', 'HDP24', 'HDP25', 'HDP26']

KNOWN_HADOOP_PLATFORMS = CDH_PLATFORMS + HDP2X_PLATFORMS


class HadoopEnvConfig(object):

    def __init__(self, settings, mapping=None):

        if settings:
            self.settings = self.prepare_settings(self.get_json_content(settings))
        else:
            raise UndefinedSettingsFile(settings)

        if mapping:
            self.mapping = self.get_json_content(mapping)
        else:
            if self.settings['platform'] in CDH4X_PLATFORMS:
                self.mapping = settings_mod.MAPPING_CDH4X
            elif self.settings['platform'] in HDP2X_PLATFORMS:
                self.mapping = settings_mod.MAPPING_HDP2X

        self.env = dict()

    @staticmethod
    def get_json_content(path):
        ''' return JSON file content
        '''
        try:
            with open(path) as _content:
                result = json.load(_content)
        except IOError, err:
            raise IncorrectJsonFormat(err)
        except ValueError, err:
            raise IncorrectJsonFormat(err)
        return result


    def prepare_settings(self, settings):
        ''' prepare settings based on parameter from command line
        '''
        if not settings.get('platform', None):
            raise EmptyPlatformName(settings.get('platform', None))

        if settings['platform'] not in KNOWN_HADOOP_PLATFORMS:
            raise UnknownPlatformName(settings['platform'])

        # Hadoop config directory
        # default path: /etc for HDP platforms

        if not settings.get('config-dir', None) and settings.get('platform', None).startswith('HDP'):
            settings['config-dir'] = '/etc/'

        # Cloudera specific parameters
        if settings['platform'] in CDH_PLATFORMS:
            for param in CDH_MANDATORY_PARAMETERS:
                if param not in settings:
                    raise MissingMandatoryParameter(param)

        return settings


    def parse(self):

        result = {}

        if self.settings['platform'] in CDH_PLATFORMS:
            result = self._cdh_config_processing()
        elif self.settings['platform'] in HDP2X_PLATFORMS:
            result = self._hdp_config_processing()

        if 'custom-env-properties' in self.settings:
            result.update(self.settings['custom-env-properties'])
        return result

    def _cdh_config_processing(self):
        ''' parse Cloudera Hadoop configuration files
        '''
        cdh_config = cdh.CDHConfig(
                protocol=self.settings['cdh-gateway-http-protocol'],
                hostname=self.settings['cdh-gateway-hostname'],
                port=self.settings['cdh-gateway-port'],
                username=self.settings['cdh-gateway-username'],
                password=self.settings['cdh-gateway-password'],
                api_version=cdh.get_api_version(self.settings['platform']),
                cluster_name=self.settings['cdh-cluster-name'],
                conf_dir=self.settings['config-dir']
        )
        cdh_config.get_service_configs()
        return create_env_props(self.settings['config-dir'], self.mapping)


    def _hdp_config_processing(self):
        ''' parse Hortonworks Hadoop configuration files
        '''
        return create_env_props(self.settings['config-dir'], self.mapping)
