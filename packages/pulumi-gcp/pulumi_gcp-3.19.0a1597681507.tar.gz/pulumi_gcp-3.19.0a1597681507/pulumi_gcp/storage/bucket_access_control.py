# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class BucketAccessControl(pulumi.CustomResource):
    bucket: pulumi.Output[str]
    """
    The name of the bucket.
    """
    domain: pulumi.Output[str]
    """
    The domain associated with the entity.
    """
    email: pulumi.Output[str]
    """
    The email address associated with the entity.
    """
    entity: pulumi.Output[str]
    """
    The entity holding the permission, in one of the following forms:
    user-userId
    user-email
    group-groupId
    group-email
    domain-domain
    project-team-projectId
    allUsers
    allAuthenticatedUsers
    Examples:
    The user liz@example.com would be user-liz@example.com.
    The group example@googlegroups.com would be
    group-example@googlegroups.com.
    To refer to all members of the Google Apps for Business domain
    example.com, the entity would be domain-example.com.
    """
    role: pulumi.Output[str]
    """
    The access permission for the entity.
    Possible values are `OWNER`, `READER`, and `WRITER`.
    """
    def __init__(__self__, resource_name, opts=None, bucket=None, entity=None, role=None, __props__=None, __name__=None, __opts__=None):
        """
        Bucket ACLs can be managed authoritatively using the
        `storage_bucket_acl` resource. Do not use these two resources in conjunction to manage the same bucket.

        The BucketAccessControls resource manages the Access Control List
        (ACLs) for a single entity/role pairing on a bucket. ACLs let you specify who
        has access to your data and to what extent.

        There are three roles that can be assigned to an entity:

        READERs can get the bucket, though no acl property will be returned, and
        list the bucket's objects.  WRITERs are READERs, and they can insert
        objects into the bucket and delete the bucket's objects.  OWNERs are
        WRITERs, and they can get the acl property of a bucket, update a bucket,
        and call all BucketAccessControls methods on the bucket.  For more
        information, see Access Control, with the caveat that this API uses
        READER, WRITER, and OWNER instead of READ, WRITE, and FULL_CONTROL.

        To get more information about BucketAccessControl, see:

        * [API documentation](https://cloud.google.com/storage/docs/json_api/v1/bucketAccessControls)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/storage/docs/access-control/lists)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[str] entity: The entity holding the permission, in one of the following forms:
               user-userId
               user-email
               group-groupId
               group-email
               domain-domain
               project-team-projectId
               allUsers
               allAuthenticatedUsers
               Examples:
               The user liz@example.com would be user-liz@example.com.
               The group example@googlegroups.com would be
               group-example@googlegroups.com.
               To refer to all members of the Google Apps for Business domain
               example.com, the entity would be domain-example.com.
        :param pulumi.Input[str] role: The access permission for the entity.
               Possible values are `OWNER`, `READER`, and `WRITER`.
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
            if entity is None:
                raise TypeError("Missing required property 'entity'")
            __props__['entity'] = entity
            __props__['role'] = role
            __props__['domain'] = None
            __props__['email'] = None
        super(BucketAccessControl, __self__).__init__(
            'gcp:storage/bucketAccessControl:BucketAccessControl',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bucket=None, domain=None, email=None, entity=None, role=None):
        """
        Get an existing BucketAccessControl resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket.
        :param pulumi.Input[str] domain: The domain associated with the entity.
        :param pulumi.Input[str] email: The email address associated with the entity.
        :param pulumi.Input[str] entity: The entity holding the permission, in one of the following forms:
               user-userId
               user-email
               group-groupId
               group-email
               domain-domain
               project-team-projectId
               allUsers
               allAuthenticatedUsers
               Examples:
               The user liz@example.com would be user-liz@example.com.
               The group example@googlegroups.com would be
               group-example@googlegroups.com.
               To refer to all members of the Google Apps for Business domain
               example.com, the entity would be domain-example.com.
        :param pulumi.Input[str] role: The access permission for the entity.
               Possible values are `OWNER`, `READER`, and `WRITER`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket"] = bucket
        __props__["domain"] = domain
        __props__["email"] = email
        __props__["entity"] = entity
        __props__["role"] = role
        return BucketAccessControl(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
