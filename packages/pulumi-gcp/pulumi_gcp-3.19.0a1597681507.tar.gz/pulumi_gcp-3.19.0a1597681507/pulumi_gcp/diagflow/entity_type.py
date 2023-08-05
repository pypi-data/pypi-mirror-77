# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class EntityType(pulumi.CustomResource):
    display_name: pulumi.Output[str]
    """
    The name of this entity type to be displayed on the console.
    """
    enable_fuzzy_extraction: pulumi.Output[bool]
    """
    Enables fuzzy entity extraction during classification.
    """
    entities: pulumi.Output[list]
    """
    The collection of entity entries associated with the entity type.
    Structure is documented below.

      * `synonyms` (`list`) - A collection of value synonyms. For example, if the entity type is vegetable, and value is scallions, a synonym
        could be green onions.
        For KIND_LIST entity types:
        * This collection must contain exactly one synonym equal to value.
      * `value` (`str`) - The primary value associated with this entity entry. For example, if the entity type is vegetable, the value
        could be scallions.
        For KIND_MAP entity types:
        * A reference value to be used in place of synonyms.
        For KIND_LIST entity types:
        * A string that can contain references to other entity types (with or without aliases).
    """
    kind: pulumi.Output[str]
    """
    Indicates the kind of entity type.
    * KIND_MAP: Map entity types allow mapping of a group of synonyms to a reference value.
    * KIND_LIST: List entity types contain a set of entries that do not map to reference values. However, list entity
    types can contain references to other entity types (with or without aliases).
    * KIND_REGEXP: Regexp entity types allow to specify regular expressions in entries values.
    Possible values are `KIND_MAP`, `KIND_LIST`, and `KIND_REGEXP`.
    """
    name: pulumi.Output[str]
    """
    The unique identifier of the entity type. Format: projects/<Project ID>/agent/entityTypes/<Entity type ID>.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    def __init__(__self__, resource_name, opts=None, display_name=None, enable_fuzzy_extraction=None, entities=None, kind=None, project=None, __props__=None, __name__=None, __opts__=None):
        """
        Represents an entity type. Entity types serve as a tool for extracting parameter values from natural language queries.

        To get more information about EntityType, see:

        * [API documentation](https://cloud.google.com/dialogflow/docs/reference/rest/v2/projects.agent.entityTypes)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/dialogflow/docs/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The name of this entity type to be displayed on the console.
        :param pulumi.Input[bool] enable_fuzzy_extraction: Enables fuzzy entity extraction during classification.
        :param pulumi.Input[list] entities: The collection of entity entries associated with the entity type.
               Structure is documented below.
        :param pulumi.Input[str] kind: Indicates the kind of entity type.
               * KIND_MAP: Map entity types allow mapping of a group of synonyms to a reference value.
               * KIND_LIST: List entity types contain a set of entries that do not map to reference values. However, list entity
               types can contain references to other entity types (with or without aliases).
               * KIND_REGEXP: Regexp entity types allow to specify regular expressions in entries values.
               Possible values are `KIND_MAP`, `KIND_LIST`, and `KIND_REGEXP`.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.

        The **entities** object supports the following:

          * `synonyms` (`pulumi.Input[list]`) - A collection of value synonyms. For example, if the entity type is vegetable, and value is scallions, a synonym
            could be green onions.
            For KIND_LIST entity types:
            * This collection must contain exactly one synonym equal to value.
          * `value` (`pulumi.Input[str]`) - The primary value associated with this entity entry. For example, if the entity type is vegetable, the value
            could be scallions.
            For KIND_MAP entity types:
            * A reference value to be used in place of synonyms.
            For KIND_LIST entity types:
            * A string that can contain references to other entity types (with or without aliases).
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

            if display_name is None:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            __props__['enable_fuzzy_extraction'] = enable_fuzzy_extraction
            __props__['entities'] = entities
            if kind is None:
                raise TypeError("Missing required property 'kind'")
            __props__['kind'] = kind
            __props__['project'] = project
            __props__['name'] = None
        super(EntityType, __self__).__init__(
            'gcp:diagflow/entityType:EntityType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, display_name=None, enable_fuzzy_extraction=None, entities=None, kind=None, name=None, project=None):
        """
        Get an existing EntityType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: The name of this entity type to be displayed on the console.
        :param pulumi.Input[bool] enable_fuzzy_extraction: Enables fuzzy entity extraction during classification.
        :param pulumi.Input[list] entities: The collection of entity entries associated with the entity type.
               Structure is documented below.
        :param pulumi.Input[str] kind: Indicates the kind of entity type.
               * KIND_MAP: Map entity types allow mapping of a group of synonyms to a reference value.
               * KIND_LIST: List entity types contain a set of entries that do not map to reference values. However, list entity
               types can contain references to other entity types (with or without aliases).
               * KIND_REGEXP: Regexp entity types allow to specify regular expressions in entries values.
               Possible values are `KIND_MAP`, `KIND_LIST`, and `KIND_REGEXP`.
        :param pulumi.Input[str] name: The unique identifier of the entity type. Format: projects/<Project ID>/agent/entityTypes/<Entity type ID>.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.

        The **entities** object supports the following:

          * `synonyms` (`pulumi.Input[list]`) - A collection of value synonyms. For example, if the entity type is vegetable, and value is scallions, a synonym
            could be green onions.
            For KIND_LIST entity types:
            * This collection must contain exactly one synonym equal to value.
          * `value` (`pulumi.Input[str]`) - The primary value associated with this entity entry. For example, if the entity type is vegetable, the value
            could be scallions.
            For KIND_MAP entity types:
            * A reference value to be used in place of synonyms.
            For KIND_LIST entity types:
            * A string that can contain references to other entity types (with or without aliases).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["display_name"] = display_name
        __props__["enable_fuzzy_extraction"] = enable_fuzzy_extraction
        __props__["entities"] = entities
        __props__["kind"] = kind
        __props__["name"] = name
        __props__["project"] = project
        return EntityType(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
