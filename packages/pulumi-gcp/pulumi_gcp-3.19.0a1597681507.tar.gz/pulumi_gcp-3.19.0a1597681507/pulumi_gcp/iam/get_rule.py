# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetRuleResult:
    """
    A collection of values returned by getRule.
    """
    def __init__(__self__, id=None, included_permissions=None, name=None, stage=None, title=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if included_permissions and not isinstance(included_permissions, list):
            raise TypeError("Expected argument 'included_permissions' to be a list")
        __self__.included_permissions = included_permissions
        """
        specifies the list of one or more permissions to include in the custom role, such as - `iam.roles.get`
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if stage and not isinstance(stage, str):
            raise TypeError("Expected argument 'stage' to be a str")
        __self__.stage = stage
        """
        indicates the stage of a role in the launch lifecycle, such as `GA`, `BETA` or `ALPHA`.
        """
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        __self__.title = title
        """
        is a friendly title for the role, such as "Role Viewer"
        """
class AwaitableGetRuleResult(GetRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleResult(
            id=self.id,
            included_permissions=self.included_permissions,
            name=self.name,
            stage=self.stage,
            title=self.title)

def get_rule(name=None,opts=None):
    """
    Use this data source to get information about a Google IAM Role.


    :param str name: The name of the Role to lookup in the form `roles/{ROLE_NAME}`, `organizations/{ORGANIZATION_ID}/roles/{ROLE_NAME}` or `projects/{PROJECT_ID}/roles/{ROLE_NAME}`
    """
    __args__ = dict()


    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:iam/getRule:getRule', __args__, opts=opts).value

    return AwaitableGetRuleResult(
        id=__ret__.get('id'),
        included_permissions=__ret__.get('includedPermissions'),
        name=__ret__.get('name'),
        stage=__ret__.get('stage'),
        title=__ret__.get('title'))
