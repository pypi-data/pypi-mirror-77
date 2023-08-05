# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetTensorflowVersionsResult:
    """
    A collection of values returned by getTensorflowVersions.
    """
    def __init__(__self__, id=None, project=None, versions=None, zone=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if versions and not isinstance(versions, list):
            raise TypeError("Expected argument 'versions' to be a list")
        __self__.versions = versions
        """
        The list of TensorFlow versions available for the given project and zone.
        """
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        __self__.zone = zone
class AwaitableGetTensorflowVersionsResult(GetTensorflowVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTensorflowVersionsResult(
            id=self.id,
            project=self.project,
            versions=self.versions,
            zone=self.zone)

def get_tensorflow_versions(project=None,zone=None,opts=None):
    """
    Get TensorFlow versions available for a project. For more information see the [official documentation](https://cloud.google.com/tpu/docs/) and [API](https://cloud.google.com/tpu/docs/reference/rest/v1/projects.locations.tensorflowVersions).


    :param str project: The project to list versions for. If it
           is not provided, the provider project is used.
    :param str zone: The zone to list versions for. If it
           is not provided, the provider zone is used.
    """
    __args__ = dict()


    __args__['project'] = project
    __args__['zone'] = zone
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:tpu/getTensorflowVersions:getTensorflowVersions', __args__, opts=opts).value

    return AwaitableGetTensorflowVersionsResult(
        id=__ret__.get('id'),
        project=__ret__.get('project'),
        versions=__ret__.get('versions'),
        zone=__ret__.get('zone'))
