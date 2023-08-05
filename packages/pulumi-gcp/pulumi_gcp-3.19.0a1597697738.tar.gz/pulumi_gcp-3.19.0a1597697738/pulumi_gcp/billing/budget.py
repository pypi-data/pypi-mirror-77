# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Budget(pulumi.CustomResource):
    all_updates_rule: pulumi.Output[dict]
    """
    Defines notifications that are sent on every update to the
    billing account's spend, regardless of the thresholds defined
    using threshold rules.
    Structure is documented below.

      * `pubsubTopic` (`str`) - The name of the Cloud Pub/Sub topic where budget related
        messages will be published, in the form
        projects/{project_id}/topics/{topic_id}. Updates are sent
        at regular intervals to the topic.
      * `schemaVersion` (`str`) - The schema version of the notification. Only "1.0" is
        accepted. It represents the JSON schema as defined in
        https://cloud.google.com/billing/docs/how-to/budgets#notification_format.
    """
    amount: pulumi.Output[dict]
    """
    The budgeted amount for each usage period.
    Structure is documented below.

      * `specifiedAmount` (`dict`) - A specified amount to use as the budget. currencyCode is
        optional. If specified, it must match the currency of the
        billing account. The currencyCode is provided on output.
        Structure is documented below.
        * `currencyCode` (`str`) - The 3-letter currency code defined in ISO 4217.
        * `nanos` (`float`) - Number of nano (10^-9) units of the amount.
          The value must be between -999,999,999 and +999,999,999
          inclusive. If units is positive, nanos must be positive or
          zero. If units is zero, nanos can be positive, zero, or
          negative. If units is negative, nanos must be negative or
          zero. For example $-1.75 is represented as units=-1 and
          nanos=-750,000,000.
        * `units` (`str`) - The whole units of the amount. For example if currencyCode
          is "USD", then 1 unit is one US dollar.
    """
    billing_account: pulumi.Output[str]
    """
    ID of the billing account to set a budget on.
    """
    budget_filter: pulumi.Output[dict]
    """
    Filters that define which resources are used to compute the actual
    spend against the budget.
    Structure is documented below.

      * `creditTypesTreatment` (`str`) - Specifies how credits should be treated when determining spend
        for threshold calculations.
        Default value is `INCLUDE_ALL_CREDITS`.
        Possible values are `INCLUDE_ALL_CREDITS` and `EXCLUDE_ALL_CREDITS`.
      * `projects` (`list`) - A set of projects of the form projects/{project_id},
        specifying that usage from only this set of projects should be
        included in the budget. If omitted, the report will include
        all usage for the billing account, regardless of which project
        the usage occurred on. Only zero or one project can be
        specified currently.
      * `services` (`list`) - A set of services of the form services/{service_id},
        specifying that usage from only this set of services should be
        included in the budget. If omitted, the report will include
        usage for all the services. The service names are available
        through the Catalog API:
        https://cloud.google.com/billing/v1/how-tos/catalog-api.
    """
    display_name: pulumi.Output[str]
    """
    User data for display name in UI. Must be <= 60 chars.
    """
    name: pulumi.Output[str]
    """
    Resource name of the budget. The resource name implies the scope of a budget. Values are of the form
    billingAccounts/{billingAccountId}/budgets/{budgetId}.
    """
    threshold_rules: pulumi.Output[list]
    """
    Rules that trigger alerts (notifications of thresholds being
    crossed) when spend exceeds the specified percentages of the
    budget.
    Structure is documented below.

      * `spendBasis` (`str`) - The type of basis used to determine if spend has passed
        the threshold.
        Default value is `CURRENT_SPEND`.
        Possible values are `CURRENT_SPEND` and `FORECASTED_SPEND`.
      * `thresholdPercent` (`float`) - Send an alert when this threshold is exceeded. This is a
        1.0-based percentage, so 0.5 = 50%. Must be >= 0.
    """
    def __init__(__self__, resource_name, opts=None, all_updates_rule=None, amount=None, billing_account=None, budget_filter=None, display_name=None, threshold_rules=None, __props__=None, __name__=None, __opts__=None):
        """
        Budget configuration for a billing account.

        To get more information about Budget, see:

        * [API documentation](https://cloud.google.com/billing/docs/reference/budget/rest/v1beta1/billingAccounts.budgets)
        * How-to Guides
            * [Creating a budget](https://cloud.google.com/billing/docs/how-to/budgets)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] all_updates_rule: Defines notifications that are sent on every update to the
               billing account's spend, regardless of the thresholds defined
               using threshold rules.
               Structure is documented below.
        :param pulumi.Input[dict] amount: The budgeted amount for each usage period.
               Structure is documented below.
        :param pulumi.Input[str] billing_account: ID of the billing account to set a budget on.
        :param pulumi.Input[dict] budget_filter: Filters that define which resources are used to compute the actual
               spend against the budget.
               Structure is documented below.
        :param pulumi.Input[str] display_name: User data for display name in UI. Must be <= 60 chars.
        :param pulumi.Input[list] threshold_rules: Rules that trigger alerts (notifications of thresholds being
               crossed) when spend exceeds the specified percentages of the
               budget.
               Structure is documented below.

        The **all_updates_rule** object supports the following:

          * `pubsubTopic` (`pulumi.Input[str]`) - The name of the Cloud Pub/Sub topic where budget related
            messages will be published, in the form
            projects/{project_id}/topics/{topic_id}. Updates are sent
            at regular intervals to the topic.
          * `schemaVersion` (`pulumi.Input[str]`) - The schema version of the notification. Only "1.0" is
            accepted. It represents the JSON schema as defined in
            https://cloud.google.com/billing/docs/how-to/budgets#notification_format.

        The **amount** object supports the following:

          * `specifiedAmount` (`pulumi.Input[dict]`) - A specified amount to use as the budget. currencyCode is
            optional. If specified, it must match the currency of the
            billing account. The currencyCode is provided on output.
            Structure is documented below.
            * `currencyCode` (`pulumi.Input[str]`) - The 3-letter currency code defined in ISO 4217.
            * `nanos` (`pulumi.Input[float]`) - Number of nano (10^-9) units of the amount.
              The value must be between -999,999,999 and +999,999,999
              inclusive. If units is positive, nanos must be positive or
              zero. If units is zero, nanos can be positive, zero, or
              negative. If units is negative, nanos must be negative or
              zero. For example $-1.75 is represented as units=-1 and
              nanos=-750,000,000.
            * `units` (`pulumi.Input[str]`) - The whole units of the amount. For example if currencyCode
              is "USD", then 1 unit is one US dollar.

        The **budget_filter** object supports the following:

          * `creditTypesTreatment` (`pulumi.Input[str]`) - Specifies how credits should be treated when determining spend
            for threshold calculations.
            Default value is `INCLUDE_ALL_CREDITS`.
            Possible values are `INCLUDE_ALL_CREDITS` and `EXCLUDE_ALL_CREDITS`.
          * `projects` (`pulumi.Input[list]`) - A set of projects of the form projects/{project_id},
            specifying that usage from only this set of projects should be
            included in the budget. If omitted, the report will include
            all usage for the billing account, regardless of which project
            the usage occurred on. Only zero or one project can be
            specified currently.
          * `services` (`pulumi.Input[list]`) - A set of services of the form services/{service_id},
            specifying that usage from only this set of services should be
            included in the budget. If omitted, the report will include
            usage for all the services. The service names are available
            through the Catalog API:
            https://cloud.google.com/billing/v1/how-tos/catalog-api.

        The **threshold_rules** object supports the following:

          * `spendBasis` (`pulumi.Input[str]`) - The type of basis used to determine if spend has passed
            the threshold.
            Default value is `CURRENT_SPEND`.
            Possible values are `CURRENT_SPEND` and `FORECASTED_SPEND`.
          * `thresholdPercent` (`pulumi.Input[float]`) - Send an alert when this threshold is exceeded. This is a
            1.0-based percentage, so 0.5 = 50%. Must be >= 0.
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

            __props__['all_updates_rule'] = all_updates_rule
            if amount is None:
                raise TypeError("Missing required property 'amount'")
            __props__['amount'] = amount
            if billing_account is None:
                raise TypeError("Missing required property 'billing_account'")
            __props__['billing_account'] = billing_account
            __props__['budget_filter'] = budget_filter
            __props__['display_name'] = display_name
            if threshold_rules is None:
                raise TypeError("Missing required property 'threshold_rules'")
            __props__['threshold_rules'] = threshold_rules
            __props__['name'] = None
        super(Budget, __self__).__init__(
            'gcp:billing/budget:Budget',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, all_updates_rule=None, amount=None, billing_account=None, budget_filter=None, display_name=None, name=None, threshold_rules=None):
        """
        Get an existing Budget resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] all_updates_rule: Defines notifications that are sent on every update to the
               billing account's spend, regardless of the thresholds defined
               using threshold rules.
               Structure is documented below.
        :param pulumi.Input[dict] amount: The budgeted amount for each usage period.
               Structure is documented below.
        :param pulumi.Input[str] billing_account: ID of the billing account to set a budget on.
        :param pulumi.Input[dict] budget_filter: Filters that define which resources are used to compute the actual
               spend against the budget.
               Structure is documented below.
        :param pulumi.Input[str] display_name: User data for display name in UI. Must be <= 60 chars.
        :param pulumi.Input[str] name: Resource name of the budget. The resource name implies the scope of a budget. Values are of the form
               billingAccounts/{billingAccountId}/budgets/{budgetId}.
        :param pulumi.Input[list] threshold_rules: Rules that trigger alerts (notifications of thresholds being
               crossed) when spend exceeds the specified percentages of the
               budget.
               Structure is documented below.

        The **all_updates_rule** object supports the following:

          * `pubsubTopic` (`pulumi.Input[str]`) - The name of the Cloud Pub/Sub topic where budget related
            messages will be published, in the form
            projects/{project_id}/topics/{topic_id}. Updates are sent
            at regular intervals to the topic.
          * `schemaVersion` (`pulumi.Input[str]`) - The schema version of the notification. Only "1.0" is
            accepted. It represents the JSON schema as defined in
            https://cloud.google.com/billing/docs/how-to/budgets#notification_format.

        The **amount** object supports the following:

          * `specifiedAmount` (`pulumi.Input[dict]`) - A specified amount to use as the budget. currencyCode is
            optional. If specified, it must match the currency of the
            billing account. The currencyCode is provided on output.
            Structure is documented below.
            * `currencyCode` (`pulumi.Input[str]`) - The 3-letter currency code defined in ISO 4217.
            * `nanos` (`pulumi.Input[float]`) - Number of nano (10^-9) units of the amount.
              The value must be between -999,999,999 and +999,999,999
              inclusive. If units is positive, nanos must be positive or
              zero. If units is zero, nanos can be positive, zero, or
              negative. If units is negative, nanos must be negative or
              zero. For example $-1.75 is represented as units=-1 and
              nanos=-750,000,000.
            * `units` (`pulumi.Input[str]`) - The whole units of the amount. For example if currencyCode
              is "USD", then 1 unit is one US dollar.

        The **budget_filter** object supports the following:

          * `creditTypesTreatment` (`pulumi.Input[str]`) - Specifies how credits should be treated when determining spend
            for threshold calculations.
            Default value is `INCLUDE_ALL_CREDITS`.
            Possible values are `INCLUDE_ALL_CREDITS` and `EXCLUDE_ALL_CREDITS`.
          * `projects` (`pulumi.Input[list]`) - A set of projects of the form projects/{project_id},
            specifying that usage from only this set of projects should be
            included in the budget. If omitted, the report will include
            all usage for the billing account, regardless of which project
            the usage occurred on. Only zero or one project can be
            specified currently.
          * `services` (`pulumi.Input[list]`) - A set of services of the form services/{service_id},
            specifying that usage from only this set of services should be
            included in the budget. If omitted, the report will include
            usage for all the services. The service names are available
            through the Catalog API:
            https://cloud.google.com/billing/v1/how-tos/catalog-api.

        The **threshold_rules** object supports the following:

          * `spendBasis` (`pulumi.Input[str]`) - The type of basis used to determine if spend has passed
            the threshold.
            Default value is `CURRENT_SPEND`.
            Possible values are `CURRENT_SPEND` and `FORECASTED_SPEND`.
          * `thresholdPercent` (`pulumi.Input[float]`) - Send an alert when this threshold is exceeded. This is a
            1.0-based percentage, so 0.5 = 50%. Must be >= 0.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["all_updates_rule"] = all_updates_rule
        __props__["amount"] = amount
        __props__["billing_account"] = billing_account
        __props__["budget_filter"] = budget_filter
        __props__["display_name"] = display_name
        __props__["name"] = name
        __props__["threshold_rules"] = threshold_rules
        return Budget(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
