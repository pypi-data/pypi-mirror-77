# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class IAMMember(pulumi.CustomResource):
    condition: pulumi.Output[dict]
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the organization's IAM policy.
    """
    member: pulumi.Output[str]
    """
    The user that the role should apply to. For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
    """
    org_id: pulumi.Output[str]
    """
    The numeric ID of the organization in which you want to create a custom role.
    """
    role: pulumi.Output[str]
    """
    The role that should be applied. Note that custom roles must be of the format
    `[projects|organizations]/{parent-name}/roles/{role-name}`.
    """
    def __init__(__self__, resource_name, opts=None, condition=None, member=None, org_id=None, role=None, __props__=None, __name__=None, __opts__=None):
        """
        Allows creation and management of a single member for a single binding within
        the IAM policy for an existing Google Cloud Platform Organization.

        > **Note:** This resource __must not__ be used in conjunction with
           `organizations.IAMBinding` for the __same role__ or they will fight over
           what your policy should be.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] member: The user that the role should apply to. For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
        :param pulumi.Input[str] org_id: The numeric ID of the organization in which you want to create a custom role.
        :param pulumi.Input[str] role: The role that should be applied. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.

        The **condition** object supports the following:

          * `description` (`pulumi.Input[str]`)
          * `expression` (`pulumi.Input[str]`)
          * `title` (`pulumi.Input[str]`)
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

            __props__['condition'] = condition
            if member is None:
                raise TypeError("Missing required property 'member'")
            __props__['member'] = member
            if org_id is None:
                raise TypeError("Missing required property 'org_id'")
            __props__['org_id'] = org_id
            if role is None:
                raise TypeError("Missing required property 'role'")
            __props__['role'] = role
            __props__['etag'] = None
        super(IAMMember, __self__).__init__(
            'gcp:organizations/iAMMember:IAMMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, condition=None, etag=None, member=None, org_id=None, role=None):
        """
        Get an existing IAMMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the organization's IAM policy.
        :param pulumi.Input[str] member: The user that the role should apply to. For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
        :param pulumi.Input[str] org_id: The numeric ID of the organization in which you want to create a custom role.
        :param pulumi.Input[str] role: The role that should be applied. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.

        The **condition** object supports the following:

          * `description` (`pulumi.Input[str]`)
          * `expression` (`pulumi.Input[str]`)
          * `title` (`pulumi.Input[str]`)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["condition"] = condition
        __props__["etag"] = etag
        __props__["member"] = member
        __props__["org_id"] = org_id
        __props__["role"] = role
        return IAMMember(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
