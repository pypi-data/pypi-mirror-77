# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class EfsLocation(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    Amazon Resource Name (ARN) of the DataSync Location.
    """
    ec2_config: pulumi.Output[dict]
    """
    Configuration block containing EC2 configurations for connecting to the EFS File System.

      * `securityGroupArns` (`list`) - List of Amazon Resource Names (ARNs) of the EC2 Security Groups that are associated with the EFS Mount Target.
      * `subnetArn` (`str`) - Amazon Resource Name (ARN) of the EC2 Subnet that is associated with the EFS Mount Target.
    """
    efs_file_system_arn: pulumi.Output[str]
    """
    Amazon Resource Name (ARN) of EFS File System.
    """
    subdirectory: pulumi.Output[str]
    """
    Subdirectory to perform actions as source or destination. Default `/`.
    """
    tags: pulumi.Output[dict]
    """
    Key-value pairs of resource tags to assign to the DataSync Location.
    """
    uri: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, ec2_config=None, efs_file_system_arn=None, subdirectory=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an AWS DataSync EFS Location.

        > **NOTE:** The EFS File System must have a mounted EFS Mount Target before creating this resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.EfsLocation("example",
            efs_file_system_arn=aws_efs_mount_target["example"]["file_system_arn"],
            ec2_config={
                "securityGroupArns": [aws_security_group["example"]["arn"]],
                "subnetArn": aws_subnet["example"]["arn"],
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[dict] tags: Key-value pairs of resource tags to assign to the DataSync Location.

        The **ec2_config** object supports the following:

          * `securityGroupArns` (`pulumi.Input[list]`) - List of Amazon Resource Names (ARNs) of the EC2 Security Groups that are associated with the EFS Mount Target.
          * `subnetArn` (`pulumi.Input[str]`) - Amazon Resource Name (ARN) of the EC2 Subnet that is associated with the EFS Mount Target.
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

            if ec2_config is None:
                raise TypeError("Missing required property 'ec2_config'")
            __props__['ec2_config'] = ec2_config
            if efs_file_system_arn is None:
                raise TypeError("Missing required property 'efs_file_system_arn'")
            __props__['efs_file_system_arn'] = efs_file_system_arn
            __props__['subdirectory'] = subdirectory
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['uri'] = None
        super(EfsLocation, __self__).__init__(
            'aws:datasync/efsLocation:EfsLocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, ec2_config=None, efs_file_system_arn=None, subdirectory=None, tags=None, uri=None):
        """
        Get an existing EfsLocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input[dict] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[dict] tags: Key-value pairs of resource tags to assign to the DataSync Location.

        The **ec2_config** object supports the following:

          * `securityGroupArns` (`pulumi.Input[list]`) - List of Amazon Resource Names (ARNs) of the EC2 Security Groups that are associated with the EFS Mount Target.
          * `subnetArn` (`pulumi.Input[str]`) - Amazon Resource Name (ARN) of the EC2 Subnet that is associated with the EFS Mount Target.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["ec2_config"] = ec2_config
        __props__["efs_file_system_arn"] = efs_file_system_arn
        __props__["subdirectory"] = subdirectory
        __props__["tags"] = tags
        __props__["uri"] = uri
        return EfsLocation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
