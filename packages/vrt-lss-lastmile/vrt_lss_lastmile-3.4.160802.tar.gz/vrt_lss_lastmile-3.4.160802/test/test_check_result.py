# coding: utf-8

"""
    VeeRoute.LSS Lastmile

    VeeRoute.LSS Lastmile API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_lastmile
from vrt_lss_lastmile.models.check_result import CheckResult  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestCheckResult(unittest.TestCase):
    """CheckResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CheckResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.check_result.CheckResult()  # noqa: E501
        if include_optional :
            return CheckResult(
                health = 0.9
            )
        else :
            return CheckResult(
                health = 0.9,
        )

    def testCheckResult(self):
        """Test CheckResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
