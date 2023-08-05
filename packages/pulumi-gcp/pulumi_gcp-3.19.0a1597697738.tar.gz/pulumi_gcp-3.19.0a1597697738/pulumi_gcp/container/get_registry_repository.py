# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetRegistryRepositoryResult:
    """
    A collection of values returned by getRegistryRepository.
    """
    def __init__(__self__, id=None, project=None, region=None, repository_url=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        __self__.region = region
        if repository_url and not isinstance(repository_url, str):
            raise TypeError("Expected argument 'repository_url' to be a str")
        __self__.repository_url = repository_url


class AwaitableGetRegistryRepositoryResult(GetRegistryRepositoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistryRepositoryResult(
            id=self.id,
            project=self.project,
            region=self.region,
            repository_url=self.repository_url)


def get_registry_repository(project=None, region=None, opts=None):
    """
    This data source fetches the project name, and provides the appropriate URLs to use for container registry for this project.

    The URLs are computed entirely offline - as long as the project exists, they will be valid, but this data source does not contact Google Container Registry (GCR) at any point.
    """
    __args__ = dict()
    __args__['project'] = project
    __args__['region'] = region
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:container/getRegistryRepository:getRegistryRepository', __args__, opts=opts).value

    return AwaitableGetRegistryRepositoryResult(
        id=__ret__.get('id'),
        project=__ret__.get('project'),
        region=__ret__.get('region'),
        repository_url=__ret__.get('repositoryUrl'))
