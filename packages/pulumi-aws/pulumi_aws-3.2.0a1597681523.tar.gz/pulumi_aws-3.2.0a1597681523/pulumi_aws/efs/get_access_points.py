# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetAccessPointsResult:
    """
    A collection of values returned by getAccessPoints.
    """
    def __init__(__self__, arns=None, file_system_id=None, id=None, ids=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        __self__.arns = arns
        """
        Set of Amazon Resource Names (ARNs).
        """
        if file_system_id and not isinstance(file_system_id, str):
            raise TypeError("Expected argument 'file_system_id' to be a str")
        __self__.file_system_id = file_system_id
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        Set of identifiers.
        """


class AwaitableGetAccessPointsResult(GetAccessPointsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessPointsResult(
            arns=self.arns,
            file_system_id=self.file_system_id,
            id=self.id,
            ids=self.ids)


def get_access_points(file_system_id=None, opts=None):
    """
    Provides information about multiple Elastic File System (EFS) Access Points.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.efs.get_access_points(file_system_id="fs-12345678")
    ```


    :param str file_system_id: EFS File System identifier.
    """
    __args__ = dict()
    __args__['fileSystemId'] = file_system_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:efs/getAccessPoints:getAccessPoints', __args__, opts=opts).value

    return AwaitableGetAccessPointsResult(
        arns=__ret__.get('arns'),
        file_system_id=__ret__.get('fileSystemId'),
        id=__ret__.get('id'),
        ids=__ret__.get('ids'))
