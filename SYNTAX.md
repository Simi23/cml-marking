## AppConfig
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **cml** | `[<class 'configuration.CmlConfig'>](#cmlconfig)` | ✅ | - | Connection parameters for the CML instance |
| **sub_criteria** | `[List[SubCriterion]](#subcriterion)` | ✅ | - | The marking scheme |


### CmlConfig
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **url** | `<class 'str'>` | ✅ | - | The URL of the CML instance. Must be reachable. |
| **username** | `<class 'str'>` | ✅ | - | The username to log in to CML. |
| **password** | `<class 'str'>` | ✅ | - | The password to log in to CML. |
| **ssl** | `Optional[bool]` | ❌ | False | Verify SSL for the CML website. |


### SubCriterion
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **sc_id** | `<class 'str'>` | ✅ | - | Sub Criterion ID, e.g. `C1` |
| **name** | `<class 'str'>` | ✅ | - | Name of the sub criterion |
| **aspects** | `[List[Aspect]](#aspect)` | ✅ | - | Aspects that belong to this sub criterion |


#### Aspect
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **aspect_type** | `<enum 'AspectType'>` | ✅ | - | Aspect type. Possible values are: `J` for judgement; `M` for measurement; `MC` for calculated measurement (a count of measurements) |
| **aspect_id** | `<class 'str'>` | ✅ | - | Aspect ID, e.g. `C1.1` |
| **description** | `<class 'str'>` | ✅ | - | Description of the aspect to print |
| **extra_description** | `Optional[str]` | ✅ | - | Extra description to print |
| **check_commands** | `[List[CheckCommand]](#checkcommand)` | ✅ | - | The commands to run for this aspect |


##### CheckCommand
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **device_name** | `Optional[str]` | ✅ | - | The display name of the device to run the command on. Either this or `random_devices` must be defined! |
| **model** | `<class 'str'>` | ✅ | - | The model to learn from the device. Find available models at [https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models] |
| **result_filter** | `Optional[List[Union[List[str], str]]]` | ❌ | ['**'] | A list of glob filters to apply on the model. Multiple search queries are merged together. Bash glob syntax is supported. The default separator is `/`, if you want to use it as text, provide the path as an array instead, e.g. `['GigabitEthernet0/1', 'oper_status']` |
| **use_cache** | `Optional[bool]` | ❌ | True | Allow the use of cached previous results (only stored in memory during runtime) |
| **update_cache** | `Optional[bool]` | ❌ | True | Update the cache with the result of this command |
| **expected_result** | `[<class 'configuration.ExpectedResult'>](#expectedresult)` | ✅ | - | The expected result of this command |
| **random_devices** | `Optional[List[str]]` | ✅ | - | A list of devices to choose from to randomly run this command. Either this or `device_name` must be defined! If this is defined, `device_name` is ignored! |
| **random_device_count** | `Optional[int]` | ❌ | 1 | How many random devices to select from the list. |


###### ExpectedResult
| Field | Type | Required | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| **description** | `Optional[str]` | ✅ | - | Description of the expected result which is always printed with the aspect. |
| **single** | `Optional[str]` | ✅ | - | A single value to search in the gathered info. |
| **multiple** | `Optional[List[str]]` | ✅ | - | A list of values to search in the gathered info. |
| **condition** | `Optional[configuration.MultiSearchCondition]` | ❌ | MultiSearchCondition.AllMatch | Mode for searching multiple values. `all`: All values must be matched to pass the aspect; `any`: Any match will pass the aspect. |
| **exact** | `Optional[bool]` | ❌ | True | If true, the provided search string has to match the whole field that is checked. |
| **search_in_key** | `Optional[bool]` | ❌ | True | Whether to search in keys of the gathered info. |
| **search_in_value** | `Optional[bool]` | ❌ | True | Whether to search in the values of the gathered info. |


