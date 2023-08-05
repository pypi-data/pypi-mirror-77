# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class DatasetAccess(pulumi.CustomResource):
    dataset_id: pulumi.Output[str]
    """
    The ID of the dataset containing this table.
    """
    domain: pulumi.Output[str]
    """
    A domain to grant access to. Any users signed in with the
    domain specified will be granted the specified access
    """
    group_by_email: pulumi.Output[str]
    """
    An email address of a Google Group to grant access to.
    """
    iam_member: pulumi.Output[str]
    """
    Some other type of member that appears in the IAM Policy but isn't a user,
    group, domain, or special group. For example: `allUsers`
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    role: pulumi.Output[str]
    """
    Describes the rights granted to the user specified by the other
    member of the access object. Primitive, Predefined and custom
    roles are supported. Predefined roles that have equivalent
    primitive roles are swapped by the API to their Primitive
    counterparts, and will show a diff post-create. See
    [official docs](https://cloud.google.com/bigquery/docs/access-control).
    """
    special_group: pulumi.Output[str]
    """
    A special group to grant access to. Possible values include:
    """
    user_by_email: pulumi.Output[str]
    """
    An email address of a user to grant access to. For example:
    fred@example.com
    """
    view: pulumi.Output[dict]
    """
    A view from a different dataset to grant access to. Queries
    executed against that view will have read access to tables in
    this dataset. The role field is not required when this field is
    set. If that view is updated by any user, access to the view
    needs to be granted again via an update operation.
    Structure is documented below.

      * `dataset_id` (`str`) - The ID of the dataset containing this table.
      * `project_id` (`str`) - The ID of the project containing this table.
      * `table_id` (`str`) - The ID of the table. The ID must contain only letters (a-z,
        A-Z), numbers (0-9), or underscores (_). The maximum length
        is 1,024 characters.
    """
    def __init__(__self__, resource_name, opts=None, dataset_id=None, domain=None, group_by_email=None, iam_member=None, project=None, role=None, special_group=None, user_by_email=None, view=None, __props__=None, __name__=None, __opts__=None):
        """
        Gives dataset access for a single entity. This resource is intended to be used in cases where
        it is not possible to compile a full list of access blocks to include in a
        `bigquery.Dataset` resource, to enable them to be added separately.

        > **Note:** If this resource is used alongside a `bigquery.Dataset` resource, the
        dataset resource must either have no defined `access` blocks or a `lifecycle` block with
        `ignore_changes = [access]` so they don't fight over which accesses should be on the dataset.

        To get more information about DatasetAccess, see:

        * [API documentation](https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets)
        * How-to Guides
            * [Controlling access to datasets](https://cloud.google.com/bigquery/docs/dataset-access-controls)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_id: The ID of the dataset containing this table.
        :param pulumi.Input[str] domain: A domain to grant access to. Any users signed in with the
               domain specified will be granted the specified access
        :param pulumi.Input[str] group_by_email: An email address of a Google Group to grant access to.
        :param pulumi.Input[str] iam_member: Some other type of member that appears in the IAM Policy but isn't a user,
               group, domain, or special group. For example: `allUsers`
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] role: Describes the rights granted to the user specified by the other
               member of the access object. Primitive, Predefined and custom
               roles are supported. Predefined roles that have equivalent
               primitive roles are swapped by the API to their Primitive
               counterparts, and will show a diff post-create. See
               [official docs](https://cloud.google.com/bigquery/docs/access-control).
        :param pulumi.Input[str] special_group: A special group to grant access to. Possible values include:
        :param pulumi.Input[str] user_by_email: An email address of a user to grant access to. For example:
               fred@example.com
        :param pulumi.Input[dict] view: A view from a different dataset to grant access to. Queries
               executed against that view will have read access to tables in
               this dataset. The role field is not required when this field is
               set. If that view is updated by any user, access to the view
               needs to be granted again via an update operation.
               Structure is documented below.

        The **view** object supports the following:

          * `dataset_id` (`pulumi.Input[str]`) - The ID of the dataset containing this table.
          * `project_id` (`pulumi.Input[str]`) - The ID of the project containing this table.
          * `table_id` (`pulumi.Input[str]`) - The ID of the table. The ID must contain only letters (a-z,
            A-Z), numbers (0-9), or underscores (_). The maximum length
            is 1,024 characters.
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

            if dataset_id is None:
                raise TypeError("Missing required property 'dataset_id'")
            __props__['dataset_id'] = dataset_id
            __props__['domain'] = domain
            __props__['group_by_email'] = group_by_email
            __props__['iam_member'] = iam_member
            __props__['project'] = project
            __props__['role'] = role
            __props__['special_group'] = special_group
            __props__['user_by_email'] = user_by_email
            __props__['view'] = view
        super(DatasetAccess, __self__).__init__(
            'gcp:bigquery/datasetAccess:DatasetAccess',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, dataset_id=None, domain=None, group_by_email=None, iam_member=None, project=None, role=None, special_group=None, user_by_email=None, view=None):
        """
        Get an existing DatasetAccess resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_id: The ID of the dataset containing this table.
        :param pulumi.Input[str] domain: A domain to grant access to. Any users signed in with the
               domain specified will be granted the specified access
        :param pulumi.Input[str] group_by_email: An email address of a Google Group to grant access to.
        :param pulumi.Input[str] iam_member: Some other type of member that appears in the IAM Policy but isn't a user,
               group, domain, or special group. For example: `allUsers`
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] role: Describes the rights granted to the user specified by the other
               member of the access object. Primitive, Predefined and custom
               roles are supported. Predefined roles that have equivalent
               primitive roles are swapped by the API to their Primitive
               counterparts, and will show a diff post-create. See
               [official docs](https://cloud.google.com/bigquery/docs/access-control).
        :param pulumi.Input[str] special_group: A special group to grant access to. Possible values include:
        :param pulumi.Input[str] user_by_email: An email address of a user to grant access to. For example:
               fred@example.com
        :param pulumi.Input[dict] view: A view from a different dataset to grant access to. Queries
               executed against that view will have read access to tables in
               this dataset. The role field is not required when this field is
               set. If that view is updated by any user, access to the view
               needs to be granted again via an update operation.
               Structure is documented below.

        The **view** object supports the following:

          * `dataset_id` (`pulumi.Input[str]`) - The ID of the dataset containing this table.
          * `project_id` (`pulumi.Input[str]`) - The ID of the project containing this table.
          * `table_id` (`pulumi.Input[str]`) - The ID of the table. The ID must contain only letters (a-z,
            A-Z), numbers (0-9), or underscores (_). The maximum length
            is 1,024 characters.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["dataset_id"] = dataset_id
        __props__["domain"] = domain
        __props__["group_by_email"] = group_by_email
        __props__["iam_member"] = iam_member
        __props__["project"] = project
        __props__["role"] = role
        __props__["special_group"] = special_group
        __props__["user_by_email"] = user_by_email
        __props__["view"] = view
        return DatasetAccess(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
