# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Volume(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The volume ARN (e.g. arn:aws:ec2:us-east-1:0123456789012:volume/vol-59fcb34e).
    """
    availability_zone: pulumi.Output[str]
    """
    The AZ where the EBS volume will exist.
    """
    encrypted: pulumi.Output[bool]
    """
    If true, the disk will be encrypted.
    """
    iops: pulumi.Output[float]
    """
    The amount of IOPS to provision for the disk. Only valid for `type` of `io1`.
    """
    kms_key_id: pulumi.Output[str]
    """
    The ARN for the KMS encryption key. When specifying `kms_key_id`, `encrypted` needs to be set to true.
    """
    multi_attach_enabled: pulumi.Output[bool]
    """
    Specifies whether to enable Amazon EBS Multi-Attach. Multi-Attach is supported exclusively on `io1` volumes.
    """
    outpost_arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the Outpost.
    """
    size: pulumi.Output[float]
    """
    The size of the drive in GiBs.
    """
    snapshot_id: pulumi.Output[str]
    """
    A snapshot to base the EBS volume off of.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the resource.
    """
    type: pulumi.Output[str]
    """
    The type of EBS volume. Can be "standard", "gp2", "io1", "sc1" or "st1" (Default: "gp2").
    """
    def __init__(__self__, resource_name, opts=None, availability_zone=None, encrypted=None, iops=None, kms_key_id=None, multi_attach_enabled=None, outpost_arn=None, size=None, snapshot_id=None, tags=None, type=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a single EBS volume.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ebs.Volume("example",
            availability_zone="us-west-2a",
            size=40,
            tags={
                "Name": "HelloWorld",
            })
        ```

        > **NOTE**: One of `size` or `snapshot_id` is required when specifying an EBS volume

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_zone: The AZ where the EBS volume will exist.
        :param pulumi.Input[bool] encrypted: If true, the disk will be encrypted.
        :param pulumi.Input[float] iops: The amount of IOPS to provision for the disk. Only valid for `type` of `io1`.
        :param pulumi.Input[str] kms_key_id: The ARN for the KMS encryption key. When specifying `kms_key_id`, `encrypted` needs to be set to true.
        :param pulumi.Input[bool] multi_attach_enabled: Specifies whether to enable Amazon EBS Multi-Attach. Multi-Attach is supported exclusively on `io1` volumes.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost.
        :param pulumi.Input[float] size: The size of the drive in GiBs.
        :param pulumi.Input[str] snapshot_id: A snapshot to base the EBS volume off of.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] type: The type of EBS volume. Can be "standard", "gp2", "io1", "sc1" or "st1" (Default: "gp2").
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

            if availability_zone is None:
                raise TypeError("Missing required property 'availability_zone'")
            __props__['availability_zone'] = availability_zone
            __props__['encrypted'] = encrypted
            __props__['iops'] = iops
            __props__['kms_key_id'] = kms_key_id
            __props__['multi_attach_enabled'] = multi_attach_enabled
            __props__['outpost_arn'] = outpost_arn
            __props__['size'] = size
            __props__['snapshot_id'] = snapshot_id
            __props__['tags'] = tags
            __props__['type'] = type
            __props__['arn'] = None
        super(Volume, __self__).__init__(
            'aws:ebs/volume:Volume',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, availability_zone=None, encrypted=None, iops=None, kms_key_id=None, multi_attach_enabled=None, outpost_arn=None, size=None, snapshot_id=None, tags=None, type=None):
        """
        Get an existing Volume resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The volume ARN (e.g. arn:aws:ec2:us-east-1:0123456789012:volume/vol-59fcb34e).
        :param pulumi.Input[str] availability_zone: The AZ where the EBS volume will exist.
        :param pulumi.Input[bool] encrypted: If true, the disk will be encrypted.
        :param pulumi.Input[float] iops: The amount of IOPS to provision for the disk. Only valid for `type` of `io1`.
        :param pulumi.Input[str] kms_key_id: The ARN for the KMS encryption key. When specifying `kms_key_id`, `encrypted` needs to be set to true.
        :param pulumi.Input[bool] multi_attach_enabled: Specifies whether to enable Amazon EBS Multi-Attach. Multi-Attach is supported exclusively on `io1` volumes.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost.
        :param pulumi.Input[float] size: The size of the drive in GiBs.
        :param pulumi.Input[str] snapshot_id: A snapshot to base the EBS volume off of.
        :param pulumi.Input[dict] tags: A map of tags to assign to the resource.
        :param pulumi.Input[str] type: The type of EBS volume. Can be "standard", "gp2", "io1", "sc1" or "st1" (Default: "gp2").
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["availability_zone"] = availability_zone
        __props__["encrypted"] = encrypted
        __props__["iops"] = iops
        __props__["kms_key_id"] = kms_key_id
        __props__["multi_attach_enabled"] = multi_attach_enabled
        __props__["outpost_arn"] = outpost_arn
        __props__["size"] = size
        __props__["snapshot_id"] = snapshot_id
        __props__["tags"] = tags
        __props__["type"] = type
        return Volume(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
