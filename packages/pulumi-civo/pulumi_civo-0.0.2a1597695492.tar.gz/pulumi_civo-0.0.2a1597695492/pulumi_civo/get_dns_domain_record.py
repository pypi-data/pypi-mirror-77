# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import _utilities, _tables


class GetDnsDomainRecordResult:
    """
    A collection of values returned by getDnsDomainRecord.
    """
    def __init__(__self__, account_id=None, created_at=None, domain_id=None, id=None, name=None, priority=None, ttl=None, type=None, updated_at=None, value=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        __self__.account_id = account_id
        """
        The id account of the domain.
        """
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        __self__.created_at = created_at
        """
        The date when it was created in UTC format
        """
        if domain_id and not isinstance(domain_id, str):
            raise TypeError("Expected argument 'domain_id' to be a str")
        __self__.domain_id = domain_id
        """
        The id of the domain
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The portion before the domain name (e.g. www) or an @ for the apex/root domain (you cannot use an A record with an amex/root domain)
        """
        if priority and not isinstance(priority, float):
            raise TypeError("Expected argument 'priority' to be a float")
        __self__.priority = priority
        """
        The priority of the record.
        """
        if ttl and not isinstance(ttl, float):
            raise TypeError("Expected argument 'ttl' to be a float")
        __self__.ttl = ttl
        """
        How long caching DNS servers should cache this record.
        """
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        __self__.type = type
        """
        The choice of record type from a, cname, mx or txt
        """
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        __self__.updated_at = updated_at
        """
        The date when it was updated in UTC format
        """
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        __self__.value = value
        """
        The IP address (A or MX), hostname (CNAME or MX) or text value (TXT) to serve for this record
        """


class AwaitableGetDnsDomainRecordResult(GetDnsDomainRecordResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDnsDomainRecordResult(
            account_id=self.account_id,
            created_at=self.created_at,
            domain_id=self.domain_id,
            id=self.id,
            name=self.name,
            priority=self.priority,
            ttl=self.ttl,
            type=self.type,
            updated_at=self.updated_at,
            value=self.value)


def get_dns_domain_record(domain_id=None, name=None, opts=None):
    """
    Use this data source to access information about an existing resource.

    :param str domain_id: The domain id of the record.
    :param str name: The name of the record.
    """
    __args__ = dict()
    __args__['domainId'] = domain_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('civo:index/getDnsDomainRecord:getDnsDomainRecord', __args__, opts=opts).value

    return AwaitableGetDnsDomainRecordResult(
        account_id=__ret__.get('accountId'),
        created_at=__ret__.get('createdAt'),
        domain_id=__ret__.get('domainId'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        priority=__ret__.get('priority'),
        ttl=__ret__.get('ttl'),
        type=__ret__.get('type'),
        updated_at=__ret__.get('updatedAt'),
        value=__ret__.get('value'))
