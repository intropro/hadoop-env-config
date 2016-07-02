import json
import settings

import cdh
from common import create_env_props


class IncorrectSettingsFile(Exception):
    pass

class IncorrectMappingFile(Exception):
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

HDP2X_PLATFORMS = ['HDP22', 'HDP23',]

KNOWN_HADOOP_PLATFORMS = CDH_PLATFORMS + HDP2X_PLATFORMS


class HadoopEnvConfig(object):

    def __init__(self, settings, mapping=None):

        self.settings = self.prepare_settings(settings)
        self.mapping = self.prepare_mapping(mapping)
        self.env = dict()


    def prepare_settings(self, settings):
        ''' prepare settings based on parameter from command line
        '''
        result = dict()
        if settings:
            try:
                with open(settings) as _settings:
                    result = json.load(_settings)
            except IOError, err:
                raise IncorrectSettingsFile(err)
            except ValueError, err:
                raise IncorrectSettingsFile(err)
        else:
            raise UndefinedSettingsFile(settings)

        if not result.get('platform', None):
            raise EmptyPlatformName(result.get('platform', None))

        if result['platform'] not in KNOWN_HADOOP_PLATFORMS:
            raise UnknownPlatformName(result['platform'])

        # Hadoop config directory
        # default path: /etc for HDP platforms

        if not result.get('config-dir', None) and result.get('platform', None).startswith('HDP'):
            result['config-dir'] = '/etc/'

        # Cloudera specific parameters
        if result['platform'] in CDH_PLATFORMS:
            for param in CDH_MANDATORY_PARAMETERS:
                if param not in result:
                    raise MissingMandatoryParameter(param)

        return result


    def prepare_mapping(self, mapping):
        ''' prepare mapping based on parameter from command line
        '''
        result = dict()
        if mapping:
            try:
                with open(mapping) as _mapping:
                    result = json.load(_mapping)
            except IOError, err:
                raise IncorrectMappingFile(err)
            except ValueError, err:
                raise IncorrectMappingFile(err)
        else:
            if self.settings['platform'] in CDH4X_PLATFORMS:
                result = settings.MAPPING_CDH4X
            elif self.settings['platform'] in HDP2X_PLATFORMS:
                result = settings.MAPPING_HDP2X

        return result


    def parse(self):

        if self.settings['platform'] in CDH_PLATFORMS:

            return self._cdh_config_processing()

        elif self.settings['platform'] in HDP2X_PLATFORMS:

            return self._hdp_config_processing()


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
