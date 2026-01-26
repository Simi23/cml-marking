import io
import dpath
from virl2_client import ClientLibrary
from typing import Any
from pyats.topology import Testbed, loader


class CmlClient:
    lab_testbed: Testbed
    _device_cache: dict[tuple[str, str], dict] = {}

    def __init__(self, url: str, username: str, password: str, ssl: bool = False):
        self._cml_username = username
        self._cml_password = password
        self._client = ClientLibrary(url, username, password, ssl_verify=ssl)
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
        self.lab_testbed = loader.load(io.StringIO(lab.get_pyats_testbed()))
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
        filter: list[str] = ["**"],
        use_cache: bool = True,
        update_cache: bool = True,
    ) -> Any:
        data_id = (device_name, model)

        # Get the output based on the cache settings
        output = {}
        if use_cache and data_id in self._device_cache:
            output = self._device_cache[data_id]
        else:
            # Get the device
            device = self.lab_testbed.devices[device_name]
            # Connect to the device
            device.connect(log_stdout=False)

            # Get all necessary output, than disconnect
            output = device.learn(model).info
            device.disconnect()

            # If cache updating is enabled, write the result
            if update_cache:
                self._device_cache[data_id] = output

        # Filter and merge output to the format needed
        all_output = {}

        for line in filter:
            dpath.merge(all_output, dict(dpath.search(output, line)))

        return all_output
