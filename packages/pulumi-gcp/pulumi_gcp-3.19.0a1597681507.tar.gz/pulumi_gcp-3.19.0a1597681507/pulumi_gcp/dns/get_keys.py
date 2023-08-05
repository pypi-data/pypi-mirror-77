# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetKeysResult:
    """
    A collection of values returned by getKeys.
    """
    def __init__(__self__, id=None, key_signing_keys=None, managed_zone=None, project=None, zone_signing_keys=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if key_signing_keys and not isinstance(key_signing_keys, list):
            raise TypeError("Expected argument 'key_signing_keys' to be a list")
        __self__.key_signing_keys = key_signing_keys
        """
        A list of Key-signing key (KSK) records. Structure is documented below. Additionally, the DS record is provided:
        """
        if managed_zone and not isinstance(managed_zone, str):
            raise TypeError("Expected argument 'managed_zone' to be a str")
        __self__.managed_zone = managed_zone
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if zone_signing_keys and not isinstance(zone_signing_keys, list):
            raise TypeError("Expected argument 'zone_signing_keys' to be a list")
        __self__.zone_signing_keys = zone_signing_keys
        """
        A list of Zone-signing key (ZSK) records. Structure is documented below.
        """
class AwaitableGetKeysResult(GetKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeysResult(
            id=self.id,
            key_signing_keys=self.key_signing_keys,
            managed_zone=self.managed_zone,
            project=self.project,
            zone_signing_keys=self.zone_signing_keys)

def get_keys(managed_zone=None,project=None,opts=None):
    """
    Get the DNSKEY and DS records of DNSSEC-signed managed zones. For more information see the
    [official documentation](https://cloud.google.com/dns/docs/dnskeys/)
    and [API](https://cloud.google.com/dns/docs/reference/v1/dnsKeys).


    :param str managed_zone: The name or id of the Cloud DNS managed zone.
    :param str project: The ID of the project in which the resource belongs. If `project` is not provided, the provider project is used.
    """
    __args__ = dict()


    __args__['managedZone'] = managed_zone
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:dns/getKeys:getKeys', __args__, opts=opts).value

    return AwaitableGetKeysResult(
        id=__ret__.get('id'),
        key_signing_keys=__ret__.get('keySigningKeys'),
        managed_zone=__ret__.get('managedZone'),
        project=__ret__.get('project'),
        zone_signing_keys=__ret__.get('zoneSigningKeys'))
