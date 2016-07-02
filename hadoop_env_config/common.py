
import os
import sys
import base64
import httplib
import urlparse

import xml.etree.ElementTree as ET

import settings as settings_mod

class ConfigBuilder(object):

    def __init__(self, config_path):

        if not os.path.exists(config_path):
            raise RuntimeError('The path does not exist, %s' % config_path)

        self.config_path = config_path
        self.config_files = []
        self._config = dict()

        for cfile, paths in settings_mod.CONFIG_FILES.items():
            for path in paths:
                path = os.path.join(config_path, path)
                if not os.path.exists(path):
                    # print >> sys.stderr, "[WARNING] Config file does not exist, %s" % path
                    continue
                else:
                    self.config_files.append(path)


    def xml2dict(self, filename):

        result = list()
        for prop in ET.parse(filename).getroot():
            result.append(dict([(c.tag, c.text) for c in prop.getchildren()]))

        return dict((kv['name'], kv['value'].strip() if kv['value'] else "") for kv in result)


    @property
    def config(self):

        if self._config:
            return self._config

        for conf_file in self.config_files:
            conf_name = os.path.basename(conf_file).replace('.xml', '')
            self._config[conf_name] = dict()
            for kv in self.xml2dict(conf_file).items():
                if kv[0] in self._config[conf_name] and self._config[conf_name][kv[0]] != kv[1]:
                    print >> sys.stderr, "[WARNING] Duplicated key with different values, %s" % kv
                else:
                    self._config[conf_name][kv[0]] = kv[1]
        return self._config



def create_env_props(conf_dir, mapping):

    def get_prop(config, prop_name):

        if prop_name in config.keys():
            return config[prop_name]
        else:
            return ''

    _config = ConfigBuilder(conf_dir).config
    _env_props = {}

    for site in mapping:
        if site in _config:
            props = dict([(v,get_prop(_config[site], k)) for k,v in mapping[site].items()])
            _env_props.update(props)

    if 'oozieServer' in _env_props and _env_props['oozieServer']:
        _env_props['oozieServer'] = urlparse.urljoin(_env_props['oozieServer'], '/')
        if _env_props['oozieServer'][-1] == '/':
            _env_props['oozieServer'] = _env_props['oozieServer'][:-1]

    return _env_props
