# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetWebAclResult:
    """
    A collection of values returned by getWebAcl.
    """
    def __init__(__self__, id=None, name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name


class AwaitableGetWebAclResult(GetWebAclResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAclResult(
            id=self.id,
            name=self.name)


def get_web_acl(name=None, opts=None):
    """
    `wafregional.WebAcl` Retrieves a WAF Regional Web ACL Resource Id.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.wafregional.get_web_acl(name="tfWAFRegionalWebACL")
    ```


    :param str name: The name of the WAF Regional Web ACL.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:wafregional/getWebAcl:getWebAcl', __args__, opts=opts).value

    return AwaitableGetWebAclResult(
        id=__ret__.get('id'),
        name=__ret__.get('name'))
