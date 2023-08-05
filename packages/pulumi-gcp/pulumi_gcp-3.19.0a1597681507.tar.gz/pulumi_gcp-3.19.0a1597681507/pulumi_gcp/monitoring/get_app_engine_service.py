# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetAppEngineServiceResult:
    """
    A collection of values returned by getAppEngineService.
    """
    def __init__(__self__, display_name=None, id=None, module_id=None, name=None, project=None, service_id=None, telemetries=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        __self__.display_name = display_name
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if module_id and not isinstance(module_id, str):
            raise TypeError("Expected argument 'module_id' to be a str")
        __self__.module_id = module_id
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if service_id and not isinstance(service_id, str):
            raise TypeError("Expected argument 'service_id' to be a str")
        __self__.service_id = service_id
        if telemetries and not isinstance(telemetries, list):
            raise TypeError("Expected argument 'telemetries' to be a list")
        __self__.telemetries = telemetries
class AwaitableGetAppEngineServiceResult(GetAppEngineServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppEngineServiceResult(
            display_name=self.display_name,
            id=self.id,
            module_id=self.module_id,
            name=self.name,
            project=self.project,
            service_id=self.service_id,
            telemetries=self.telemetries)

def get_app_engine_service(module_id=None,project=None,opts=None):
    """
    A Monitoring Service is the root resource under which operational aspects of a
    generic service are accessible. A service is some discrete, autonomous, and
    network-accessible unit, designed to solve an individual concern

    An App Engine monitoring service is automatically created by GCP to monitor
    App Engine services.

    To get more information about Service, see:

    * [API documentation](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/services)
    * How-to Guides
        * [Service Monitoring](https://cloud.google.com/monitoring/service-monitoring)
        * [Monitoring API Documentation](https://cloud.google.com/monitoring/api/v3/)

    ## Example Usage


    :param str module_id: The ID of the App Engine module underlying this
           service. Corresponds to the moduleId resource label in the [gae_app](https://cloud.google.com/monitoring/api/resources#tag_gae_app) monitored resource, or the service/module name.
    :param str project: The ID of the project in which the resource belongs.
           If it is not provided, the provider project is used.
    """
    __args__ = dict()


    __args__['moduleId'] = module_id
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:monitoring/getAppEngineService:getAppEngineService', __args__, opts=opts).value

    return AwaitableGetAppEngineServiceResult(
        display_name=__ret__.get('displayName'),
        id=__ret__.get('id'),
        module_id=__ret__.get('moduleId'),
        name=__ret__.get('name'),
        project=__ret__.get('project'),
        service_id=__ret__.get('serviceId'),
        telemetries=__ret__.get('telemetries'))
