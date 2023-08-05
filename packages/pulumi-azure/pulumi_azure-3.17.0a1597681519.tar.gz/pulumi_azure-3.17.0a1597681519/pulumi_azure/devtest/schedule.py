# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class Schedule(pulumi.CustomResource):
    daily_recurrence: pulumi.Output[dict]
    hourly_recurrence: pulumi.Output[dict]
    lab_name: pulumi.Output[str]
    """
    The name of the dev test lab. Changing this forces a new resource to be created.
    """
    location: pulumi.Output[str]
    """
    The location where the schedule is created. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    The name of the dev test lab schedule. Valid value for name depends on the `task_type`. For instance for task_type `LabVmsStartupTask` the name needs to be `LabVmAutoStart`.
    """
    notification_settings: pulumi.Output[dict]
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the dev test lab schedule. Changing this forces a new resource to be created.
    """
    status: pulumi.Output[str]
    """
    The status of this schedule. Possible values are `Enabled` and `Disabled`. Defaults to `Disabled`.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    task_type: pulumi.Output[str]
    """
    The task type of the schedule. Possible values include `LabVmsShutdownTask` and `LabVmAutoStart`.
    """
    time_zone_id: pulumi.Output[str]
    """
    The time zone ID (e.g. Pacific Standard time).
    """
    weekly_recurrence: pulumi.Output[dict]
    def __init__(__self__, resource_name, opts=None, daily_recurrence=None, hourly_recurrence=None, lab_name=None, location=None, name=None, notification_settings=None, resource_group_name=None, status=None, tags=None, task_type=None, time_zone_id=None, weekly_recurrence=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages automated startup and shutdown schedules for Azure Dev Test Lab.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_lab = azure.devtest.Lab("exampleLab",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name)
        example_schedule = azure.devtest.Schedule("exampleSchedule",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            lab_name=example_lab.name,
            weekly_recurrence={
                "time": "1100",
                "week_days": [
                    "Monday",
                    "Tuesday",
                ],
            },
            time_zone_id="Pacific Standard Time",
            task_type="LabVmsStartupTask",
            notification_settings={},
            tags={
                "environment": "Production",
            })
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] lab_name: The name of the dev test lab. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The location where the schedule is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the dev test lab schedule. Valid value for name depends on the `task_type`. For instance for task_type `LabVmsStartupTask` the name needs to be `LabVmAutoStart`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the dev test lab schedule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The status of this schedule. Possible values are `Enabled` and `Disabled`. Defaults to `Disabled`.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] task_type: The task type of the schedule. Possible values include `LabVmsShutdownTask` and `LabVmAutoStart`.
        :param pulumi.Input[str] time_zone_id: The time zone ID (e.g. Pacific Standard time).

        The **daily_recurrence** object supports the following:

          * `time` (`pulumi.Input[str]`) - The time each day when the schedule takes effect.

        The **hourly_recurrence** object supports the following:

          * `minute` (`pulumi.Input[float]`)

        The **notification_settings** object supports the following:

          * `status` (`pulumi.Input[str]`) - The status of the notification. Possible values are `Enabled` and `Disabled`. Defaults to `Disabled`
          * `timeInMinutes` (`pulumi.Input[float]`) - Time in minutes before event at which notification will be sent.
          * `webhookUrl` (`pulumi.Input[str]`) - The webhook URL to which the notification will be sent.

        The **weekly_recurrence** object supports the following:

          * `time` (`pulumi.Input[str]`) - The time when the schedule takes effect.
          * `week_days` (`pulumi.Input[list]`) - A list of days that this schedule takes effect . Possible values include `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday` and `Sunday`.
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
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['daily_recurrence'] = daily_recurrence
            __props__['hourly_recurrence'] = hourly_recurrence
            if lab_name is None:
                raise TypeError("Missing required property 'lab_name'")
            __props__['lab_name'] = lab_name
            __props__['location'] = location
            __props__['name'] = name
            if notification_settings is None:
                raise TypeError("Missing required property 'notification_settings'")
            __props__['notification_settings'] = notification_settings
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['status'] = status
            __props__['tags'] = tags
            if task_type is None:
                raise TypeError("Missing required property 'task_type'")
            __props__['task_type'] = task_type
            if time_zone_id is None:
                raise TypeError("Missing required property 'time_zone_id'")
            __props__['time_zone_id'] = time_zone_id
            __props__['weekly_recurrence'] = weekly_recurrence
        super(Schedule, __self__).__init__(
            'azure:devtest/schedule:Schedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, daily_recurrence=None, hourly_recurrence=None, lab_name=None, location=None, name=None, notification_settings=None, resource_group_name=None, status=None, tags=None, task_type=None, time_zone_id=None, weekly_recurrence=None):
        """
        Get an existing Schedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] lab_name: The name of the dev test lab. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: The location where the schedule is created. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the dev test lab schedule. Valid value for name depends on the `task_type`. For instance for task_type `LabVmsStartupTask` the name needs to be `LabVmAutoStart`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the dev test lab schedule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] status: The status of this schedule. Possible values are `Enabled` and `Disabled`. Defaults to `Disabled`.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] task_type: The task type of the schedule. Possible values include `LabVmsShutdownTask` and `LabVmAutoStart`.
        :param pulumi.Input[str] time_zone_id: The time zone ID (e.g. Pacific Standard time).

        The **daily_recurrence** object supports the following:

          * `time` (`pulumi.Input[str]`) - The time each day when the schedule takes effect.

        The **hourly_recurrence** object supports the following:

          * `minute` (`pulumi.Input[float]`)

        The **notification_settings** object supports the following:

          * `status` (`pulumi.Input[str]`) - The status of the notification. Possible values are `Enabled` and `Disabled`. Defaults to `Disabled`
          * `timeInMinutes` (`pulumi.Input[float]`) - Time in minutes before event at which notification will be sent.
          * `webhookUrl` (`pulumi.Input[str]`) - The webhook URL to which the notification will be sent.

        The **weekly_recurrence** object supports the following:

          * `time` (`pulumi.Input[str]`) - The time when the schedule takes effect.
          * `week_days` (`pulumi.Input[list]`) - A list of days that this schedule takes effect . Possible values include `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday` and `Sunday`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["daily_recurrence"] = daily_recurrence
        __props__["hourly_recurrence"] = hourly_recurrence
        __props__["lab_name"] = lab_name
        __props__["location"] = location
        __props__["name"] = name
        __props__["notification_settings"] = notification_settings
        __props__["resource_group_name"] = resource_group_name
        __props__["status"] = status
        __props__["tags"] = tags
        __props__["task_type"] = task_type
        __props__["time_zone_id"] = time_zone_id
        __props__["weekly_recurrence"] = weekly_recurrence
        return Schedule(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
