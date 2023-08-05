# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetIpSetResult:
    """
    A collection of values returned by getIpSet.
    """
    def __init__(__self__, addresses=None, arn=None, description=None, id=None, ip_address_version=None, name=None, scope=None):
        if addresses and not isinstance(addresses, list):
            raise TypeError("Expected argument 'addresses' to be a list")
        __self__.addresses = addresses
        """
        An array of strings that specify one or more IP addresses or blocks of IP addresses in Classless Inter-Domain Routing (CIDR) notation.
        """
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        The Amazon Resource Name (ARN) of the entity.
        """
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        The description of the set that helps with identification.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if ip_address_version and not isinstance(ip_address_version, str):
            raise TypeError("Expected argument 'ip_address_version' to be a str")
        __self__.ip_address_version = ip_address_version
        """
        The IP address version of the set.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        __self__.scope = scope


class AwaitableGetIpSetResult(GetIpSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpSetResult(
            addresses=self.addresses,
            arn=self.arn,
            description=self.description,
            id=self.id,
            ip_address_version=self.ip_address_version,
            name=self.name,
            scope=self.scope)


def get_ip_set(name=None, scope=None, opts=None):
    """
    Retrieves the summary of a WAFv2 IP Set.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.wafv2.get_ip_set(name="some-ip-set",
        scope="REGIONAL")
    ```


    :param str name: The name of the WAFv2 IP Set.
    :param str scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:wafv2/getIpSet:getIpSet', __args__, opts=opts).value

    return AwaitableGetIpSetResult(
        addresses=__ret__.get('addresses'),
        arn=__ret__.get('arn'),
        description=__ret__.get('description'),
        id=__ret__.get('id'),
        ip_address_version=__ret__.get('ipAddressVersion'),
        name=__ret__.get('name'),
        scope=__ret__.get('scope'))
