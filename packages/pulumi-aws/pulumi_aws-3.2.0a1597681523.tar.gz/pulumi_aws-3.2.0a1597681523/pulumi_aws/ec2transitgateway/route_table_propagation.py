# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class RouteTablePropagation(pulumi.CustomResource):
    resource_id: pulumi.Output[str]
    """
    Identifier of the resource
    """
    resource_type: pulumi.Output[str]
    """
    Type of the resource
    """
    transit_gateway_attachment_id: pulumi.Output[str]
    """
    Identifier of EC2 Transit Gateway Attachment.
    """
    transit_gateway_route_table_id: pulumi.Output[str]
    """
    Identifier of EC2 Transit Gateway Route Table.
    """
    def __init__(__self__, resource_name, opts=None, transit_gateway_attachment_id=None, transit_gateway_route_table_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an EC2 Transit Gateway Route Table propagation.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2transitgateway.RouteTablePropagation("example",
            transit_gateway_attachment_id=aws_ec2_transit_gateway_vpc_attachment["example"]["id"],
            transit_gateway_route_table_id=aws_ec2_transit_gateway_route_table["example"]["id"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] transit_gateway_attachment_id: Identifier of EC2 Transit Gateway Attachment.
        :param pulumi.Input[str] transit_gateway_route_table_id: Identifier of EC2 Transit Gateway Route Table.
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

            if transit_gateway_attachment_id is None:
                raise TypeError("Missing required property 'transit_gateway_attachment_id'")
            __props__['transit_gateway_attachment_id'] = transit_gateway_attachment_id
            if transit_gateway_route_table_id is None:
                raise TypeError("Missing required property 'transit_gateway_route_table_id'")
            __props__['transit_gateway_route_table_id'] = transit_gateway_route_table_id
            __props__['resource_id'] = None
            __props__['resource_type'] = None
        super(RouteTablePropagation, __self__).__init__(
            'aws:ec2transitgateway/routeTablePropagation:RouteTablePropagation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, resource_id=None, resource_type=None, transit_gateway_attachment_id=None, transit_gateway_route_table_id=None):
        """
        Get an existing RouteTablePropagation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] resource_id: Identifier of the resource
        :param pulumi.Input[str] resource_type: Type of the resource
        :param pulumi.Input[str] transit_gateway_attachment_id: Identifier of EC2 Transit Gateway Attachment.
        :param pulumi.Input[str] transit_gateway_route_table_id: Identifier of EC2 Transit Gateway Route Table.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["resource_id"] = resource_id
        __props__["resource_type"] = resource_type
        __props__["transit_gateway_attachment_id"] = transit_gateway_attachment_id
        __props__["transit_gateway_route_table_id"] = transit_gateway_route_table_id
        return RouteTablePropagation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
