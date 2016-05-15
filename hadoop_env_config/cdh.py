#
#   Cloudera
#
import os
import sys
import json
import urllib
import zipfile
import contextlib

from packages import sh
from common import ConfigBuilder

SERVICES_IGNORE_LIST = ["FLUME", "HUE", "IMPALA", "OOZIE", "SOLR", "SQOOP", "ZOOKEEPER",]


def get_api_version(platform):

    _versions = {
        'CDH46': 4, 'CDH47': 5, 'CDH51': 7, 'CDH52': 8, 'CDH53': 9
    }
    return _versions.get(platform, None)


class CDHConfig(object):

    def __init__(self, protocol, hostname, port, username, password, api_version, cluster_name, conf_dir):

        self._config = {
            'protocol': protocol,
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'api_version': api_version,
            'cluster_name': cluster_name
        }

        self.deployment_config = None

        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)
        self.conf_dir=conf_dir


    def prepare_url(self, path, **props):

        if 'username' in self._config and 'password' in self._config:
            URL_TEMPLATE = "{protocol}://{username}:{password}@{hostname}:{port}/api/v{api_version}/clusters/{cluster_name}"
        else:
            URL_TEMPLATE = "{protocol}://{hostname}:{port}/api/v{api_version}/clusters/{cluster_name}"
        URL = URL_TEMPLATE.format(**self._config)

        if props:
            path = path.format(**props)

        if path:
            return '/'.join([URL, path])
        else:
            return URL


    def services(self):

        URL = self.prepare_url('services')
        resp = json.loads(sh.curl('-k', URL, silent=True).stdout)
        return resp['items']


    def service_config(self, service_name):

        URL = self.prepare_url('services/{service_name}/clientConfig', service_name=service_name)
        config_path = "%s.zip" % os.path.join(self.conf_dir, service_name)
        sh.curl('-k', URL, '-o', config_path, silent=True).stdout

        with contextlib.closing(zipfile.ZipFile(config_path)) as zipped_config:
            zipped_config.extractall(self.conf_dir)
        os.remove(config_path)


    def get_service_configs(self):

        for service in self.services():
            if service['type'] in SERVICES_IGNORE_LIST:
                continue
            print >> sys.stderr, '[INFO] getting config for service: %s' % service['name']
            self.service_config(service['name'])

        self.prepare_oozie_config()


    def role(self, service_name):

        URL = self.prepare_url('services/{service_name}/roles', service_name=service_name)
        resp = json.loads(sh.curl('-k', URL, silent=True).stdout)
        return resp['items']


    def oozie_hosts(self):

        _hosts = list()
        for service in self.services():
            if service['type'] == 'OOZIE':
                _hosts.extend([s['hostRef']['hostId'] for s in self.role(service['name'])])
        return _hosts


    def prepare_oozie_config(self):

        oozieSiteXMLPath = os.path.join(self.conf_dir, 'oozie-conf/oozie-site.xml')
        if not os.path.exists(oozieSiteXMLPath):
            os.makedirs(os.path.join(self.conf_dir, 'oozie-conf'))

        with open(oozieSiteXMLPath, 'w') as oozieSiteXML:
            oozieSite='''<configuration>
            <property>
              <name>oozie.base.url</name>
              <value>{oozieServerUrls}</value>
            </property>
            </configuration>'''
            oozieSiteXML.write(oozieSite.format(oozieServerUrls=','.join(["http://%s:11000/oozie" % h for h in self.oozie_hosts()])))
