# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class FunctionIamPolicy(pulumi.CustomResource):
    cloud_function: pulumi.Output[str]
    """
    Used to find the parent resource to bind the IAM policy to
    """
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the IAM policy.
    """
    policy_data: pulumi.Output[str]
    """
    The policy data generated by
    a `organizations.getIAMPolicy` data source.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
    """
    region: pulumi.Output[str]
    """
    The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
    the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
    region is specified, it is taken from the provider configuration.
    """
    def __init__(__self__, resource_name, opts=None, cloud_function=None, policy_data=None, project=None, region=None, __props__=None, __name__=None, __opts__=None):
        """
        Three different resources help you manage your IAM policy for Cloud Functions CloudFunction. Each of these resources serves a different use case:

        * `cloudfunctions.FunctionIamPolicy`: Authoritative. Sets the IAM policy for the cloudfunction and replaces any existing policy already attached.
        * `cloudfunctions.FunctionIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the cloudfunction are preserved.
        * `cloudfunctions.FunctionIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the cloudfunction are preserved.

        > **Note:** `cloudfunctions.FunctionIamPolicy` **cannot** be used in conjunction with `cloudfunctions.FunctionIamBinding` and `cloudfunctions.FunctionIamMember` or they will fight over what your policy should be.

        > **Note:** `cloudfunctions.FunctionIamBinding` resources **can be** used in conjunction with `cloudfunctions.FunctionIamMember` resources **only if** they do not grant privilege to the same role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.getIAMPolicy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if cloud_function is None:
                raise TypeError("Missing required property 'cloud_function'")
            __props__['cloud_function'] = cloud_function
            if policy_data is None:
                raise TypeError("Missing required property 'policy_data'")
            __props__['policy_data'] = policy_data
            __props__['project'] = project
            __props__['region'] = region
            __props__['etag'] = None
        super(FunctionIamPolicy, __self__).__init__(
            'gcp:cloudfunctions/functionIamPolicy:FunctionIamPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cloud_function=None, etag=None, policy_data=None, project=None, region=None):
        """
        Get an existing FunctionIamPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_function: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] policy_data: The policy data generated by
               a `organizations.getIAMPolicy` data source.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the project will be parsed from the identifier of the parent resource. If no project is provided in the parent identifier and no project is specified, the provider project is used.
        :param pulumi.Input[str] region: The location of this cloud function. Used to find the parent resource to bind the IAM policy to. If not specified,
               the value will be parsed from the identifier of the parent resource. If no region is provided in the parent identifier and no
               region is specified, it is taken from the provider configuration.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cloud_function"] = cloud_function
        __props__["etag"] = etag
        __props__["policy_data"] = policy_data
        __props__["project"] = project
        __props__["region"] = region
        return FunctionIamPolicy(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
