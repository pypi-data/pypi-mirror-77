# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables


class FirewallPolicy(pulumi.CustomResource):
    custom_block_response_body: pulumi.Output[str]
    """
    If a `custom_rule` block's action type is `block`, this is the response body. The body must be specified in base64 encoding.
    """
    custom_block_response_status_code: pulumi.Output[float]
    """
    If a `custom_rule` block's action type is `block`, this is the response status code. Possible values are `200`, `403`, `405`, `406`, or `429`.
    """
    custom_rules: pulumi.Output[list]
    """
    One or more `custom_rule` blocks as defined below.

      * `action` (`str`) - The action to perform when the rule is matched. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
      * `enabled` (`bool`) - Is the rule is enabled or disabled? Defaults to `true`.
      * `matchConditions` (`list`) - One or more `match_condition` block defined below.
        * `matchValues` (`list`) - Up to `100` possible values to match.
        * `matchVariable` (`str`) - The request variable to compare with. Possible values are `Cookies`, `PostArgs`, `QueryString`, `RemoteAddr`, `RequestBody`, `RequestHeader`, `RequestMethod`, or `RequestUri`.
        * `negationCondition` (`bool`) - Should the result of the condition be negated.
        * `operator` (`str`) - Comparison type to use for matching with the variable value. Possible values are `Any`, `BeginsWith`, `Contains`, `EndsWith`, `Equal`, `GeoMatch`, `GreaterThan`, `GreaterThanOrEqual`, `IPMatch`, `LessThan`, `LessThanOrEqual` or `RegEx`.
        * `selector` (`str`) - Match against a specific key if the `match_variable` is `QueryString`, `PostArgs`, `RequestHeader` or `Cookies`.
        * `transforms` (`list`) - Up to `5` transforms to apply. Possible values are `Lowercase`, `RemoveNulls`, `Trim`, `Uppercase`, `URLDecode` or`URLEncode`.

      * `name` (`str`) - Gets name of the resource that is unique within a policy. This name can be used to access the resource.
      * `priority` (`float`) - The priority of the rule. Rules with a lower value will be evaluated before rules with a higher value. Defaults to `1`.
      * `rateLimitDurationInMinutes` (`float`) - The rate limit duration in minutes. Defaults to `1`.
      * `rateLimitThreshold` (`float`) - The rate limit threshold. Defaults to `10`.
      * `type` (`str`) - The type of rule. Possible values are `MatchRule` or `RateLimitRule`.
    """
    enabled: pulumi.Output[bool]
    """
    Is the policy a enabled state or disabled state. Defaults to `true`.
    """
    frontend_endpoint_ids: pulumi.Output[list]
    """
    the Frontend Endpoints associated with this Front Door Web Application Firewall policy.
    """
    location: pulumi.Output[str]
    """
    Resource location.
    """
    managed_rules: pulumi.Output[list]
    """
    One or more `managed_rule` blocks as defined below.

      * `exclusions` (`list`) - One or more `exclusion` blocks as defined below.
        * `matchVariable` (`str`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
        * `operator` (`str`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
        * `selector` (`str`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

      * `overrides` (`list`) - One or more `override` blocks as defined below.
        * `exclusions` (`list`) - One or more `exclusion` blocks as defined below.
          * `matchVariable` (`str`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
          * `operator` (`str`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
          * `selector` (`str`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

        * `ruleGroupName` (`str`) - The managed rule group to override.
        * `rules` (`list`) - One or more `rule` blocks as defined below. If none are specified, all of the rules in the group will be disabled.
          * `action` (`str`) - The action to be applied when the rule matches. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
          * `enabled` (`bool`) - Is the managed rule override enabled or disabled. Defaults to `false`
          * `exclusions` (`list`) - One or more `exclusion` blocks as defined below.
            * `matchVariable` (`str`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
            * `operator` (`str`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
            * `selector` (`str`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

          * `rule_id` (`str`) - Identifier for the managed rule.

      * `type` (`str`) - The name of the managed rule to use with this resource.
      * `version` (`str`) - The version on the managed rule to use with this resource.
    """
    mode: pulumi.Output[str]
    """
    The firewall policy mode. Possible values are `Detection`, `Prevention` and defaults to `Prevention`.
    """
    name: pulumi.Output[str]
    """
    The name of the policy. Changing this forces a new resource to be created.
    """
    redirect_url: pulumi.Output[str]
    """
    If action type is redirect, this field represents redirect URL for the client.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the Web Application Firewall Policy.
    """
    def __init__(__self__, resource_name, opts=None, custom_block_response_body=None, custom_block_response_status_code=None, custom_rules=None, enabled=None, managed_rules=None, mode=None, name=None, redirect_url=None, resource_group_name=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Azure Front Door Web Application Firewall Policy instance.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US 2")
        example_firewall_policy = azure.frontdoor.FirewallPolicy("exampleFirewallPolicy",
            resource_group_name=example_resource_group.name,
            enabled=True,
            mode="Prevention",
            redirect_url="https://www.contoso.com",
            custom_block_response_status_code=403,
            custom_block_response_body="PGh0bWw+CjxoZWFkZXI+PHRpdGxlPkhlbGxvPC90aXRsZT48L2hlYWRlcj4KPGJvZHk+CkhlbGxvIHdvcmxkCjwvYm9keT4KPC9odG1sPg==",
            custom_rules=[
                {
                    "name": "Rule1",
                    "enabled": True,
                    "priority": 1,
                    "rateLimitDurationInMinutes": 1,
                    "rateLimitThreshold": 10,
                    "type": "MatchRule",
                    "action": "Block",
                    "matchConditions": [{
                        "matchVariable": "RemoteAddr",
                        "operator": "IPMatch",
                        "negationCondition": False,
                        "matchValues": [
                            "192.168.1.0/24",
                            "10.0.0.0/24",
                        ],
                    }],
                },
                {
                    "name": "Rule2",
                    "enabled": True,
                    "priority": 2,
                    "rateLimitDurationInMinutes": 1,
                    "rateLimitThreshold": 10,
                    "type": "MatchRule",
                    "action": "Block",
                    "matchConditions": [
                        {
                            "matchVariable": "RemoteAddr",
                            "operator": "IPMatch",
                            "negationCondition": False,
                            "matchValues": ["192.168.1.0/24"],
                        },
                        {
                            "matchVariable": "RequestHeader",
                            "selector": "UserAgent",
                            "operator": "Contains",
                            "negationCondition": False,
                            "matchValues": ["windows"],
                            "transforms": [
                                "Lowercase",
                                "Trim",
                            ],
                        },
                    ],
                },
            ],
            managed_rules=[
                {
                    "type": "DefaultRuleSet",
                    "version": "1.0",
                    "exclusions": [{
                        "matchVariable": "QueryStringArgNames",
                        "operator": "Equals",
                        "selector": "not_suspicious",
                    }],
                    "overrides": [
                        {
                            "ruleGroupName": "PHP",
                            "rules": [{
                                "rule_id": "933100",
                                "enabled": False,
                                "action": "Block",
                            }],
                        },
                        {
                            "ruleGroupName": "SQLI",
                            "exclusions": [{
                                "matchVariable": "QueryStringArgNames",
                                "operator": "Equals",
                                "selector": "really_not_suspicious",
                            }],
                            "rules": [{
                                "rule_id": "942200",
                                "action": "Block",
                                "exclusions": [{
                                    "matchVariable": "QueryStringArgNames",
                                    "operator": "Equals",
                                    "selector": "innocent",
                                }],
                            }],
                        },
                    ],
                },
                {
                    "type": "Microsoft_BotManagerRuleSet",
                    "version": "1.0",
                },
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_block_response_body: If a `custom_rule` block's action type is `block`, this is the response body. The body must be specified in base64 encoding.
        :param pulumi.Input[float] custom_block_response_status_code: If a `custom_rule` block's action type is `block`, this is the response status code. Possible values are `200`, `403`, `405`, `406`, or `429`.
        :param pulumi.Input[list] custom_rules: One or more `custom_rule` blocks as defined below.
        :param pulumi.Input[bool] enabled: Is the policy a enabled state or disabled state. Defaults to `true`.
        :param pulumi.Input[list] managed_rules: One or more `managed_rule` blocks as defined below.
        :param pulumi.Input[str] mode: The firewall policy mode. Possible values are `Detection`, `Prevention` and defaults to `Prevention`.
        :param pulumi.Input[str] name: The name of the policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] redirect_url: If action type is redirect, this field represents redirect URL for the client.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the Web Application Firewall Policy.

        The **custom_rules** object supports the following:

          * `action` (`pulumi.Input[str]`) - The action to perform when the rule is matched. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
          * `enabled` (`pulumi.Input[bool]`) - Is the rule is enabled or disabled? Defaults to `true`.
          * `matchConditions` (`pulumi.Input[list]`) - One or more `match_condition` block defined below.
            * `matchValues` (`pulumi.Input[list]`) - Up to `100` possible values to match.
            * `matchVariable` (`pulumi.Input[str]`) - The request variable to compare with. Possible values are `Cookies`, `PostArgs`, `QueryString`, `RemoteAddr`, `RequestBody`, `RequestHeader`, `RequestMethod`, or `RequestUri`.
            * `negationCondition` (`pulumi.Input[bool]`) - Should the result of the condition be negated.
            * `operator` (`pulumi.Input[str]`) - Comparison type to use for matching with the variable value. Possible values are `Any`, `BeginsWith`, `Contains`, `EndsWith`, `Equal`, `GeoMatch`, `GreaterThan`, `GreaterThanOrEqual`, `IPMatch`, `LessThan`, `LessThanOrEqual` or `RegEx`.
            * `selector` (`pulumi.Input[str]`) - Match against a specific key if the `match_variable` is `QueryString`, `PostArgs`, `RequestHeader` or `Cookies`.
            * `transforms` (`pulumi.Input[list]`) - Up to `5` transforms to apply. Possible values are `Lowercase`, `RemoveNulls`, `Trim`, `Uppercase`, `URLDecode` or`URLEncode`.

          * `name` (`pulumi.Input[str]`) - Gets name of the resource that is unique within a policy. This name can be used to access the resource.
          * `priority` (`pulumi.Input[float]`) - The priority of the rule. Rules with a lower value will be evaluated before rules with a higher value. Defaults to `1`.
          * `rateLimitDurationInMinutes` (`pulumi.Input[float]`) - The rate limit duration in minutes. Defaults to `1`.
          * `rateLimitThreshold` (`pulumi.Input[float]`) - The rate limit threshold. Defaults to `10`.
          * `type` (`pulumi.Input[str]`) - The type of rule. Possible values are `MatchRule` or `RateLimitRule`.

        The **managed_rules** object supports the following:

          * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
            * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
            * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
            * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

          * `overrides` (`pulumi.Input[list]`) - One or more `override` blocks as defined below.
            * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
              * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
              * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
              * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

            * `ruleGroupName` (`pulumi.Input[str]`) - The managed rule group to override.
            * `rules` (`pulumi.Input[list]`) - One or more `rule` blocks as defined below. If none are specified, all of the rules in the group will be disabled.
              * `action` (`pulumi.Input[str]`) - The action to be applied when the rule matches. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
              * `enabled` (`pulumi.Input[bool]`) - Is the managed rule override enabled or disabled. Defaults to `false`
              * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
                * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
                * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
                * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

              * `rule_id` (`pulumi.Input[str]`) - Identifier for the managed rule.

          * `type` (`pulumi.Input[str]`) - The name of the managed rule to use with this resource.
          * `version` (`pulumi.Input[str]`) - The version on the managed rule to use with this resource.
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

            __props__['custom_block_response_body'] = custom_block_response_body
            __props__['custom_block_response_status_code'] = custom_block_response_status_code
            __props__['custom_rules'] = custom_rules
            __props__['enabled'] = enabled
            __props__['managed_rules'] = managed_rules
            __props__['mode'] = mode
            __props__['name'] = name
            __props__['redirect_url'] = redirect_url
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['frontend_endpoint_ids'] = None
            __props__['location'] = None
        super(FirewallPolicy, __self__).__init__(
            'azure:frontdoor/firewallPolicy:FirewallPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, custom_block_response_body=None, custom_block_response_status_code=None, custom_rules=None, enabled=None, frontend_endpoint_ids=None, location=None, managed_rules=None, mode=None, name=None, redirect_url=None, resource_group_name=None, tags=None):
        """
        Get an existing FirewallPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_block_response_body: If a `custom_rule` block's action type is `block`, this is the response body. The body must be specified in base64 encoding.
        :param pulumi.Input[float] custom_block_response_status_code: If a `custom_rule` block's action type is `block`, this is the response status code. Possible values are `200`, `403`, `405`, `406`, or `429`.
        :param pulumi.Input[list] custom_rules: One or more `custom_rule` blocks as defined below.
        :param pulumi.Input[bool] enabled: Is the policy a enabled state or disabled state. Defaults to `true`.
        :param pulumi.Input[list] frontend_endpoint_ids: the Frontend Endpoints associated with this Front Door Web Application Firewall policy.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[list] managed_rules: One or more `managed_rule` blocks as defined below.
        :param pulumi.Input[str] mode: The firewall policy mode. Possible values are `Detection`, `Prevention` and defaults to `Prevention`.
        :param pulumi.Input[str] name: The name of the policy. Changing this forces a new resource to be created.
        :param pulumi.Input[str] redirect_url: If action type is redirect, this field represents redirect URL for the client.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the Web Application Firewall Policy.

        The **custom_rules** object supports the following:

          * `action` (`pulumi.Input[str]`) - The action to perform when the rule is matched. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
          * `enabled` (`pulumi.Input[bool]`) - Is the rule is enabled or disabled? Defaults to `true`.
          * `matchConditions` (`pulumi.Input[list]`) - One or more `match_condition` block defined below.
            * `matchValues` (`pulumi.Input[list]`) - Up to `100` possible values to match.
            * `matchVariable` (`pulumi.Input[str]`) - The request variable to compare with. Possible values are `Cookies`, `PostArgs`, `QueryString`, `RemoteAddr`, `RequestBody`, `RequestHeader`, `RequestMethod`, or `RequestUri`.
            * `negationCondition` (`pulumi.Input[bool]`) - Should the result of the condition be negated.
            * `operator` (`pulumi.Input[str]`) - Comparison type to use for matching with the variable value. Possible values are `Any`, `BeginsWith`, `Contains`, `EndsWith`, `Equal`, `GeoMatch`, `GreaterThan`, `GreaterThanOrEqual`, `IPMatch`, `LessThan`, `LessThanOrEqual` or `RegEx`.
            * `selector` (`pulumi.Input[str]`) - Match against a specific key if the `match_variable` is `QueryString`, `PostArgs`, `RequestHeader` or `Cookies`.
            * `transforms` (`pulumi.Input[list]`) - Up to `5` transforms to apply. Possible values are `Lowercase`, `RemoveNulls`, `Trim`, `Uppercase`, `URLDecode` or`URLEncode`.

          * `name` (`pulumi.Input[str]`) - Gets name of the resource that is unique within a policy. This name can be used to access the resource.
          * `priority` (`pulumi.Input[float]`) - The priority of the rule. Rules with a lower value will be evaluated before rules with a higher value. Defaults to `1`.
          * `rateLimitDurationInMinutes` (`pulumi.Input[float]`) - The rate limit duration in minutes. Defaults to `1`.
          * `rateLimitThreshold` (`pulumi.Input[float]`) - The rate limit threshold. Defaults to `10`.
          * `type` (`pulumi.Input[str]`) - The type of rule. Possible values are `MatchRule` or `RateLimitRule`.

        The **managed_rules** object supports the following:

          * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
            * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
            * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
            * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

          * `overrides` (`pulumi.Input[list]`) - One or more `override` blocks as defined below.
            * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
              * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
              * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
              * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

            * `ruleGroupName` (`pulumi.Input[str]`) - The managed rule group to override.
            * `rules` (`pulumi.Input[list]`) - One or more `rule` blocks as defined below. If none are specified, all of the rules in the group will be disabled.
              * `action` (`pulumi.Input[str]`) - The action to be applied when the rule matches. Possible values are `Allow`, `Block`, `Log`, or `Redirect`.
              * `enabled` (`pulumi.Input[bool]`) - Is the managed rule override enabled or disabled. Defaults to `false`
              * `exclusions` (`pulumi.Input[list]`) - One or more `exclusion` blocks as defined below.
                * `matchVariable` (`pulumi.Input[str]`) - The variable type to be excluded. Possible values are `QueryStringArgNames`, `RequestBodyPostArgNames`, `RequestCookieNames`, `RequestHeaderNames`.
                * `operator` (`pulumi.Input[str]`) - Comparison operator to apply to the selector when specifying which elements in the collection this exclusion applies to. Possible values are: `Equals`, `Contains`, `StartsWith`, `EndsWith`, `EqualsAny`.
                * `selector` (`pulumi.Input[str]`) - Selector for the value in the `match_variable` attribute this exclusion applies to.

              * `rule_id` (`pulumi.Input[str]`) - Identifier for the managed rule.

          * `type` (`pulumi.Input[str]`) - The name of the managed rule to use with this resource.
          * `version` (`pulumi.Input[str]`) - The version on the managed rule to use with this resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["custom_block_response_body"] = custom_block_response_body
        __props__["custom_block_response_status_code"] = custom_block_response_status_code
        __props__["custom_rules"] = custom_rules
        __props__["enabled"] = enabled
        __props__["frontend_endpoint_ids"] = frontend_endpoint_ids
        __props__["location"] = location
        __props__["managed_rules"] = managed_rules
        __props__["mode"] = mode
        __props__["name"] = name
        __props__["redirect_url"] = redirect_url
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        return FirewallPolicy(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
