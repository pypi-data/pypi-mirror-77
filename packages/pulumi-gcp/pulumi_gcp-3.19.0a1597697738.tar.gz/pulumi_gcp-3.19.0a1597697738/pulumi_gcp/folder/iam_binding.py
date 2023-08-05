# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class IAMBinding(pulumi.CustomResource):
    condition: pulumi.Output[dict]
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the folder's IAM policy.
    """
    folder: pulumi.Output[str]
    """
    The resource name of the folder the policy is attached to. Its format is folders/{folder_id}.
    """
    members: pulumi.Output[list]
    """
    An array of identities that will be granted the privilege in the `role`.
    Each entry can have one of the following values:
    * **user:{emailid}**: An email address that is associated with a specific Google account. For example, alice@gmail.com.
    * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
    * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
    * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
    * For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
    """
    role: pulumi.Output[str]
    """
    The role that should be applied. Only one
    `folder.IAMBinding` can be used per role. Note that custom roles must be of the format
    `[projects|organizations]/{parent-name}/roles/{role-name}`.
    """
    def __init__(__self__, resource_name, opts=None, condition=None, folder=None, members=None, role=None, __props__=None, __name__=None, __opts__=None):
        """
        Allows creation and management of a single binding within IAM policy for
        an existing Google Cloud Platform folder.

        > **Note:** This resource _must not_ be used in conjunction with
           `folder.IAMPolicy` or they will fight over what your policy
           should be.

        > **Note:** On create, this resource will overwrite members of any existing roles.
            Use `pulumi import` and inspect the output to ensure
            your existing members are preserved.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] folder: The resource name of the folder the policy is attached to. Its format is folders/{folder_id}.
        :param pulumi.Input[list] members: An array of identities that will be granted the privilege in the `role`.
               Each entry can have one of the following values:
               * **user:{emailid}**: An email address that is associated with a specific Google account. For example, alice@gmail.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `folder.IAMBinding` can be used per role. Note that custom roles must be of the format
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
            if folder is None:
                raise TypeError("Missing required property 'folder'")
            __props__['folder'] = folder
            if members is None:
                raise TypeError("Missing required property 'members'")
            __props__['members'] = members
            if role is None:
                raise TypeError("Missing required property 'role'")
            __props__['role'] = role
            __props__['etag'] = None
        super(IAMBinding, __self__).__init__(
            'gcp:folder/iAMBinding:IAMBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, condition=None, etag=None, folder=None, members=None, role=None):
        """
        Get an existing IAMBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: (Computed) The etag of the folder's IAM policy.
        :param pulumi.Input[str] folder: The resource name of the folder the policy is attached to. Its format is folders/{folder_id}.
        :param pulumi.Input[list] members: An array of identities that will be granted the privilege in the `role`.
               Each entry can have one of the following values:
               * **user:{emailid}**: An email address that is associated with a specific Google account. For example, alice@gmail.com.
               * **serviceAccount:{emailid}**: An email address that represents a service account. For example, my-other-app@appspot.gserviceaccount.com.
               * **group:{emailid}**: An email address that represents a Google group. For example, admins@example.com.
               * **domain:{domain}**: A G Suite domain (primary, instead of alias) name that represents all the users of that domain. For example, google.com or example.com.
               * For more details on format and restrictions see https://cloud.google.com/billing/reference/rest/v1/Policy#Binding
        :param pulumi.Input[str] role: The role that should be applied. Only one
               `folder.IAMBinding` can be used per role. Note that custom roles must be of the format
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
        __props__["folder"] = folder
        __props__["members"] = members
        __props__["role"] = role
        return IAMBinding(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
