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


class Cluster(object):
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
        'performer_key': 'str',
        'points_keys': 'list[str]',
        'representer_key': 'str'
    }

    attribute_map = {
        'performer_key': 'performer_key',
        'points_keys': 'points_keys',
        'representer_key': 'representer_key'
    }

    def __init__(self, performer_key=None, points_keys=None, representer_key=None, local_vars_configuration=None):  # noqa: E501
        """Cluster - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._performer_key = None
        self._points_keys = None
        self._representer_key = None
        self.discriminator = None

        self.performer_key = performer_key
        self.points_keys = points_keys
        if representer_key is not None:
            self.representer_key = representer_key

    @property
    def performer_key(self):
        """Gets the performer_key of this Cluster.  # noqa: E501

        Performer's key, unique ID.  # noqa: E501

        :return: The performer_key of this Cluster.  # noqa: E501
        :rtype: str
        """
        return self._performer_key

    @performer_key.setter
    def performer_key(self, performer_key):
        """Sets the performer_key of this Cluster.

        Performer's key, unique ID.  # noqa: E501

        :param performer_key: The performer_key of this Cluster.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and performer_key is None:  # noqa: E501
            raise ValueError("Invalid value for `performer_key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_key is not None and len(performer_key) > 1024):
            raise ValueError("Invalid value for `performer_key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_key is not None and len(performer_key) < 1):
            raise ValueError("Invalid value for `performer_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._performer_key = performer_key

    @property
    def points_keys(self):
        """Gets the points_keys of this Cluster.  # noqa: E501

        Point keys list.  # noqa: E501

        :return: The points_keys of this Cluster.  # noqa: E501
        :rtype: list[str]
        """
        return self._points_keys

    @points_keys.setter
    def points_keys(self, points_keys):
        """Sets the points_keys of this Cluster.

        Point keys list.  # noqa: E501

        :param points_keys: The points_keys of this Cluster.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and points_keys is None:  # noqa: E501
            raise ValueError("Invalid value for `points_keys`, must not be `None`")  # noqa: E501

        self._points_keys = points_keys

    @property
    def representer_key(self):
        """Gets the representer_key of this Cluster.  # noqa: E501

        Key of the cluster representative point.  # noqa: E501

        :return: The representer_key of this Cluster.  # noqa: E501
        :rtype: str
        """
        return self._representer_key

    @representer_key.setter
    def representer_key(self, representer_key):
        """Sets the representer_key of this Cluster.

        Key of the cluster representative point.  # noqa: E501

        :param representer_key: The representer_key of this Cluster.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                representer_key is not None and len(representer_key) > 1024):
            raise ValueError("Invalid value for `representer_key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                representer_key is not None and len(representer_key) < 1):
            raise ValueError("Invalid value for `representer_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._representer_key = representer_key

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
        if not isinstance(other, Cluster):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Cluster):
            return True

        return self.to_dict() != other.to_dict()
