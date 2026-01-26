import io
import sys
import logging
from virl2_client import ClientLibrary
from pyats.topology import loader
import json
import dpath

# needed_info = ["*/oper_status", "*/ipv4"]
needed_info = ["**"]

# Setup logging to see pyATS connection details
# logging.basicConfig(level=logging.ERROR)

# --- Configuration ---
CML_URL = "https://192.168.1.24"  # Address of your CML instance
CML_USER = "admin"
CML_PASS = "Passw0rd!"
LAB_NAME = "test"  # The name (or ID) of the running lab


def main():
    print("--- Connecting to CML Controller ---")
    # 1. Connect to the CML API
    # ssl_verify=False is common for self-signed CML certs; use True in production
    client = ClientLibrary(CML_URL, CML_USER, CML_PASS, ssl_verify=False)

    # 2. Find and Join the Running Lab
    # You can also use client.join_lab("lab-id-string") if you know the ID
    labs = client.find_labs_by_title(LAB_NAME)
    if not labs:
        print(f"Error: Lab '{LAB_NAME}' not found.")
        sys.exit(1)

    lab = labs[0]
    print(f"--- Joined Lab: {lab.title} ({lab.id}) ---")

    # 3. Generate the pyATS Testbed Dynamically
    # This is the key step. CML builds the YAML string for you, automatically
    # configuring the 'ssh' connections to go through the CML Console Server.
    print("--- Fetching pyATS Testbed from CML ---")
    testbed_yaml = lab.get_pyats_testbed()

    # Optional: Save it to see what it looks like
    # with open("cml_testbed.yaml", "w") as f:
    #     f.write(testbed_yaml)

    # 4. Load the Testbed into pyATS
    testbed = loader.load(io.StringIO(testbed_yaml))

    testbed.devices.terminal_server.credentials["default"] = {
        "username": CML_USER,
        "password": CML_PASS,
    }

    device = testbed.devices["ISP"]
    device.connect(log_stdout=False)
    output = device.learn("interface")

    device.disconnect()

    # print(output.info)

    total_info = {}

    for info_piece in needed_info:
        dpath.merge(total_info, dpath.search(output.info, info_piece))

    with open("isp-interface-all.json", "w") as f:
        f.write(json.dumps(output.info))

    with open("isp-interface-filter.json", "w") as f:
        f.write(json.dumps(total_info))

    # # 5. Connect and Pull Data
    # print("\n--- Starting Device Checks ---")

    # # Example: Loop through all devices and check version
    # for device_name, device in testbed.devices.items():
    #     # Skip external connectors or unmanaged nodes if necessary
    #     if device.os == "linux":
    #         continue

    #     print(f"\n[+] Connecting to {device_name} via CML Console...")
    #     try:
    #         # Connect to the device (tunneling via CML SSH)
    #         device.connect(log_stdout=False)

    #         # Use Genie to parse a command
    #         # This turns the text output into a Python Dictionary
    #         print(f"    Parsing 'show version' on {device_name}...")
    #         output = device.parse("show version")

    #         # Extract data from the structured dictionary
    #         # Note: The keys depend on the specific OS (IOS-XE, NX-OS, etc.)
    #         version = output.get("version", {}).get("version")
    #         uptime = output.get("version", {}).get("uptime")

    #         print(f"    RESULT: {device_name} is running version {version}")
    #         print(f"    UPTIME: {uptime}")

    #         device.disconnect()

    #     except Exception as e:
    #         print(f"    ERROR: Could not connect or parse {device_name}. Reason: {e}")


if __name__ == "__main__":
    main()
