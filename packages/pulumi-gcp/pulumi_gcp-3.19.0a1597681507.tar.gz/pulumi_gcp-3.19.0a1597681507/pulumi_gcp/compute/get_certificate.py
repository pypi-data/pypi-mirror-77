# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetCertificateResult:
    """
    A collection of values returned by getCertificate.
    """
    def __init__(__self__, certificate=None, certificate_id=None, creation_timestamp=None, description=None, id=None, name=None, name_prefix=None, private_key=None, project=None, self_link=None):
        if certificate and not isinstance(certificate, str):
            raise TypeError("Expected argument 'certificate' to be a str")
        __self__.certificate = certificate
        if certificate_id and not isinstance(certificate_id, float):
            raise TypeError("Expected argument 'certificate_id' to be a float")
        __self__.certificate_id = certificate_id
        if creation_timestamp and not isinstance(creation_timestamp, str):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        __self__.creation_timestamp = creation_timestamp
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if name_prefix and not isinstance(name_prefix, str):
            raise TypeError("Expected argument 'name_prefix' to be a str")
        __self__.name_prefix = name_prefix
        if private_key and not isinstance(private_key, str):
            raise TypeError("Expected argument 'private_key' to be a str")
        __self__.private_key = private_key
        if project and not isinstance(project, str):
            raise TypeError("Expected argument 'project' to be a str")
        __self__.project = project
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        __self__.self_link = self_link
class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            certificate=self.certificate,
            certificate_id=self.certificate_id,
            creation_timestamp=self.creation_timestamp,
            description=self.description,
            id=self.id,
            name=self.name,
            name_prefix=self.name_prefix,
            private_key=self.private_key,
            project=self.project,
            self_link=self.self_link)

def get_certificate(name=None,project=None,opts=None):
    """
    Get info about a Google Compute SSL Certificate from its name.


    :param str name: The name of the certificate.
    :param str project: The project in which the resource belongs. If it
           is not provided, the provider project is used.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:compute/getCertificate:getCertificate', __args__, opts=opts).value

    return AwaitableGetCertificateResult(
        certificate=__ret__.get('certificate'),
        certificate_id=__ret__.get('certificateId'),
        creation_timestamp=__ret__.get('creationTimestamp'),
        description=__ret__.get('description'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        name_prefix=__ret__.get('namePrefix'),
        private_key=__ret__.get('privateKey'),
        project=__ret__.get('project'),
        self_link=__ret__.get('selfLink'))
