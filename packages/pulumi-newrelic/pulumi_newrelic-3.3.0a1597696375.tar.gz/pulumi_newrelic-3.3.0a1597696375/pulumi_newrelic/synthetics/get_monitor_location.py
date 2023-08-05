# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetMonitorLocationResult:
    """
    A collection of values returned by getMonitorLocation.
    """
    def __init__(__self__, description=None, high_security_mode=None, id=None, label=None, name=None, private=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        A description of the Synthetics monitor location.
        """
        if high_security_mode and not isinstance(high_security_mode, bool):
            raise TypeError("Expected argument 'high_security_mode' to be a bool")
        __self__.high_security_mode = high_security_mode
        """
        Represents if high security mode is enabled for the location. A value of true means that high security mode is enabled, and a value of false means it is disabled.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        __self__.label = label
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The name of the Synthetics monitor location.
        """
        if private and not isinstance(private, bool):
            raise TypeError("Expected argument 'private' to be a bool")
        __self__.private = private
        """
        Represents if this location is a private location. A value of true means that the location is private, and a value of false means it is public.
        """


class AwaitableGetMonitorLocationResult(GetMonitorLocationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMonitorLocationResult(
            description=self.description,
            high_security_mode=self.high_security_mode,
            id=self.id,
            label=self.label,
            name=self.name,
            private=self.private)


def get_monitor_location(label=None, opts=None):
    """
    Use this data source to get information about a specific Synthetics monitor location in New Relic that already exists.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_newrelic as newrelic

    bar = newrelic.synthetics.get_monitor_location(label="My private location")
    foo = newrelic.synthetics.Monitor("foo",
        type="SIMPLE",
        frequency=5,
        status="ENABLED",
        locations=[bar.name],
        uri="https://example.com",
        validation_string="add example validation check here",
        verify_ssl=True)
    # Optional for type "SIMPLE" and "BROWSER"
    ```


    :param str label: The label of the Synthetics monitor location.
    """
    __args__ = dict()
    __args__['label'] = label
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('newrelic:synthetics/getMonitorLocation:getMonitorLocation', __args__, opts=opts).value

    return AwaitableGetMonitorLocationResult(
        description=__ret__.get('description'),
        high_security_mode=__ret__.get('highSecurityMode'),
        id=__ret__.get('id'),
        label=__ret__.get('label'),
        name=__ret__.get('name'),
        private=__ret__.get('private'))
