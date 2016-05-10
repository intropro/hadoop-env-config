# hadoop-env-config

The script for collecting Hadoop env parameters from different platforms (CDH, HDP)

Supported platforms:

 - HDP (Hortonworks): HDP2.2.8
 - Cloudera (CDH): CDH4.6, CDH4.7, CDH5.3


## How to use

```sh
$ ./hadoop-env-config-0.1.0 --help
Usage: hadoop-env-config-0.1.0 [options]

Options:
  -h, --help           show this help message and exit
  --settings=SETTINGS  the path to JSON file with settings
  --mapping=MAPPING    the path to JSON file with env properties mapping
  --output=OUTPUT      the path to JSON file with env properties output
```

## Configuration

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
