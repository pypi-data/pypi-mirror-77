# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class NetworkEndpoint(pulumi.CustomResource):
    instance: pulumi.Output[str]
    """
    The name for a specific VM instance that the IP address belongs to.
    This is required for network endpoints of type GCE_VM_IP_PORT.
    The instance must be in the same zone of network endpoint group.
    """
    ip_address: pulumi.Output[str]
    """
    IPv4 address of network endpoint. The IP address must belong
    to a VM in GCE (either the primary IP or as part of an aliased IP
    range).
    """
    network_endpoint_group: pulumi.Output[str]
    """
    The network endpoint group this endpoint is part of.
    """
    port: pulumi.Output[float]
    """
    Port number of network endpoint.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    zone: pulumi.Output[str]
    """
    Zone where the containing network endpoint group is located.
    """
    def __init__(__self__, resource_name, opts=None, instance=None, ip_address=None, network_endpoint_group=None, port=None, project=None, zone=None, __props__=None, __name__=None, __opts__=None):
        """
        A Network endpoint represents a IP address and port combination that is
        part of a specific network endpoint group (NEG). NEGs are zonals
        collection of these endpoints for GCP resources within a
        single subnet. **NOTE**: Network endpoints cannot be created outside of a
        network endpoint group.

        To get more information about NetworkEndpoint, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/beta/networkEndpointGroups)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/load-balancing/docs/negs/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance: The name for a specific VM instance that the IP address belongs to.
               This is required for network endpoints of type GCE_VM_IP_PORT.
               The instance must be in the same zone of network endpoint group.
        :param pulumi.Input[str] ip_address: IPv4 address of network endpoint. The IP address must belong
               to a VM in GCE (either the primary IP or as part of an aliased IP
               range).
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group this endpoint is part of.
        :param pulumi.Input[float] port: Port number of network endpoint.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
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

            if instance is None:
                raise TypeError("Missing required property 'instance'")
            __props__['instance'] = instance
            if ip_address is None:
                raise TypeError("Missing required property 'ip_address'")
            __props__['ip_address'] = ip_address
            if network_endpoint_group is None:
                raise TypeError("Missing required property 'network_endpoint_group'")
            __props__['network_endpoint_group'] = network_endpoint_group
            if port is None:
                raise TypeError("Missing required property 'port'")
            __props__['port'] = port
            __props__['project'] = project
            __props__['zone'] = zone
        super(NetworkEndpoint, __self__).__init__(
            'gcp:compute/networkEndpoint:NetworkEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, instance=None, ip_address=None, network_endpoint_group=None, port=None, project=None, zone=None):
        """
        Get an existing NetworkEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance: The name for a specific VM instance that the IP address belongs to.
               This is required for network endpoints of type GCE_VM_IP_PORT.
               The instance must be in the same zone of network endpoint group.
        :param pulumi.Input[str] ip_address: IPv4 address of network endpoint. The IP address must belong
               to a VM in GCE (either the primary IP or as part of an aliased IP
               range).
        :param pulumi.Input[str] network_endpoint_group: The network endpoint group this endpoint is part of.
        :param pulumi.Input[float] port: Port number of network endpoint.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] zone: Zone where the containing network endpoint group is located.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["instance"] = instance
        __props__["ip_address"] = ip_address
        __props__["network_endpoint_group"] = network_endpoint_group
        __props__["port"] = port
        __props__["project"] = project
        __props__["zone"] = zone
        return NetworkEndpoint(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
