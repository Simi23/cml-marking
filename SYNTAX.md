# AppConfig

| Field            | Type                                | Required | Default | Description                                |
| :--------------- | :---------------------------------- | :------: | :------ | :----------------------------------------- |
| **cml**          | [CmlConfig](#cmlconfig)             |    ✅    | -       | Connection parameters for the CML instance |
| **sub_criteria** | [List[SubCriterion]](#subcriterion) |    ✅    | -       | The marking scheme                         |

## CmlConfig

| Field        | Type   | Required | Default | Description                                     |
| :----------- | :----- | :------: | :------ | :---------------------------------------------- |
| **url**      | `str`  |    ✅    | -       | The URL of the CML instance. Must be reachable. |
| **username** | `str`  |    ✅    | -       | The username to log in to CML.                  |
| **password** | `str`  |    ✅    | -       | The password to log in to CML.                  |
| **ssl**      | `bool` |    ❌    | False   | Verify SSL for the CML website.                 |

## SubCriterion

| Field       | Type                    | Required | Default | Description                               |
| :---------- | :---------------------- | :------: | :------ | :---------------------------------------- |
| **sc_id**   | `str`                   |    ✅    | -       | Sub Criterion ID, e.g. `C1`               |
| **name**    | `str`                   |    ✅    | -       | Name of the sub criterion                 |
| **aspects** | [List[Aspect]](#aspect) |    ✅    | -       | Aspects that belong to this sub criterion |

### Aspect

| Field                 | Type                                | Required | Default | Description                                                                                                                         |
| :-------------------- | :---------------------------------- | :------: | :------ | :---------------------------------------------------------------------------------------------------------------------------------- |
| **aspect_type**       | `AspectType`                        |    ✅    | -       | Aspect type. Possible values are: `J` for judgement; `M` for measurement; `MC` for calculated measurement (a count of measurements) |
| **aspect_id**         | `str`                               |    ✅    | -       | Aspect ID, e.g. `C1.1`                                                                                                              |
| **description**       | `str`                               |    ✅    | -       | Description of the aspect to print                                                                                                  |
| **extra_description** | `str`                               |    ❌    | -       | Extra description to print                                                                                                          |
| **check_commands**    | [List[CheckCommand]](#checkcommand) |    ✅    | -       | The commands to run for this aspect                                                                                                 |

#### CheckCommand

| Field                   | Type                                    | Required | Default | Description                                                                                                                                                                                                                                                                                                          |
| :---------------------- | :-------------------------------------- | :------: | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **device_name**         | `str`                                   |    ❌    | -       | ❗**Mutually exclusive with `random_devices`. One of them is required.**<br><br>The display name of the device to run the command on.                                                                                                                                                                                |
| **model**               | `str`                                   |    ❌    | -       | ❗**Mutually exclusive with `parser` and `command`. One of them is required.**<br><br>The model to learn from the device. Find available models at [https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models)              |
| **parser**              | `str`                                   |    ❌    | -       | ❗**Mutually exclusive with `model` and `command`. One of them is required.**<br><br>The command of the device that will be parsed. Find available parsers at [https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers) |
| **command**             | `str`                                   |    ❌    | -       | ❗**Mutually exclusive with `model` and `parser`. One of them is required.**<br><br>Any command to execute on the device. The output will be returned as plain text.                                                                                                                                                 |
| **result_filter**       | `List[List[str] \| str]`                |    ❌    | ['**']  | A list of glob filters to apply on the model. Multiple search queries are merged together. Bash glob syntax is supported. The default separator is `/`, if you want to use it as text, provide the path as an array instead, e.g. `['GigabitEthernet0/1', 'oper_status']`                                            |
| **reuse_cache**         | `bool`                                  |    ❌    | True    | Allow the use of cached previous results (only stored in memory during runtime)                                                                                                                                                                                                                                      |
| **update_cache**        | `bool`                                  |    ❌    | True    | Update the cache with the result of this command                                                                                                                                                                                                                                                                     |
| **expected_results**    | [List[ExpectedResult]](#expectedresult) |    ✅    | -       | The expected result of this command                                                                                                                                                                                                                                                                                  |
| **random_devices**      | `List[str]`                             |    ❌    | -       | ❗**Mutually exclusive with `device_name`. One of them is required.**<br><br>A list of devices to choose from to randomly run this command.                                                                                                                                                                          |
| **random_device_count** | `int`                                   |    ❌    | 1       | How many random devices to select from the list.                                                                                                                                                                                                                                                                     |

##### ExpectedResult

| Field               | Type                   | Required | Default | Description                                                                                                                      |
| :------------------ | :--------------------- | :------: | :------ | :------------------------------------------------------------------------------------------------------------------------------- |
| **description**     | `str`                  |    ❌    | -       | Description of the expected result which is always printed with the aspect.                                                      |
| **single**          | `str`                  |    ❌    | -       | A single value to search in the gathered info.                                                                                   |
| **multiple**        | `List[str]`            |    ❌    | -       | A list of values to search in the gathered info.                                                                                 |
| **condition**       | `MultiSearchCondition` |    ❌    | `all`   | Mode for searching multiple values. `all`: All values must be matched to pass the aspect; `any`: Any match will pass the aspect. |
| **exact**           | `bool`                 |    ❌    | True    | If true, the provided search string has to match the whole field that is checked.                                                |
| **negate**          | `bool`                 |    ❌    | False   | Negate the result. Useful for checking the absence of a given string.                                                            |
| **search_filter**   | `List[str] \| str`     |    ❌    | -       | A glob filter to apply on the output of the command. If provided, the search will only happen on the leaf found by the filter.   |
| **search_in_key**   | `bool`                 |    ❌    | True    | Whether to search in keys of the gathered info.                                                                                  |
| **search_in_value** | `bool`                 |    ❌    | True    | Whether to search in the values of the gathered info.                                                                            |
| **mark**            | `str`                  |    ❌    | -       | Marking info (e.g. points) to display next to the expected result.                                                               |
