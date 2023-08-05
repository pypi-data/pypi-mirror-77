# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetPublicIPResult:
    """
    A collection of values returned by getPublicIP.
    """
    def __init__(__self__, allocation_method=None, domain_name_label=None, fqdn=None, id=None, idle_timeout_in_minutes=None, ip_address=None, ip_version=None, location=None, name=None, resource_group_name=None, reverse_fqdn=None, sku=None, tags=None, zones=None):
        if allocation_method and not isinstance(allocation_method, str):
            raise TypeError("Expected argument 'allocation_method' to be a str")
        __self__.allocation_method = allocation_method
        if domain_name_label and not isinstance(domain_name_label, str):
            raise TypeError("Expected argument 'domain_name_label' to be a str")
        __self__.domain_name_label = domain_name_label
        """
        The label for the Domain Name.
        """
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        __self__.fqdn = fqdn
        """
        Fully qualified domain name of the A DNS record associated with the public IP. This is the concatenation of the domainNameLabel and the regionalized DNS zone.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if idle_timeout_in_minutes and not isinstance(idle_timeout_in_minutes, float):
            raise TypeError("Expected argument 'idle_timeout_in_minutes' to be a float")
        __self__.idle_timeout_in_minutes = idle_timeout_in_minutes
        """
        Specifies the timeout for the TCP idle connection.
        """
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        __self__.ip_address = ip_address
        """
        The IP address value that was allocated.
        """
        if ip_version and not isinstance(ip_version, str):
            raise TypeError("Expected argument 'ip_version' to be a str")
        __self__.ip_version = ip_version
        """
        The IP version being used, for example `IPv4` or `IPv6`.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if reverse_fqdn and not isinstance(reverse_fqdn, str):
            raise TypeError("Expected argument 'reverse_fqdn' to be a str")
        __self__.reverse_fqdn = reverse_fqdn
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        __self__.sku = sku
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags to assigned to the resource.
        """
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        __self__.zones = zones
class AwaitableGetPublicIPResult(GetPublicIPResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicIPResult(
            allocation_method=self.allocation_method,
            domain_name_label=self.domain_name_label,
            fqdn=self.fqdn,
            id=self.id,
            idle_timeout_in_minutes=self.idle_timeout_in_minutes,
            ip_address=self.ip_address,
            ip_version=self.ip_version,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            reverse_fqdn=self.reverse_fqdn,
            sku=self.sku,
            tags=self.tags,
            zones=self.zones)

def get_public_ip(name=None,resource_group_name=None,tags=None,zones=None,opts=None):
    """
    Use this data source to access information about an existing Public IP Address.

    ## Example Usage
    ### Reference An Existing)

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_public_ip(name="name_of_public_ip",
        resource_group_name="name_of_resource_group")
    pulumi.export("domainNameLabel", example.domain_name_label)
    pulumi.export("publicIpAddress", example.ip_address)
    ```
    ### Retrieve The Dynamic Public IP Of A New VM)

    ```python
    import pulumi
    import pulumi_azure as azure

    example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US 2")
    example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
        address_spaces=["10.0.0.0/16"],
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name)
    example_subnet = azure.network.Subnet("exampleSubnet",
        resource_group_name=example_resource_group.name,
        virtual_network_name=example_virtual_network.name,
        address_prefix="10.0.2.0/24")
    example_public_ip = azure.network.PublicIp("examplePublicIp",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        allocation_method="Dynamic",
        idle_timeout_in_minutes=30,
        tags={
            "environment": "test",
        })
    example_network_interface = azure.network.NetworkInterface("exampleNetworkInterface",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        ip_configurations=[{
            "name": "testconfiguration1",
            "subnet_id": example_subnet.id,
            "privateIpAddressAllocation": "Static",
            "private_ip_address": "10.0.2.5",
            "public_ip_address_id": example_public_ip.id,
        }])
    example_virtual_machine = azure.compute.VirtualMachine("exampleVirtualMachine",
        location=example_resource_group.location,
        resource_group_name=example_resource_group.name,
        network_interface_ids=[example_network_interface.id])
    # ...
    example_public_ip = pulumi.Output.all(example_public_ip.name, example_virtual_machine.resource_group_name).apply(lambda name, resource_group_name: azure.network.get_public_ip(name=name,
        resource_group_name=resource_group_name))
    pulumi.export("publicIpAddress", example_public_ip.ip_address)
    ```


    :param str name: Specifies the name of the public IP address.
    :param str resource_group_name: Specifies the name of the resource group.
    :param dict tags: A mapping of tags to assigned to the resource.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tags'] = tags
    __args__['zones'] = zones
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:network/getPublicIP:getPublicIP', __args__, opts=opts).value

    return AwaitableGetPublicIPResult(
        allocation_method=__ret__.get('allocationMethod'),
        domain_name_label=__ret__.get('domainNameLabel'),
        fqdn=__ret__.get('fqdn'),
        id=__ret__.get('id'),
        idle_timeout_in_minutes=__ret__.get('idleTimeoutInMinutes'),
        ip_address=__ret__.get('ipAddress'),
        ip_version=__ret__.get('ipVersion'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        reverse_fqdn=__ret__.get('reverseFqdn'),
        sku=__ret__.get('sku'),
        tags=__ret__.get('tags'),
        zones=__ret__.get('zones'))
