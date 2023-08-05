# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetLocalGatewayRouteTableResult:
    """
    A collection of values returned by getLocalGatewayRouteTable.
    """
    def __init__(__self__, filters=None, id=None, local_gateway_id=None, local_gateway_route_table_id=None, outpost_arn=None, state=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        __self__.filters = filters
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if local_gateway_id and not isinstance(local_gateway_id, str):
            raise TypeError("Expected argument 'local_gateway_id' to be a str")
        __self__.local_gateway_id = local_gateway_id
        if local_gateway_route_table_id and not isinstance(local_gateway_route_table_id, str):
            raise TypeError("Expected argument 'local_gateway_route_table_id' to be a str")
        __self__.local_gateway_route_table_id = local_gateway_route_table_id
        if outpost_arn and not isinstance(outpost_arn, str):
            raise TypeError("Expected argument 'outpost_arn' to be a str")
        __self__.outpost_arn = outpost_arn
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        __self__.state = state
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags


class AwaitableGetLocalGatewayRouteTableResult(GetLocalGatewayRouteTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocalGatewayRouteTableResult(
            filters=self.filters,
            id=self.id,
            local_gateway_id=self.local_gateway_id,
            local_gateway_route_table_id=self.local_gateway_route_table_id,
            outpost_arn=self.outpost_arn,
            state=self.state,
            tags=self.tags)


def get_local_gateway_route_table(filters=None, local_gateway_id=None, local_gateway_route_table_id=None, outpost_arn=None, state=None, tags=None, opts=None):
    """
    Provides details about an EC2 Local Gateway Route Table.

    This data source can prove useful when a module accepts a local gateway route table id as
    an input variable and needs to, for example, find the associated Outpost or Local Gateway.

    ## Example Usage

    The following example returns a specific local gateway route table ID

    ```python
    import pulumi
    import pulumi_aws as aws

    config = pulumi.Config()
    aws_ec2_local_gateway_route_table = config.require_object("awsEc2LocalGatewayRouteTable")
    selected = aws.ec2.get_local_gateway_route_table(local_gateway_route_table_id=aws_ec2_local_gateway_route_table)
    ```


    :param str local_gateway_id: The id of the specific local gateway route table to retrieve.
    :param str local_gateway_route_table_id: Local Gateway Route Table Id assigned to desired local gateway route table
    :param str outpost_arn: The arn of the Outpost the local gateway route table is associated with.
    :param str state: The state of the local gateway route table.
    :param dict tags: A mapping of tags, each pair of which must exactly match
           a pair on the desired local gateway route table.

    The **filters** object supports the following:

      * `name` (`str`) - The name of the field to filter by, as defined by
        [the underlying AWS API](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeLocalGatewayRouteTables.html).
      * `values` (`list`) - Set of values that are accepted for the given field.
        A local gateway route table will be selected if any one of the given values matches.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['localGatewayId'] = local_gateway_id
    __args__['localGatewayRouteTableId'] = local_gateway_route_table_id
    __args__['outpostArn'] = outpost_arn
    __args__['state'] = state
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ec2/getLocalGatewayRouteTable:getLocalGatewayRouteTable', __args__, opts=opts).value

    return AwaitableGetLocalGatewayRouteTableResult(
        filters=__ret__.get('filters'),
        id=__ret__.get('id'),
        local_gateway_id=__ret__.get('localGatewayId'),
        local_gateway_route_table_id=__ret__.get('localGatewayRouteTableId'),
        outpost_arn=__ret__.get('outpostArn'),
        state=__ret__.get('state'),
        tags=__ret__.get('tags'))
