# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetDatabaseInstanceResult:
    """
    A collection of values returned by getDatabaseInstance.
    """
    def __init__(__self__, connection_name=None, database_version=None, encryption_key_name=None, first_ip_address=None, id=None, ip_addresses=None, master_instance_name=None, name=None, private_ip_address=None, project=None, public_ip_address=None, region=None, replica_configurations=None, root_password=None, self_link=None, server_ca_certs=None, service_account_email_address=None, settings=None):
        if connection_name and not isinstance(connection_name, str):
            raise TypeError("Expected argument 'connection_name' to be a str")
        __self__.connection_name = connection_name
        """
        The connection name of the instance to be used in connection strings.
        """
        if database_version and not isinstance(database_version, str):
            raise TypeError("Expected argument 'database_version' to be a str")
        __self__.database_version = database_version
        """
        The MySQL, PostgreSQL or SQL Server (beta) version to use.
        """
        if encryption_key_name and not isinstance(encryption_key_name, str):
            raise TypeError("Expected argument 'encryption_key_name' to be a str")
        __self__.encryption_key_name = encryption_key_name
        if first_ip_address and not isinstance(first_ip_address, str):
            raise TypeError("Expected argument 'first_ip_address' to be a str")
        __self__.first_ip_address = first_ip_address
        """
        The first IPv4 address of any type assigned.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if ip_addresses and not isinstance(ip_addresses, list):
            raise TypeError("Expected argument 'ip_addresses' to be a list")
        __self__.ip_addresses = ip_addresses
        if master_instance_name and not isinstance(master_instance_name, str):
            raise TypeError("Expected argument 'master_instance_name' to be a str")
        __self__.master_instance_name = master_instance_name
        """
        The name of the instance that will act as
        the master in the replication setup.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        A name for this whitelist entry.
        """
        if private_ip_address and not isinstance(private_ip_address, str):
            raise TypeError("Expected argument 'private_ip_address' to be a str")
        __self__.private_ip_address = private_ip_address
        """
        The first private (`PRIVATE`) IPv4 address assigned.
        """
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if public_ip_address and not isinstance(public_ip_address, str):
            raise TypeError("Expected argument 'public_ip_address' to be a str")
        __self__.public_ip_address = public_ip_address
        """
        The first public (`PRIMARY`) IPv4 address assigned.
        """
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        __self__.region = region
        if replica_configurations and not isinstance(replica_configurations, list):
            raise TypeError("Expected argument 'replica_configurations' to be a list")
        __self__.replica_configurations = replica_configurations
        """
        The configuration for replication. The
        configuration is detailed below.
        """
        if root_password and not isinstance(root_password, str):
            raise TypeError("Expected argument 'root_password' to be a str")
        __self__.root_password = root_password
        """
        Initial root password. Required for MS SQL Server, ignored by MySQL and PostgreSQL.
        """
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        __self__.self_link = self_link
        """
        The URI of the created resource.
        """
        if server_ca_certs and not isinstance(server_ca_certs, list):
            raise TypeError("Expected argument 'server_ca_certs' to be a list")
        __self__.server_ca_certs = server_ca_certs
        if service_account_email_address and not isinstance(service_account_email_address, str):
            raise TypeError("Expected argument 'service_account_email_address' to be a str")
        __self__.service_account_email_address = service_account_email_address
        """
        The service account email address assigned to the instance.
        """
        if settings and not isinstance(settings, list):
            raise TypeError("Expected argument 'settings' to be a list")
        __self__.settings = settings
        """
        The settings to use for the database. The
        configuration is detailed below.
        """
class AwaitableGetDatabaseInstanceResult(GetDatabaseInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatabaseInstanceResult(
            connection_name=self.connection_name,
            database_version=self.database_version,
            encryption_key_name=self.encryption_key_name,
            first_ip_address=self.first_ip_address,
            id=self.id,
            ip_addresses=self.ip_addresses,
            master_instance_name=self.master_instance_name,
            name=self.name,
            private_ip_address=self.private_ip_address,
            project=self.project,
            public_ip_address=self.public_ip_address,
            region=self.region,
            replica_configurations=self.replica_configurations,
            root_password=self.root_password,
            self_link=self.self_link,
            server_ca_certs=self.server_ca_certs,
            service_account_email_address=self.service_account_email_address,
            settings=self.settings)

def get_database_instance(name=None,opts=None):
    """
    Use this data source to get information about a Cloud SQL instance


    :param str name: The name of the instance.
    """
    __args__ = dict()


    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:sql/getDatabaseInstance:getDatabaseInstance', __args__, opts=opts).value

    return AwaitableGetDatabaseInstanceResult(
        connection_name=__ret__.get('connectionName'),
        database_version=__ret__.get('databaseVersion'),
        encryption_key_name=__ret__.get('encryptionKeyName'),
        first_ip_address=__ret__.get('firstIpAddress'),
        id=__ret__.get('id'),
        ip_addresses=__ret__.get('ipAddresses'),
        master_instance_name=__ret__.get('masterInstanceName'),
        name=__ret__.get('name'),
        private_ip_address=__ret__.get('privateIpAddress'),
        project=__ret__.get('project'),
        public_ip_address=__ret__.get('publicIpAddress'),
        region=__ret__.get('region'),
        replica_configurations=__ret__.get('replicaConfigurations'),
        root_password=__ret__.get('rootPassword'),
        self_link=__ret__.get('selfLink'),
        server_ca_certs=__ret__.get('serverCaCerts'),
        service_account_email_address=__ret__.get('serviceAccountEmailAddress'),
        settings=__ret__.get('settings'))
