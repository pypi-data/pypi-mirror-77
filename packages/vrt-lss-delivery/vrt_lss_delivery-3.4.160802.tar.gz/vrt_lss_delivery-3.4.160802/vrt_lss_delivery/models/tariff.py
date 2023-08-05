# coding: utf-8

"""
    VeeRoute.LSS Delivery

    VeeRoute.LSS Delivery API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_lss_delivery.configuration import Configuration


class Tariff(object):
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
        'basic': 'TariffPrimary',
        'extra': 'list[TariffPrimary]'
    }

    attribute_map = {
        'basic': 'basic',
        'extra': 'extra'
    }

    def __init__(self, basic=None, extra=None, local_vars_configuration=None):  # noqa: E501
        """Tariff - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._basic = None
        self._extra = None
        self.discriminator = None

        self.basic = basic
        if extra is not None:
            self.extra = extra

    @property
    def basic(self):
        """Gets the basic of this Tariff.  # noqa: E501


        :return: The basic of this Tariff.  # noqa: E501
        :rtype: TariffPrimary
        """
        return self._basic

    @basic.setter
    def basic(self, basic):
        """Sets the basic of this Tariff.


        :param basic: The basic of this Tariff.  # noqa: E501
        :type: TariffPrimary
        """

        self._basic = basic

    @property
    def extra(self):
        """Gets the extra of this Tariff.  # noqa: E501

        Additional billing used for overtime work. It can be presented as several stages: for each stage of processing, it is possible to specify its own payment rate. Each stage is determined by the length and mileage from the previous one (the first from the basic tariff).   # noqa: E501

        :return: The extra of this Tariff.  # noqa: E501
        :rtype: list[TariffPrimary]
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """Sets the extra of this Tariff.

        Additional billing used for overtime work. It can be presented as several stages: for each stage of processing, it is possible to specify its own payment rate. Each stage is determined by the length and mileage from the previous one (the first from the basic tariff).   # noqa: E501

        :param extra: The extra of this Tariff.  # noqa: E501
        :type: list[TariffPrimary]
        """

        self._extra = extra

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
        if not isinstance(other, Tariff):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Tariff):
            return True

        return self.to_dict() != other.to_dict()
