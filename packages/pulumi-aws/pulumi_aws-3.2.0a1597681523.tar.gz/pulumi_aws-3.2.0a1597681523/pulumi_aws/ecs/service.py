# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class Service(pulumi.CustomResource):
    capacity_provider_strategies: pulumi.Output[list]
    """
    The capacity provider strategy to use for the service. Can be one or more.  Defined below.

      * `base` (`float`) - The number of tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined.
      * `capacityProvider` (`str`) - The short name of the capacity provider.
      * `weight` (`float`) - The relative percentage of the total number of launched tasks that should use the specified capacity provider.
    """
    cluster: pulumi.Output[str]
    """
    ARN of an ECS cluster
    """
    deployment_controller: pulumi.Output[dict]
    """
    Configuration block containing deployment controller configuration. Defined below.

      * `type` (`str`) - Type of deployment controller. Valid values: `CODE_DEPLOY`, `ECS`, `EXTERNAL`. Default: `ECS`.
    """
    deployment_maximum_percent: pulumi.Output[float]
    """
    The upper limit (as a percentage of the service's desiredCount) of the number of running tasks that can be running in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
    """
    deployment_minimum_healthy_percent: pulumi.Output[float]
    """
    The lower limit (as a percentage of the service's desiredCount) of the number of running tasks that must remain running and healthy in a service during a deployment.
    """
    desired_count: pulumi.Output[float]
    """
    The number of instances of the task definition to place and keep running. Defaults to 0. Do not specify if using the `DAEMON` scheduling strategy.
    """
    enable_ecs_managed_tags: pulumi.Output[bool]
    """
    Specifies whether to enable Amazon ECS managed tags for the tasks within the service.
    """
    force_new_deployment: pulumi.Output[bool]
    """
    Enable to force a new task deployment of the service. This can be used to update tasks to use a newer Docker image with same image/tag combination (e.g. `myimage:latest`), roll Fargate tasks onto a newer platform version, or immediately deploy `ordered_placement_strategy` and `placement_constraints` updates.
    """
    health_check_grace_period_seconds: pulumi.Output[float]
    """
    Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 2147483647. Only valid for services configured to use load balancers.
    """
    iam_role: pulumi.Output[str]
    """
    ARN of the IAM role that allows Amazon ECS to make calls to your load balancer on your behalf. This parameter is required if you are using a load balancer with your service, but only if your task definition does not use the `awsvpc` network mode. If using `awsvpc` network mode, do not specify this role. If your account has already created the Amazon ECS service-linked role, that role is used by default for your service unless you specify a role here.
    """
    launch_type: pulumi.Output[str]
    """
    The launch type on which to run your service. The valid values are `EC2` and `FARGATE`. Defaults to `EC2`.
    """
    load_balancers: pulumi.Output[list]
    """
    A load balancer block. Load balancers documented below.

      * `container_name` (`str`) - The name of the container to associate with the load balancer (as it appears in a container definition).
      * `containerPort` (`float`) - The port on the container to associate with the load balancer.
      * `elbName` (`str`) - The name of the ELB (Classic) to associate with the service.
      * `target_group_arn` (`str`) - The ARN of the Load Balancer target group to associate with the service.
    """
    name: pulumi.Output[str]
    """
    The name of the service (up to 255 letters, numbers, hyphens, and underscores)
    """
    network_configuration: pulumi.Output[dict]
    """
    The network configuration for the service. This parameter is required for task definitions that use the `awsvpc` network mode to receive their own Elastic Network Interface, and it is not supported for other network modes.

      * `assignPublicIp` (`bool`) - Assign a public IP address to the ENI (Fargate launch type only). Valid values are `true` or `false`. Default `false`.
      * `security_groups` (`list`) - The security groups associated with the task or service. If you do not specify a security group, the default security group for the VPC is used.
      * `subnets` (`list`) - The subnets associated with the task or service.
    """
    ordered_placement_strategies: pulumi.Output[list]
    """
    Service level strategy rules that are taken into consideration during task placement. List from top to bottom in order of precedence. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. The maximum number of `ordered_placement_strategy` blocks is `5`. Defined below.

      * `field` (`str`) - For the `spread` placement strategy, valid values are `instanceId` (or `host`,
        which has the same effect), or any platform or custom attribute that is applied to a container instance.
        For the `binpack` type, valid values are `memory` and `cpu`. For the `random` type, this attribute is not
        needed. For more information, see [Placement Strategy](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PlacementStrategy.html).
      * `type` (`str`) - The type of placement strategy. Must be one of: `binpack`, `random`, or `spread`
    """
    placement_constraints: pulumi.Output[list]
    """
    rules that are taken into consideration during task placement. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. Maximum number of `placement_constraints` is `10`. Defined below.

      * `expression` (`str`) - Cluster Query Language expression to apply to the constraint. Does not need to be specified
        for the `distinctInstance` type.
        For more information, see [Cluster Query Language in the Amazon EC2 Container
        Service Developer
        Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html).
      * `type` (`str`) - The type of constraint. The only valid values at this time are `memberOf` and `distinctInstance`.
    """
    platform_version: pulumi.Output[str]
    """
    The platform version on which to run your service. Only applicable for `launch_type` set to `FARGATE`. Defaults to `LATEST`. More information about Fargate platform versions can be found in the [AWS ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html).
    """
    propagate_tags: pulumi.Output[str]
    """
    Specifies whether to propagate the tags from the task definition or the service to the tasks. The valid values are `SERVICE` and `TASK_DEFINITION`.
    """
    scheduling_strategy: pulumi.Output[str]
    """
    The scheduling strategy to use for the service. The valid values are `REPLICA` and `DAEMON`. Defaults to `REPLICA`. Note that [*Tasks using the Fargate launch type or the `CODE_DEPLOY` or `EXTERNAL` deployment controller types don't support the `DAEMON` scheduling strategy*](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateService.html).
    """
    service_registries: pulumi.Output[dict]
    """
    The service discovery registries for the service. The maximum number of `service_registries` blocks is `1`.

      * `container_name` (`str`) - The container name value, already specified in the task definition, to be used for your service discovery service.
      * `containerPort` (`float`) - The port value, already specified in the task definition, to be used for your service discovery service.
      * `port` (`float`) - The port value used if your Service Discovery service specified an SRV record.
      * `registryArn` (`str`) - The ARN of the Service Registry. The currently supported service registry is Amazon Route 53 Auto Naming Service(`servicediscovery.Service`). For more information, see [Service](https://docs.aws.amazon.com/Route53/latest/APIReference/API_autonaming_Service.html)
    """
    tags: pulumi.Output[dict]
    """
    Key-value map of resource tags
    """
    task_definition: pulumi.Output[str]
    """
    The family and revision (`family:revision`) or full ARN of the task definition that you want to run in your service. Required unless using the `EXTERNAL` deployment controller. If a revision is not specified, the latest `ACTIVE` revision is used.
    """
    wait_for_steady_state: pulumi.Output[bool]
    def __init__(__self__, resource_name, opts=None, capacity_provider_strategies=None, cluster=None, deployment_controller=None, deployment_maximum_percent=None, deployment_minimum_healthy_percent=None, desired_count=None, enable_ecs_managed_tags=None, force_new_deployment=None, health_check_grace_period_seconds=None, iam_role=None, launch_type=None, load_balancers=None, name=None, network_configuration=None, ordered_placement_strategies=None, placement_constraints=None, platform_version=None, propagate_tags=None, scheduling_strategy=None, service_registries=None, tags=None, task_definition=None, wait_for_steady_state=None, __props__=None, __name__=None, __opts__=None):
        """
        > **Note:** To prevent a race condition during service deletion, make sure to set `depends_on` to the related `iam.RolePolicy`; otherwise, the policy may be destroyed too soon and the ECS service will then get stuck in the `DRAINING` state.

        Provides an ECS service - effectively a task that is expected to run until an error occurs or a user terminates it (typically a webserver or a database).

        See [ECS Services section in AWS developer guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        mongo = aws.ecs.Service("mongo",
            cluster=aws_ecs_cluster["foo"]["id"],
            task_definition=aws_ecs_task_definition["mongo"]["arn"],
            desired_count=3,
            iam_role=aws_iam_role["foo"]["arn"],
            ordered_placement_strategies=[{
                "type": "binpack",
                "field": "cpu",
            }],
            load_balancers=[{
                "target_group_arn": aws_lb_target_group["foo"]["arn"],
                "container_name": "mongo",
                "containerPort": 8080,
            }],
            placement_constraints=[{
                "type": "memberOf",
                "expression": "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]",
            }],
            opts=ResourceOptions(depends_on=[aws_iam_role_policy["foo"]]))
        ```
        ### Ignoring Changes to Desired Count

        You can use [`ignoreChanges`](https://www.pulumi.com/docs/intro/concepts/programming-model/#ignorechanges) to create an ECS service with an initial count of running instances, then ignore any changes to that count caused externally (e.g. Application Autoscaling).

        ```python
        import pulumi
        import pulumi_aws as aws

        # ... other configurations ...
        example = aws.ecs.Service("example", desired_count=2)
        ```
        ### Daemon Scheduling Strategy

        ```python
        import pulumi
        import pulumi_aws as aws

        bar = aws.ecs.Service("bar",
            cluster=aws_ecs_cluster["foo"]["id"],
            task_definition=aws_ecs_task_definition["bar"]["arn"],
            scheduling_strategy="DAEMON")
        ```
        ### External Deployment Controller

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ecs.Service("example",
            cluster=aws_ecs_cluster["example"]["id"],
            deployment_controller={
                "type": "EXTERNAL",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] capacity_provider_strategies: The capacity provider strategy to use for the service. Can be one or more.  Defined below.
        :param pulumi.Input[str] cluster: ARN of an ECS cluster
        :param pulumi.Input[dict] deployment_controller: Configuration block containing deployment controller configuration. Defined below.
        :param pulumi.Input[float] deployment_maximum_percent: The upper limit (as a percentage of the service's desiredCount) of the number of running tasks that can be running in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
        :param pulumi.Input[float] deployment_minimum_healthy_percent: The lower limit (as a percentage of the service's desiredCount) of the number of running tasks that must remain running and healthy in a service during a deployment.
        :param pulumi.Input[float] desired_count: The number of instances of the task definition to place and keep running. Defaults to 0. Do not specify if using the `DAEMON` scheduling strategy.
        :param pulumi.Input[bool] enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service.
        :param pulumi.Input[bool] force_new_deployment: Enable to force a new task deployment of the service. This can be used to update tasks to use a newer Docker image with same image/tag combination (e.g. `myimage:latest`), roll Fargate tasks onto a newer platform version, or immediately deploy `ordered_placement_strategy` and `placement_constraints` updates.
        :param pulumi.Input[float] health_check_grace_period_seconds: Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 2147483647. Only valid for services configured to use load balancers.
        :param pulumi.Input[str] iam_role: ARN of the IAM role that allows Amazon ECS to make calls to your load balancer on your behalf. This parameter is required if you are using a load balancer with your service, but only if your task definition does not use the `awsvpc` network mode. If using `awsvpc` network mode, do not specify this role. If your account has already created the Amazon ECS service-linked role, that role is used by default for your service unless you specify a role here.
        :param pulumi.Input[str] launch_type: The launch type on which to run your service. The valid values are `EC2` and `FARGATE`. Defaults to `EC2`.
        :param pulumi.Input[list] load_balancers: A load balancer block. Load balancers documented below.
        :param pulumi.Input[str] name: The name of the service (up to 255 letters, numbers, hyphens, and underscores)
        :param pulumi.Input[dict] network_configuration: The network configuration for the service. This parameter is required for task definitions that use the `awsvpc` network mode to receive their own Elastic Network Interface, and it is not supported for other network modes.
        :param pulumi.Input[list] ordered_placement_strategies: Service level strategy rules that are taken into consideration during task placement. List from top to bottom in order of precedence. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. The maximum number of `ordered_placement_strategy` blocks is `5`. Defined below.
        :param pulumi.Input[list] placement_constraints: rules that are taken into consideration during task placement. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. Maximum number of `placement_constraints` is `10`. Defined below.
        :param pulumi.Input[str] platform_version: The platform version on which to run your service. Only applicable for `launch_type` set to `FARGATE`. Defaults to `LATEST`. More information about Fargate platform versions can be found in the [AWS ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html).
        :param pulumi.Input[str] propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks. The valid values are `SERVICE` and `TASK_DEFINITION`.
        :param pulumi.Input[str] scheduling_strategy: The scheduling strategy to use for the service. The valid values are `REPLICA` and `DAEMON`. Defaults to `REPLICA`. Note that [*Tasks using the Fargate launch type or the `CODE_DEPLOY` or `EXTERNAL` deployment controller types don't support the `DAEMON` scheduling strategy*](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateService.html).
        :param pulumi.Input[dict] service_registries: The service discovery registries for the service. The maximum number of `service_registries` blocks is `1`.
        :param pulumi.Input[dict] tags: Key-value map of resource tags
        :param pulumi.Input[str] task_definition: The family and revision (`family:revision`) or full ARN of the task definition that you want to run in your service. Required unless using the `EXTERNAL` deployment controller. If a revision is not specified, the latest `ACTIVE` revision is used.

        The **capacity_provider_strategies** object supports the following:

          * `base` (`pulumi.Input[float]`) - The number of tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined.
          * `capacityProvider` (`pulumi.Input[str]`) - The short name of the capacity provider.
          * `weight` (`pulumi.Input[float]`) - The relative percentage of the total number of launched tasks that should use the specified capacity provider.

        The **deployment_controller** object supports the following:

          * `type` (`pulumi.Input[str]`) - Type of deployment controller. Valid values: `CODE_DEPLOY`, `ECS`, `EXTERNAL`. Default: `ECS`.

        The **load_balancers** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The name of the container to associate with the load balancer (as it appears in a container definition).
          * `containerPort` (`pulumi.Input[float]`) - The port on the container to associate with the load balancer.
          * `elbName` (`pulumi.Input[str]`) - The name of the ELB (Classic) to associate with the service.
          * `target_group_arn` (`pulumi.Input[str]`) - The ARN of the Load Balancer target group to associate with the service.

        The **network_configuration** object supports the following:

          * `assignPublicIp` (`pulumi.Input[bool]`) - Assign a public IP address to the ENI (Fargate launch type only). Valid values are `true` or `false`. Default `false`.
          * `security_groups` (`pulumi.Input[list]`) - The security groups associated with the task or service. If you do not specify a security group, the default security group for the VPC is used.
          * `subnets` (`pulumi.Input[list]`) - The subnets associated with the task or service.

        The **ordered_placement_strategies** object supports the following:

          * `field` (`pulumi.Input[str]`) - For the `spread` placement strategy, valid values are `instanceId` (or `host`,
            which has the same effect), or any platform or custom attribute that is applied to a container instance.
            For the `binpack` type, valid values are `memory` and `cpu`. For the `random` type, this attribute is not
            needed. For more information, see [Placement Strategy](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PlacementStrategy.html).
          * `type` (`pulumi.Input[str]`) - The type of placement strategy. Must be one of: `binpack`, `random`, or `spread`

        The **placement_constraints** object supports the following:

          * `expression` (`pulumi.Input[str]`) - Cluster Query Language expression to apply to the constraint. Does not need to be specified
            for the `distinctInstance` type.
            For more information, see [Cluster Query Language in the Amazon EC2 Container
            Service Developer
            Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html).
          * `type` (`pulumi.Input[str]`) - The type of constraint. The only valid values at this time are `memberOf` and `distinctInstance`.

        The **service_registries** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The container name value, already specified in the task definition, to be used for your service discovery service.
          * `containerPort` (`pulumi.Input[float]`) - The port value, already specified in the task definition, to be used for your service discovery service.
          * `port` (`pulumi.Input[float]`) - The port value used if your Service Discovery service specified an SRV record.
          * `registryArn` (`pulumi.Input[str]`) - The ARN of the Service Registry. The currently supported service registry is Amazon Route 53 Auto Naming Service(`servicediscovery.Service`). For more information, see [Service](https://docs.aws.amazon.com/Route53/latest/APIReference/API_autonaming_Service.html)
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

            __props__['capacity_provider_strategies'] = capacity_provider_strategies
            __props__['cluster'] = cluster
            __props__['deployment_controller'] = deployment_controller
            __props__['deployment_maximum_percent'] = deployment_maximum_percent
            __props__['deployment_minimum_healthy_percent'] = deployment_minimum_healthy_percent
            __props__['desired_count'] = desired_count
            __props__['enable_ecs_managed_tags'] = enable_ecs_managed_tags
            __props__['force_new_deployment'] = force_new_deployment
            __props__['health_check_grace_period_seconds'] = health_check_grace_period_seconds
            __props__['iam_role'] = iam_role
            __props__['launch_type'] = launch_type
            __props__['load_balancers'] = load_balancers
            __props__['name'] = name
            __props__['network_configuration'] = network_configuration
            __props__['ordered_placement_strategies'] = ordered_placement_strategies
            __props__['placement_constraints'] = placement_constraints
            __props__['platform_version'] = platform_version
            __props__['propagate_tags'] = propagate_tags
            __props__['scheduling_strategy'] = scheduling_strategy
            __props__['service_registries'] = service_registries
            __props__['tags'] = tags
            __props__['task_definition'] = task_definition
            __props__['wait_for_steady_state'] = wait_for_steady_state
        super(Service, __self__).__init__(
            'aws:ecs/service:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, capacity_provider_strategies=None, cluster=None, deployment_controller=None, deployment_maximum_percent=None, deployment_minimum_healthy_percent=None, desired_count=None, enable_ecs_managed_tags=None, force_new_deployment=None, health_check_grace_period_seconds=None, iam_role=None, launch_type=None, load_balancers=None, name=None, network_configuration=None, ordered_placement_strategies=None, placement_constraints=None, platform_version=None, propagate_tags=None, scheduling_strategy=None, service_registries=None, tags=None, task_definition=None, wait_for_steady_state=None):
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] capacity_provider_strategies: The capacity provider strategy to use for the service. Can be one or more.  Defined below.
        :param pulumi.Input[str] cluster: ARN of an ECS cluster
        :param pulumi.Input[dict] deployment_controller: Configuration block containing deployment controller configuration. Defined below.
        :param pulumi.Input[float] deployment_maximum_percent: The upper limit (as a percentage of the service's desiredCount) of the number of running tasks that can be running in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
        :param pulumi.Input[float] deployment_minimum_healthy_percent: The lower limit (as a percentage of the service's desiredCount) of the number of running tasks that must remain running and healthy in a service during a deployment.
        :param pulumi.Input[float] desired_count: The number of instances of the task definition to place and keep running. Defaults to 0. Do not specify if using the `DAEMON` scheduling strategy.
        :param pulumi.Input[bool] enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service.
        :param pulumi.Input[bool] force_new_deployment: Enable to force a new task deployment of the service. This can be used to update tasks to use a newer Docker image with same image/tag combination (e.g. `myimage:latest`), roll Fargate tasks onto a newer platform version, or immediately deploy `ordered_placement_strategy` and `placement_constraints` updates.
        :param pulumi.Input[float] health_check_grace_period_seconds: Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 2147483647. Only valid for services configured to use load balancers.
        :param pulumi.Input[str] iam_role: ARN of the IAM role that allows Amazon ECS to make calls to your load balancer on your behalf. This parameter is required if you are using a load balancer with your service, but only if your task definition does not use the `awsvpc` network mode. If using `awsvpc` network mode, do not specify this role. If your account has already created the Amazon ECS service-linked role, that role is used by default for your service unless you specify a role here.
        :param pulumi.Input[str] launch_type: The launch type on which to run your service. The valid values are `EC2` and `FARGATE`. Defaults to `EC2`.
        :param pulumi.Input[list] load_balancers: A load balancer block. Load balancers documented below.
        :param pulumi.Input[str] name: The name of the service (up to 255 letters, numbers, hyphens, and underscores)
        :param pulumi.Input[dict] network_configuration: The network configuration for the service. This parameter is required for task definitions that use the `awsvpc` network mode to receive their own Elastic Network Interface, and it is not supported for other network modes.
        :param pulumi.Input[list] ordered_placement_strategies: Service level strategy rules that are taken into consideration during task placement. List from top to bottom in order of precedence. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. The maximum number of `ordered_placement_strategy` blocks is `5`. Defined below.
        :param pulumi.Input[list] placement_constraints: rules that are taken into consideration during task placement. Updates to this configuration will take effect next task deployment unless `force_new_deployment` is enabled. Maximum number of `placement_constraints` is `10`. Defined below.
        :param pulumi.Input[str] platform_version: The platform version on which to run your service. Only applicable for `launch_type` set to `FARGATE`. Defaults to `LATEST`. More information about Fargate platform versions can be found in the [AWS ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html).
        :param pulumi.Input[str] propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks. The valid values are `SERVICE` and `TASK_DEFINITION`.
        :param pulumi.Input[str] scheduling_strategy: The scheduling strategy to use for the service. The valid values are `REPLICA` and `DAEMON`. Defaults to `REPLICA`. Note that [*Tasks using the Fargate launch type or the `CODE_DEPLOY` or `EXTERNAL` deployment controller types don't support the `DAEMON` scheduling strategy*](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateService.html).
        :param pulumi.Input[dict] service_registries: The service discovery registries for the service. The maximum number of `service_registries` blocks is `1`.
        :param pulumi.Input[dict] tags: Key-value map of resource tags
        :param pulumi.Input[str] task_definition: The family and revision (`family:revision`) or full ARN of the task definition that you want to run in your service. Required unless using the `EXTERNAL` deployment controller. If a revision is not specified, the latest `ACTIVE` revision is used.

        The **capacity_provider_strategies** object supports the following:

          * `base` (`pulumi.Input[float]`) - The number of tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined.
          * `capacityProvider` (`pulumi.Input[str]`) - The short name of the capacity provider.
          * `weight` (`pulumi.Input[float]`) - The relative percentage of the total number of launched tasks that should use the specified capacity provider.

        The **deployment_controller** object supports the following:

          * `type` (`pulumi.Input[str]`) - Type of deployment controller. Valid values: `CODE_DEPLOY`, `ECS`, `EXTERNAL`. Default: `ECS`.

        The **load_balancers** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The name of the container to associate with the load balancer (as it appears in a container definition).
          * `containerPort` (`pulumi.Input[float]`) - The port on the container to associate with the load balancer.
          * `elbName` (`pulumi.Input[str]`) - The name of the ELB (Classic) to associate with the service.
          * `target_group_arn` (`pulumi.Input[str]`) - The ARN of the Load Balancer target group to associate with the service.

        The **network_configuration** object supports the following:

          * `assignPublicIp` (`pulumi.Input[bool]`) - Assign a public IP address to the ENI (Fargate launch type only). Valid values are `true` or `false`. Default `false`.
          * `security_groups` (`pulumi.Input[list]`) - The security groups associated with the task or service. If you do not specify a security group, the default security group for the VPC is used.
          * `subnets` (`pulumi.Input[list]`) - The subnets associated with the task or service.

        The **ordered_placement_strategies** object supports the following:

          * `field` (`pulumi.Input[str]`) - For the `spread` placement strategy, valid values are `instanceId` (or `host`,
            which has the same effect), or any platform or custom attribute that is applied to a container instance.
            For the `binpack` type, valid values are `memory` and `cpu`. For the `random` type, this attribute is not
            needed. For more information, see [Placement Strategy](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PlacementStrategy.html).
          * `type` (`pulumi.Input[str]`) - The type of placement strategy. Must be one of: `binpack`, `random`, or `spread`

        The **placement_constraints** object supports the following:

          * `expression` (`pulumi.Input[str]`) - Cluster Query Language expression to apply to the constraint. Does not need to be specified
            for the `distinctInstance` type.
            For more information, see [Cluster Query Language in the Amazon EC2 Container
            Service Developer
            Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html).
          * `type` (`pulumi.Input[str]`) - The type of constraint. The only valid values at this time are `memberOf` and `distinctInstance`.

        The **service_registries** object supports the following:

          * `container_name` (`pulumi.Input[str]`) - The container name value, already specified in the task definition, to be used for your service discovery service.
          * `containerPort` (`pulumi.Input[float]`) - The port value, already specified in the task definition, to be used for your service discovery service.
          * `port` (`pulumi.Input[float]`) - The port value used if your Service Discovery service specified an SRV record.
          * `registryArn` (`pulumi.Input[str]`) - The ARN of the Service Registry. The currently supported service registry is Amazon Route 53 Auto Naming Service(`servicediscovery.Service`). For more information, see [Service](https://docs.aws.amazon.com/Route53/latest/APIReference/API_autonaming_Service.html)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["capacity_provider_strategies"] = capacity_provider_strategies
        __props__["cluster"] = cluster
        __props__["deployment_controller"] = deployment_controller
        __props__["deployment_maximum_percent"] = deployment_maximum_percent
        __props__["deployment_minimum_healthy_percent"] = deployment_minimum_healthy_percent
        __props__["desired_count"] = desired_count
        __props__["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        __props__["force_new_deployment"] = force_new_deployment
        __props__["health_check_grace_period_seconds"] = health_check_grace_period_seconds
        __props__["iam_role"] = iam_role
        __props__["launch_type"] = launch_type
        __props__["load_balancers"] = load_balancers
        __props__["name"] = name
        __props__["network_configuration"] = network_configuration
        __props__["ordered_placement_strategies"] = ordered_placement_strategies
        __props__["placement_constraints"] = placement_constraints
        __props__["platform_version"] = platform_version
        __props__["propagate_tags"] = propagate_tags
        __props__["scheduling_strategy"] = scheduling_strategy
        __props__["service_registries"] = service_registries
        __props__["tags"] = tags
        __props__["task_definition"] = task_definition
        __props__["wait_for_steady_state"] = wait_for_steady_state
        return Service(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
