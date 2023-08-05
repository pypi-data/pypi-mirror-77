# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class InstanceGroup(pulumi.CustomResource):
    description: pulumi.Output[str]
    """
    An optional textual description of the instance
    group.
    """
    instances: pulumi.Output[list]
    """
    List of instances in the group. They should be given
    as either self_link or id. When adding instances they must all be in the same
    network and zone as the instance group.
    """
    name: pulumi.Output[str]
    """
    The name which the port will be mapped to.
    """
    named_ports: pulumi.Output[list]
    """
    The named port configuration. See the section below
    for details on configuration.

      * `name` (`str`) - The name which the port will be mapped to.
      * `port` (`float`) - The port number to map the name to.
    """
    network: pulumi.Output[str]
    """
    The URL of the network the instance group is in. If
    this is different from the network where the instances are in, the creation
    fails. Defaults to the network where the instances are in (if neither
    `network` nor `instances` is specified, this field will be blank).
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs. If it
    is not provided, the provider project is used.
    """
    self_link: pulumi.Output[str]
    """
    The URI of the created resource.
    """
    size: pulumi.Output[float]
    """
    The number of instances in the group.
    """
    zone: pulumi.Output[str]
    """
    The zone that this instance group should be created in.
    """
    def __init__(__self__, resource_name, opts=None, description=None, instances=None, name=None, named_ports=None, network=None, project=None, zone=None, __props__=None, __name__=None, __opts__=None):
        """
        Creates a group of dissimilar Compute Engine virtual machine instances.
        For more information, see [the official documentation](https://cloud.google.com/compute/docs/instance-groups/#unmanaged_instance_groups)
        and [API](https://cloud.google.com/compute/docs/reference/latest/instanceGroups)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional textual description of the instance
               group.
        :param pulumi.Input[list] instances: List of instances in the group. They should be given
               as either self_link or id. When adding instances they must all be in the same
               network and zone as the instance group.
        :param pulumi.Input[str] name: The name which the port will be mapped to.
        :param pulumi.Input[list] named_ports: The named port configuration. See the section below
               for details on configuration.
        :param pulumi.Input[str] network: The URL of the network the instance group is in. If
               this is different from the network where the instances are in, the creation
               fails. Defaults to the network where the instances are in (if neither
               `network` nor `instances` is specified, this field will be blank).
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] zone: The zone that this instance group should be created in.

        The **named_ports** object supports the following:

          * `name` (`pulumi.Input[str]`) - The name which the port will be mapped to.
          * `port` (`pulumi.Input[float]`) - The port number to map the name to.
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

            __props__['description'] = description
            __props__['instances'] = instances
            __props__['name'] = name
            __props__['named_ports'] = named_ports
            __props__['network'] = network
            __props__['project'] = project
            __props__['zone'] = zone
            __props__['self_link'] = None
            __props__['size'] = None
        super(InstanceGroup, __self__).__init__(
            'gcp:compute/instanceGroup:InstanceGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, description=None, instances=None, name=None, named_ports=None, network=None, project=None, self_link=None, size=None, zone=None):
        """
        Get an existing InstanceGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional textual description of the instance
               group.
        :param pulumi.Input[list] instances: List of instances in the group. They should be given
               as either self_link or id. When adding instances they must all be in the same
               network and zone as the instance group.
        :param pulumi.Input[str] name: The name which the port will be mapped to.
        :param pulumi.Input[list] named_ports: The named port configuration. See the section below
               for details on configuration.
        :param pulumi.Input[str] network: The URL of the network the instance group is in. If
               this is different from the network where the instances are in, the creation
               fails. Defaults to the network where the instances are in (if neither
               `network` nor `instances` is specified, this field will be blank).
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs. If it
               is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[float] size: The number of instances in the group.
        :param pulumi.Input[str] zone: The zone that this instance group should be created in.

        The **named_ports** object supports the following:

          * `name` (`pulumi.Input[str]`) - The name which the port will be mapped to.
          * `port` (`pulumi.Input[float]`) - The port number to map the name to.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["description"] = description
        __props__["instances"] = instances
        __props__["name"] = name
        __props__["named_ports"] = named_ports
        __props__["network"] = network
        __props__["project"] = project
        __props__["self_link"] = self_link
        __props__["size"] = size
        __props__["zone"] = zone
        return InstanceGroup(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
