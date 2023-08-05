# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Key(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the key.
    """
    customer_master_key_spec: pulumi.Output[str]
    """
    Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
    Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
    """
    deletion_window_in_days: pulumi.Output[float]
    """
    Duration in days after which the key is deleted
    after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
    """
    description: pulumi.Output[str]
    """
    The description of the key as viewed in AWS console.
    """
    enable_key_rotation: pulumi.Output[bool]
    """
    Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
    is enabled. Defaults to false.
    """
    is_enabled: pulumi.Output[bool]
    """
    Specifies whether the key is enabled. Defaults to true.
    """
    key_id: pulumi.Output[str]
    """
    The globally unique identifier for the key.
    """
    key_usage: pulumi.Output[str]
    """
    Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
    Defaults to `ENCRYPT_DECRYPT`.
    """
    policy: pulumi.Output[str]
    """
    A valid policy JSON document.
    """
    tags: pulumi.Output[dict]
    """
    A map of tags to assign to the object.
    """
    def __init__(__self__, resource_name, opts=None, customer_master_key_spec=None, deletion_window_in_days=None, description=None, enable_key_rotation=None, is_enabled=None, key_usage=None, policy=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a KMS customer master key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        key = aws.kms.Key("key",
            deletion_window_in_days=10,
            description="KMS key 1")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[float] deletion_window_in_days: Duration in days after which the key is deleted
               after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
               is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document.
        :param pulumi.Input[dict] tags: A map of tags to assign to the object.
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

            __props__['customer_master_key_spec'] = customer_master_key_spec
            __props__['deletion_window_in_days'] = deletion_window_in_days
            __props__['description'] = description
            __props__['enable_key_rotation'] = enable_key_rotation
            __props__['is_enabled'] = is_enabled
            __props__['key_usage'] = key_usage
            __props__['policy'] = policy
            __props__['tags'] = tags
            __props__['arn'] = None
            __props__['key_id'] = None
        super(Key, __self__).__init__(
            'aws:kms/key:Key',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, customer_master_key_spec=None, deletion_window_in_days=None, description=None, enable_key_rotation=None, is_enabled=None, key_id=None, key_usage=None, policy=None, tags=None):
        """
        Get an existing Key resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the key.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[float] deletion_window_in_days: Duration in days after which the key is deleted
               after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)
               is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_id: The globally unique identifier for the key.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document.
        :param pulumi.Input[dict] tags: A map of tags to assign to the object.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["customer_master_key_spec"] = customer_master_key_spec
        __props__["deletion_window_in_days"] = deletion_window_in_days
        __props__["description"] = description
        __props__["enable_key_rotation"] = enable_key_rotation
        __props__["is_enabled"] = is_enabled
        __props__["key_id"] = key_id
        __props__["key_usage"] = key_usage
        __props__["policy"] = policy
        __props__["tags"] = tags
        return Key(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
