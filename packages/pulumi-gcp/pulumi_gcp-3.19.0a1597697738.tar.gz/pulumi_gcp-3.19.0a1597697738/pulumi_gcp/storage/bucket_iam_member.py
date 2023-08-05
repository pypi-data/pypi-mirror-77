# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class BucketIAMMember(pulumi.CustomResource):
    bucket: pulumi.Output[str]
    """
    Used to find the parent resource to bind the IAM policy to
    """
    condition: pulumi.Output[dict]
    """
    ) An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
    Structure is documented below.

      * `description` (`str`) - An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
      * `expression` (`str`) - Textual representation of an expression in Common Expression Language syntax.
      * `title` (`str`) - A title for the expression, i.e. a short string describing its purpose.
    """
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the IAM policy.
    """
    member: pulumi.Output[str]
    role: pulumi.Output[str]
    """
    The role that should be applied. Only one
    `storage.BucketIAMBinding` can be used per role. Note that custom roles must be of the format
    `[projects|organizations]/{parent-name}/roles/{role-name}`.
    """
    def __init__(__self__, resource_name, opts=None, bucket=None, condition=None, member=None, role=None, __props__=None, __name__=None, __opts__=None):
        """
        Three different resources help you manage your IAM policy for Cloud Storage Bucket. Each of these resources serves a different use case:

        * `storage.BucketIAMPolicy`: Authoritative. Sets the IAM policy for the bucket and replaces any existing policy already attached.
        * `storage.BucketIAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the bucket are preserved.
        * `storage.BucketIAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the bucket are preserved.

        > **Note:** `storage.BucketIAMPolicy` **cannot** be used in conjunction with `storage.BucketIAMBinding` and `storage.BucketIAMMember` or they will fight over what your policy should be.

        > **Note:** `storage.BucketIAMBinding` resources **can be** used in conjunction with `storage.BucketIAMMember` resources **only if** they do not grant privilege to the same role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[dict] condition: ) An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `storage.BucketIAMBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.

        The **condition** object supports the following:

          * `description` (`pulumi.Input[str]`) - An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
          * `expression` (`pulumi.Input[str]`) - Textual representation of an expression in Common Expression Language syntax.
          * `title` (`pulumi.Input[str]`) - A title for the expression, i.e. a short string describing its purpose.
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

            if bucket is None:
                raise TypeError("Missing required property 'bucket'")
            __props__['bucket'] = bucket
            __props__['condition'] = condition
            if member is None:
                raise TypeError("Missing required property 'member'")
            __props__['member'] = member
            if role is None:
                raise TypeError("Missing required property 'role'")
            __props__['role'] = role
            __props__['etag'] = None
        super(BucketIAMMember, __self__).__init__(
            'gcp:storage/bucketIAMMember:BucketIAMMember',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bucket=None, condition=None, etag=None, member=None, role=None):
        """
        Get an existing BucketIAMMember resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Used to find the parent resource to bind the IAM policy to
        :param pulumi.Input[dict] condition: ) An [IAM Condition](https://cloud.google.com/iam/docs/conditions-overview) for a given binding.
               Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the IAM policy.
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `storage.BucketIAMBinding` can be used per role. Note that custom roles must be of the format
               `[projects|organizations]/{parent-name}/roles/{role-name}`.

        The **condition** object supports the following:

          * `description` (`pulumi.Input[str]`) - An optional description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
          * `expression` (`pulumi.Input[str]`) - Textual representation of an expression in Common Expression Language syntax.
          * `title` (`pulumi.Input[str]`) - A title for the expression, i.e. a short string describing its purpose.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket"] = bucket
        __props__["condition"] = condition
        __props__["etag"] = etag
        __props__["member"] = member
        __props__["role"] = role
        return BucketIAMMember(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
