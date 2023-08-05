# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetAccountIdTokenResult:
    """
    A collection of values returned by getAccountIdToken.
    """
    def __init__(__self__, delegates=None, id=None, id_token=None, include_email=None, target_audience=None, target_service_account=None):
        if delegates and not isinstance(delegates, list):
            raise TypeError("Expected argument 'delegates' to be a list")
        __self__.delegates = delegates
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if id_token and not isinstance(id_token, str):
            raise TypeError("Expected argument 'id_token' to be a str")
        __self__.id_token = id_token
        """
        The `id_token` representing the new generated identity.
        """
        if include_email and not isinstance(include_email, bool):
            raise TypeError("Expected argument 'include_email' to be a bool")
        __self__.include_email = include_email
        if target_audience and not isinstance(target_audience, str):
            raise TypeError("Expected argument 'target_audience' to be a str")
        __self__.target_audience = target_audience
        if target_service_account and not isinstance(target_service_account, str):
            raise TypeError("Expected argument 'target_service_account' to be a str")
        __self__.target_service_account = target_service_account
class AwaitableGetAccountIdTokenResult(GetAccountIdTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccountIdTokenResult(
            delegates=self.delegates,
            id=self.id,
            id_token=self.id_token,
            include_email=self.include_email,
            target_audience=self.target_audience,
            target_service_account=self.target_service_account)

def get_account_id_token(delegates=None,include_email=None,target_audience=None,target_service_account=None,opts=None):
    """
    Use this data source to access information about an existing resource.

    :param list delegates: Delegate chain of approvals needed to perform full impersonation. Specify the fully qualified service account name.   Used only when using impersonation mode.
    :param bool include_email: Include the verified email in the claim. Used only when using impersonation mode.
    :param str target_audience: The audience claim for the `id_token`.
    :param str target_service_account: The email of the service account being impersonated.  Used only when using impersonation mode.
    """
    __args__ = dict()


    __args__['delegates'] = delegates
    __args__['includeEmail'] = include_email
    __args__['targetAudience'] = target_audience
    __args__['targetServiceAccount'] = target_service_account
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:serviceAccount/getAccountIdToken:getAccountIdToken', __args__, opts=opts).value

    return AwaitableGetAccountIdTokenResult(
        delegates=__ret__.get('delegates'),
        id=__ret__.get('id'),
        id_token=__ret__.get('idToken'),
        include_email=__ret__.get('includeEmail'),
        target_audience=__ret__.get('targetAudience'),
        target_service_account=__ret__.get('targetServiceAccount'))
