# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetKMSSecretCiphertextResult:
    """
    A collection of values returned by getKMSSecretCiphertext.
    """
    def __init__(__self__, ciphertext=None, crypto_key=None, id=None, plaintext=None):
        if ciphertext and not isinstance(ciphertext, str):
            raise TypeError("Expected argument 'ciphertext' to be a str")
        __self__.ciphertext = ciphertext
        """
        Contains the result of encrypting the provided plaintext, encoded in base64.
        """
        if crypto_key and not isinstance(crypto_key, str):
            raise TypeError("Expected argument 'crypto_key' to be a str")
        __self__.crypto_key = crypto_key
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if plaintext and not isinstance(plaintext, str):
            raise TypeError("Expected argument 'plaintext' to be a str")
        __self__.plaintext = plaintext
class AwaitableGetKMSSecretCiphertextResult(GetKMSSecretCiphertextResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKMSSecretCiphertextResult(
            ciphertext=self.ciphertext,
            crypto_key=self.crypto_key,
            id=self.id,
            plaintext=self.plaintext)

def get_kms_secret_ciphertext(crypto_key=None,plaintext=None,opts=None):
    """
    !> **Warning:** This data source is deprecated. Use the `kms.SecretCiphertext` **resource** instead.

    This data source allows you to encrypt data with Google Cloud KMS and use the
    ciphertext within your resource definitions.

    For more information see
    [the official documentation](https://cloud.google.com/kms/docs/encrypt-decrypt).

    > **NOTE:** Using this data source will allow you to conceal secret data within your
    resource definitions, but it does not take care of protecting that data in the
    logging output, plan output, or state output.  Please take care to secure your secret
    data outside of resource definitions.


    :param str crypto_key: The id of the CryptoKey that will be used to
           encrypt the provided plaintext. This is represented by the format
           `{projectId}/{location}/{keyRingName}/{cryptoKeyName}`.
    :param str plaintext: The plaintext to be encrypted
    """
    __args__ = dict()


    __args__['cryptoKey'] = crypto_key
    __args__['plaintext'] = plaintext
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('gcp:kms/getKMSSecretCiphertext:getKMSSecretCiphertext', __args__, opts=opts).value

    return AwaitableGetKMSSecretCiphertextResult(
        ciphertext=__ret__.get('ciphertext'),
        crypto_key=__ret__.get('cryptoKey'),
        id=__ret__.get('id'),
        plaintext=__ret__.get('plaintext'))
