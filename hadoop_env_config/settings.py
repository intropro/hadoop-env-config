#
#   Hadoop config files
#
CONFIG_FILES = {
    'hdfs-site.xml': ['hadoop/conf/hdfs-site.xml', 'hadoop-conf/hdfs-site.xml'],
    'core-site.xml': ['hadoop/conf/core-site.xml', 'hadoop-conf/core-site.xml'],
    'hbase-site.xml': ['hbase/conf/hbase-site.xml', 'hbase-conf/hbase-site.xml'],
    'hive-site.xml': ['hive/conf/hive-site.xml', 'hive-conf/hive-site.xml'],
    'yarn-site.xml': ['hadoop/conf/yarn-site.xml', 'hadoop-conf/yarn-site.xml'],
    'mapred-site.xml': ['hadoop/conf/mapred-site.xml', 'hadoop-conf/mapred-site.xml'],
    'oozie-site.xml': ['oozie/conf/oozie-site.xml','oozie-conf/oozie-site.xml' ],
}

#
#   Parameters mapping for CDH4.x platforms
#
MAPPING_CDH4X = {
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
        "oozie.base.url": "oozieServerUrl",
        "oozie.base.url": "oozieServer"
    }
}

#
#   Parameters mapping for HDP2.2 platform
#
MAPPING_HDP2X = {
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
        "oozie.base.url": "oozieServerUrl",
        "oozie.base.url": "oozieServer"
    }
}
