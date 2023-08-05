# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Occurence(pulumi.CustomResource):
    attestation: pulumi.Output[dict]
    """
    Occurrence that represents a single "attestation". The authenticity
    of an attestation can be verified using the attached signature.
    If the verifier trusts the public key of the signer, then verifying
    the signature is sufficient to establish trust. In this circumstance,
    the authority to which this attestation is attached is primarily
    useful for lookup (how to find this attestation if you already
    know the authority and artifact to be verified) and intent (for
    which authority this attestation was intended to sign.
    Structure is documented below.

      * `serializedPayload` (`str`) - The serialized payload that is verified by one or
        more signatures. A base64-encoded string.
      * `signatures` (`list`) - One or more signatures over serializedPayload.
        Verifier implementations should consider this attestation
        message verified if at least one signature verifies
        serializedPayload. See Signature in common.proto for more
        details on signature structure and verification.
        Structure is documented below.
        * `publicKeyId` (`str`) - The identifier for the public key that verifies this
          signature. MUST be an RFC3986 conformant
          URI. * When possible, the key id should be an
          immutable reference, such as a cryptographic digest.
          Examples of valid values:
          * OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
          for more details on this scheme.
          * `openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA`
          * RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):
          * "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
        * `signature` (`str`) - The content of the signature, an opaque bytestring.
          The payload that this signature verifies MUST be
          unambiguously provided with the Signature during
          verification. A wrapper message might provide the
          payload explicitly. Alternatively, a message might
          have a canonical serialization that can always be
          unambiguously computed to derive the payload.
    """
    create_time: pulumi.Output[str]
    """
    The time when the repository was created.
    """
    kind: pulumi.Output[str]
    """
    The note kind which explicitly denotes which of the occurrence details are specified. This field can be used as a filter
    in list requests.
    """
    name: pulumi.Output[str]
    """
    The name of the occurrence.
    """
    note_name: pulumi.Output[str]
    """
    The analysis note associated with this occurrence, in the form of
    projects/[PROJECT]/notes/[NOTE_ID]. This field can be used as a
    filter in list requests.
    """
    project: pulumi.Output[str]
    """
    The ID of the project in which the resource belongs.
    If it is not provided, the provider project is used.
    """
    remediation: pulumi.Output[str]
    """
    A description of actions that can be taken to remedy the note.
    """
    resource_uri: pulumi.Output[str]
    """
    Required. Immutable. A URI that represents the resource for which
    the occurrence applies. For example,
    https://gcr.io/project/image@sha256:123abc for a Docker image.
    """
    update_time: pulumi.Output[str]
    """
    The time when the repository was last updated.
    """
    def __init__(__self__, resource_name, opts=None, attestation=None, note_name=None, project=None, remediation=None, resource_uri=None, __props__=None, __name__=None, __opts__=None):
        """
        An occurrence is an instance of a Note, or type of analysis that
        can be done for a resource.

        To get more information about Occurrence, see:

        * [API documentation](https://cloud.google.com/container-analysis/api/reference/rest/)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/container-analysis/)

        ## Example Usage

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] attestation: Occurrence that represents a single "attestation". The authenticity
               of an attestation can be verified using the attached signature.
               If the verifier trusts the public key of the signer, then verifying
               the signature is sufficient to establish trust. In this circumstance,
               the authority to which this attestation is attached is primarily
               useful for lookup (how to find this attestation if you already
               know the authority and artifact to be verified) and intent (for
               which authority this attestation was intended to sign.
               Structure is documented below.
        :param pulumi.Input[str] note_name: The analysis note associated with this occurrence, in the form of
               projects/[PROJECT]/notes/[NOTE_ID]. This field can be used as a
               filter in list requests.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] remediation: A description of actions that can be taken to remedy the note.
        :param pulumi.Input[str] resource_uri: Required. Immutable. A URI that represents the resource for which
               the occurrence applies. For example,
               https://gcr.io/project/image@sha256:123abc for a Docker image.

        The **attestation** object supports the following:

          * `serializedPayload` (`pulumi.Input[str]`) - The serialized payload that is verified by one or
            more signatures. A base64-encoded string.
          * `signatures` (`pulumi.Input[list]`) - One or more signatures over serializedPayload.
            Verifier implementations should consider this attestation
            message verified if at least one signature verifies
            serializedPayload. See Signature in common.proto for more
            details on signature structure and verification.
            Structure is documented below.
            * `publicKeyId` (`pulumi.Input[str]`) - The identifier for the public key that verifies this
              signature. MUST be an RFC3986 conformant
              URI. * When possible, the key id should be an
              immutable reference, such as a cryptographic digest.
              Examples of valid values:
              * OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
              for more details on this scheme.
              * `openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA`
              * RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):
              * "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
            * `signature` (`pulumi.Input[str]`) - The content of the signature, an opaque bytestring.
              The payload that this signature verifies MUST be
              unambiguously provided with the Signature during
              verification. A wrapper message might provide the
              payload explicitly. Alternatively, a message might
              have a canonical serialization that can always be
              unambiguously computed to derive the payload.
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

            if attestation is None:
                raise TypeError("Missing required property 'attestation'")
            __props__['attestation'] = attestation
            if note_name is None:
                raise TypeError("Missing required property 'note_name'")
            __props__['note_name'] = note_name
            __props__['project'] = project
            __props__['remediation'] = remediation
            if resource_uri is None:
                raise TypeError("Missing required property 'resource_uri'")
            __props__['resource_uri'] = resource_uri
            __props__['create_time'] = None
            __props__['kind'] = None
            __props__['name'] = None
            __props__['update_time'] = None
        super(Occurence, __self__).__init__(
            'gcp:containeranalysis/occurence:Occurence',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, attestation=None, create_time=None, kind=None, name=None, note_name=None, project=None, remediation=None, resource_uri=None, update_time=None):
        """
        Get an existing Occurence resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] attestation: Occurrence that represents a single "attestation". The authenticity
               of an attestation can be verified using the attached signature.
               If the verifier trusts the public key of the signer, then verifying
               the signature is sufficient to establish trust. In this circumstance,
               the authority to which this attestation is attached is primarily
               useful for lookup (how to find this attestation if you already
               know the authority and artifact to be verified) and intent (for
               which authority this attestation was intended to sign.
               Structure is documented below.
        :param pulumi.Input[str] create_time: The time when the repository was created.
        :param pulumi.Input[str] kind: The note kind which explicitly denotes which of the occurrence details are specified. This field can be used as a filter
               in list requests.
        :param pulumi.Input[str] name: The name of the occurrence.
        :param pulumi.Input[str] note_name: The analysis note associated with this occurrence, in the form of
               projects/[PROJECT]/notes/[NOTE_ID]. This field can be used as a
               filter in list requests.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] remediation: A description of actions that can be taken to remedy the note.
        :param pulumi.Input[str] resource_uri: Required. Immutable. A URI that represents the resource for which
               the occurrence applies. For example,
               https://gcr.io/project/image@sha256:123abc for a Docker image.
        :param pulumi.Input[str] update_time: The time when the repository was last updated.

        The **attestation** object supports the following:

          * `serializedPayload` (`pulumi.Input[str]`) - The serialized payload that is verified by one or
            more signatures. A base64-encoded string.
          * `signatures` (`pulumi.Input[list]`) - One or more signatures over serializedPayload.
            Verifier implementations should consider this attestation
            message verified if at least one signature verifies
            serializedPayload. See Signature in common.proto for more
            details on signature structure and verification.
            Structure is documented below.
            * `publicKeyId` (`pulumi.Input[str]`) - The identifier for the public key that verifies this
              signature. MUST be an RFC3986 conformant
              URI. * When possible, the key id should be an
              immutable reference, such as a cryptographic digest.
              Examples of valid values:
              * OpenPGP V4 public key fingerprint. See https://www.iana.org/assignments/uri-schemes/prov/openpgp4fpr
              for more details on this scheme.
              * `openpgp4fpr:74FAF3B861BDA0870C7B6DEF607E48D2A663AEEA`
              * RFC6920 digest-named SubjectPublicKeyInfo (digest of the DER serialization):
              * "ni:///sha-256;cD9o9Cq6LG3jD0iKXqEi_vdjJGecm_iXkbqVoScViaU"
            * `signature` (`pulumi.Input[str]`) - The content of the signature, an opaque bytestring.
              The payload that this signature verifies MUST be
              unambiguously provided with the Signature during
              verification. A wrapper message might provide the
              payload explicitly. Alternatively, a message might
              have a canonical serialization that can always be
              unambiguously computed to derive the payload.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["attestation"] = attestation
        __props__["create_time"] = create_time
        __props__["kind"] = kind
        __props__["name"] = name
        __props__["note_name"] = note_name
        __props__["project"] = project
        __props__["remediation"] = remediation
        __props__["resource_uri"] = resource_uri
        __props__["update_time"] = update_time
        return Occurence(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
