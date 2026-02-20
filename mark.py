from cml_client import CmlClient
import configuration
import dpath
import random
from configuration import MultiSearchCondition


def generate_runs(cc: configuration.CheckCommand, is_retry: bool = False):
    devices: list[str] = []
    runs: list[tuple[str, str, str, list[list[str] | str], bool, bool]] = []

    result_filter = cc.result_filter or ["**"]

    use_cache = True
    update_cache = True

    if cc.use_cache is not None:
        use_cache = cc.use_cache
    if cc.update_cache is not None:
        update_cache = cc.update_cache
    if is_retry:
        use_cache = False

    if cc.device_name:
        devices.append(cc.device_name)
    elif cc.random_devices and cc.random_device_count:
        rd = random.sample(cc.random_devices, cc.random_device_count)
        devices.extend(rd)

    for d in devices:
        if cc.model:
            runs.append((d, "model", cc.model, result_filter, use_cache, update_cache))
        elif cc.parser:
            runs.append(
                (d, "parser", cc.parser, result_filter, use_cache, update_cache)
            )
        elif cc.command:
            runs.append(
                (d, "command", cc.command, result_filter, use_cache, update_cache)
            )
    return runs


def perform_runs(
    client: CmlClient,
    runs: list[tuple[str, str, str, list[list[str] | str], bool, bool]],
):
    results: list[tuple[str, str, str, dict]] = []
    for run in runs:
        d, mode, mode_command, result_filter, use_cache, update_cache = run
        if mode == "model":
            result = client.learn_device_info(
                d,
                mode_command,
                filter=result_filter,
                use_cache=use_cache,
                update_cache=update_cache,
            )
            results.append((d, "model", mode_command, result))
        elif mode == "parser":
            result = client.parse_device_info(
                d,
                mode_command,
                filter=result_filter,
                use_cache=use_cache,
                update_cache=update_cache,
            )
            results.append((d, "parser", mode_command, result))
        elif mode == "command":
            result = client.run_device_command(
                d, mode_command, use_cache=use_cache, update_cache=update_cache
            )
            results.append((d, "command", mode_command, result))
    return results


def perform_mark(result: dict, cc: configuration.CheckCommand) -> list[int]:
    results: list[int] = []
    for er in cc.expected_results:
        SUCCESS = 0 if er.negate else 1
        FAILURE = 1 if er.negate else 0

        if cc.model or cc.parser:
            # All of the values to perform the search on
            data: list[str] = []

            # Get all of the value nodes into the data list
            # Convert them all to strings
            if er.search_in_value:
                if er.search_filter:
                    data = [str(x) for x in dpath.values(result, er.search_filter)]
                else:
                    data = [str(x) for x in dpath.values(result, "**")]

            # Get all of the dict keys into the data list
            # Convert them all to strings
            if er.search_in_key:
                data.extend(
                    [
                        x[0].split(";")[-1]
                        for x in dpath.search(result, "**", yielded=True, separator=";")
                    ]
                )

            if er.exact:
                if er.single:
                    results.append(SUCCESS if er.single in data else FAILURE)
                elif er.multiple and er.condition:
                    sub_results = [1 if s in data else 0 for s in er.multiple]
                    if er.condition == MultiSearchCondition.AnyMatch:
                        results.append(SUCCESS if sum(sub_results) > 0 else FAILURE)
                    elif er.condition == MultiSearchCondition.AllMatch:
                        results.append(
                            SUCCESS if sum(sub_results) == len(sub_results) else FAILURE
                        )
            else:
                if er.single:
                    results.append(
                        SUCCESS
                        if sum([1 if er.single in s else 0 for s in data]) > 0
                        else FAILURE
                    )
                elif er.multiple and er.condition:
                    sub_results = []
                    for single in er.multiple:
                        sub_results.append(
                            1 if sum([1 if single in s else 0 for s in data]) > 0 else 0
                        )
                    if er.condition == MultiSearchCondition.AnyMatch:
                        results.append(SUCCESS if sum(sub_results) > 0 else FAILURE)
                    elif er.condition == MultiSearchCondition.AllMatch:
                        results.append(
                            SUCCESS if sum(sub_results) == len(sub_results) else FAILURE
                        )
        elif cc.command:
            if er.exact:
                if er.single:
                    results.append(
                        SUCCESS if er.single == result["output"] else FAILURE
                    )
                elif er.multiple and er.condition:
                    sub_results = [
                        1 if s in result["output"] else 0 for s in er.multiple
                    ]
                    if er.condition == MultiSearchCondition.AnyMatch:
                        results.append(SUCCESS if sum(sub_results) > 0 else FAILURE)
                    elif er.condition == MultiSearchCondition.AllMatch:
                        results.append(
                            SUCCESS if sum(sub_results) == len(sub_results) else FAILURE
                        )
            else:
                if er.single:
                    results.append(
                        SUCCESS if er.single in result["output"] else FAILURE
                    )
                elif er.multiple and er.condition:
                    sub_results = [
                        1 if s in result["output"] else 0 for s in er.multiple
                    ]
                    if er.condition == MultiSearchCondition.AnyMatch:
                        results.append(SUCCESS if sum(sub_results) > 0 else FAILURE)
                    elif er.condition == MultiSearchCondition.AllMatch:
                        results.append(
                            SUCCESS if sum(sub_results) == len(sub_results) else FAILURE
                        )
    return results
