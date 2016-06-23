# hadoop-env-config

[![Build Status](https://travis-ci.org/intropro/hadoop-env-config.svg?branch=master)](https://travis-ci.org/intropro/hadoop-env-config)

The script for collecting Hadoop env parameters from different platforms (CDH, HDP)

Supported platforms:

Platform    | Versions
------------| ------------------
HDP         | HDP 2.2.8
CDH         | CDH 4.6, 4.7, 5.3


## Installation

The installation process is simple as possible. You just need to download latest version of self-contained
binary package `hadoop-env-config` from Releases page https://github.com/intropro/hadoop-env-config/releases

## How to use

```sh
$ ./hadoop-env-config --help
Usage: hadoop-env-config [options]

Options:
  --version             show program\'s version number and exit
  -h, --help            show this help message and exit
  -s SETTINGS, --settings=SETTINGS
                        the path to JSON file with settings

  Optional arguments:
    -m MAPPING, --mapping=MAPPING
                        the path to JSON file with env properties mapping.
                        By default will be used the mapping from the package,
                        depends on platform parameter in the settings file.
    -o OUTPUT, --output=OUTPUT
                        the path to JSON file with env properties output,
                        default: stdout

```

## Configuration

### Parameters

Name                        | Env      | Description
--------------------------- | -------- | --------------------
platform                    | HDP/CDH  | Platform name: CDH46, CDH53, HDP22, ...
config-dir                  | HDP/CDH  | The directory path to configuration files
cdh-gateway-http-protocol   | CDH      | Protocol for connecting via Cloudera API: http, https
cdh-gateway-hostname        | CDH      | Hostname for connecting to Cloudera API
cdh-gateway-port            | CDH      | Port for Cloudera API
cdh-gateway-username        | CDH      | Username
cdh-gateway-password        | CDH      | Password
cdh-cluster-name            | CDH      | Cloudera cluster name
server                      | CDH/HDP  | Web server


### CDH4/5 settings file (example)

```json
{
    "platform": "CDH47",
    "config-dir": "/tmp/cloudera-env-config/",

    "cdh-gateway-http-protocol": "http",
    "cdh-gateway-hostname": "test-gw-node",
    "cdh-gateway-port": 7180,
    "cdh-gateway-username": "cloudera",
    "cdh-gateway-password": "cloudera",
    "cdh-cluster-name": "TestCluster1",

    "server": "localhost:8080"
}
```



### HDP settings file (example)

```json
{
    "platform": "HDP22",
    "config-dir": "/etc",

    "server": "localhost:8080"
}
```

### Custom settings

Time to time there are needed to add custom parameters to configuration files, like ssh credentials to Hadoop cluster.
These parameters can be specified in the settings file, the section: custom-env-properties

```json
{
    "platform": "HDP22",
    "config-dir": "/etc",

    "server": "localhost:8080",
    "custom-env-properties": {
        "sshPort": 22,
        "sshUserName": "username",
        "sshPassword": "password"
    }
}
```


### Mapping file

Example for CDH4.x

```json
{
    "core-site": {
        "fs.defaultFS": "nameNode",
        "hadoop.security.authentication": "securityAuthentication"
    },
    "mapred-site": {
        "mapred.job.tracker": "jobTracker"
    },
    "hbase-site": {
        "hbase.zookeeper.quorum": "hbaseZookeeperQuorum"
    },
    "hive-site": {
        "hive.zookeeper.quorum": "hiveZookeeperQuorum",
        "hive.metastore.uris": "hiveMetastoreUris",
        "hive.metastore.kerberos.principal": "hiveMetastorePrincipal"
    },
    "oozie-site": {
        "oozie.base.url": "oozieServerUrl"
    }
}
```

Example for HDP2.2

```json
{
    "core-site": {
        "fs.defaultFS": "nameNode",
        "hadoop.security.authentication": "securityAuthentication"
    },
    "yarn-site": {
        "yarn.resourcemanager.address": "jobTracker"
    },
    "hbase-site": {
        "hbase.zookeeper.quorum": "hbaseZookeeperQuorum"
    },
    "hive-site": {
        "hive.zookeeper.quorum": "hiveZookeeperQuorum",
        "hive.metastore.uris": "hiveMetastoreUris",
        "hive.metastore.kerberos.principal": "hiveMetastorePrincipal"
    },
    "oozie-site": {
        "oozie.base.url": "oozieServerUrl"
    }
}

```
