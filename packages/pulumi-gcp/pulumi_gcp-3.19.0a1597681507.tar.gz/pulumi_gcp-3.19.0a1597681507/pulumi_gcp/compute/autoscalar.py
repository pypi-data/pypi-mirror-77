# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

warnings.warn("gcp.compute.Autoscalar has been deprecated in favor of gcp.compute.Autoscaler", DeprecationWarning)


class Autoscalar(pulumi.CustomResource):
    autoscaling_policy: pulumi.Output[dict]
    """
    The configuration parameters for the autoscaling algorithm. You can
    define one or more of the policies for an autoscaler: cpuUtilization,
    customMetricUtilizations, and loadBalancingUtilization.
    If none of these are specified, the default will be to autoscale based
    on cpuUtilization to 0.6 or 60%.
    Structure is documented below.

      * `cooldownPeriod` (`float`) - The number of seconds that the autoscaler should wait before it
        starts collecting information from a new instance. This prevents
        the autoscaler from collecting information when the instance is
        initializing, during which the collected usage would not be
        reliable. The default time autoscaler waits is 60 seconds.
        Virtual machine initialization times might vary because of
        numerous factors. We recommend that you test how long an
        instance may take to initialize. To do this, create an instance
        and time the startup process.
      * `cpuUtilization` (`dict`) - Defines the CPU utilization policy that allows the autoscaler to
        scale based on the average CPU utilization of a managed instance
        group.
        Structure is documented below.
        * `target` (`float`) - Fraction of backend capacity utilization (set in HTTP(s) load
          balancing configuration) that autoscaler should maintain. Must
          be a positive float value. If not defined, the default is 0.8.

      * `loadBalancingUtilization` (`dict`) - Configuration parameters of autoscaling based on a load balancer.
        Structure is documented below.
        * `target` (`float`) - Fraction of backend capacity utilization (set in HTTP(s) load
          balancing configuration) that autoscaler should maintain. Must
          be a positive float value. If not defined, the default is 0.8.

      * `maxReplicas` (`float`) - The maximum number of instances that the autoscaler can scale up
        to. This is required when creating or updating an autoscaler. The
        maximum number of replicas should not be lower than minimal number
        of replicas.
      * `metrics` (`list`) - Configuration parameters of autoscaling based on a custom metric.
        Structure is documented below.
        * `filter` (`str`) - A filter string to be used as the filter string for
          a Stackdriver Monitoring TimeSeries.list API call.
          This filter is used to select a specific TimeSeries for
          the purpose of autoscaling and to determine whether the metric
          is exporting per-instance or per-group data.
          You can only use the AND operator for joining selectors.
          You can only use direct equality comparison operator (=) without
          any functions for each selector.
          You can specify the metric in both the filter string and in the
          metric field. However, if specified in both places, the metric must
          be identical.
          The monitored resource type determines what kind of values are
          expected for the metric. If it is a gce_instance, the autoscaler
          expects the metric to include a separate TimeSeries for each
          instance in a group. In such a case, you cannot filter on resource
          labels.
          If the resource type is any other value, the autoscaler expects
          this metric to contain values that apply to the entire autoscaled
          instance group and resource label filtering can be performed to
          point autoscaler at the correct TimeSeries to scale upon.
          This is called a per-group metric for the purpose of autoscaling.
          If not specified, the type defaults to gce_instance.
          You should provide a filter that is selective enough to pick just
          one TimeSeries for the autoscaled group or for each of the instances
          (if you are using gce_instance resource type). If multiple
          TimeSeries are returned upon the query execution, the autoscaler
          will sum their respective values to obtain its scaling value.
        * `name` (`str`) - The identifier (type) of the Stackdriver Monitoring metric.
          The metric cannot have negative values.
          The metric must have a value type of INT64 or DOUBLE.
        * `singleInstanceAssignment` (`float`) - If scaling is based on a per-group metric value that represents the
          total amount of work to be done or resource usage, set this value to
          an amount assigned for a single instance of the scaled group.
          The autoscaler will keep the number of instances proportional to the
          value of this metric, the metric itself should not change value due
          to group resizing.
          For example, a good metric to use with the target is
          `pubsub.googleapis.com/subscription/num_undelivered_messages`
          or a custom metric exporting the total number of requests coming to
          your instances.
          A bad example would be a metric exporting an average or median
          latency, since this value can't include a chunk assignable to a
          single instance, it could be better used with utilization_target
          instead.
        * `target` (`float`) - Fraction of backend capacity utilization (set in HTTP(s) load
          balancing configuration) that autoscaler should maintain. Must
          be a positive float value. If not defined, the default is 0.8.
        * `type` (`str`) - Defines how target utilization value is expressed for a
          Stackdriver Monitoring metric.
          Possible values are `GAUGE`, `DELTA_PER_SECOND`, and `DELTA_PER_MINUTE`.

      * `minReplicas` (`float`) - The minimum number of replicas that the autoscaler can scale down
        to. This cannot be less than 0. If not provided, autoscaler will
        choose a default value depending on maximum number of instances
        allowed.
      * `mode` (`str`) - Defines operating mode for this policy.
        Default value is `ON`.
        Possible values are `OFF`, `ONLY_UP`, and `ON`.
      * `scaleDownControl` (`dict`)
        * `maxScaledDownReplicas` (`dict`) - A nested object resource
          Structure is documented below.
          * `fixed` (`float`) - Specifies a fixed number of VM instances. This must be a positive
            integer.
          * `percent` (`float`) - Specifies a percentage of instances between 0 to 100%, inclusive.
            For example, specify 80 for 80%.

        * `timeWindowSec` (`float`) - How long back autoscaling should look when computing recommendations
          to include directives regarding slower scale down, as described above.
    """
    creation_timestamp: pulumi.Output[str]
    """
    Creation timestamp in RFC3339 text format.
    """
    description: pulumi.Output[str]
    """
    An optional description of this resource.
    """
    name: pulumi.Output[str]
    """
    The identifier (type) of the Stackdriver Monitoring metric.
    The metric cannot have negative values.
    The metric must have a value type of INT64 or DOUBLE.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    self_link: pulumi.Output[str]
    """
    The URI of the created resource.
    """
    target: pulumi.Output[str]
    """
    Fraction of backend capacity utilization (set in HTTP(s) load
    balancing configuration) that autoscaler should maintain. Must
    be a positive float value. If not defined, the default is 0.8.
    """
    zone: pulumi.Output[str]
    """
    URL of the zone where the instance group resides.
    """
    warnings.warn("gcp.compute.Autoscalar has been deprecated in favor of gcp.compute.Autoscaler", DeprecationWarning)

    def __init__(__self__, resource_name, opts=None, autoscaling_policy=None, description=None, name=None, project=None, target=None, zone=None, __props__=None, __name__=None, __opts__=None):
        """
        Represents an Autoscaler resource.

        Autoscalers allow you to automatically scale virtual machine instances in
        managed instance groups according to an autoscaling policy that you
        define.

        To get more information about Autoscaler, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/autoscalers)
        * How-to Guides
            * [Autoscaling Groups of Instances](https://cloud.google.com/compute/docs/autoscaler/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: The identifier (type) of the Stackdriver Monitoring metric.
               The metric cannot have negative values.
               The metric must have a value type of INT64 or DOUBLE.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] target: Fraction of backend capacity utilization (set in HTTP(s) load
               balancing configuration) that autoscaler should maintain. Must
               be a positive float value. If not defined, the default is 0.8.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.

        The **autoscaling_policy** object supports the following:

          * `cooldownPeriod` (`pulumi.Input[float]`) - The number of seconds that the autoscaler should wait before it
            starts collecting information from a new instance. This prevents
            the autoscaler from collecting information when the instance is
            initializing, during which the collected usage would not be
            reliable. The default time autoscaler waits is 60 seconds.
            Virtual machine initialization times might vary because of
            numerous factors. We recommend that you test how long an
            instance may take to initialize. To do this, create an instance
            and time the startup process.
          * `cpuUtilization` (`pulumi.Input[dict]`) - Defines the CPU utilization policy that allows the autoscaler to
            scale based on the average CPU utilization of a managed instance
            group.
            Structure is documented below.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.

          * `loadBalancingUtilization` (`pulumi.Input[dict]`) - Configuration parameters of autoscaling based on a load balancer.
            Structure is documented below.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.

          * `maxReplicas` (`pulumi.Input[float]`) - The maximum number of instances that the autoscaler can scale up
            to. This is required when creating or updating an autoscaler. The
            maximum number of replicas should not be lower than minimal number
            of replicas.
          * `metrics` (`pulumi.Input[list]`) - Configuration parameters of autoscaling based on a custom metric.
            Structure is documented below.
            * `filter` (`pulumi.Input[str]`) - A filter string to be used as the filter string for
              a Stackdriver Monitoring TimeSeries.list API call.
              This filter is used to select a specific TimeSeries for
              the purpose of autoscaling and to determine whether the metric
              is exporting per-instance or per-group data.
              You can only use the AND operator for joining selectors.
              You can only use direct equality comparison operator (=) without
              any functions for each selector.
              You can specify the metric in both the filter string and in the
              metric field. However, if specified in both places, the metric must
              be identical.
              The monitored resource type determines what kind of values are
              expected for the metric. If it is a gce_instance, the autoscaler
              expects the metric to include a separate TimeSeries for each
              instance in a group. In such a case, you cannot filter on resource
              labels.
              If the resource type is any other value, the autoscaler expects
              this metric to contain values that apply to the entire autoscaled
              instance group and resource label filtering can be performed to
              point autoscaler at the correct TimeSeries to scale upon.
              This is called a per-group metric for the purpose of autoscaling.
              If not specified, the type defaults to gce_instance.
              You should provide a filter that is selective enough to pick just
              one TimeSeries for the autoscaled group or for each of the instances
              (if you are using gce_instance resource type). If multiple
              TimeSeries are returned upon the query execution, the autoscaler
              will sum their respective values to obtain its scaling value.
            * `name` (`pulumi.Input[str]`) - The identifier (type) of the Stackdriver Monitoring metric.
              The metric cannot have negative values.
              The metric must have a value type of INT64 or DOUBLE.
            * `singleInstanceAssignment` (`pulumi.Input[float]`) - If scaling is based on a per-group metric value that represents the
              total amount of work to be done or resource usage, set this value to
              an amount assigned for a single instance of the scaled group.
              The autoscaler will keep the number of instances proportional to the
              value of this metric, the metric itself should not change value due
              to group resizing.
              For example, a good metric to use with the target is
              `pubsub.googleapis.com/subscription/num_undelivered_messages`
              or a custom metric exporting the total number of requests coming to
              your instances.
              A bad example would be a metric exporting an average or median
              latency, since this value can't include a chunk assignable to a
              single instance, it could be better used with utilization_target
              instead.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.
            * `type` (`pulumi.Input[str]`) - Defines how target utilization value is expressed for a
              Stackdriver Monitoring metric.
              Possible values are `GAUGE`, `DELTA_PER_SECOND`, and `DELTA_PER_MINUTE`.

          * `minReplicas` (`pulumi.Input[float]`) - The minimum number of replicas that the autoscaler can scale down
            to. This cannot be less than 0. If not provided, autoscaler will
            choose a default value depending on maximum number of instances
            allowed.
          * `mode` (`pulumi.Input[str]`) - Defines operating mode for this policy.
            Default value is `ON`.
            Possible values are `OFF`, `ONLY_UP`, and `ON`.
          * `scaleDownControl` (`pulumi.Input[dict]`)
            * `maxScaledDownReplicas` (`pulumi.Input[dict]`) - A nested object resource
              Structure is documented below.
              * `fixed` (`pulumi.Input[float]`) - Specifies a fixed number of VM instances. This must be a positive
                integer.
              * `percent` (`pulumi.Input[float]`) - Specifies a percentage of instances between 0 to 100%, inclusive.
                For example, specify 80 for 80%.

            * `timeWindowSec` (`pulumi.Input[float]`) - How long back autoscaling should look when computing recommendations
              to include directives regarding slower scale down, as described above.
        """
        pulumi.log.warn("Autoscalar is deprecated: gcp.compute.Autoscalar has been deprecated in favor of gcp.compute.Autoscaler")
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

            if autoscaling_policy is None:
                raise TypeError("Missing required property 'autoscaling_policy'")
            __props__['autoscaling_policy'] = autoscaling_policy
            __props__['description'] = description
            __props__['name'] = name
            __props__['project'] = project
            if target is None:
                raise TypeError("Missing required property 'target'")
            __props__['target'] = target
            __props__['zone'] = zone
            __props__['creation_timestamp'] = None
            __props__['self_link'] = None
        super(Autoscalar, __self__).__init__(
            'gcp:compute/autoscalar:Autoscalar',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, autoscaling_policy=None, creation_timestamp=None, description=None, name=None, project=None, self_link=None, target=None, zone=None):
        """
        Get an existing Autoscalar resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] autoscaling_policy: The configuration parameters for the autoscaling algorithm. You can
               define one or more of the policies for an autoscaler: cpuUtilization,
               customMetricUtilizations, and loadBalancingUtilization.
               If none of these are specified, the default will be to autoscale based
               on cpuUtilization to 0.6 or 60%.
               Structure is documented below.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: The identifier (type) of the Stackdriver Monitoring metric.
               The metric cannot have negative values.
               The metric must have a value type of INT64 or DOUBLE.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[str] target: Fraction of backend capacity utilization (set in HTTP(s) load
               balancing configuration) that autoscaler should maintain. Must
               be a positive float value. If not defined, the default is 0.8.
        :param pulumi.Input[str] zone: URL of the zone where the instance group resides.

        The **autoscaling_policy** object supports the following:

          * `cooldownPeriod` (`pulumi.Input[float]`) - The number of seconds that the autoscaler should wait before it
            starts collecting information from a new instance. This prevents
            the autoscaler from collecting information when the instance is
            initializing, during which the collected usage would not be
            reliable. The default time autoscaler waits is 60 seconds.
            Virtual machine initialization times might vary because of
            numerous factors. We recommend that you test how long an
            instance may take to initialize. To do this, create an instance
            and time the startup process.
          * `cpuUtilization` (`pulumi.Input[dict]`) - Defines the CPU utilization policy that allows the autoscaler to
            scale based on the average CPU utilization of a managed instance
            group.
            Structure is documented below.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.

          * `loadBalancingUtilization` (`pulumi.Input[dict]`) - Configuration parameters of autoscaling based on a load balancer.
            Structure is documented below.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.

          * `maxReplicas` (`pulumi.Input[float]`) - The maximum number of instances that the autoscaler can scale up
            to. This is required when creating or updating an autoscaler. The
            maximum number of replicas should not be lower than minimal number
            of replicas.
          * `metrics` (`pulumi.Input[list]`) - Configuration parameters of autoscaling based on a custom metric.
            Structure is documented below.
            * `filter` (`pulumi.Input[str]`) - A filter string to be used as the filter string for
              a Stackdriver Monitoring TimeSeries.list API call.
              This filter is used to select a specific TimeSeries for
              the purpose of autoscaling and to determine whether the metric
              is exporting per-instance or per-group data.
              You can only use the AND operator for joining selectors.
              You can only use direct equality comparison operator (=) without
              any functions for each selector.
              You can specify the metric in both the filter string and in the
              metric field. However, if specified in both places, the metric must
              be identical.
              The monitored resource type determines what kind of values are
              expected for the metric. If it is a gce_instance, the autoscaler
              expects the metric to include a separate TimeSeries for each
              instance in a group. In such a case, you cannot filter on resource
              labels.
              If the resource type is any other value, the autoscaler expects
              this metric to contain values that apply to the entire autoscaled
              instance group and resource label filtering can be performed to
              point autoscaler at the correct TimeSeries to scale upon.
              This is called a per-group metric for the purpose of autoscaling.
              If not specified, the type defaults to gce_instance.
              You should provide a filter that is selective enough to pick just
              one TimeSeries for the autoscaled group or for each of the instances
              (if you are using gce_instance resource type). If multiple
              TimeSeries are returned upon the query execution, the autoscaler
              will sum their respective values to obtain its scaling value.
            * `name` (`pulumi.Input[str]`) - The identifier (type) of the Stackdriver Monitoring metric.
              The metric cannot have negative values.
              The metric must have a value type of INT64 or DOUBLE.
            * `singleInstanceAssignment` (`pulumi.Input[float]`) - If scaling is based on a per-group metric value that represents the
              total amount of work to be done or resource usage, set this value to
              an amount assigned for a single instance of the scaled group.
              The autoscaler will keep the number of instances proportional to the
              value of this metric, the metric itself should not change value due
              to group resizing.
              For example, a good metric to use with the target is
              `pubsub.googleapis.com/subscription/num_undelivered_messages`
              or a custom metric exporting the total number of requests coming to
              your instances.
              A bad example would be a metric exporting an average or median
              latency, since this value can't include a chunk assignable to a
              single instance, it could be better used with utilization_target
              instead.
            * `target` (`pulumi.Input[float]`) - Fraction of backend capacity utilization (set in HTTP(s) load
              balancing configuration) that autoscaler should maintain. Must
              be a positive float value. If not defined, the default is 0.8.
            * `type` (`pulumi.Input[str]`) - Defines how target utilization value is expressed for a
              Stackdriver Monitoring metric.
              Possible values are `GAUGE`, `DELTA_PER_SECOND`, and `DELTA_PER_MINUTE`.

          * `minReplicas` (`pulumi.Input[float]`) - The minimum number of replicas that the autoscaler can scale down
            to. This cannot be less than 0. If not provided, autoscaler will
            choose a default value depending on maximum number of instances
            allowed.
          * `mode` (`pulumi.Input[str]`) - Defines operating mode for this policy.
            Default value is `ON`.
            Possible values are `OFF`, `ONLY_UP`, and `ON`.
          * `scaleDownControl` (`pulumi.Input[dict]`)
            * `maxScaledDownReplicas` (`pulumi.Input[dict]`) - A nested object resource
              Structure is documented below.
              * `fixed` (`pulumi.Input[float]`) - Specifies a fixed number of VM instances. This must be a positive
                integer.
              * `percent` (`pulumi.Input[float]`) - Specifies a percentage of instances between 0 to 100%, inclusive.
                For example, specify 80 for 80%.

            * `timeWindowSec` (`pulumi.Input[float]`) - How long back autoscaling should look when computing recommendations
              to include directives regarding slower scale down, as described above.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["autoscaling_policy"] = autoscaling_policy
        __props__["creation_timestamp"] = creation_timestamp
        __props__["description"] = description
        __props__["name"] = name
        __props__["project"] = project
        __props__["self_link"] = self_link
        __props__["target"] = target
        __props__["zone"] = zone
        return Autoscalar(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
