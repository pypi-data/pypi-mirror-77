# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Reservation(pulumi.CustomResource):
    commitment: pulumi.Output[str]
    """
    Full or partial URL to a parent commitment. This field displays for reservations that are tied to a commitment.
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
    Name of the resource. Provided by the client when the resource is
    created. The name must be 1-63 characters long, and comply with
    RFC1035. Specifically, the name must be 1-63 characters long and match
    the regular expression `a-z?` which means the
    first character must be a lowercase letter, and all following
    characters must be a dash, lowercase letter, or digit, except the last
    character, which cannot be a dash.
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
    specific_reservation: pulumi.Output[dict]
    """
    Reservation for instances with specific machine shapes.
    Structure is documented below.

      * `count` (`float`) - The number of resources that are allocated.
      * `inUseCount` (`float`) - -
        How many instances are in use.
      * `instanceProperties` (`dict`) - The instance properties for the reservation.
        Structure is documented below.
        * `guest_accelerators` (`list`) - Guest accelerator type and count.
          Structure is documented below.
          * `acceleratorCount` (`float`) - The number of the guest accelerator cards exposed to
            this instance.
          * `accelerator_type` (`str`) - The full or partial URL of the accelerator type to
            attach to this instance. For example:
            `projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100`
            If you are creating an instance template, specify only the accelerator name.

        * `localSsds` (`list`) - The amount of local ssd to reserve with each instance. This
          reserves disks of type `local-ssd`.
          Structure is documented below.
          * `disk_size_gb` (`float`) - The size of the disk in base-2 GB.
          * `interface` (`str`) - The disk interface to use for attaching this disk.
            Default value is `SCSI`.
            Possible values are `SCSI` and `NVME`.

        * `machine_type` (`str`) - The name of the machine type to reserve.
        * `min_cpu_platform` (`str`) - The minimum CPU platform for the reservation. For example,
          `"Intel Skylake"`. See
          the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones)
          for information on available CPU platforms.
    """
    specific_reservation_required: pulumi.Output[bool]
    """
    When set to true, only VMs that target this reservation by name can
    consume this reservation. Otherwise, it can be consumed by VMs with
    affinity for any reservation. Defaults to false.
    """
    status: pulumi.Output[str]
    """
    The status of the reservation.
    """
    zone: pulumi.Output[str]
    """
    The zone where the reservation is made.
    """
    def __init__(__self__, resource_name, opts=None, description=None, name=None, project=None, specific_reservation=None, specific_reservation_required=None, zone=None, __props__=None, __name__=None, __opts__=None):
        """
        Represents a reservation resource. A reservation ensures that capacity is
        held in a specific zone even if the reserved VMs are not running.

        Reservations apply only to Compute Engine, Cloud Dataproc, and Google
        Kubernetes Engine VM usage.Reservations do not apply to `f1-micro` or
        `g1-small` machine types, preemptible VMs, sole tenant nodes, or other
        services not listed above
        like Cloud SQL and Dataflow.

        To get more information about Reservation, see:

        * [API documentation](https://cloud.google.com/compute/docs/reference/rest/v1/reservations)
        * How-to Guides
            * [Reserving zonal resources](https://cloud.google.com/compute/docs/instances/reserving-zonal-resources)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[dict] specific_reservation: Reservation for instances with specific machine shapes.
               Structure is documented below.
        :param pulumi.Input[bool] specific_reservation_required: When set to true, only VMs that target this reservation by name can
               consume this reservation. Otherwise, it can be consumed by VMs with
               affinity for any reservation. Defaults to false.
        :param pulumi.Input[str] zone: The zone where the reservation is made.

        The **specific_reservation** object supports the following:

          * `count` (`pulumi.Input[float]`) - The number of resources that are allocated.
          * `inUseCount` (`pulumi.Input[float]`) - -
            How many instances are in use.
          * `instanceProperties` (`pulumi.Input[dict]`) - The instance properties for the reservation.
            Structure is documented below.
            * `guest_accelerators` (`pulumi.Input[list]`) - Guest accelerator type and count.
              Structure is documented below.
              * `acceleratorCount` (`pulumi.Input[float]`) - The number of the guest accelerator cards exposed to
                this instance.
              * `accelerator_type` (`pulumi.Input[str]`) - The full or partial URL of the accelerator type to
                attach to this instance. For example:
                `projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100`
                If you are creating an instance template, specify only the accelerator name.

            * `localSsds` (`pulumi.Input[list]`) - The amount of local ssd to reserve with each instance. This
              reserves disks of type `local-ssd`.
              Structure is documented below.
              * `disk_size_gb` (`pulumi.Input[float]`) - The size of the disk in base-2 GB.
              * `interface` (`pulumi.Input[str]`) - The disk interface to use for attaching this disk.
                Default value is `SCSI`.
                Possible values are `SCSI` and `NVME`.

            * `machine_type` (`pulumi.Input[str]`) - The name of the machine type to reserve.
            * `min_cpu_platform` (`pulumi.Input[str]`) - The minimum CPU platform for the reservation. For example,
              `"Intel Skylake"`. See
              the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones)
              for information on available CPU platforms.
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
            __props__['name'] = name
            __props__['project'] = project
            if specific_reservation is None:
                raise TypeError("Missing required property 'specific_reservation'")
            __props__['specific_reservation'] = specific_reservation
            __props__['specific_reservation_required'] = specific_reservation_required
            if zone is None:
                raise TypeError("Missing required property 'zone'")
            __props__['zone'] = zone
            __props__['commitment'] = None
            __props__['creation_timestamp'] = None
            __props__['self_link'] = None
            __props__['status'] = None
        super(Reservation, __self__).__init__(
            'gcp:compute/reservation:Reservation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, commitment=None, creation_timestamp=None, description=None, name=None, project=None, self_link=None, specific_reservation=None, specific_reservation_required=None, status=None, zone=None):
        """
        Get an existing Reservation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] commitment: Full or partial URL to a parent commitment. This field displays for reservations that are tied to a commitment.
        :param pulumi.Input[str] creation_timestamp: Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is
               created. The name must be 1-63 characters long, and comply with
               RFC1035. Specifically, the name must be 1-63 characters long and match
               the regular expression `a-z?` which means the
               first character must be a lowercase letter, and all following
               characters must be a dash, lowercase letter, or digit, except the last
               character, which cannot be a dash.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] self_link: The URI of the created resource.
        :param pulumi.Input[dict] specific_reservation: Reservation for instances with specific machine shapes.
               Structure is documented below.
        :param pulumi.Input[bool] specific_reservation_required: When set to true, only VMs that target this reservation by name can
               consume this reservation. Otherwise, it can be consumed by VMs with
               affinity for any reservation. Defaults to false.
        :param pulumi.Input[str] status: The status of the reservation.
        :param pulumi.Input[str] zone: The zone where the reservation is made.

        The **specific_reservation** object supports the following:

          * `count` (`pulumi.Input[float]`) - The number of resources that are allocated.
          * `inUseCount` (`pulumi.Input[float]`) - -
            How many instances are in use.
          * `instanceProperties` (`pulumi.Input[dict]`) - The instance properties for the reservation.
            Structure is documented below.
            * `guest_accelerators` (`pulumi.Input[list]`) - Guest accelerator type and count.
              Structure is documented below.
              * `acceleratorCount` (`pulumi.Input[float]`) - The number of the guest accelerator cards exposed to
                this instance.
              * `accelerator_type` (`pulumi.Input[str]`) - The full or partial URL of the accelerator type to
                attach to this instance. For example:
                `projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100`
                If you are creating an instance template, specify only the accelerator name.

            * `localSsds` (`pulumi.Input[list]`) - The amount of local ssd to reserve with each instance. This
              reserves disks of type `local-ssd`.
              Structure is documented below.
              * `disk_size_gb` (`pulumi.Input[float]`) - The size of the disk in base-2 GB.
              * `interface` (`pulumi.Input[str]`) - The disk interface to use for attaching this disk.
                Default value is `SCSI`.
                Possible values are `SCSI` and `NVME`.

            * `machine_type` (`pulumi.Input[str]`) - The name of the machine type to reserve.
            * `min_cpu_platform` (`pulumi.Input[str]`) - The minimum CPU platform for the reservation. For example,
              `"Intel Skylake"`. See
              the CPU platform availability reference](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform#availablezones)
              for information on available CPU platforms.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["commitment"] = commitment
        __props__["creation_timestamp"] = creation_timestamp
        __props__["description"] = description
        __props__["name"] = name
        __props__["project"] = project
        __props__["self_link"] = self_link
        __props__["specific_reservation"] = specific_reservation
        __props__["specific_reservation_required"] = specific_reservation_required
        __props__["status"] = status
        __props__["zone"] = zone
        return Reservation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
