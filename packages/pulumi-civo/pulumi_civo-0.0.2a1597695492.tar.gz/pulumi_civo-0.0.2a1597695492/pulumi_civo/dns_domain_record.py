# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import _utilities, _tables


class DnsDomainRecord(pulumi.CustomResource):
    account_id: pulumi.Output[str]
    """
    The id account of the domain
    """
    created_at: pulumi.Output[str]
    """
    The date when it was created in UTC format
    """
    domain_id: pulumi.Output[str]
    """
    The id of the domain
    """
    name: pulumi.Output[str]
    """
    The portion before the domain name (e.g. www) or an @ for the apex/root domain (you cannot use an A record with an amex/root domain)
    """
    priority: pulumi.Output[float]
    """
    Useful for MX records only, the priority mail should be attempted it (defaults to 10)
    """
    ttl: pulumi.Output[float]
    """
    How long caching DNS servers should cache this record for, in seconds (the minimum is 600 and the default if unspecified is 600)
    """
    type: pulumi.Output[str]
    """
    The choice of record type from a, cname, mx or txt
    """
    updated_at: pulumi.Output[str]
    """
    The date when it was updated in UTC format
    """
    value: pulumi.Output[str]
    """
    The IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
    """
    def __init__(__self__, resource_name, opts=None, domain_id=None, name=None, priority=None, ttl=None, type=None, value=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Civo dns domain record resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_civo as civo

        # Create a new domain record
        www = civo.DnsDomainRecord("www",
            domain_id=civo_dns_domain_name["main"]["id"],
            type="a",
            value=civo_instance["foo"]["public_ip"],
            ttl=600,
            opts=ResourceOptions(depends_on=[
                    civo_dns_domain_name["main"],
                    civo_instance["foo"],
                ]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_id: The id of the domain
        :param pulumi.Input[str] name: The portion before the domain name (e.g. www) or an @ for the apex/root domain (you cannot use an A record with an amex/root domain)
        :param pulumi.Input[float] priority: Useful for MX records only, the priority mail should be attempted it (defaults to 10)
        :param pulumi.Input[float] ttl: How long caching DNS servers should cache this record for, in seconds (the minimum is 600 and the default if unspecified is 600)
        :param pulumi.Input[str] type: The choice of record type from a, cname, mx or txt
        :param pulumi.Input[str] value: The IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
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

            if domain_id is None:
                raise TypeError("Missing required property 'domain_id'")
            __props__['domain_id'] = domain_id
            __props__['name'] = name
            __props__['priority'] = priority
            if ttl is None:
                raise TypeError("Missing required property 'ttl'")
            __props__['ttl'] = ttl
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            if value is None:
                raise TypeError("Missing required property 'value'")
            __props__['value'] = value
            __props__['account_id'] = None
            __props__['created_at'] = None
            __props__['updated_at'] = None
        super(DnsDomainRecord, __self__).__init__(
            'civo:index/dnsDomainRecord:DnsDomainRecord',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, account_id=None, created_at=None, domain_id=None, name=None, priority=None, ttl=None, type=None, updated_at=None, value=None):
        """
        Get an existing DnsDomainRecord resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The id account of the domain
        :param pulumi.Input[str] created_at: The date when it was created in UTC format
        :param pulumi.Input[str] domain_id: The id of the domain
        :param pulumi.Input[str] name: The portion before the domain name (e.g. www) or an @ for the apex/root domain (you cannot use an A record with an amex/root domain)
        :param pulumi.Input[float] priority: Useful for MX records only, the priority mail should be attempted it (defaults to 10)
        :param pulumi.Input[float] ttl: How long caching DNS servers should cache this record for, in seconds (the minimum is 600 and the default if unspecified is 600)
        :param pulumi.Input[str] type: The choice of record type from a, cname, mx or txt
        :param pulumi.Input[str] updated_at: The date when it was updated in UTC format
        :param pulumi.Input[str] value: The IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["account_id"] = account_id
        __props__["created_at"] = created_at
        __props__["domain_id"] = domain_id
        __props__["name"] = name
        __props__["priority"] = priority
        __props__["ttl"] = ttl
        __props__["type"] = type
        __props__["updated_at"] = updated_at
        __props__["value"] = value
        return DnsDomainRecord(resource_name, opts=opts, __props__=__props__)

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop
