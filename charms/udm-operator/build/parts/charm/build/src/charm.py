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
"""Defining udm charm events"""

import logging
from typing import Any, Dict, NoReturn
from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState, EventBase
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus

from oci_image import OCIImageResource, OCIImageResourceError

from pod_spec import make_pod_spec


logger = logging.getLogger(__name__)


class UdmCharm(CharmBase):
    """UDM charm events class definition"""

    state = StoredState()

    def __init__(self, *args):
        """UDM charm constructor."""
        super().__init__(*args)
        self.state.set_default(pod_spec=None)

        self.image = OCIImageResource(self, "image")

        # Registering regular events
        self.framework.observe(self.on.config_changed, self.configure_pod)

        # Registering required relation changed events
        self.framework.observe(
            self.on.nrf_relation_changed, self._on_nrf_relation_changed
        )

        # Registering required relation broken events
        self.framework.observe(
            self.on.nrf_relation_broken, self._on_nrf_relation_broken
        )

        # -- initialize states --
        self.state.set_default(nrf_host=None)

    def _on_nrf_relation_changed(self, event: EventBase) -> NoReturn:
        """Reads information about the NRF relation.

        Args:
           event (EventBase): NRF relation event.
        """
        if event.app not in event.relation.data:
            return

        nrf_host = event.relation.data[event.app].get("hostname")
        if nrf_host and self.state.nrf_host != nrf_host:
            self.state.nrf_host = nrf_host
            self.configure_pod()

    def _on_nrf_relation_broken(self, _=None) -> NoReturn:
        """Clears data from NRF relation."""
        self.state.nrf_host = None
        self.configure_pod()

    def _missing_relations(self) -> str:
        """Checks if there missing relations.

        Returns:
            str: string with missing relations
        """
        data_status = {"nrf": self.state.nrf_host}
        missing_relations = [k for k, v in data_status.items() if not v]
        return ", ".join(missing_relations)

    @property
    def relation_state(self) -> Dict[str, Any]:
        """Collects relation state configuration for pod spec assembly.

        Returns:
            Dict[str, Any]: relation state information.
        """
        relation_state = {"nrf_host": self.state.nrf_host}

        return relation_state

    def configure_pod(self, _=None) -> NoReturn:
        """Assemble the pod spec and apply it, if possible."""
        missing = self._missing_relations()
        if missing:
            self.unit.status = BlockedStatus(
                "Waiting for {0} relation{1}".format(
                    missing, "s" if "," in missing else ""
                )
            )
            return
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus("ready")
            return

        self.unit.status = MaintenanceStatus("Assembling pod spec")

        # Fetch image information
        try:
            self.unit.status = MaintenanceStatus("Fetching image information")
            image_info = self.image.fetch()
        except OCIImageResourceError:
            self.unit.status = BlockedStatus("Error fetching image information")
            return

        try:
            pod_spec = make_pod_spec(
                image_info,
                self.model.config,
                self.model.app.name,
                self.relation_state,
            )
        except ValueError as exc:
            logger.exception("Config data validation error")
            self.unit.status = BlockedStatus(str(exc))
            return

        if self.state.pod_spec != pod_spec:
            self.model.pod.set_spec(pod_spec)
            self.state.pod_spec = pod_spec

        self.unit.status = ActiveStatus("ready")


if __name__ == "__main__":
    main(UdmCharm)
