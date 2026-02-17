import logging
import io
import dpath
from virl2_client import ClientLibrary
from typing import Any
from pyats.topology import Testbed, loader
import json
import yaml


class CmlClient:
    lab_testbed: Testbed
    _device_cache: dict[tuple[str, str, str], dict] = {}
    _visited_devices: list[str] = []

    def __init__(self, url: str, username: str, password: str, ssl: bool = False):
        self._cml_username = username
        self._cml_password = password
        self._client = ClientLibrary(url, username, password, ssl_verify=ssl)
        dpath.options.ALLOW_EMPTY_STRING_KEYS = True
        return

    @property
    def device_cache(self):
        """
        ### Device Cache

        Key is a tuple of device name and the info model

        Value is the full result of that search
        """
        return self._device_cache

    def list_labs(self):
        return self._client.all_labs()

    def prep_lab_test(self, lab_id: str) -> None:
        lab = self._client.join_existing_lab(lab_id, False)
        testbed_yaml = lab.get_pyats_testbed()
        with open("testbed.yaml", "w") as f:
            f.write(testbed_yaml)
        testbed_data = yaml.safe_load(testbed_yaml)
        testbed_data["devices"]["terminal_server"]["type"] = "linux"
        testbed_data["topology"]["terminal_server"] = {
            "interfaces": {"eth0": {"type": "ethernet"}}
        }
        self.lab_testbed = loader.load(testbed_data)
        self.lab_testbed.devices.terminal_server.credentials["default"] = {
            "username": self._cml_username,
            "password": self._cml_password,
        }
        return

    def get_devices(self) -> list[str]:
        return [x for x in self.lab_testbed.devices.keys() if x != "terminal_server"]

    def learn_device_info(
        self,
        device_name: str,
        model: str,
        filter: list[list[str] | str] = ["**"],
        use_cache: bool = True,
        update_cache: bool = True,
    ) -> Any:
        data_id = (device_name, "model", model)

        # Get the output based on the cache settings
        output = {}
        if use_cache and data_id in self._device_cache:
            output = self._device_cache[data_id]
        else:
            # Get the device
            device = self.lab_testbed.devices[device_name]

            # Connect to the device
            # If the device has already been used, do not configure it again
            if device_name in self._visited_devices:
                device.connect(
                    init_exec_commands=[],
                    init_config_commands=[],
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )
            else:
                device.connect(
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )

            # Get all necessary output, than disconnect
            output = device.learn(model).info
            device.destroy()

            # If cache updating is enabled, write the result
            if update_cache:
                self._device_cache[data_id] = output

        # Filter and merge output to the format needed
        all_output = {}

        for line in filter:
            current = json.loads(
                json.dumps(dpath.search(json.loads(json.dumps(output)), line))
            )
            dpath.merge(all_output, current)

        return all_output

    def parse_device_info(
        self,
        device_name: str,
        parser: str,
        filter: list[list[str] | str] = ["**"],
        use_cache: bool = True,
        update_cache: bool = True,
    ) -> Any:
        data_id = (device_name, "parser", parser)

        # Get the output based on the cache settings
        output = {}
        if use_cache and data_id in self._device_cache:
            output = self._device_cache[data_id]
        else:
            # Get the device
            device = self.lab_testbed.devices[device_name]

            # Connect to the device
            # If the device has already been used, do not configure it again
            if device_name in self._visited_devices:
                device.connect(
                    init_exec_commands=[],
                    init_config_commands=[],
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )
            else:
                device.connect(
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )

            # Get all necessary output, than disconnect
            output = device.parse(parser)
            device.destroy()

            # If cache updating is enabled, write the result
            if update_cache:
                self._device_cache[data_id] = output

        # Filter and merge output to the format needed
        all_output = dict()

        for line in filter:
            # print(output)
            current = json.loads(
                json.dumps(dpath.search(json.loads(json.dumps(output)), line))
            )
            # print(json.dumps(current, indent=2))
            dpath.merge(all_output, current)

        return all_output

    def run_device_command(
        self,
        device_name: str,
        command: str,
        use_cache: bool = True,
        update_cache: bool = True,
    ) -> Any:
        data_id = (device_name, "command", command)

        # Get the output based on the cache settings
        output = {"output": ""}
        if use_cache and data_id in self._device_cache:
            output = self._device_cache[data_id]
        else:
            # Get the device
            device = self.lab_testbed.devices[device_name]

            # Connect to the device
            # If the device has already been used, do not configure it again
            if device_name in self._visited_devices:
                device.connect(
                    init_exec_commands=[],
                    init_config_commands=[],
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )
            else:
                device.connect(
                    log_stdout=False,
                    settings={
                        "GRACEFUL_DISCONNECT_WAIT_SEC": 1,
                        "POST_DISCONNECT_WAIT_SEC": 0,
                    },
                )

            # Get all necessary output, than disconnect
            output = {"output": device.execute(command)}
            device.destroy()

            # If cache updating is enabled, write the result
            if update_cache:
                self._device_cache[data_id] = output

        self._visited_devices.append(device_name)

        return output
