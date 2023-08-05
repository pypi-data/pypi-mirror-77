# coding: utf-8

"""
    VeeRoute.LSS Clustering

    VeeRoute.LSS Clustering API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_lss_clustering.configuration import Configuration


class Performer(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'key': 'str',
        'home_location': 'Location',
        'transport_type': 'TransportType',
        'cost_per_meter': 'float',
        'cost_per_minute': 'float',
        'limits': 'ClusterLimits'
    }

    attribute_map = {
        'key': 'key',
        'home_location': 'home_location',
        'transport_type': 'transport_type',
        'cost_per_meter': 'cost_per_meter',
        'cost_per_minute': 'cost_per_minute',
        'limits': 'limits'
    }

    def __init__(self, key=None, home_location=None, transport_type=None, cost_per_meter=0, cost_per_minute=0, limits=None, local_vars_configuration=None):  # noqa: E501
        """Performer - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._home_location = None
        self._transport_type = None
        self._cost_per_meter = None
        self._cost_per_minute = None
        self._limits = None
        self.discriminator = None

        self.key = key
        if home_location is not None:
            self.home_location = home_location
        self.transport_type = transport_type
        if cost_per_meter is not None:
            self.cost_per_meter = cost_per_meter
        if cost_per_minute is not None:
            self.cost_per_minute = cost_per_minute
        if limits is not None:
            self.limits = limits

    @property
    def key(self):
        """Gets the key of this Performer.  # noqa: E501

        Unique ID.  # noqa: E501

        :return: The key of this Performer.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Performer.

        Unique ID.  # noqa: E501

        :param key: The key of this Performer.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and key is None:  # noqa: E501
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) > 1024):
            raise ValueError("Invalid value for `key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) < 1):
            raise ValueError("Invalid value for `key`, length must be greater than or equal to `1`")  # noqa: E501

        self._key = key

    @property
    def home_location(self):
        """Gets the home_location of this Performer.  # noqa: E501


        :return: The home_location of this Performer.  # noqa: E501
        :rtype: Location
        """
        return self._home_location

    @home_location.setter
    def home_location(self, home_location):
        """Sets the home_location of this Performer.


        :param home_location: The home_location of this Performer.  # noqa: E501
        :type: Location
        """

        self._home_location = home_location

    @property
    def transport_type(self):
        """Gets the transport_type of this Performer.  # noqa: E501


        :return: The transport_type of this Performer.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this Performer.


        :param transport_type: The transport_type of this Performer.  # noqa: E501
        :type: TransportType
        """
        if self.local_vars_configuration.client_side_validation and transport_type is None:  # noqa: E501
            raise ValueError("Invalid value for `transport_type`, must not be `None`")  # noqa: E501

        self._transport_type = transport_type

    @property
    def cost_per_meter(self):
        """Gets the cost_per_meter of this Performer.  # noqa: E501

        Cost per move per meter.  # noqa: E501

        :return: The cost_per_meter of this Performer.  # noqa: E501
        :rtype: float
        """
        return self._cost_per_meter

    @cost_per_meter.setter
    def cost_per_meter(self, cost_per_meter):
        """Sets the cost_per_meter of this Performer.

        Cost per move per meter.  # noqa: E501

        :param cost_per_meter: The cost_per_meter of this Performer.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                cost_per_meter is not None and cost_per_meter < 0):  # noqa: E501
            raise ValueError("Invalid value for `cost_per_meter`, must be a value greater than or equal to `0`")  # noqa: E501

        self._cost_per_meter = cost_per_meter

    @property
    def cost_per_minute(self):
        """Gets the cost_per_minute of this Performer.  # noqa: E501

        Cost per minute.  # noqa: E501

        :return: The cost_per_minute of this Performer.  # noqa: E501
        :rtype: float
        """
        return self._cost_per_minute

    @cost_per_minute.setter
    def cost_per_minute(self, cost_per_minute):
        """Sets the cost_per_minute of this Performer.

        Cost per minute.  # noqa: E501

        :param cost_per_minute: The cost_per_minute of this Performer.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                cost_per_minute is not None and cost_per_minute < 0):  # noqa: E501
            raise ValueError("Invalid value for `cost_per_minute`, must be a value greater than or equal to `0`")  # noqa: E501

        self._cost_per_minute = cost_per_minute

    @property
    def limits(self):
        """Gets the limits of this Performer.  # noqa: E501


        :return: The limits of this Performer.  # noqa: E501
        :rtype: ClusterLimits
        """
        return self._limits

    @limits.setter
    def limits(self, limits):
        """Sets the limits of this Performer.


        :param limits: The limits of this Performer.  # noqa: E501
        :type: ClusterLimits
        """

        self._limits = limits

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Performer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Performer):
            return True

        return self.to_dict() != other.to_dict()
