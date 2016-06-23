#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import json
import optparse
import env_config

from __init__ import __version__

parser = optparse.OptionParser(usage="usage: %prog [options]", version=__version__)
parser.add_option('-s', '--settings', type=str, help='the path to JSON file with settings')

optional_group = optparse.OptionGroup(parser, 'Optional arguments')
optional_group.add_option('-m', '--mapping', type=str,
    help='''the path to JSON file with env properties mapping.
            By default will be used the mapping from the package,
            depends on platform parameter in the settings file.''')
optional_group.add_option('-o', '--output', type=str,
    help='''the path to JSON file with env properties output,
            default: stdout''')
parser.add_option_group(optional_group)

opts, args = parser.parse_args()


try:
    hadoop_env_config = env_config.HadoopEnvConfig(opts.settings, opts.mapping)
    env_props = json.dumps(hadoop_env_config.parse())

    if not opts.output:
        print env_props
    else:
        with (open(opts.output, 'w')) as env_props_output:
            env_props_output.write(env_props)


# Settings file error handling

except env_config.IncorrectSettingsFile:
    print >> sys.stderr, '[ERROR] Incorrect settings file: %s' % opts.settings
    sys.exit(1)
except env_config.EmptySettingsFile:
    print >> sys.stderr, '[ERROR] Settings file is empty: %s' % opts.settings
    sys.exit(1)
except env_config.EmptyPlatformName:
    print >> sys.stderr, '[ERROR] Platform name is empty in the settings file: %s' % opts.settings
    sys.exit(1)
except env_config.MissingMandatoryParameter, err:
    print >> sys.stderr, '[ERROR] Missing mandatory parameter in the settings file: %s' % err
    sys.exit(1)


# Mapping file error handling

except env_config.IncorrectMappingFile:
    print >> sys.stderr, '[ERROR] Incorrect mapping file: %s' % opts.mapping
    sys.exit(1)
except env_config.IncorrectMappingFile:
    print >> sys.stderr, '[ERROR] mMpping file is empty: %s' % opts.mapping
    sys.exit(1)


# Hadoop web server

if hadoop_env_config.settings.get('server', None):

    from server import run_server

    address, port = hadoop_env_config.settings.get('server', None).split(':')
    run_server(address, port, hadoop_env_config)
