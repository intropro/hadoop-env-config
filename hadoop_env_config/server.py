#
#   Config server
#
import os
import sys
import json
import socket
import SocketServer
import SimpleHTTPServer

from settings import CONFIG_FILES

from common import ConfigBuilder
from common import create_env_props

CSS_STYLE='''
table {
    font-size: 14px;
}
'''

#     <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.11/js/dataTables.bootstrap.min.js"></script>


HTML_PAGE='''
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script type="text/javascript" language="javascript" src="http://code.jquery.com/jquery-1.12.0.min.js"></script>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.11/css/jquery.dataTables.min.css">
    <script type="text/javascript" language="javascript" src="http://cdn.datatables.net/1.10.11/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" class="init">{init_func}</script>

    <link rel="stylesheet" type="text/css" href="/style.css" >
</head>

<body>
    <div class="container">

        <h1>Hadoop environment configuration</h1>
        <ul class="nav nav-tabs">
            <li class="active"><a data-toggle="tab" href="#services">Services</a></li>
            <li><a data-toggle="tab" href="#configs">Configs</a></li>
            <li><a data-toggle="tab" href="#site-files">Site files</a></li>
            <li><a data-toggle="tab" href="#cluster-params">Cluster parameters</a></li>
        </ul>

        <div class="tab-content">
            <div id="services" class="tab-pane fade in active">
                <h2>Services</h2>
                <table class="table table-striped">
                    <tr> <td>Ambari</td> <td><a href="http://{hostname}:8080/">http://{hostname}:8080/</a></td> </tr>
                    <tr> <td>Cloudera Manager</td> <td><a href="http://{hostname}:8080/">http://{hostname}:7180/</a></td> </tr>
                    <tr> <td>Hue</td> <td><a href="http://{hostname}:8000/">http://{hostname}:8000/</a></td> </tr>
                </table>
            </div>

            <div id="configs" class="tab-pane">
                <h2>Configs</h2>
                <table class="table table-striped">
                <tr> <td> <a href="/conf/environment.properties">environment.properties</a> </td> </tr>
                <tr> <td> <a href="/conf/environment.json">environment.json</a> </td> </tr>
                <tr> <td> <a href="/conf/config.json">config.json</a></td> </tr>
                </table>
            </div>

            <div id="site-files" class="tab-pane">
                <h2>Hadoop configs</h2>
                <table class="table table-striped">
                <tr> <td> <a href="/conf/hdfs-site.xml">hdfs-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/core-site.xml">core-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/hbase-site.xml">hbase-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/hive-site.xml">hive-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/yarn-site.xml">yarn-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/mapred-site.xml">mapred-site.xml</a> </td> </tr>
                <tr> <td> <a href="/conf/oozie-site.xml">oozie-site.xml</a> </td> </tr>
                </table>
            </div>

            <div id="cluster-params" class="tab-pane">
                <h2>Cluster parameters</h2>
                <table id="cluster-params-table" class="table table-striped" style="width:100%;table-layout:fixed;word-wrap:break-word;">
                    <thead><tr><th>config</th><th>parameter</th><th>value</th></tr></thead>
                </table>
            </div>
        </div>

    </div>
</body>
</html>
'''

# CONF_DIR = None
# CONFIG_FILES = None
# MAPPING = None
#
ENV_CONFIG=None

class ConfigHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

        message = 'ConfigServer'
        config_dir = ENV_CONFIG.settings['config-dir']

        if self.path == '/':
            message = HTML_PAGE.format(
                hostname=socket.getfqdn(),
                init_func="""$(document).ready(
                                function() {
                                    $('#cluster-params-table').DataTable({
                                        'ajax': '/conf/config.json',
                                    });
                                } );"""
            )
        elif self.path.startswith('/conf/config.json'):
            _msg = []
            for name, conf in ConfigBuilder(config_dir).config.items():
                for k,v in conf.items():
                    _msg.append((name,k,v))
            # self.send_header("Content-Type", "application/json")
            message = json.dumps({'data': _msg})
        elif self.path == '/conf/environment.json':
            message = json.dumps(ENV_CONFIG.parse().items())
        elif self.path == '/conf/environment.properties':
            message = '\n'.join("%s=%s" % (k,v) for k,v in ENV_CONFIG.parse().items())
            message += "\n"
        elif self.path.startswith('/conf/'):
            conf_file = os.path.basename(self.path)
            try:
                for f in CONFIG_FILES[conf_file]:
                    path = os.path.join(config_dir, f)
                    if os.path.exists(path):
                        message = open(path).read()
                        break
            except:
                message = ''
        elif self.path.startswith('/style.css'):
            message = CSS_STYLE

        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)


def run_server(address, port, env_config):
    ''' run server
    '''
    global ENV_CONFIG
    ENV_CONFIG = env_config

    # global  CONF_DIR, MAPPING, CONFIG_FILES
    # CONF_DIR = env_config.settings.get("config-dir")
    # MAPPING = env_config.mapping
    # CONFIG_FILES = env_config.

    httpd = SocketServer.TCPServer((address, int(port)), ConfigHandler)
    print "serving at %s:%s" % (address, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print >> sys.stderr, 'Interrupted by user'
