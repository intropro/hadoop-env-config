#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   settings:
#   - cdh-gateway-hostname: CDH Gateway node
#   - cdh-gateway-username: CDH Gateway username
#   - cdh-gateway-password: CDH Gateway password
#

import os
import sys
import json
import optparse

import cdh

from server import run_server
from common import ConfigBuilder
from common import create_env_props
from common import CONFIG_FILES


parser = optparse.OptionParser(usage="usage: %prog [options]")
parser.add_option('--settings', type=str, help='the path to JSON file with settings')
parser.add_option('--mapping', type=str, help='the path to JSON file with env properties mapping')
parser.add_option('--output', type=str, help='the path to JSON file with env properties output')

opts, args = parser.parse_args()

SETTINGS = dict()
if opts.settings:

    try:
        with open(opts.settings) as settings:
            SETTINGS = json.load(settings)
    except IOError:
        print >> sys.stderr, "[ERROR] Cannot process settings file, %s" % opts.settings
        sys.exit(1)
    except ValueError, err:
        print >> sys.stderr, "[ERROR] Incorrect settings format, %s, %s" % (opts.settings, err)
        sys.exit(1)

MAPPING = dict()
if opts.mapping:

    try:
        with open(opts.mapping) as mapping:
            MAPPING = json.load(mapping)
    except IOError:
        print >> sys.stderr, "[ERROR] Cannot process mapping file, %s" % opts.mapping
        sys.exit(1)
    except ValueError, err:
        print >> sys.stderr, "[ERROR] Incorrect mapping format, %s, %s" % (opts.mapping, err)
        sys.exit(1)

# Environment properties
ENV_PROPS = dict()

if not opts.output:
    print >> sys.stderr, '[ERROR] Output file for environment properties does not specified, %s' % opts.output
    sys.exit()

# Hadoop platform

if not SETTINGS.get(u'platform', None):

    print >> sys.stderr, '[ERROR] Please specify platform, %s' % opts.platform
    sys.exit(1)

# Hadoop config directory
# default path: /etc for HDP platforms

if not SETTINGS.get('config-dir', None) and SETTINGS.get('platform', None).startswith('HDP'):
    SETTINGS['config-dir'] = '/etc/'


#
# Cloudera Hadoop settings
#
if SETTINGS.get('platform', None) in ['CDH46', 'CDH47', 'CDH51', 'CDH52', 'CDH53', ]:

    if  not SETTINGS.get('cdh-gateway-hostname', None) \
        and not SETTINGS.get('cdh-gateway-username', None) \
        and not SETTINGS.get('cdh-gateway-password', None):

        print >> sys.stderr, "[ERROR] One of the parameters is not specified, %s" % \
            ['cdh-gateway-hostname', 'cdh-gateway-username', 'cdh-gateway-password']
        sys.exit(1)

    cdh_config = cdh.CDHConfig(
            protocol=SETTINGS['cdh-gateway-http-protocol'],
            hostname=SETTINGS['cdh-gateway-hostname'],
            port=SETTINGS['cdh-gateway-port'],
            username=SETTINGS['cdh-gateway-username'],
            password=SETTINGS['cdh-gateway-password'],
            api_version=cdh.get_api_version(SETTINGS['platform']),
            cluster_name=SETTINGS['cdh-cluster-name'],
            conf_dir=SETTINGS['config-dir']
    )
    cdh_config.get_service_configs()

    oozieSiteXMLPath = os.path.join(SETTINGS['config-dir'], 'oozie-conf', 'oozie-site.xml')
    if not os.path.exists(oozieSiteXMLPath):
        os.makedirs(os.path.join(SETTINGS['config-dir'], 'oozie-conf'))

    with open(oozieSiteXMLPath, 'w') as oozieSiteXML:
        oozieSite='''<configuration>
        <property>
          <name>oozie.base.url</name>
          <value>{oozieServerUrls}</value>
        </property>
        </configuration>'''
        oozieSiteXML.write(oozieSite.format(oozieServerUrls=','.join(["http://%s:11000/oozie" % h for h in cdh_config.oozie_hosts()])))


    ENV_PROPS = create_env_props(SETTINGS['config-dir'], MAPPING)
    # ENV_PROPS['oozieServerUrl'] = ','.join(["http://%s:11000/oozie" % h for h in cdh_config.oozie_hosts()])

#
# Cloudera Hadoop settings
#
elif SETTINGS.get('platform', None) in ['HDP22', ]:

    ENV_PROPS = create_env_props(SETTINGS['config-dir'], MAPPING)


if not ENV_PROPS:
    print >> sys.stderr, '[ERROR] The list of environment properties is empty, %s' % ENV_PROPS
else:
    with (open(opts.output, 'w')) as env_props_output:
        env_props_output.write(json.dumps(ENV_PROPS))


# Hadoop web server

if SETTINGS.get('server', None):

    address, port = SETTINGS.get('server', None).split(':')
    run_server(address, port, SETTINGS.get('config-dir'), MAPPING, CONFIG_FILES)
