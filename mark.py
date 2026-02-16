from cml_client import CmlClient
import configuration
import dpath


def run_check(
    client: CmlClient, cc: configuration.CheckCommand, is_retry: bool = False
):
    devices: list[str] = []
    runs: list[tuple[str, str, str, dict]] = []

    result_filter = cc.result_filter or ["**"]

    if cc.device_name:
        devices.append(cc.device_name)

    for d in devices:
        if cc.model:
            result = client.learn_device_info(
                d, cc.model, filter=result_filter, use_cache=(not is_retry)
            )
            runs.append((d, "model", cc.model, result))
        elif cc.parser:
            result = client.parse_device_info(
                d, cc.parser, filter=result_filter, use_cache=(not is_retry)
            )
            runs.append((d, "parser", cc.parser, result))
        elif cc.command:
            result = client.run_device_command(d, cc.command, use_cache=(not is_retry))
            runs.append((d, "command", cc.command, result))
    return runs


def perform_mark(result: dict, cc: configuration.CheckCommand) -> list[int]:
    results: list[int] = []
    for er in cc.expected_results:
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
            if er.search_in_value:
                data.extend(
                    [
                        x[0].split(";")[-1]
                        for x in dpath.search(result, "**", yielded=True, separator=";")
                    ]
                )

            if er.single:
                results.append(1 if er.single in data else 0)
        elif cc.command:
            if er.single:
                results.append(1 if er.single == result["output"] else 0)
    return results
