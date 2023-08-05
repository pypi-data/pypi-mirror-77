# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class AttachedDisk(pulumi.CustomResource):
    device_name: pulumi.Output[str]
    """
    Specifies a unique device name of your choice that is
    reflected into the /dev/disk/by-id/google-* tree of a Linux operating
    system running within the instance. This name can be used to
    reference the device for mounting, resizing, and so on, from within
    the instance.
    """
    disk: pulumi.Output[str]
    """
    `name` or `self_link` of the disk that will be attached.
    """
    instance: pulumi.Output[str]
    """
    `name` or `self_link` of the compute instance that the disk will be attached to.
    If the `self_link` is provided then `zone` and `project` are extracted from the
    self link. If only the name is used then `zone` and `project` must be defined
    as properties on the resource or provider.
    """
    mode: pulumi.Output[str]
    """
    The mode in which to attach this disk, either READ_WRITE or
    READ_ONLY. If not specified, the default is to attach the disk in
    READ_WRITE mode.
    """
    project: pulumi.Output[str]
    """
    The project that the referenced compute instance is a part of. If `instance` is referenced by its
    `self_link` the project defined in the link will take precedence.
    """
    zone: pulumi.Output[str]
    """
    The zone that the referenced compute instance is located within. If `instance` is referenced by its
    `self_link` the zone defined in the link will take precedence.
    """
    def __init__(__self__, resource_name, opts=None, device_name=None, disk=None, instance=None, mode=None, project=None, zone=None, __props__=None, __name__=None, __opts__=None):
        """
        Persistent disks can be attached to a compute instance using the `attached_disk`
        section within the compute instance configuration.
        However there may be situations where managing the attached disks via the compute
        instance config isn't preferable or possible, such as attaching dynamic
        numbers of disks using the `count` variable.

        To get more information about attaching disks, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/instances/attachDisk)
        * How-to Guides
            * [Adding a persistent disk](https://cloud.google.com/compute/docs/disks/add-persistent-disk)

        **Note:** When using `compute.AttachedDisk` you **must** use `lifecycle.ignore_changes = ["attached_disk"]` on the `compute.Instance` resource that has the disks attached. Otherwise the two resources will fight for control of the attached disk block.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: Specifies a unique device name of your choice that is
               reflected into the /dev/disk/by-id/google-* tree of a Linux operating
               system running within the instance. This name can be used to
               reference the device for mounting, resizing, and so on, from within
               the instance.
        :param pulumi.Input[str] disk: `name` or `self_link` of the disk that will be attached.
        :param pulumi.Input[str] instance: `name` or `self_link` of the compute instance that the disk will be attached to.
               If the `self_link` is provided then `zone` and `project` are extracted from the
               self link. If only the name is used then `zone` and `project` must be defined
               as properties on the resource or provider.
        :param pulumi.Input[str] mode: The mode in which to attach this disk, either READ_WRITE or
               READ_ONLY. If not specified, the default is to attach the disk in
               READ_WRITE mode.
        :param pulumi.Input[str] project: The project that the referenced compute instance is a part of. If `instance` is referenced by its
               `self_link` the project defined in the link will take precedence.
        :param pulumi.Input[str] zone: The zone that the referenced compute instance is located within. If `instance` is referenced by its
               `self_link` the zone defined in the link will take precedence.
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

            __props__['device_name'] = device_name
            if disk is None:
                raise TypeError("Missing required property 'disk'")
            __props__['disk'] = disk
            if instance is None:
                raise TypeError("Missing required property 'instance'")
            __props__['instance'] = instance
            __props__['mode'] = mode
            __props__['project'] = project
            __props__['zone'] = zone
        super(AttachedDisk, __self__).__init__(
            'gcp:compute/attachedDisk:AttachedDisk',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, device_name=None, disk=None, instance=None, mode=None, project=None, zone=None):
        """
        Get an existing AttachedDisk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: Specifies a unique device name of your choice that is
               reflected into the /dev/disk/by-id/google-* tree of a Linux operating
               system running within the instance. This name can be used to
               reference the device for mounting, resizing, and so on, from within
               the instance.
        :param pulumi.Input[str] disk: `name` or `self_link` of the disk that will be attached.
        :param pulumi.Input[str] instance: `name` or `self_link` of the compute instance that the disk will be attached to.
               If the `self_link` is provided then `zone` and `project` are extracted from the
               self link. If only the name is used then `zone` and `project` must be defined
               as properties on the resource or provider.
        :param pulumi.Input[str] mode: The mode in which to attach this disk, either READ_WRITE or
               READ_ONLY. If not specified, the default is to attach the disk in
               READ_WRITE mode.
        :param pulumi.Input[str] project: The project that the referenced compute instance is a part of. If `instance` is referenced by its
               `self_link` the project defined in the link will take precedence.
        :param pulumi.Input[str] zone: The zone that the referenced compute instance is located within. If `instance` is referenced by its
               `self_link` the zone defined in the link will take precedence.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["device_name"] = device_name
        __props__["disk"] = disk
        __props__["instance"] = instance
        __props__["mode"] = mode
        __props__["project"] = project
        __props__["zone"] = zone
        return AttachedDisk(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
