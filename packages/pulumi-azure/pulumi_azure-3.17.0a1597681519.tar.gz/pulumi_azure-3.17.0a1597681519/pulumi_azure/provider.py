# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables


class Provider(pulumi.ProviderResource):
    def __init__(__self__, resource_name, opts=None, auxiliary_tenant_ids=None, client_certificate_password=None, client_certificate_path=None, client_id=None, client_secret=None, disable_correlation_request_id=None, disable_terraform_partner_id=None, environment=None, features=None, metadata_host=None, metadata_url=None, msi_endpoint=None, partner_id=None, skip_credentials_validation=None, skip_provider_registration=None, storage_use_azuread=None, subscription_id=None, tenant_id=None, use_msi=None, __props__=None, __name__=None, __opts__=None):
        """
        The provider type for the azurerm package. By default, resources use package-wide configuration
        settings, however an explicit `Provider` instance may be created and passed during resource
        construction to achieve fine-grained programmatic control over provider settings. See the
        [documentation](https://www.pulumi.com/docs/reference/programming-model/#providers) for more information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_certificate_password: The password associated with the Client Certificate. For use when authenticating as a Service Principal using a Client
               Certificate
        :param pulumi.Input[str] client_certificate_path: The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service
               Principal using a Client Certificate.
        :param pulumi.Input[str] client_id: The Client ID which should be used.
        :param pulumi.Input[str] client_secret: The Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret.
        :param pulumi.Input[bool] disable_correlation_request_id: This will disable the x-ms-correlation-request-id header.
        :param pulumi.Input[bool] disable_terraform_partner_id: This will disable the Terraform Partner ID which is used if a custom `partner_id` isn't specified.
        :param pulumi.Input[str] environment: The Cloud Environment which should be used. Possible values are public, usgovernment, german, and china. Defaults to
               public.
        :param pulumi.Input[str] metadata_host: The Hostname which should be used for the Azure Metadata Service.
        :param pulumi.Input[str] metadata_url: Deprecated - replaced by `metadata_host`.
        :param pulumi.Input[str] msi_endpoint: The path to a custom endpoint for Managed Service Identity - in most circumstances this should be detected
               automatically.
        :param pulumi.Input[str] partner_id: A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution.
        :param pulumi.Input[bool] skip_credentials_validation: This will cause the AzureRM Provider to skip verifying the credentials being used are valid.
        :param pulumi.Input[bool] skip_provider_registration: Should the AzureRM Provider skip registering all of the Resource Providers that it supports, if they're not already
               registered?
        :param pulumi.Input[bool] storage_use_azuread: Should the AzureRM Provider use AzureAD to access the Storage Data Plane API's?
        :param pulumi.Input[str] subscription_id: The Subscription ID which should be used.
        :param pulumi.Input[str] tenant_id: The Tenant ID which should be used.
        :param pulumi.Input[bool] use_msi: Allowed Managed Service Identity be used for Authentication.

        The **features** object supports the following:

          * `key_vault` (`pulumi.Input[dict]`)
            * `purgeSoftDeleteOnDestroy` (`pulumi.Input[bool]`)
            * `recoverSoftDeletedKeyVaults` (`pulumi.Input[bool]`)

          * `network` (`pulumi.Input[dict]`)
            * `relaxedLocking` (`pulumi.Input[bool]`)

          * `virtual_machine` (`pulumi.Input[dict]`)
            * `deleteOsDiskOnDeletion` (`pulumi.Input[bool]`)

          * `virtual_machine_scale_set` (`pulumi.Input[dict]`)
            * `rollInstancesWhenRequired` (`pulumi.Input[bool]`)
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

            __props__['auxiliary_tenant_ids'] = pulumi.Output.from_input(auxiliary_tenant_ids).apply(json.dumps) if auxiliary_tenant_ids is not None else None
            __props__['client_certificate_password'] = client_certificate_password
            __props__['client_certificate_path'] = client_certificate_path
            __props__['client_id'] = client_id
            __props__['client_secret'] = client_secret
            __props__['disable_correlation_request_id'] = pulumi.Output.from_input(disable_correlation_request_id).apply(json.dumps) if disable_correlation_request_id is not None else None
            __props__['disable_terraform_partner_id'] = pulumi.Output.from_input(disable_terraform_partner_id).apply(json.dumps) if disable_terraform_partner_id is not None else None
            if environment is None:
                environment = (utilities.get_env('AZURE_ENVIRONMENT', 'ARM_ENVIRONMENT') or 'public')
            __props__['environment'] = environment
            __props__['features'] = pulumi.Output.from_input(features).apply(json.dumps) if features is not None else None
            if metadata_host is None:
                metadata_host = (utilities.get_env('ARM_METADATA_HOSTNAME') or '')
            __props__['metadata_host'] = metadata_host
            if metadata_url is None:
                metadata_url = (utilities.get_env('ARM_METADATA_URL') or '')
            if metadata_url is not None:
                warnings.warn("use `metadata_host` instead", DeprecationWarning)
                pulumi.log.warn("metadata_url is deprecated: use `metadata_host` instead")
            __props__['metadata_url'] = metadata_url
            __props__['msi_endpoint'] = msi_endpoint
            __props__['partner_id'] = partner_id
            __props__['skip_credentials_validation'] = pulumi.Output.from_input(skip_credentials_validation).apply(json.dumps) if skip_credentials_validation is not None else None
            if skip_provider_registration is None:
                skip_provider_registration = (utilities.get_env_bool('ARM_SKIP_PROVIDER_REGISTRATION') or False)
            __props__['skip_provider_registration'] = pulumi.Output.from_input(skip_provider_registration).apply(json.dumps) if skip_provider_registration is not None else None
            if storage_use_azuread is None:
                storage_use_azuread = (utilities.get_env_bool('ARM_STORAGE_USE_AZUREAD') or False)
            __props__['storage_use_azuread'] = pulumi.Output.from_input(storage_use_azuread).apply(json.dumps) if storage_use_azuread is not None else None
            if subscription_id is None:
                subscription_id = (utilities.get_env('ARM_SUBSCRIPTION_ID') or '')
            __props__['subscription_id'] = subscription_id
            __props__['tenant_id'] = tenant_id
            __props__['use_msi'] = pulumi.Output.from_input(use_msi).apply(json.dumps) if use_msi is not None else None
        super(Provider, __self__).__init__(
            'azure',
            resource_name,
            __props__,
            opts)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
