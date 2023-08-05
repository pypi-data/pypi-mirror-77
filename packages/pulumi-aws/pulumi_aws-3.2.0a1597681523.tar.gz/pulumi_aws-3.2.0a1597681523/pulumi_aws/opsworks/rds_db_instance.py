# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class RdsDbInstance(pulumi.CustomResource):
    db_password: pulumi.Output[str]
    """
    A db password
    """
    db_user: pulumi.Output[str]
    """
    A db username
    """
    rds_db_instance_arn: pulumi.Output[str]
    """
    The db instance to register for this stack. Changing this will force a new resource.
    """
    stack_id: pulumi.Output[str]
    """
    The stack to register a db instance for. Changing this will force a new resource.
    """
    def __init__(__self__, resource_name, opts=None, db_password=None, db_user=None, rds_db_instance_arn=None, stack_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an OpsWorks RDS DB Instance resource.

        > **Note:** All arguments including the username and password will be stored in the raw state as plain-text.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_instance = aws.opsworks.RdsDbInstance("myInstance",
            stack_id=aws_opsworks_stack["my_stack"]["id"],
            rds_db_instance_arn=aws_db_instance["my_instance"]["arn"],
            db_user="someUser",
            db_password="somePass")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
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

            if db_password is None:
                raise TypeError("Missing required property 'db_password'")
            __props__['db_password'] = db_password
            if db_user is None:
                raise TypeError("Missing required property 'db_user'")
            __props__['db_user'] = db_user
            if rds_db_instance_arn is None:
                raise TypeError("Missing required property 'rds_db_instance_arn'")
            __props__['rds_db_instance_arn'] = rds_db_instance_arn
            if stack_id is None:
                raise TypeError("Missing required property 'stack_id'")
            __props__['stack_id'] = stack_id
        super(RdsDbInstance, __self__).__init__(
            'aws:opsworks/rdsDbInstance:RdsDbInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, db_password=None, db_user=None, rds_db_instance_arn=None, stack_id=None):
        """
        Get an existing RdsDbInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_password: A db password
        :param pulumi.Input[str] db_user: A db username
        :param pulumi.Input[str] rds_db_instance_arn: The db instance to register for this stack. Changing this will force a new resource.
        :param pulumi.Input[str] stack_id: The stack to register a db instance for. Changing this will force a new resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["db_password"] = db_password
        __props__["db_user"] = db_user
        __props__["rds_db_instance_arn"] = rds_db_instance_arn
        __props__["stack_id"] = stack_id
        return RdsDbInstance(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
