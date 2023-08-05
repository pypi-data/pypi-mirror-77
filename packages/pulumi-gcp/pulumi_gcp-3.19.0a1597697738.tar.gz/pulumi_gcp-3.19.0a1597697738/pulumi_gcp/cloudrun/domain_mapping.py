# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class DomainMapping(pulumi.CustomResource):
    location: pulumi.Output[str]
    """
    The location of the cloud run instance. eg us-central1
    """
    metadata: pulumi.Output[dict]
    """
    Metadata associated with this DomainMapping.
    Structure is documented below.

      * `annotations` (`dict`) - Annotations is a key value map stored with a resource that
        may be set by external tools to store and retrieve arbitrary metadata. More
        info: http://kubernetes.io/docs/user-guide/annotations
      * `generation` (`float`) - -
        A sequence number representing a specific generation of the desired state.
      * `labels` (`dict`) - Map of string keys and values that can be used to organize and categorize
        (scope and select) objects. May match selectors of replication controllers
        and routes.
        More info: http://kubernetes.io/docs/user-guide/labels
      * `namespace` (`str`) - In Cloud Run the namespace must be equal to either the
        project ID or project number.
      * `resourceVersion` (`str`) - -
        An opaque value that represents the internal version of this object that
        can be used by clients to determine when objects have changed. May be used
        for optimistic concurrency, change detection, and the watch operation on a
        resource or set of resources. They may only be valid for a
        particular resource or set of resources.
        More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#concurrency-control-and-consistency
      * `self_link` (`str`) - -
        SelfLink is a URL representing this object.
      * `uid` (`str`) - -
        UID is a unique id generated by the server on successful creation of a resource and is not
        allowed to change on PUT operations.
        More info: http://kubernetes.io/docs/user-guide/identifiers#uids
    """
    name: pulumi.Output[str]
    """
    Name should be a verified domain
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    spec: pulumi.Output[dict]
    """
    The spec for this DomainMapping.
    Structure is documented below.

      * `certificateMode` (`str`) - The mode of the certificate.
        Default value is `AUTOMATIC`.
        Possible values are `NONE` and `AUTOMATIC`.
      * `forceOverride` (`bool`) - If set, the mapping will override any mapping set before this spec was set.
        It is recommended that the user leaves this empty to receive an error
        warning about a potential conflict and only set it once the respective UI
        has given such a warning.
      * `routeName` (`str`) - The name of the Cloud Run Service that this DomainMapping applies to.
        The route must exist.
    """
    status: pulumi.Output[dict]
    """
    The current status of the DomainMapping.

      * `conditions` (`list`)
        * `message` (`str`)
        * `reason` (`str`)
        * `status` (`str`)
        * `type` (`str`)

      * `mappedRouteName` (`str`)
      * `observedGeneration` (`float`)
      * `resource_records` (`list`)
        * `name` (`str`) - Name should be a verified domain
        * `rrdata` (`str`)
        * `type` (`str`)
    """
    def __init__(__self__, resource_name, opts=None, location=None, metadata=None, name=None, project=None, spec=None, __props__=None, __name__=None, __opts__=None):
        """
        Resource to hold the state and status of a user's domain mapping.

        To get more information about DomainMapping, see:

        * [API documentation](https://cloud.google.com/run/docs/reference/rest/v1alpha1/projects.locations.domainmappings)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/run/docs/mapping-custom-domains)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the cloud run instance. eg us-central1
        :param pulumi.Input[dict] metadata: Metadata associated with this DomainMapping.
               Structure is documented below.
        :param pulumi.Input[str] name: Name should be a verified domain
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[dict] spec: The spec for this DomainMapping.
               Structure is documented below.

        The **metadata** object supports the following:

          * `annotations` (`pulumi.Input[dict]`) - Annotations is a key value map stored with a resource that
            may be set by external tools to store and retrieve arbitrary metadata. More
            info: http://kubernetes.io/docs/user-guide/annotations
          * `generation` (`pulumi.Input[float]`) - -
            A sequence number representing a specific generation of the desired state.
          * `labels` (`pulumi.Input[dict]`) - Map of string keys and values that can be used to organize and categorize
            (scope and select) objects. May match selectors of replication controllers
            and routes.
            More info: http://kubernetes.io/docs/user-guide/labels
          * `namespace` (`pulumi.Input[str]`) - In Cloud Run the namespace must be equal to either the
            project ID or project number.
          * `resourceVersion` (`pulumi.Input[str]`) - -
            An opaque value that represents the internal version of this object that
            can be used by clients to determine when objects have changed. May be used
            for optimistic concurrency, change detection, and the watch operation on a
            resource or set of resources. They may only be valid for a
            particular resource or set of resources.
            More info:
            https://git.k8s.io/community/contributors/devel/api-conventions.md#concurrency-control-and-consistency
          * `self_link` (`pulumi.Input[str]`) - -
            SelfLink is a URL representing this object.
          * `uid` (`pulumi.Input[str]`) - -
            UID is a unique id generated by the server on successful creation of a resource and is not
            allowed to change on PUT operations.
            More info: http://kubernetes.io/docs/user-guide/identifiers#uids

        The **spec** object supports the following:

          * `certificateMode` (`pulumi.Input[str]`) - The mode of the certificate.
            Default value is `AUTOMATIC`.
            Possible values are `NONE` and `AUTOMATIC`.
          * `forceOverride` (`pulumi.Input[bool]`) - If set, the mapping will override any mapping set before this spec was set.
            It is recommended that the user leaves this empty to receive an error
            warning about a potential conflict and only set it once the respective UI
            has given such a warning.
          * `routeName` (`pulumi.Input[str]`) - The name of the Cloud Run Service that this DomainMapping applies to.
            The route must exist.
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

            if location is None:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if metadata is None:
                raise TypeError("Missing required property 'metadata'")
            __props__['metadata'] = metadata
            __props__['name'] = name
            __props__['project'] = project
            if spec is None:
                raise TypeError("Missing required property 'spec'")
            __props__['spec'] = spec
            __props__['status'] = None
        super(DomainMapping, __self__).__init__(
            'gcp:cloudrun/domainMapping:DomainMapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, location=None, metadata=None, name=None, project=None, spec=None, status=None):
        """
        Get an existing DomainMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the cloud run instance. eg us-central1
        :param pulumi.Input[dict] metadata: Metadata associated with this DomainMapping.
               Structure is documented below.
        :param pulumi.Input[str] name: Name should be a verified domain
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[dict] spec: The spec for this DomainMapping.
               Structure is documented below.
        :param pulumi.Input[dict] status: The current status of the DomainMapping.

        The **metadata** object supports the following:

          * `annotations` (`pulumi.Input[dict]`) - Annotations is a key value map stored with a resource that
            may be set by external tools to store and retrieve arbitrary metadata. More
            info: http://kubernetes.io/docs/user-guide/annotations
          * `generation` (`pulumi.Input[float]`) - -
            A sequence number representing a specific generation of the desired state.
          * `labels` (`pulumi.Input[dict]`) - Map of string keys and values that can be used to organize and categorize
            (scope and select) objects. May match selectors of replication controllers
            and routes.
            More info: http://kubernetes.io/docs/user-guide/labels
          * `namespace` (`pulumi.Input[str]`) - In Cloud Run the namespace must be equal to either the
            project ID or project number.
          * `resourceVersion` (`pulumi.Input[str]`) - -
            An opaque value that represents the internal version of this object that
            can be used by clients to determine when objects have changed. May be used
            for optimistic concurrency, change detection, and the watch operation on a
            resource or set of resources. They may only be valid for a
            particular resource or set of resources.
            More info:
            https://git.k8s.io/community/contributors/devel/api-conventions.md#concurrency-control-and-consistency
          * `self_link` (`pulumi.Input[str]`) - -
            SelfLink is a URL representing this object.
          * `uid` (`pulumi.Input[str]`) - -
            UID is a unique id generated by the server on successful creation of a resource and is not
            allowed to change on PUT operations.
            More info: http://kubernetes.io/docs/user-guide/identifiers#uids

        The **spec** object supports the following:

          * `certificateMode` (`pulumi.Input[str]`) - The mode of the certificate.
            Default value is `AUTOMATIC`.
            Possible values are `NONE` and `AUTOMATIC`.
          * `forceOverride` (`pulumi.Input[bool]`) - If set, the mapping will override any mapping set before this spec was set.
            It is recommended that the user leaves this empty to receive an error
            warning about a potential conflict and only set it once the respective UI
            has given such a warning.
          * `routeName` (`pulumi.Input[str]`) - The name of the Cloud Run Service that this DomainMapping applies to.
            The route must exist.

        The **status** object supports the following:

          * `conditions` (`pulumi.Input[list]`)
            * `message` (`pulumi.Input[str]`)
            * `reason` (`pulumi.Input[str]`)
            * `status` (`pulumi.Input[str]`)
            * `type` (`pulumi.Input[str]`)

          * `mappedRouteName` (`pulumi.Input[str]`)
          * `observedGeneration` (`pulumi.Input[float]`)
          * `resource_records` (`pulumi.Input[list]`)
            * `name` (`pulumi.Input[str]`) - Name should be a verified domain
            * `rrdata` (`pulumi.Input[str]`)
            * `type` (`pulumi.Input[str]`)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["location"] = location
        __props__["metadata"] = metadata
        __props__["name"] = name
        __props__["project"] = project
        __props__["spec"] = spec
        __props__["status"] = status
        return DomainMapping(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
