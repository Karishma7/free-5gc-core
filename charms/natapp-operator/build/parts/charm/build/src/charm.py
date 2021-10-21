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
"""Defining NatApp charm events"""

import logging
from typing import NoReturn
from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState, EventBase
from ops.model import ActiveStatus, BlockedStatus, MaintenanceStatus

from oci_image import OCIImageResource, OCIImageResourceError

from pod_spec import make_pod_spec

logger = logging.getLogger(__name__)


class NatappCharm(CharmBase):
    """Natapp charm events definition"""

    state = StoredState()

    def __init__(self, *args):
        "Natapp charm constructor." ""
        super().__init__(*args)
        self.state.set_default(pod_spec=None)

        self.image = OCIImageResource(self, "image")

        #self.image=config["image"]

        # Registering regular events
        self.framework.observe(self.on.config_changed, self.configure_pod)

        # Registering provided relation events
        self.framework.observe(
            self.on.natapp_relation_changed, self._publish_natapp_info
        )

    def _publish_natapp_info(self, event: EventBase) -> NoReturn:
        """Publishes NATAPP IP information for UPF
          relation.7

        Args:
             event (EventBase): Natapp relation event to update UPF.
        """
        config = self.model.config
        try:
            static_ip = config["static_ip"]
            if self.unit.is_leader():
                rel_data = {
                    "hostname": self.model.app.name,
                    "static_ip": static_ip,
                }
                for k, param in rel_data.items():
                    event.relation.data[self.model.app][k] = param

        except TypeError:
            self.unit.status = BlockedStatus("Ip not yet fetched")
            return

    def configure_pod(self, _=None) -> NoReturn:
        """Assemble the pod spec and apply it, if possible."""
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus("ready")
            return

        self.unit.status = MaintenanceStatus("Assembling pod spec")
        #image_info=self.image

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
    main(NatappCharm)
