# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class S3BucketAssociation(pulumi.CustomResource):
    bucket_name: pulumi.Output[str]
    """
    The name of the S3 bucket that you want to associate with Amazon Macie.
    """
    classification_type: pulumi.Output[dict]
    """
    The configuration of how Amazon Macie classifies the S3 objects.

      * `continuous` (`str`) - A string value indicating that Macie perform a one-time classification of all of the existing objects in the bucket.
        The only valid value is the default value, `FULL`.
      * `oneTime` (`str`) - A string value indicating whether or not Macie performs a one-time classification of all of the existing objects in the bucket.
        Valid values are `NONE` and `FULL`. Defaults to `NONE` indicating that Macie only classifies objects that are added after the association was created.
    """
    member_account_id: pulumi.Output[str]
    """
    The ID of the Amazon Macie member account whose S3 resources you want to associate with Macie. If `member_account_id` isn't specified, the action associates specified S3 resources with Macie for the current master account.
    """
    prefix: pulumi.Output[str]
    """
    Object key prefix identifying one or more S3 objects to which the association applies.
    """
    def __init__(__self__, resource_name, opts=None, bucket_name=None, classification_type=None, member_account_id=None, prefix=None, __props__=None, __name__=None, __opts__=None):
        """
        > **NOTE:** This resource interacts with [Amazon Macie Classic](https://docs.aws.amazon.com/macie/latest/userguide/what-is-macie.html). Macie Classic cannot be activated in new accounts. See the [FAQ](https://aws.amazon.com/macie/classic-faqs/) for more details.

        Associates an S3 resource with Amazon Macie for monitoring and data classification.

        > **NOTE:** Before using Amazon Macie for the first time it must be enabled manually. Instructions are [here](https://docs.aws.amazon.com/macie/latest/userguide/macie-setting-up.html#macie-setting-up-enable).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.macie.S3BucketAssociation("example",
            bucket_name="tf-macie-example",
            classification_type={
                "oneTime": "FULL",
            },
            prefix="data")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket_name: The name of the S3 bucket that you want to associate with Amazon Macie.
        :param pulumi.Input[dict] classification_type: The configuration of how Amazon Macie classifies the S3 objects.
        :param pulumi.Input[str] member_account_id: The ID of the Amazon Macie member account whose S3 resources you want to associate with Macie. If `member_account_id` isn't specified, the action associates specified S3 resources with Macie for the current master account.
        :param pulumi.Input[str] prefix: Object key prefix identifying one or more S3 objects to which the association applies.

        The **classification_type** object supports the following:

          * `continuous` (`pulumi.Input[str]`) - A string value indicating that Macie perform a one-time classification of all of the existing objects in the bucket.
            The only valid value is the default value, `FULL`.
          * `oneTime` (`pulumi.Input[str]`) - A string value indicating whether or not Macie performs a one-time classification of all of the existing objects in the bucket.
            Valid values are `NONE` and `FULL`. Defaults to `NONE` indicating that Macie only classifies objects that are added after the association was created.
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

            if bucket_name is None:
                raise TypeError("Missing required property 'bucket_name'")
            __props__['bucket_name'] = bucket_name
            __props__['classification_type'] = classification_type
            __props__['member_account_id'] = member_account_id
            __props__['prefix'] = prefix
        super(S3BucketAssociation, __self__).__init__(
            'aws:macie/s3BucketAssociation:S3BucketAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bucket_name=None, classification_type=None, member_account_id=None, prefix=None):
        """
        Get an existing S3BucketAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket_name: The name of the S3 bucket that you want to associate with Amazon Macie.
        :param pulumi.Input[dict] classification_type: The configuration of how Amazon Macie classifies the S3 objects.
        :param pulumi.Input[str] member_account_id: The ID of the Amazon Macie member account whose S3 resources you want to associate with Macie. If `member_account_id` isn't specified, the action associates specified S3 resources with Macie for the current master account.
        :param pulumi.Input[str] prefix: Object key prefix identifying one or more S3 objects to which the association applies.

        The **classification_type** object supports the following:

          * `continuous` (`pulumi.Input[str]`) - A string value indicating that Macie perform a one-time classification of all of the existing objects in the bucket.
            The only valid value is the default value, `FULL`.
          * `oneTime` (`pulumi.Input[str]`) - A string value indicating whether or not Macie performs a one-time classification of all of the existing objects in the bucket.
            Valid values are `NONE` and `FULL`. Defaults to `NONE` indicating that Macie only classifies objects that are added after the association was created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket_name"] = bucket_name
        __props__["classification_type"] = classification_type
        __props__["member_account_id"] = member_account_id
        __props__["prefix"] = prefix
        return S3BucketAssociation(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
