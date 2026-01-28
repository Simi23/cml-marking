from typing import Optional, List
from pydantic import BaseModel, ValidationError, Field
from enum import Enum


class CmlConfig(BaseModel):
    url: str = Field(description="The URL of the CML instance. Must be reachable.")
    username: str = Field(description="The username to log in to CML.")
    password: str = Field(description="The password to log in to CML.")
    ssl: Optional[bool] = Field(False, description="Verify SSL for the CML website.")


class MultiSearchCondition(str, Enum):
    AllMatch = "all"
    AnyMatch = "any"


class ExpectedResult(BaseModel):
    description: Optional[str] = Field(
        None,
        description="Description of the expected result which is always printed with the aspect.",
    )

    single: Optional[str] = Field(
        None, description="A single value to search in the gathered info."
    )

    multiple: Optional[List[str]] = Field(
        None, description="A list of values to search in the gathered info."
    )
    condition: Optional[MultiSearchCondition] = Field(
        MultiSearchCondition.AllMatch,
        description="Mode for searching multiple values. `all`: All values must be matched to pass the aspect; `any`: Any match will pass the aspect.",
    )

    exact: Optional[bool] = Field(
        True,
        description="If true, the provided search string has to match the whole field that is checked.",
    )

    search_filter: Optional[str] = Field("")

    search_in_key: Optional[bool] = Field(
        True, description="Whether to search in keys of the gathered info."
    )
    search_in_value: Optional[bool] = Field(
        True, description="Whether to search in the values of the gathered info."
    )


class CheckCommand(BaseModel):
    device_name: Optional[str] = Field(
        None,
        description="The display name of the device to run the command on. Either this or `random_devices` must be defined!",
    )
    model: Optional[str] = Field("")
    parser: Optional[str] = Field("")
    command: Optional[str] = Field("")
    result_filter: Optional[List[List[str] | str]] = Field(
        ["**"],
        description="A list of glob filters to apply on the model. Multiple search queries are merged together. Bash glob syntax is supported. The default separator is `/`, if you want to use it as text, provide the path as an array instead, e.g. `['GigabitEthernet0/1', 'oper_status']`",
    )

    use_cache: Optional[bool] = Field(
        True,
        description="Allow the use of cached previous results (only stored in memory during runtime)",
    )
    update_cache: Optional[bool] = Field(
        True, description="Update the cache with the result of this command"
    )

    expected_results: List[ExpectedResult] = Field(
        description="The expected result of this command",
    )

    random_devices: Optional[List[str]] = Field(
        None,
        description="A list of devices to choose from to randomly run this command. Either this or `device_name` must be defined! If this is defined, `device_name` is ignored!",
    )
    random_device_count: Optional[int] = Field(
        1, description="How many random devices to select from the list."
    )


class AspectType(str, Enum):
    judgement = "J"
    measurement = "M"
    measurement_count = "MC"


class Aspect(BaseModel):
    aspect_type: AspectType = Field(
        description="Aspect type. Possible values are: `J` for judgement; `M` for measurement; `MC` for calculated measurement (a count of measurements)"
    )
    aspect_id: str = Field(
        description="Aspect ID, e.g. `C1.1`",
    )
    description: str = Field(description="Description of the aspect to print")
    extra_description: Optional[str] = Field(
        None, description="Extra description to print"
    )
    check_commands: List[CheckCommand] = Field(
        description="The commands to run for this aspect"
    )


class SubCriterion(BaseModel):
    sc_id: str = Field(description="Sub Criterion ID, e.g. `C1`")
    name: str = Field(description="Name of the sub criterion")
    aspects: List[Aspect] = Field(
        description="Aspects that belong to this sub criterion"
    )


class AppConfig(BaseModel):
    cml: CmlConfig = Field(description="Connection parameters for the CML instance")
    sub_criteria: List[SubCriterion] = Field(description="The marking scheme")


def load_config(path: str) -> AppConfig:
    try:
        with open(path, "r") as f:
            raw_data = f.read()

        # This performs the parsing AND validation
        # Equivalent to Zod's .parse()
        config = AppConfig.model_validate_json(raw_data)

        return config

    except ValidationError as e:
        # Pydantic gives detailed error messages detailing exactly
        # which field failed and why
        print("Configuration Error:")
        print(e.json())
        exit(1)
    except FileNotFoundError:
        print(f"Error: Config file '{path}' not found.")
        exit(1)
