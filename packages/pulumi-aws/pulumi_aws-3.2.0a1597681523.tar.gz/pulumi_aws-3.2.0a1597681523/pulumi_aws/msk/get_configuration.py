# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetConfigurationResult:
    """
    A collection of values returned by getConfiguration.
    """
    def __init__(__self__, arn=None, description=None, id=None, kafka_versions=None, latest_revision=None, name=None, server_properties=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        __self__.arn = arn
        """
        Amazon Resource Name (ARN) of the configuration.
        """
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        Description of the configuration.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if kafka_versions and not isinstance(kafka_versions, list):
            raise TypeError("Expected argument 'kafka_versions' to be a list")
        __self__.kafka_versions = kafka_versions
        """
        List of Apache Kafka versions which can use this configuration.
        """
        if latest_revision and not isinstance(latest_revision, float):
            raise TypeError("Expected argument 'latest_revision' to be a float")
        __self__.latest_revision = latest_revision
        """
        Latest revision of the configuration.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if server_properties and not isinstance(server_properties, str):
            raise TypeError("Expected argument 'server_properties' to be a str")
        __self__.server_properties = server_properties
        """
        Contents of the server.properties file.
        """


class AwaitableGetConfigurationResult(GetConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            kafka_versions=self.kafka_versions,
            latest_revision=self.latest_revision,
            name=self.name,
            server_properties=self.server_properties)


def get_configuration(name=None, opts=None):
    """
    Get information on an Amazon MSK Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.msk.get_configuration(name="example")
    ```


    :param str name: Name of the configuration.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:msk/getConfiguration:getConfiguration', __args__, opts=opts).value

    return AwaitableGetConfigurationResult(
        arn=__ret__.get('arn'),
        description=__ret__.get('description'),
        id=__ret__.get('id'),
        kafka_versions=__ret__.get('kafkaVersions'),
        latest_revision=__ret__.get('latestRevision'),
        name=__ret__.get('name'),
        server_properties=__ret__.get('serverProperties'))
