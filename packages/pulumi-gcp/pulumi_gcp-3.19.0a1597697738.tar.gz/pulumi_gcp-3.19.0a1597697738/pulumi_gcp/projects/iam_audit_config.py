# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class IAMAuditConfig(pulumi.CustomResource):
    audit_log_configs: pulumi.Output[list]
    """
    The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.

      * `exemptedMembers` (`list`) - Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
      * `logType` (`str`) - Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
    """
    etag: pulumi.Output[str]
    """
    (Computed) The etag of the project's IAM policy.
    """
    project: pulumi.Output[str]
    """
    The project ID. If not specified for `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig`, uses the ID of the project configured with the provider.
    Required for `projects.IAMPolicy` - you must explicitly set the project, and it
    will not be inferred from the provider.
    """
    service: pulumi.Output[str]
    """
    Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\_project\_iam\_audit\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.
    """
    def __init__(__self__, resource_name, opts=None, audit_log_configs=None, project=None, service=None, __props__=None, __name__=None, __opts__=None):
        """
        Four different resources help you manage your IAM policy for a project. Each of these resources serves a different use case:

        * `projects.IAMPolicy`: Authoritative. Sets the IAM policy for the project and replaces any existing policy already attached.
        * `projects.IAMBinding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the project are preserved.
        * `projects.IAMMember`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the project are preserved.
        * `projects.IAMAuditConfig`: Authoritative for a given service. Updates the IAM policy to enable audit logging for the given service.

        > **Note:** `projects.IAMPolicy` **cannot** be used in conjunction with `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig` or they will fight over what your policy should be.

        > **Note:** `projects.IAMBinding` resources **can be** used in conjunction with `projects.IAMMember` resources **only if** they do not grant privilege to the same role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] project: The project ID. If not specified for `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig`, uses the ID of the project configured with the provider.
               Required for `projects.IAMPolicy` - you must explicitly set the project, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\_project\_iam\_audit\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.

        The **audit_log_configs** object supports the following:

          * `exemptedMembers` (`pulumi.Input[list]`) - Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
          * `logType` (`pulumi.Input[str]`) - Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
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

            if audit_log_configs is None:
                raise TypeError("Missing required property 'audit_log_configs'")
            __props__['audit_log_configs'] = audit_log_configs
            __props__['project'] = project
            if service is None:
                raise TypeError("Missing required property 'service'")
            __props__['service'] = service
            __props__['etag'] = None
        super(IAMAuditConfig, __self__).__init__(
            'gcp:projects/iAMAuditConfig:IAMAuditConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, audit_log_configs=None, etag=None, project=None, service=None):
        """
        Get an existing IAMAuditConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] audit_log_configs: The configuration for logging of each type of permission.  This can be specified multiple times.  Structure is documented below.
        :param pulumi.Input[str] etag: (Computed) The etag of the project's IAM policy.
        :param pulumi.Input[str] project: The project ID. If not specified for `projects.IAMBinding`, `projects.IAMMember`, or `projects.IAMAuditConfig`, uses the ID of the project configured with the provider.
               Required for `projects.IAMPolicy` - you must explicitly set the project, and it
               will not be inferred from the provider.
        :param pulumi.Input[str] service: Service which will be enabled for audit logging.  The special value `allServices` covers all services.  Note that if there are google\_project\_iam\_audit\_config resources covering both `allServices` and a specific service then the union of the two AuditConfigs is used for that service: the `log_types` specified in each `audit_log_config` are enabled, and the `exempted_members` in each `audit_log_config` are exempted.

        The **audit_log_configs** object supports the following:

          * `exemptedMembers` (`pulumi.Input[list]`) - Identities that do not cause logging for this type of permission.  The format is the same as that for `members`.
          * `logType` (`pulumi.Input[str]`) - Permission type for which logging is to be configured.  Must be one of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["audit_log_configs"] = audit_log_configs
        __props__["etag"] = etag
        __props__["project"] = project
        __props__["service"] = service
        return IAMAuditConfig(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
