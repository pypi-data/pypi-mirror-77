# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class DatasetIamBinding(pulumi.CustomResource):
    condition: pulumi.Output[dict]
    dataset_id: pulumi.Output[str]
    """
    The dataset ID, in the form
    `{project_id}/{location_name}/{dataset_name}` or
    `{location_name}/{dataset_name}`. In the second form, the provider's
    project setting will be used as a fallback.
    """
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the dataset's IAM policy.
    """
    members: pulumi.Output[list]
    role: pulumi.Output[str]
    """
    The role that should be applied. Only one
    `healthcare.DatasetIamBinding` can be used per role. Note that custom roles must be of the format
    `[projects|organizations]/{parent-name}/roles/{role-name}`.
    """
    def __init__(__self__, resource_name, opts=None, condition=None, dataset_id=None, members=None, role=None, __props__=None, __name__=None, __opts__=None):
        """
        Three different resources help you manage your IAM policy for Healthcare dataset. Each of these resources serves a different use case:

        * `healthcare.DatasetIamPolicy`: Authoritative. Sets the IAM policy for the dataset and replaces any existing policy already attached.
        * `healthcare.DatasetIamBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the dataset are preserved.
        * `healthcare.DatasetIamMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the dataset are preserved.

        > **Note:** `healthcare.DatasetIamPolicy` **cannot** be used in conjunction with `healthcare.DatasetIamBinding` and `healthcare.DatasetIamMember` or they will fight over what your policy should be.

        > **Note:** `healthcare.DatasetIamBinding` resources **can be** used in conjunction with `healthcare.DatasetIamMember` resources **only if** they do not grant privilege to the same role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_id: The dataset ID, in the form
               `{project_id}/{location_name}/{dataset_name}` or
               `{location_name}/{dataset_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.DatasetIamBinding` can be used per role. Note that custom roles must be of the format
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
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['condition'] = condition
            if dataset_id is None:
                raise TypeError("Missing required property 'dataset_id'")
            __props__['dataset_id'] = dataset_id
            if members is None:
                raise TypeError("Missing required property 'members'")
            __props__['members'] = members
            if role is None:
                raise TypeError("Missing required property 'role'")
            __props__['role'] = role
            __props__['etag'] = None
        super(DatasetIamBinding, __self__).__init__(
            'gcp:healthcare/datasetIamBinding:DatasetIamBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, condition=None, dataset_id=None, etag=None, members=None, role=None):
        """
        Get an existing DatasetIamBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_id: The dataset ID, in the form
               `{project_id}/{location_name}/{dataset_name}` or
               `{location_name}/{dataset_name}`. In the second form, the provider's
               project setting will be used as a fallback.
        :param pulumi.Input[str] etag: (Computed) The etag of the dataset's IAM policy.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `healthcare.DatasetIamBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.

        The **condition** object supports the following:

          * `description` (`pulumi.Input[str]`)
          * `expression` (`pulumi.Input[str]`)
          * `title` (`pulumi.Input[str]`)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["condition"] = condition
        __props__["dataset_id"] = dataset_id
        __props__["etag"] = etag
        __props__["members"] = members
        __props__["role"] = role
        return DatasetIamBinding(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
