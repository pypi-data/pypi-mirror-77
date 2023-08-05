# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetDirectoryResult:
    """
    A collection of values returned by getDirectory.
    """
    def __init__(__self__, alias=None, customer_user_name=None, directory_id=None, directory_name=None, directory_type=None, dns_ip_addresses=None, iam_role_id=None, id=None, ip_group_ids=None, registration_code=None, self_service_permissions=None, subnet_ids=None, tags=None, workspace_security_group_id=None):
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        __self__.alias = alias
        """
        The directory alias.
        """
        if customer_user_name and not isinstance(customer_user_name, str):
            raise TypeError("Expected argument 'customer_user_name' to be a str")
        __self__.customer_user_name = customer_user_name
        """
        The user name for the service account.
        """
        if directory_id and not isinstance(directory_id, str):
            raise TypeError("Expected argument 'directory_id' to be a str")
        __self__.directory_id = directory_id
        if directory_name and not isinstance(directory_name, str):
            raise TypeError("Expected argument 'directory_name' to be a str")
        __self__.directory_name = directory_name
        """
        The name of the directory.
        """
        if directory_type and not isinstance(directory_type, str):
            raise TypeError("Expected argument 'directory_type' to be a str")
        __self__.directory_type = directory_type
        """
        The directory type.
        """
        if dns_ip_addresses and not isinstance(dns_ip_addresses, list):
            raise TypeError("Expected argument 'dns_ip_addresses' to be a list")
        __self__.dns_ip_addresses = dns_ip_addresses
        """
        The IP addresses of the DNS servers for the directory.
        """
        if iam_role_id and not isinstance(iam_role_id, str):
            raise TypeError("Expected argument 'iam_role_id' to be a str")
        __self__.iam_role_id = iam_role_id
        """
        The identifier of the IAM role. This is the role that allows Amazon WorkSpaces to make calls to other services, such as Amazon EC2, on your behalf.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if ip_group_ids and not isinstance(ip_group_ids, list):
            raise TypeError("Expected argument 'ip_group_ids' to be a list")
        __self__.ip_group_ids = ip_group_ids
        """
        The identifiers of the IP access control groups associated with the directory.
        """
        if registration_code and not isinstance(registration_code, str):
            raise TypeError("Expected argument 'registration_code' to be a str")
        __self__.registration_code = registration_code
        """
        The registration code for the directory. This is the code that users enter in their Amazon WorkSpaces client application to connect to the directory.
        """
        if self_service_permissions and not isinstance(self_service_permissions, list):
            raise TypeError("Expected argument 'self_service_permissions' to be a list")
        __self__.self_service_permissions = self_service_permissions
        """
        The permissions to enable or disable self-service capabilities.
        """
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        __self__.subnet_ids = subnet_ids
        """
        The identifiers of the subnets where the directory resides.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A map of tags assigned to the WorkSpaces directory.
        """
        if workspace_security_group_id and not isinstance(workspace_security_group_id, str):
            raise TypeError("Expected argument 'workspace_security_group_id' to be a str")
        __self__.workspace_security_group_id = workspace_security_group_id
        """
        The identifier of the security group that is assigned to new WorkSpaces.
        """


class AwaitableGetDirectoryResult(GetDirectoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDirectoryResult(
            alias=self.alias,
            customer_user_name=self.customer_user_name,
            directory_id=self.directory_id,
            directory_name=self.directory_name,
            directory_type=self.directory_type,
            dns_ip_addresses=self.dns_ip_addresses,
            iam_role_id=self.iam_role_id,
            id=self.id,
            ip_group_ids=self.ip_group_ids,
            registration_code=self.registration_code,
            self_service_permissions=self.self_service_permissions,
            subnet_ids=self.subnet_ids,
            tags=self.tags,
            workspace_security_group_id=self.workspace_security_group_id)


def get_directory(directory_id=None, tags=None, opts=None):
    """
    Retrieve information about an AWS WorkSpaces directory.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.workspaces.get_directory(directory_id="d-9067783251")
    ```


    :param str directory_id: The directory identifier for registration in WorkSpaces service.
    :param dict tags: A map of tags assigned to the WorkSpaces directory.
    """
    __args__ = dict()
    __args__['directoryId'] = directory_id
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:workspaces/getDirectory:getDirectory', __args__, opts=opts).value

    return AwaitableGetDirectoryResult(
        alias=__ret__.get('alias'),
        customer_user_name=__ret__.get('customerUserName'),
        directory_id=__ret__.get('directoryId'),
        directory_name=__ret__.get('directoryName'),
        directory_type=__ret__.get('directoryType'),
        dns_ip_addresses=__ret__.get('dnsIpAddresses'),
        iam_role_id=__ret__.get('iamRoleId'),
        id=__ret__.get('id'),
        ip_group_ids=__ret__.get('ipGroupIds'),
        registration_code=__ret__.get('registrationCode'),
        self_service_permissions=__ret__.get('selfServicePermissions'),
        subnet_ids=__ret__.get('subnetIds'),
        tags=__ret__.get('tags'),
        workspace_security_group_id=__ret__.get('workspaceSecurityGroupId'))
