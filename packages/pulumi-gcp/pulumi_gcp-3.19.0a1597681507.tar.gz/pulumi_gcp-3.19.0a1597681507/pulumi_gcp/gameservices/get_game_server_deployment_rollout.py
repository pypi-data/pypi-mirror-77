# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetGameServerDeploymentRolloutResult:
    """
    A collection of values returned by getGameServerDeploymentRollout.
    """
    def __init__(__self__, default_game_server_config=None, deployment_id=None, game_server_config_overrides=None, id=None, name=None, project=None):
        if default_game_server_config and not isinstance(default_game_server_config, str):
            raise TypeError("Expected argument 'default_game_server_config' to be a str")
        __self__.default_game_server_config = default_game_server_config
        if deployment_id and not isinstance(deployment_id, str):
            raise TypeError("Expected argument 'deployment_id' to be a str")
        __self__.deployment_id = deployment_id
        if game_server_config_overrides and not isinstance(game_server_config_overrides, list):
            raise TypeError("Expected argument 'game_server_config_overrides' to be a list")
        __self__.game_server_config_overrides = game_server_config_overrides
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
class AwaitableGetGameServerDeploymentRolloutResult(GetGameServerDeploymentRolloutResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGameServerDeploymentRolloutResult(
            default_game_server_config=self.default_game_server_config,
            deployment_id=self.deployment_id,
            game_server_config_overrides=self.game_server_config_overrides,
            id=self.id,
            name=self.name,
            project=self.project)

def get_game_server_deployment_rollout(deployment_id=None,opts=None):
    """
    Use this data source to get the rollout state.

    https://cloud.google.com/game-servers/docs/reference/rest/v1beta/GameServerDeploymentRollout


    :param str deployment_id: The deployment to get the rollout state from. Only 1 rollout must be associated with each deployment.
    """
    __args__ = dict()


    __args__['deploymentId'] = deployment_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:gameservices/getGameServerDeploymentRollout:getGameServerDeploymentRollout', __args__, opts=opts).value

    return AwaitableGetGameServerDeploymentRolloutResult(
        default_game_server_config=__ret__.get('defaultGameServerConfig'),
        deployment_id=__ret__.get('deploymentId'),
        game_server_config_overrides=__ret__.get('gameServerConfigOverrides'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        project=__ret__.get('project'))
