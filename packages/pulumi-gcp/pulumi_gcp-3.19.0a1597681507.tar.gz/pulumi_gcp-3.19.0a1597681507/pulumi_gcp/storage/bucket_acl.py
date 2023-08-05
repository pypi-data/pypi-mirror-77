# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class BucketACL(pulumi.CustomResource):
    bucket: pulumi.Output[str]
    """
    The name of the bucket it applies to.
    """
    default_acl: pulumi.Output[str]
    """
    Configure this ACL to be the default ACL.
    """
    predefined_acl: pulumi.Output[str]
    """
    The [canned GCS ACL](https://cloud.google.com/storage/docs/access-control/lists#predefined-acl) to apply. Must be set if `role_entity` is not.
    """
    role_entities: pulumi.Output[list]
    """
    List of role/entity pairs in the form `ROLE:entity`. See [GCS Bucket ACL documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)  for more details. Must be set if `predefined_acl` is not.
    """
    def __init__(__self__, resource_name, opts=None, bucket=None, default_acl=None, predefined_acl=None, role_entities=None, __props__=None, __name__=None, __opts__=None):
        """
        Authoritatively manages a bucket's ACLs in Google cloud storage service (GCS). For more information see
        [the official documentation](https://cloud.google.com/storage/docs/access-control/lists)
        and
        [API](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls).

        Bucket ACLs can be managed non authoritatively using the `storage_bucket_access_control` resource. Do not use these two resources in conjunction to manage the same bucket.

        Permissions can be granted either by ACLs or Cloud IAM policies. In general, permissions granted by Cloud IAM policies do not appear in ACLs, and permissions granted by ACLs do not appear in Cloud IAM policies. The only exception is for ACLs applied directly on a bucket and certain bucket-level Cloud IAM policies, as described in [Cloud IAM relation to ACLs](https://cloud.google.com/storage/docs/access-control/iam#acls).

        **NOTE** This resource will not remove the `project-owners-<project_id>` entity from the `OWNER` role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket it applies to.
        :param pulumi.Input[str] default_acl: Configure this ACL to be the default ACL.
        :param pulumi.Input[str] predefined_acl: The [canned GCS ACL](https://cloud.google.com/storage/docs/access-control/lists#predefined-acl) to apply. Must be set if `role_entity` is not.
        :param pulumi.Input[list] role_entities: List of role/entity pairs in the form `ROLE:entity`. See [GCS Bucket ACL documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)  for more details. Must be set if `predefined_acl` is not.
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

            if bucket is None:
                raise TypeError("Missing required property 'bucket'")
            __props__['bucket'] = bucket
            __props__['default_acl'] = default_acl
            __props__['predefined_acl'] = predefined_acl
            __props__['role_entities'] = role_entities
        super(BucketACL, __self__).__init__(
            'gcp:storage/bucketACL:BucketACL',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bucket=None, default_acl=None, predefined_acl=None, role_entities=None):
        """
        Get an existing BucketACL resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket it applies to.
        :param pulumi.Input[str] default_acl: Configure this ACL to be the default ACL.
        :param pulumi.Input[str] predefined_acl: The [canned GCS ACL](https://cloud.google.com/storage/docs/access-control/lists#predefined-acl) to apply. Must be set if `role_entity` is not.
        :param pulumi.Input[list] role_entities: List of role/entity pairs in the form `ROLE:entity`. See [GCS Bucket ACL documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)  for more details. Must be set if `predefined_acl` is not.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket"] = bucket
        __props__["default_acl"] = default_acl
        __props__["predefined_acl"] = predefined_acl
        __props__["role_entities"] = role_entities
        return BucketACL(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
