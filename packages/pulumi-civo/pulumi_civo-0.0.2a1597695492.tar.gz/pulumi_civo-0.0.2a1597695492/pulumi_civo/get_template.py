# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import _utilities, _tables


class GetTemplateResult:
    """
    A collection of values returned by getTemplate.
    """
    def __init__(__self__, filters=None, id=None, sorts=None, templates=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        __self__.filters = filters
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if sorts and not isinstance(sorts, list):
            raise TypeError("Expected argument 'sorts' to be a list")
        __self__.sorts = sorts
        if templates and not isinstance(templates, list):
            raise TypeError("Expected argument 'templates' to be a list")
        __self__.templates = templates


class AwaitableGetTemplateResult(GetTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTemplateResult(
            filters=self.filters,
            id=self.id,
            sorts=self.sorts,
            templates=self.templates)


def get_template(filters=None, sorts=None, opts=None):
    """
    Use this data source to access information about an existing resource.

    :param list filters: Filter the results.
           The `filter` block is documented below.
    :param list sorts: Sort the results.
           The `sort` block is documented below.

    The **filters** object supports the following:

      * `key` (`str`) - Filter the sizes by this key. This may be one of `code`,
        `name`.
      * `values` (`list`) - Only retrieves the template which keys has value that matches
        one of the values provided here.

    The **sorts** object supports the following:

      * `direction` (`str`) - The sort direction. This may be either `asc` or `desc`.
      * `key` (`str`) - Sort the sizes by this key. This may be one of `code`, 
        `name`.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['sorts'] = sorts
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('civo:index/getTemplate:getTemplate', __args__, opts=opts).value

    return AwaitableGetTemplateResult(
        filters=__ret__.get('filters'),
        id=__ret__.get('id'),
        sorts=__ret__.get('sorts'),
        templates=__ret__.get('templates'))
