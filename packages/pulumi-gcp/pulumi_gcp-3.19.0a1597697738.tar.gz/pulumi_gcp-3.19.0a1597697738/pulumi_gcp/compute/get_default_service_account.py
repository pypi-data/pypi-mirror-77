# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetDefaultServiceAccountResult:
    """
    A collection of values returned by getDefaultServiceAccount.
    """
    def __init__(__self__, display_name=None, email=None, id=None, name=None, project=None, unique_id=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        __self__.display_name = display_name
        """
        The display name for the service account.
        """
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        __self__.email = email
        """
        Email address of the default service account used by VMs running in this project
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The fully-qualified name of the service account.
        """
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if unique_id and not isinstance(unique_id, str):
            raise TypeError("Expected argument 'unique_id' to be a str")
        __self__.unique_id = unique_id
        """
        The unique id of the service account.
        """


class AwaitableGetDefaultServiceAccountResult(GetDefaultServiceAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDefaultServiceAccountResult(
            display_name=self.display_name,
            email=self.email,
            id=self.id,
            name=self.name,
            project=self.project,
            unique_id=self.unique_id)


def get_default_service_account(project=None, opts=None):
    """
    Use this data source to retrieve default service account for this project


    :param str project: The project ID. If it is not provided, the provider project is used.
    """
    __args__ = dict()
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:compute/getDefaultServiceAccount:getDefaultServiceAccount', __args__, opts=opts).value

    return AwaitableGetDefaultServiceAccountResult(
        display_name=__ret__.get('displayName'),
        email=__ret__.get('email'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        project=__ret__.get('project'),
        unique_id=__ret__.get('uniqueId'))
