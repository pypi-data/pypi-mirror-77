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


class AnalyticsTask(object):
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
        'plan_task': 'PlanTask',
        'plan_result': 'PlanResult'
    }

    attribute_map = {
        'plan_task': 'plan_task',
        'plan_result': 'plan_result'
    }

    def __init__(self, plan_task=None, plan_result=None, local_vars_configuration=None):  # noqa: E501
        """AnalyticsTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._plan_task = None
        self._plan_result = None
        self.discriminator = None

        self.plan_task = plan_task
        self.plan_result = plan_result

    @property
    def plan_task(self):
        """Gets the plan_task of this AnalyticsTask.  # noqa: E501


        :return: The plan_task of this AnalyticsTask.  # noqa: E501
        :rtype: PlanTask
        """
        return self._plan_task

    @plan_task.setter
    def plan_task(self, plan_task):
        """Sets the plan_task of this AnalyticsTask.


        :param plan_task: The plan_task of this AnalyticsTask.  # noqa: E501
        :type: PlanTask
        """
        if self.local_vars_configuration.client_side_validation and plan_task is None:  # noqa: E501
            raise ValueError("Invalid value for `plan_task`, must not be `None`")  # noqa: E501

        self._plan_task = plan_task

    @property
    def plan_result(self):
        """Gets the plan_result of this AnalyticsTask.  # noqa: E501


        :return: The plan_result of this AnalyticsTask.  # noqa: E501
        :rtype: PlanResult
        """
        return self._plan_result

    @plan_result.setter
    def plan_result(self, plan_result):
        """Sets the plan_result of this AnalyticsTask.


        :param plan_result: The plan_result of this AnalyticsTask.  # noqa: E501
        :type: PlanResult
        """
        if self.local_vars_configuration.client_side_validation and plan_result is None:  # noqa: E501
            raise ValueError("Invalid value for `plan_result`, must not be `None`")  # noqa: E501

        self._plan_result = plan_result

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
        if not isinstance(other, AnalyticsTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnalyticsTask):
            return True

        return self.to_dict() != other.to_dict()
