# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class JobQueue(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name of the job queue.
    """
    compute_environments: pulumi.Output[list]
    """
    Specifies the set of compute environments
    mapped to a job queue and their order.  The position of the compute environments
    in the list will dictate the order. You can associate up to 3 compute environments
    with a job queue.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the job queue.
    """
    priority: pulumi.Output[float]
    """
    The priority of the job queue. Job queues with a higher priority
    are evaluated first when associated with the same compute environment.
    """
    state: pulumi.Output[str]
    """
    The state of the job queue. Must be one of: `ENABLED` or `DISABLED`
    """
    def __init__(__self__, resource_name, opts=None, compute_environments=None, name=None, priority=None, state=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Batch Job Queue resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test_queue = aws.batch.JobQueue("testQueue",
            state="ENABLED",
            priority=1,
            compute_environments=[
                aws_batch_compute_environment["test_environment_1"]["arn"],
                aws_batch_compute_environment["test_environment_2"]["arn"],
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] compute_environments: Specifies the set of compute environments
               mapped to a job queue and their order.  The position of the compute environments
               in the list will dictate the order. You can associate up to 3 compute environments
               with a job queue.
        :param pulumi.Input[str] name: Specifies the name of the job queue.
        :param pulumi.Input[float] priority: The priority of the job queue. Job queues with a higher priority
               are evaluated first when associated with the same compute environment.
        :param pulumi.Input[str] state: The state of the job queue. Must be one of: `ENABLED` or `DISABLED`
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

            if compute_environments is None:
                raise TypeError("Missing required property 'compute_environments'")
            __props__['compute_environments'] = compute_environments
            __props__['name'] = name
            if priority is None:
                raise TypeError("Missing required property 'priority'")
            __props__['priority'] = priority
            if state is None:
                raise TypeError("Missing required property 'state'")
            __props__['state'] = state
            __props__['arn'] = None
        super(JobQueue, __self__).__init__(
            'aws:batch/jobQueue:JobQueue',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, arn=None, compute_environments=None, name=None, priority=None, state=None):
        """
        Get an existing JobQueue resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name of the job queue.
        :param pulumi.Input[list] compute_environments: Specifies the set of compute environments
               mapped to a job queue and their order.  The position of the compute environments
               in the list will dictate the order. You can associate up to 3 compute environments
               with a job queue.
        :param pulumi.Input[str] name: Specifies the name of the job queue.
        :param pulumi.Input[float] priority: The priority of the job queue. Job queues with a higher priority
               are evaluated first when associated with the same compute environment.
        :param pulumi.Input[str] state: The state of the job queue. Must be one of: `ENABLED` or `DISABLED`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["compute_environments"] = compute_environments
        __props__["name"] = name
        __props__["priority"] = priority
        __props__["state"] = state
        return JobQueue(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
