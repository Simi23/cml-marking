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
            data = result
            if er.search_filter:
                data = dpath.values(data, er.search_filter)
            else:
                data = dpath.values(data, "**")

            if er.single:
                results.append(1 if er.single in data else 0)
        elif cc.command:
            if er.single:
                results.append(1 if er.single == result["output"] else 0)
    return results
