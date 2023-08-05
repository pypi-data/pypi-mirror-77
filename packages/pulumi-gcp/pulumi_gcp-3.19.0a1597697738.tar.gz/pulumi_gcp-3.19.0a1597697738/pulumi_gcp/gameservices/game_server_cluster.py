# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GameServerCluster(pulumi.CustomResource):
    cluster_id: pulumi.Output[str]
    """
    Required. The resource name of the game server cluster
    """
    connection_info: pulumi.Output[dict]
    """
    Game server cluster connection information. This information is used to
    manage game server clusters.
    Structure is documented below.

      * `gkeClusterReference` (`dict`) - Reference of the GKE cluster where the game servers are installed.
        Structure is documented below.
        * `cluster` (`str`) - The full or partial name of a GKE cluster, using one of the following
          forms:
          * `projects/{project_id}/locations/{location}/clusters/{cluster_id}`
          * `locations/{location}/clusters/{cluster_id}`
          * `{cluster_id}`
          If project and location are not specified, the project and location of the
          GameServerCluster resource are used to generate the full name of the
          GKE cluster.

      * `namespace` (`str`) - Namespace designated on the game server cluster where the game server
        instances will be created. The namespace existence will be validated
        during creation.
    """
    description: pulumi.Output[str]
    """
    Human readable description of the cluster.
    """
    labels: pulumi.Output[dict]
    """
    The labels associated with this game server cluster. Each label is a
    key-value pair.
    """
    location: pulumi.Output[str]
    """
    Location of the Cluster.
    """
    name: pulumi.Output[str]
    """
    The resource id of the game server cluster, eg:
    'projects/{project_id}/locations/{location}/realms/{realm_id}/gameServerClusters/{cluster_id}'. For example,
    'projects/my-project/locations/{location}/realms/zanzibar/gameServerClusters/my-onprem-cluster'.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    realm_id: pulumi.Output[str]
    """
    The realm id of the game server realm.
    """
    def __init__(__self__, resource_name, opts=None, cluster_id=None, connection_info=None, description=None, labels=None, location=None, project=None, realm_id=None, __props__=None, __name__=None, __opts__=None):
        """
        A game server cluster resource.

        To get more information about GameServerCluster, see:

        * [API documentation](https://cloud.google.com/game-servers/docs/reference/rest/v1beta/projects.locations.realms.gameServerClusters)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/game-servers/docs)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: Required. The resource name of the game server cluster
        :param pulumi.Input[dict] connection_info: Game server cluster connection information. This information is used to
               manage game server clusters.
               Structure is documented below.
        :param pulumi.Input[str] description: Human readable description of the cluster.
        :param pulumi.Input[dict] labels: The labels associated with this game server cluster. Each label is a
               key-value pair.
        :param pulumi.Input[str] location: Location of the Cluster.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] realm_id: The realm id of the game server realm.

        The **connection_info** object supports the following:

          * `gkeClusterReference` (`pulumi.Input[dict]`) - Reference of the GKE cluster where the game servers are installed.
            Structure is documented below.
            * `cluster` (`pulumi.Input[str]`) - The full or partial name of a GKE cluster, using one of the following
              forms:
              * `projects/{project_id}/locations/{location}/clusters/{cluster_id}`
              * `locations/{location}/clusters/{cluster_id}`
              * `{cluster_id}`
              If project and location are not specified, the project and location of the
              GameServerCluster resource are used to generate the full name of the
              GKE cluster.

          * `namespace` (`pulumi.Input[str]`) - Namespace designated on the game server cluster where the game server
            instances will be created. The namespace existence will be validated
            during creation.
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

            if cluster_id is None:
                raise TypeError("Missing required property 'cluster_id'")
            __props__['cluster_id'] = cluster_id
            if connection_info is None:
                raise TypeError("Missing required property 'connection_info'")
            __props__['connection_info'] = connection_info
            __props__['description'] = description
            __props__['labels'] = labels
            __props__['location'] = location
            __props__['project'] = project
            if realm_id is None:
                raise TypeError("Missing required property 'realm_id'")
            __props__['realm_id'] = realm_id
            __props__['name'] = None
        super(GameServerCluster, __self__).__init__(
            'gcp:gameservices/gameServerCluster:GameServerCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cluster_id=None, connection_info=None, description=None, labels=None, location=None, name=None, project=None, realm_id=None):
        """
        Get an existing GameServerCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: Required. The resource name of the game server cluster
        :param pulumi.Input[dict] connection_info: Game server cluster connection information. This information is used to
               manage game server clusters.
               Structure is documented below.
        :param pulumi.Input[str] description: Human readable description of the cluster.
        :param pulumi.Input[dict] labels: The labels associated with this game server cluster. Each label is a
               key-value pair.
        :param pulumi.Input[str] location: Location of the Cluster.
        :param pulumi.Input[str] name: The resource id of the game server cluster, eg:
               'projects/{project_id}/locations/{location}/realms/{realm_id}/gameServerClusters/{cluster_id}'. For example,
               'projects/my-project/locations/{location}/realms/zanzibar/gameServerClusters/my-onprem-cluster'.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] realm_id: The realm id of the game server realm.

        The **connection_info** object supports the following:

          * `gkeClusterReference` (`pulumi.Input[dict]`) - Reference of the GKE cluster where the game servers are installed.
            Structure is documented below.
            * `cluster` (`pulumi.Input[str]`) - The full or partial name of a GKE cluster, using one of the following
              forms:
              * `projects/{project_id}/locations/{location}/clusters/{cluster_id}`
              * `locations/{location}/clusters/{cluster_id}`
              * `{cluster_id}`
              If project and location are not specified, the project and location of the
              GameServerCluster resource are used to generate the full name of the
              GKE cluster.

          * `namespace` (`pulumi.Input[str]`) - Namespace designated on the game server cluster where the game server
            instances will be created. The namespace existence will be validated
            during creation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["cluster_id"] = cluster_id
        __props__["connection_info"] = connection_info
        __props__["description"] = description
        __props__["labels"] = labels
        __props__["location"] = location
        __props__["name"] = name
        __props__["project"] = project
        __props__["realm_id"] = realm_id
        return GameServerCluster(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
