# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class IpGroup(pulumi.CustomResource):
    description: pulumi.Output[str]
    """
    The description.
    """
    name: pulumi.Output[str]
    """
    The name of the IP group.
    """
    rules: pulumi.Output[list]
    """
    One or more pairs specifying the IP group rule (in CIDR format) from which web requests originate.

      * `description` (`str`) - The description.
      * `source` (`str`) - The IP address range, in CIDR notation, e.g. `10.0.0.0/16`
    """
    tags: pulumi.Output[dict]
    def __init__(__self__, resource_name, opts=None, description=None, name=None, rules=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an IP access control group in AWS WorkSpaces Service

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        contractors = aws.workspaces.IpGroup("contractors", description="Contractors IP access control group")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description.
        :param pulumi.Input[str] name: The name of the IP group.
        :param pulumi.Input[list] rules: One or more pairs specifying the IP group rule (in CIDR format) from which web requests originate.

        The **rules** object supports the following:

          * `description` (`pulumi.Input[str]`) - The description.
          * `source` (`pulumi.Input[str]`) - The IP address range, in CIDR notation, e.g. `10.0.0.0/16`
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

            __props__['description'] = description
            __props__['name'] = name
            __props__['rules'] = rules
            __props__['tags'] = tags
        super(IpGroup, __self__).__init__(
            'aws:workspaces/ipGroup:IpGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, description=None, name=None, rules=None, tags=None):
        """
        Get an existing IpGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description.
        :param pulumi.Input[str] name: The name of the IP group.
        :param pulumi.Input[list] rules: One or more pairs specifying the IP group rule (in CIDR format) from which web requests originate.

        The **rules** object supports the following:

          * `description` (`pulumi.Input[str]`) - The description.
          * `source` (`pulumi.Input[str]`) - The IP address range, in CIDR notation, e.g. `10.0.0.0/16`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["description"] = description
        __props__["name"] = name
        __props__["rules"] = rules
        __props__["tags"] = tags
        return IpGroup(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
