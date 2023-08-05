# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Connector(pulumi.CustomResource):
    ip_cidr_range: pulumi.Output[str]
    """
    The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
    """
    max_throughput: pulumi.Output[float]
    """
    Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
    """
    min_throughput: pulumi.Output[float]
    """
    Minimum throughput of the connector in Mbps. Default and min is 200.
    """
    name: pulumi.Output[str]
    """
    The name of the resource (Max 25 characters).
    """
    network: pulumi.Output[str]
    """
    Name of a VPC network.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    region: pulumi.Output[str]
    """
    Region where the VPC Access connector resides
    """
    self_link: pulumi.Output[str]
    """
    The fully qualified name of this VPC connector
    """
    state: pulumi.Output[str]
    """
    State of the VPC access connector.
    """
    def __init__(__self__, resource_name, opts=None, ip_cidr_range=None, max_throughput=None, min_throughput=None, name=None, network=None, project=None, region=None, __props__=None, __name__=None, __opts__=None):
        """
        Serverless VPC Access connector resource.

        To get more information about Connector, see:

        * [API documentation](https://cloud.google.com/vpc/docs/reference/vpcaccess/rest/v1/projects.locations.connectors)
        * How-to Guides
            * [Configuring Serverless VPC Access](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[float] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[float] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of a VPC network.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides
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

            if ip_cidr_range is None:
                raise TypeError("Missing required property 'ip_cidr_range'")
            __props__['ip_cidr_range'] = ip_cidr_range
            __props__['max_throughput'] = max_throughput
            __props__['min_throughput'] = min_throughput
            __props__['name'] = name
            if network is None:
                raise TypeError("Missing required property 'network'")
            __props__['network'] = network
            __props__['project'] = project
            if region is None:
                raise TypeError("Missing required property 'region'")
            __props__['region'] = region
            __props__['self_link'] = None
            __props__['state'] = None
        super(Connector, __self__).__init__(
            'gcp:vpcaccess/connector:Connector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, ip_cidr_range=None, max_throughput=None, min_throughput=None, name=None, network=None, project=None, region=None, self_link=None, state=None):
        """
        Get an existing Connector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_cidr_range: The range of internal addresses that follows RFC 4632 notation. Example: `10.132.0.0/28`.
        :param pulumi.Input[float] max_throughput: Maximum throughput of the connector in Mbps, must be greater than `min_throughput`. Default is 1000.
        :param pulumi.Input[float] min_throughput: Minimum throughput of the connector in Mbps. Default and min is 200.
        :param pulumi.Input[str] name: The name of the resource (Max 25 characters).
        :param pulumi.Input[str] network: Name of a VPC network.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Region where the VPC Access connector resides
        :param pulumi.Input[str] self_link: The fully qualified name of this VPC connector
        :param pulumi.Input[str] state: State of the VPC access connector.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["ip_cidr_range"] = ip_cidr_range
        __props__["max_throughput"] = max_throughput
        __props__["min_throughput"] = min_throughput
        __props__["name"] = name
        __props__["network"] = network
        __props__["project"] = project
        __props__["region"] = region
        __props__["self_link"] = self_link
        __props__["state"] = state
        return Connector(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
