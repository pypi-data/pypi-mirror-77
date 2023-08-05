# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class SecurityConfiguration(pulumi.CustomResource):
    configuration: pulumi.Output[str]
    """
    A JSON formatted Security Configuration
    """
    creation_date: pulumi.Output[str]
    """
    Date the Security Configuration was created
    """
    name: pulumi.Output[str]
    """
    The name of the EMR Security Configuration. By default generated by this provider.
    """
    name_prefix: pulumi.Output[str]
    """
    Creates a unique name beginning with the specified
    prefix. Conflicts with `name`.
    """
    def __init__(__self__, resource_name, opts=None, configuration=None, name=None, name_prefix=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a resource to manage AWS EMR Security Configurations

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo = aws.emr.SecurityConfiguration("foo", configuration=\"\"\"{
          "EncryptionConfiguration": {
            "AtRestEncryptionConfiguration": {
              "S3EncryptionConfiguration": {
                "EncryptionMode": "SSE-S3"
              },
              "LocalDiskEncryptionConfiguration": {
                "EncryptionKeyProviderType": "AwsKms",
                "AwsKmsKey": "arn:aws:kms:us-west-2:187416307283:alias/tf_emr_test_key"
              }
            },
            "EnableInTransitEncryption": false,
            "EnableAtRestEncryption": true
          }
        }

        \"\"\")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration: A JSON formatted Security Configuration
        :param pulumi.Input[str] name: The name of the EMR Security Configuration. By default generated by this provider.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified
               prefix. Conflicts with `name`.
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

            if configuration is None:
                raise TypeError("Missing required property 'configuration'")
            __props__['configuration'] = configuration
            __props__['name'] = name
            __props__['name_prefix'] = name_prefix
            __props__['creation_date'] = None
        super(SecurityConfiguration, __self__).__init__(
            'aws:emr/securityConfiguration:SecurityConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, configuration=None, creation_date=None, name=None, name_prefix=None):
        """
        Get an existing SecurityConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration: A JSON formatted Security Configuration
        :param pulumi.Input[str] creation_date: Date the Security Configuration was created
        :param pulumi.Input[str] name: The name of the EMR Security Configuration. By default generated by this provider.
        :param pulumi.Input[str] name_prefix: Creates a unique name beginning with the specified
               prefix. Conflicts with `name`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["configuration"] = configuration
        __props__["creation_date"] = creation_date
        __props__["name"] = name
        __props__["name_prefix"] = name_prefix
        return SecurityConfiguration(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
