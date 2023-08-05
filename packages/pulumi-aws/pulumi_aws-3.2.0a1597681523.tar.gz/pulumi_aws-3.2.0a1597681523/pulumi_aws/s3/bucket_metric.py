# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class BucketMetric(pulumi.CustomResource):
    bucket: pulumi.Output[str]
    """
    The name of the bucket to put metric configuration.
    """
    filter: pulumi.Output[dict]
    """
    [Object filtering](http://docs.aws.amazon.com/AmazonS3/latest/dev/metrics-configurations.html#metrics-configurations-filter) that accepts a prefix, tags, or a logical AND of prefix and tags (documented below).

      * `prefix` (`str`) - Object prefix for filtering (singular).
      * `tags` (`dict`) - Object tags for filtering (up to 10).
    """
    name: pulumi.Output[str]
    """
    Unique identifier of the metrics configuration for the bucket.
    """
    def __init__(__self__, resource_name, opts=None, bucket=None, filter=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a S3 bucket [metrics configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/metrics-configurations.html) resource.

        ## Example Usage
        ### Add metrics configuration for entire S3 bucket

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.Bucket("example")
        example_entire_bucket = aws.s3.BucketMetric("example-entire-bucket", bucket=example.bucket)
        ```
        ### Add metrics configuration with S3 bucket object filter

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.Bucket("example")
        example_filtered = aws.s3.BucketMetric("example-filtered",
            bucket=example.bucket,
            filter={
                "prefix": "documents/",
                "tags": {
                    "priority": "high",
                    "class": "blue",
                },
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket to put metric configuration.
        :param pulumi.Input[dict] filter: [Object filtering](http://docs.aws.amazon.com/AmazonS3/latest/dev/metrics-configurations.html#metrics-configurations-filter) that accepts a prefix, tags, or a logical AND of prefix and tags (documented below).
        :param pulumi.Input[str] name: Unique identifier of the metrics configuration for the bucket.

        The **filter** object supports the following:

          * `prefix` (`pulumi.Input[str]`) - Object prefix for filtering (singular).
          * `tags` (`pulumi.Input[dict]`) - Object tags for filtering (up to 10).
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

            if bucket is None:
                raise TypeError("Missing required property 'bucket'")
            __props__['bucket'] = bucket
            __props__['filter'] = filter
            __props__['name'] = name
        super(BucketMetric, __self__).__init__(
            'aws:s3/bucketMetric:BucketMetric',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bucket=None, filter=None, name=None):
        """
        Get an existing BucketMetric resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket to put metric configuration.
        :param pulumi.Input[dict] filter: [Object filtering](http://docs.aws.amazon.com/AmazonS3/latest/dev/metrics-configurations.html#metrics-configurations-filter) that accepts a prefix, tags, or a logical AND of prefix and tags (documented below).
        :param pulumi.Input[str] name: Unique identifier of the metrics configuration for the bucket.

        The **filter** object supports the following:

          * `prefix` (`pulumi.Input[str]`) - Object prefix for filtering (singular).
          * `tags` (`pulumi.Input[dict]`) - Object tags for filtering (up to 10).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket"] = bucket
        __props__["filter"] = filter
        __props__["name"] = name
        return BucketMetric(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
