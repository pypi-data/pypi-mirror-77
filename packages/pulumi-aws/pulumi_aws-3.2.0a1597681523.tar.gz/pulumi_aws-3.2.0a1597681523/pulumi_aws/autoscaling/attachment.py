# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Attachment(pulumi.CustomResource):
    alb_target_group_arn: pulumi.Output[str]
    """
    The ARN of an ALB Target Group.
    """
    autoscaling_group_name: pulumi.Output[str]
    """
    Name of ASG to associate with the ELB.
    """
    elb: pulumi.Output[str]
    """
    The name of the ELB.
    """
    def __init__(__self__, resource_name, opts=None, alb_target_group_arn=None, autoscaling_group_name=None, elb=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an AutoScaling Attachment resource.

        > **NOTE on AutoScaling Groups and ASG Attachments:** This provider currently provides
        both a standalone ASG Attachment resource (describing an ASG attached to
        an ELB or ALB), and an AutoScaling Group resource with
        `load_balancers` and `target_group_arns` defined in-line. At this time you can use an ASG with in-line
        `load balancers` or `target_group_arns` in conjunction with an ASG Attachment resource, however, to prevent
        unintended resource updates, the `autoscaling.Group` resource must be configured
        to ignore changes to the `load_balancers` and `target_group_arns` arguments within a [`lifecycle` configuration block](https://www.terraform.io/docs/configuration/resources.html#lifecycle-lifecycle-customizations).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        # Create a new load balancer attachment
        asg_attachment_bar = aws.autoscaling.Attachment("asgAttachmentBar",
            autoscaling_group_name=aws_autoscaling_group["asg"]["id"],
            elb=aws_elb["bar"]["id"])
        ```

        ```python
        import pulumi
        import pulumi_aws as aws

        # Create a new ALB Target Group attachment
        asg_attachment_bar = aws.autoscaling.Attachment("asgAttachmentBar",
            autoscaling_group_name=aws_autoscaling_group["asg"]["id"],
            alb_target_group_arn=aws_alb_target_group["test"]["arn"])
        ```
        ## With An AutoScaling Group Resource

        ```python
        import pulumi
        import pulumi_aws as aws

        # ... other configuration ...
        asg = aws.autoscaling.Group("asg")
        asg_attachment_bar = aws.autoscaling.Attachment("asgAttachmentBar",
            autoscaling_group_name=asg.id,
            elb=aws_elb["test"]["id"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alb_target_group_arn: The ARN of an ALB Target Group.
        :param pulumi.Input[str] autoscaling_group_name: Name of ASG to associate with the ELB.
        :param pulumi.Input[str] elb: The name of the ELB.
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

            __props__['alb_target_group_arn'] = alb_target_group_arn
            if autoscaling_group_name is None:
                raise TypeError("Missing required property 'autoscaling_group_name'")
            __props__['autoscaling_group_name'] = autoscaling_group_name
            __props__['elb'] = elb
        super(Attachment, __self__).__init__(
            'aws:autoscaling/attachment:Attachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, alb_target_group_arn=None, autoscaling_group_name=None, elb=None):
        """
        Get an existing Attachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alb_target_group_arn: The ARN of an ALB Target Group.
        :param pulumi.Input[str] autoscaling_group_name: Name of ASG to associate with the ELB.
        :param pulumi.Input[str] elb: The name of the ELB.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["alb_target_group_arn"] = alb_target_group_arn
        __props__["autoscaling_group_name"] = autoscaling_group_name
        __props__["elb"] = elb
        return Attachment(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
