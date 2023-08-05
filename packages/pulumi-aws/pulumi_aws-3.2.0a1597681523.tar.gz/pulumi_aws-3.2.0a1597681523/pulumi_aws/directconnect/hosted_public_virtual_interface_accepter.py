# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class HostedPublicVirtualInterfaceAccepter(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the virtual interface.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    virtual_interface_id: pulumi.Output[str]
    """
    The ID of the Direct Connect virtual interface to accept.
    """
    def __init__(__self__, resource_name, opts=None, tags=None, virtual_interface_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to manage the accepter's side of a Direct Connect hosted public virtual interface.
        This resource accepts ownership of a public virtual interface created by another AWS account.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_pulumi as pulumi

        accepter = pulumi.providers.Aws("accepter")
        # Accepter's credentials.
        accepter_caller_identity = aws.get_caller_identity()
        # Creator's side of the VIF
        creator = aws.directconnect.HostedPublicVirtualInterface("creator",
            connection_id="dxcon-zzzzzzzz",
            owner_account_id=accepter_caller_identity.account_id,
            vlan=4094,
            address_family="ipv4",
            bgp_asn=65352,
            customer_address="175.45.176.1/30",
            amazon_address="175.45.176.2/30",
            route_filter_prefixes=[
                "210.52.109.0/24",
                "175.45.176.0/22",
            ])
        # Accepter's side of the VIF.
        accepter_hosted_public_virtual_interface_accepter = aws.directconnect.HostedPublicVirtualInterfaceAccepter("accepterHostedPublicVirtualInterfaceAccepter",
            virtual_interface_id=creator.id,
            tags={
                "Side": "Accepter",
            },
            opts=ResourceOptions(provider=aws["accepter"]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
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

            __props__['tags'] = tags
            if virtual_interface_id is None:
                raise TypeError("Missing required property 'virtual_interface_id'")
            __props__['virtual_interface_id'] = virtual_interface_id
            __props__['arn'] = None
        super(HostedPublicVirtualInterfaceAccepter, __self__).__init__(
            'aws:directconnect/hostedPublicVirtualInterfaceAccepter:HostedPublicVirtualInterfaceAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, tags=None, virtual_interface_id=None):
        """
        Get an existing HostedPublicVirtualInterfaceAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the virtual interface.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] virtual_interface_id: The ID of the Direct Connect virtual interface to accept.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["tags"] = tags
        __props__["virtual_interface_id"] = virtual_interface_id
        return HostedPublicVirtualInterfaceAccepter(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
