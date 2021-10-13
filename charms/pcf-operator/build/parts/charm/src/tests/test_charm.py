#!/usr/bin/env python3
# Copyright 2020 Tata Elxsi
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact: canonical@tataelxsi.onmicrosoft.com
#
# To get in touch with the maintainers, please contact:
# canonical@tataelxsi.onmicrosoft.com
##
"""PCF test script for charm.py"""

import unittest
from typing import NoReturn
from ops.testing import Harness
from ops.model import BlockedStatus

from charm import PcfCharm


class TestCharm(unittest.TestCase):
    """Test script for checking pod spec and relations"""

    def setUp(self) -> NoReturn:
        """Test setup."""
        self.harness = Harness(PcfCharm)
        self.harness.set_leader(is_leader=True)
        self.harness.begin()

    def test_config_changed(self) -> NoReturn:
        """Test installation without any relation."""
        self.harness.charm.on.config_changed.emit()
        expected_result = {
            "version": 3,
            "containers": [
                {
                    "name": "pcf",
                    "imageDetails": self.harness.charm.image.fetch(),
                    "imagePullPolicy": "Always",
                    "ports": [
                        {
                            "name": "pcf",
                            "containerPort": 29507,
                            "protocol": "TCP",
                        }
                    ],
                    "envConfig": {
                        "ALLOW_ANONYMOUS_LOGIN": "yes",
                        "GIN_MODE": "release",
                        "NRF_HOST": "nrf",
                        "AMF_HOST": "amf",
                    },
                    "command": ["./pcf_start.sh", "&"],
                },
            ],
        }

        self.assertIsNone(self.harness.charm.state.nrf_host)
        self.assertIsNone(self.harness.charm.state.amf_host)

        # Initializing the nrf relation
        nrf_relation_id = self.harness.add_relation("nrf", "nrf")
        self.harness.add_relation_unit(nrf_relation_id, "nrf/0")
        self.harness.update_relation_data(nrf_relation_id, "nrf", {"hostname": "nrf"})

        # Initializing the amf relation
        amf_relation_id = self.harness.add_relation("amf", "amf")
        self.harness.add_relation_unit(amf_relation_id, "amf/0")
        self.harness.update_relation_data(amf_relation_id, "amf", {"hostname": "amf"})

        self.assertEqual(self.harness.charm.state.nrf_host, "nrf")
        self.assertEqual(self.harness.charm.state.amf_host, "amf")

        # Verifying status
        self.assertNotIsInstance(self.harness.charm.unit.status, BlockedStatus)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        self.assertFalse(self.harness.charm.unit.status.message.endswith(" relations"))

        pod_spec, _ = self.harness.get_pod_spec()
        self.assertDictEqual(expected_result, pod_spec)

    def test_on_nrf_app_relation_changed(self) -> NoReturn:
        """Test to see if Nrf relation is updated."""

        self.assertIsNone(self.harness.charm.state.nrf_host)

        relation_id = self.harness.add_relation("nrf", "nrf")
        self.harness.add_relation_unit(relation_id, "nrf/0")
        self.harness.update_relation_data(relation_id, "nrf", {"hostname": "nrf"})

        self.assertEqual(self.harness.charm.state.nrf_host, "nrf")
        # Verifying status
        self.assertIsInstance(self.harness.charm.unit.status, BlockedStatus)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        self.assertTrue(
            self.harness.charm.unit.status.message.startswith("Waiting for ")
        )

    def test_on_amf_app_relation_changed(self) -> NoReturn:
        """Test to see if Amf relation is updated."""
        self.harness.charm.on.start.emit()

        self.assertIsNone(self.harness.charm.state.amf_host)

        relation_id = self.harness.add_relation("amf", "amf")
        self.harness.add_relation_unit(relation_id, "amf/0")
        self.harness.update_relation_data(relation_id, "amf", {"hostname": "amf"})

        self.assertEqual(self.harness.charm.state.amf_host, "amf")

        # Verifying status
        self.assertIsInstance(self.harness.charm.unit.status, BlockedStatus)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        self.assertTrue(
            self.harness.charm.unit.status.message.startswith("Waiting for ")
        )


if __name__ == "__main__":
    unittest.main()
