# Marking script for Cisco Modeling Labs

This marking program uses pyATS to test a CML Lab based on the provided configuration file.

## Usage

Clone the repo, and install all requirements.

```bash
pip install -r requirements.txt
```

Put your configuration inside `configuration.json`.

Run `main.py`.

## Configuration syntax

Read about the configuration file in `SYNTAX.md`.

For the source, check `configuration.py`.

An example configuration can be found here:

```json
{
  "cml": {
    "url": "https://192.168.1.1",
    "username": "admin",
    "password": "password"
  },
  "sub_criteria": [
    {
      "sc_id": "C1",
      "name": "ISP Configuration",
      "aspects": [
        {
          "aspect_type": "M",
          "aspect_id": "C1.1",
          "description": "Interface G0/1 is enabled",
          "check_commands": [
            {
              "device_name": "ISP",
              "model": "interface",
              "result_filter": [["GigabitEthernet0/1", "oper_status"]],
              "expected_result": [
                {
                  "description": "Interface is up",
                  "single": "up"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

# Other info

Important links:

https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models
https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers
https://developer.cisco.com/docs/genie-docs/
https://questionary.readthedocs.io/en/stable/pages/api_reference.html#questionary.Choice
https://rich.readthedocs.io/en/latest/appendix/colors.html
