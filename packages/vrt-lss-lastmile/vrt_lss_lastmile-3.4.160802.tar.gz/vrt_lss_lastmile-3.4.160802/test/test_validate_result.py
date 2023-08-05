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
from vrt_lss_lastmile.models.validate_result import ValidateResult  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestValidateResult(unittest.TestCase):
    """ValidateResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ValidateResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.validate_result.ValidateResult()  # noqa: E501
        if include_optional :
            return ValidateResult(
                tracedata = vrt_lss_lastmile.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                validations = [
                    vrt_lss_lastmile.models.validation.Validation(
                        type = 'info', 
                        entity_key = 'ord0001', 
                        entity_type = 'order', 
                        info = 'bad time windows', )
                    ]
            )
        else :
            return ValidateResult(
        )

    def testValidateResult(self):
        """Test ValidateResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
