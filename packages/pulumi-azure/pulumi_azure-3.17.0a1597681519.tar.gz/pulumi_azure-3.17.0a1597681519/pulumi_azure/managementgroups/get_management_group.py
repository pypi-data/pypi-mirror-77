# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

warnings.warn("azure.managementgroups.getManagementGroup has been deprecated in favor of azure.management.getGroup", DeprecationWarning)
class GetManagementGroupResult:
    """
    A collection of values returned by getManagementGroup.
    """
    def __init__(__self__, display_name=None, group_id=None, id=None, name=None, parent_management_group_id=None, subscription_ids=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        __self__.display_name = display_name
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        if group_id is not None:
            warnings.warn("Deprecated in favour of `name`", DeprecationWarning)
            pulumi.log.warn("group_id is deprecated: Deprecated in favour of `name`")

        __self__.group_id = group_id
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if parent_management_group_id and not isinstance(parent_management_group_id, str):
            raise TypeError("Expected argument 'parent_management_group_id' to be a str")
        __self__.parent_management_group_id = parent_management_group_id
        """
        The ID of any Parent Management Group.
        """
        if subscription_ids and not isinstance(subscription_ids, list):
            raise TypeError("Expected argument 'subscription_ids' to be a list")
        __self__.subscription_ids = subscription_ids
        """
        A list of Subscription IDs which are assigned to the Management Group.
        """
class AwaitableGetManagementGroupResult(GetManagementGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagementGroupResult(
            display_name=self.display_name,
            group_id=self.group_id,
            id=self.id,
            name=self.name,
            parent_management_group_id=self.parent_management_group_id,
            subscription_ids=self.subscription_ids)

def get_management_group(display_name=None,group_id=None,name=None,opts=None):
    """
    Use this data source to access information about an existing Management Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.management.get_group(name="00000000-0000-0000-0000-000000000000")
    pulumi.export("displayName", example.display_name)
    ```


    :param str display_name: Specifies the display name of this Management Group.
    :param str group_id: Specifies the name or UUID of this Management Group.
    :param str name: Specifies the name or UUID of this Management Group.
    """
    pulumi.log.warn("get_management_group is deprecated: azure.managementgroups.getManagementGroup has been deprecated in favor of azure.management.getGroup")
    __args__ = dict()


    __args__['displayName'] = display_name
    __args__['groupId'] = group_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:managementgroups/getManagementGroup:getManagementGroup', __args__, opts=opts).value

    return AwaitableGetManagementGroupResult(
        display_name=__ret__.get('displayName'),
        group_id=__ret__.get('groupId'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        parent_management_group_id=__ret__.get('parentManagementGroupId'),
        subscription_ids=__ret__.get('subscriptionIds'))
