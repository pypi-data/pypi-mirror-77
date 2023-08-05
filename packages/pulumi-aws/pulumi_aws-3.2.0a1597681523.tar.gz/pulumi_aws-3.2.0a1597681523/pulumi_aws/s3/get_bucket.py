# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetBucketResult:
    """
    A collection of values returned by getBucket.
    """
    def __init__(__self__, arn=None, bucket=None, bucket_domain_name=None, bucket_regional_domain_name=None, hosted_zone_id=None, id=None, region=None, website_domain=None, website_endpoint=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        The ARN of the bucket. Will be of format `arn:aws:s3:::bucketname`.
        """
        if bucket and not isinstance(bucket, str):
            raise TypeError("Expected argument 'bucket' to be a str")
        __self__.bucket = bucket
        if bucket_domain_name and not isinstance(bucket_domain_name, str):
            raise TypeError("Expected argument 'bucket_domain_name' to be a str")
        __self__.bucket_domain_name = bucket_domain_name
        """
        The bucket domain name. Will be of format `bucketname.s3.amazonaws.com`.
        """
        if bucket_regional_domain_name and not isinstance(bucket_regional_domain_name, str):
            raise TypeError("Expected argument 'bucket_regional_domain_name' to be a str")
        __self__.bucket_regional_domain_name = bucket_regional_domain_name
        """
        The bucket region-specific domain name. The bucket domain name including the region name, please refer [here](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) for format. Note: The AWS CloudFront allows specifying S3 region-specific endpoint when creating S3 origin, it will prevent [redirect issues](https://forums.aws.amazon.com/thread.jspa?threadID=216814) from CloudFront to S3 Origin URL.
        """
        if hosted_zone_id and not isinstance(hosted_zone_id, str):
            raise TypeError("Expected argument 'hosted_zone_id' to be a str")
        __self__.hosted_zone_id = hosted_zone_id
        """
        The [Route 53 Hosted Zone ID](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_website_region_endpoints) for this bucket's region.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        __self__.region = region
        """
        The AWS region this bucket resides in.
        """
        if website_domain and not isinstance(website_domain, str):
            raise TypeError("Expected argument 'website_domain' to be a str")
        __self__.website_domain = website_domain
        """
        The domain of the website endpoint, if the bucket is configured with a website. If not, this will be an empty string. This is used to create Route 53 alias records.
        """
        if website_endpoint and not isinstance(website_endpoint, str):
            raise TypeError("Expected argument 'website_endpoint' to be a str")
        __self__.website_endpoint = website_endpoint
        """
        The website endpoint, if the bucket is configured with a website. If not, this will be an empty string.
        """


class AwaitableGetBucketResult(GetBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketResult(
            arn=self.arn,
            bucket=self.bucket,
            bucket_domain_name=self.bucket_domain_name,
            bucket_regional_domain_name=self.bucket_regional_domain_name,
            hosted_zone_id=self.hosted_zone_id,
            id=self.id,
            region=self.region,
            website_domain=self.website_domain,
            website_endpoint=self.website_endpoint)


def get_bucket(bucket=None, opts=None):
    """
    Provides details about a specific S3 bucket.

    This resource may prove useful when setting up a Route53 record, or an origin for a CloudFront
    Distribution.

    ## Example Usage
    ### Route53 Record

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="bucket.test.com")
    test_zone = aws.route53.get_zone(name="test.com.")
    example = aws.route53.Record("example",
        zone_id=test_zone.id,
        name="bucket",
        type="A",
        aliases=[{
            "name": selected.website_domain,
            "zone_id": selected.hosted_zone_id,
        }])
    ```
    ### CloudFront Origin

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="a-test-bucket")
    test = aws.cloudfront.Distribution("test", origins=[{
        "domain_name": selected.bucket_domain_name,
        "originId": "s3-selected-bucket",
    }])
    ```


    :param str bucket: The name of the bucket
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:s3/getBucket:getBucket', __args__, opts=opts).value

    return AwaitableGetBucketResult(
        arn=__ret__.get('arn'),
        bucket=__ret__.get('bucket'),
        bucket_domain_name=__ret__.get('bucketDomainName'),
        bucket_regional_domain_name=__ret__.get('bucketRegionalDomainName'),
        hosted_zone_id=__ret__.get('hostedZoneId'),
        id=__ret__.get('id'),
        region=__ret__.get('region'),
        website_domain=__ret__.get('websiteDomain'),
        website_endpoint=__ret__.get('websiteEndpoint'))
