# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class GlobalAddress(pulumi.CustomResource):
    address: pulumi.Output[str]
    """
    The IP address or beginning of the address range represented by this
    resource. This can be supplied as an input to reserve a specific
    address or omitted to allow GCP to choose a valid one for you.
    """
    address_type: pulumi.Output[str]
    """
    The type of the address to reserve.
    * EXTERNAL indicates public/external single IP address.
    * INTERNAL indicates internal IP ranges belonging to some network.
    Default value is `EXTERNAL`.
    Possible values are `EXTERNAL` and `INTERNAL`.
    """
    creation_timestamp: pulumi.Output[str]
    """
    Creation timestamp in RFC3339 text format.
    """
    description: pulumi.Output[str]
    """
    An optional description of this resource.
    """
    ip_version: pulumi.Output[str]
    """
    The IP Version that will be used by this address. The default value is `IPV4`.
    Possible values are `IPV4` and `IPV6`.
    """
    label_fingerprint: pulumi.Output[str]
    """
    The fingerprint used for optimistic locking of this resource. Used internally during updates.
    """
    labels: pulumi.Output[dict]
    """
    Labels to apply to this address.  A list of key->value pairs.
    """
    name: pulumi.Output[str]
    """
    Name of the resource. Provided by the client when the resource is
    created. The name must be 1-63 characters long, and comply with
    RFC1035.  Specifically, the name must be 1-63 characters long and
    match the regular expression `a-z?` which means
    the first character must be a lowercase letter, and all following
    characters must be a dash, lowercase letter, or digit, except the last
    character, which cannot be a dash.
    """
    network: pulumi.Output[str]
    """
    The URL of the network in which to reserve the IP range. The IP range
    must be in RFC1918 space. The network cannot be deleted if there are
    any reserved IP ranges referring to it.
    This should only be set when using an Internal address.
    """
    prefix_length: pulumi.Output[float]
    """
    The prefix length of the IP range. If not present, it means the
    address field is a single IP address.
    This field is not applicable to addresses with addressType=EXTERNAL.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    purpose: pulumi.Output[str]
    """
    The purpose of the resource. For global internal addresses it can be
    * VPC_PEERING - for peer networks
    This should only be set when using an Internal address.
    Possible values are `VPC_PEERING`.
    """
    self_link: pulumi.Output[str]
    """
    The URI of the created resource.
    """
    def __init__(__self__, resource_name, opts=None, address=None, address_type=None, description=None, ip_version=None, labels=None, name=None, network=None, prefix_length=None, project=None, purpose=None, __props__=None, __name__=None, __opts__=None):
        """
        Represents a Global Address resource. Global addresses are used for
        HTTP(S) load balancing.

        To get more information about GlobalAddress, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/v1/globalAddresses)
        * How-to Guides
            * [Reserving a Static External IP Address](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The IP address or beginning of the address range represented by this
               resource. This can be supplied as an input to reserve a specific
               address or omitted to allow GCP to choose a valid one for you.
        :param pulumi.Input[str] address_type: The type of the address to reserve.
               * EXTERNAL indicates public/external single IP address.
               * INTERNAL indicates internal IP ranges belonging to some network.
               Default value is `EXTERNAL`.
               Possible values are `EXTERNAL` and `INTERNAL`.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] ip_version: The IP Version that will be used by this address. The default value is `IPV4`.
               Possible values are `IPV4` and `IPV6`.
        :param pulumi.Input[dict] labels: Labels to apply to this address.  A list of key->value pairs.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035.  Specifically, the name must be 1-63 characters long and
               match the regular expression `a-z?` which means
               the first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] network: The URL of the network in which to reserve the IP range. The IP range
               must be in RFC1918 space. The network cannot be deleted if there are
               any reserved IP ranges referring to it.
               This should only be set when using an Internal address.
        :param pulumi.Input[float] prefix_length: The prefix length of the IP range. If not present, it means the
               address field is a single IP address.
               This field is not applicable to addresses with addressType=EXTERNAL.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] purpose: The purpose of the resource. For global internal addresses it can be
               * VPC_PEERING - for peer networks
               This should only be set when using an Internal address.
               Possible values are `VPC_PEERING`.
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

            __props__['address'] = address
            __props__['address_type'] = address_type
            __props__['description'] = description
            __props__['ip_version'] = ip_version
            __props__['labels'] = labels
            __props__['name'] = name
            __props__['network'] = network
            __props__['prefix_length'] = prefix_length
            __props__['project'] = project
            __props__['purpose'] = purpose
            __props__['creation_timestamp'] = None
            __props__['label_fingerprint'] = None
            __props__['self_link'] = None
        super(GlobalAddress, __self__).__init__(
            'gcp:compute/globalAddress:GlobalAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, address=None, address_type=None, creation_timestamp=None, description=None, ip_version=None, label_fingerprint=None, labels=None, name=None, network=None, prefix_length=None, project=None, purpose=None, self_link=None):
        """
        Get an existing GlobalAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The IP address or beginning of the address range represented by this
               resource. This can be supplied as an input to reserve a specific
               address or omitted to allow GCP to choose a valid one for you.
        :param pulumi.Input[str] address_type: The type of the address to reserve.
               * EXTERNAL indicates public/external single IP address.
               * INTERNAL indicates internal IP ranges belonging to some network.
               Default value is `EXTERNAL`.
               Possible values are `EXTERNAL` and `INTERNAL`.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] ip_version: The IP Version that will be used by this address. The default value is `IPV4`.
               Possible values are `IPV4` and `IPV6`.
        :param pulumi.Input[str] label_fingerprint: The fingerprint used for optimistic locking of this resource. Used internally during updates.
        :param pulumi.Input[dict] labels: Labels to apply to this address.  A list of key->value pairs.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035.  Specifically, the name must be 1-63 characters long and
               match the regular expression `a-z?` which means
               the first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] network: The URL of the network in which to reserve the IP range. The IP range
               must be in RFC1918 space. The network cannot be deleted if there are
               any reserved IP ranges referring to it.
               This should only be set when using an Internal address.
        :param pulumi.Input[float] prefix_length: The prefix length of the IP range. If not present, it means the
               address field is a single IP address.
               This field is not applicable to addresses with addressType=EXTERNAL.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] purpose: The purpose of the resource. For global internal addresses it can be
               * VPC_PEERING - for peer networks
               This should only be set when using an Internal address.
               Possible values are `VPC_PEERING`.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["address"] = address
        __props__["address_type"] = address_type
        __props__["creation_timestamp"] = creation_timestamp
        __props__["description"] = description
        __props__["ip_version"] = ip_version
        __props__["label_fingerprint"] = label_fingerprint
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["network"] = network
        __props__["prefix_length"] = prefix_length
        __props__["project"] = project
        __props__["purpose"] = purpose
        __props__["self_link"] = self_link
        return GlobalAddress(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
