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
"""Pod spec for UDM charm"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


UDM_PORT = 29503


def _make_pod_ports() -> List[Dict[str, Any]]:
    """Generate pod ports details.

    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    return [{"name": "udm", "containerPort": UDM_PORT, "protocol": "TCP"}]


def _make_pod_envconfig(
    config: Dict[str, Any], relation_state: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate pod environment configuration.

    Args:
        config (Dict[str, Any]): configuration information.

    Returns:
        Dict[str, Any]: pod environment configuration.
    """
    return {
        # General configuration
        "ALLOW_ANONYMOUS_LOGIN": "yes",
        "GIN_MODE": config["gin_mode"],
        "NRF_HOST": relation_state["nrf_host"],
    }


def _make_pod_command() -> List[str]:
    """Generate pod command.

    Returns:
        List[str]:pod command.
    """
    return ["./udm_start.sh", "&"]


def _validate_config(config: Dict[str, Any]):
    """Validate config data.

    Args:
        config (Dict[str, Any]): configuration information.
    """
    valid_gin_modes = ["release", "debug"]
    if config.get("gin_mode") not in valid_gin_modes:
        raise ValueError("Invalid gin_mode")


def _validate_relation_state(relation_state: Dict[str, Any]):
    """Validate relation data.

    Args:
        relation (Dict[str, Any]): relation state information.
    """
    nrf_host = relation_state.get("nrf_host")
    if not nrf_host:
        raise ValueError("Value error in nrf relations")


def make_pod_spec(
    image_info: Dict[str, str],
    config: Dict[str, Any],
    app_name: str,
    relation_state: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate the pod spec information.

    Args:
        image_info (Dict[str, str]): Object provided by
                                     OCIImageResource("image").fetch().
        config (Dict[str, Any]): Configuration information.
        app_name (str, optional): Application name. Defaults to "pol".

    Returns:
        Dict[str, Any]: Pod spec dictionary for the charm.
    """
    if not image_info:
        return None

    _validate_config(config)
    _validate_relation_state(relation_state)
    ports = _make_pod_ports()
    env_config = _make_pod_envconfig(config, relation_state)
    command = _make_pod_command()
    return {
        "version": 3,
        "containers": [
            {
                "name": app_name,
                "imageDetails": image_info,
                "imagePullPolicy": "Always",
                "ports": ports,
                "envConfig": env_config,
                "command": command,
            }
        ],
    }
