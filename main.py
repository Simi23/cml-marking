from cml_client import CmlClient
from configuration import load_config
from menu import Menu
import mark
import log_clean


def main():
    log_clean.applyFilters()

    config = load_config("configuration.json")
    client = CmlClient(config.cml.url, config.cml.username, config.cml.password)
    menu = Menu()

    menu.main_title()
    chosen_lab_id = menu.choose_labs(client.list_labs())

    print(f"User chose lab {chosen_lab_id}")
    client.prep_lab_test(chosen_lab_id)

    menu.console.clear()
    menu.console.line(2)

    for sub_criterion in config.sub_criteria:
        menu.announce_sc(f"{sub_criterion.sc_id} - {sub_criterion.name}")
        aspect_count = len(sub_criterion.aspects)
        i_aspect = 0
        is_retry = False
        while i_aspect < aspect_count:
            aspect = sub_criterion.aspects[i_aspect]
            menu.console.clear()
            menu.console.line(2)
            menu.announce_sc(f"{sub_criterion.sc_id} - {sub_criterion.name}")
            menu.announce_aspect(aspect)
            check_command_count = len(aspect.check_commands)
            i_check_command = 0

            while i_check_command < check_command_count:
                check_command = aspect.check_commands[i_check_command]
                scheduled_runs = mark.generate_runs(check_command, is_retry)
                try:
                    with menu.console.status("Running command(s) on device(s)..."):
                        results = mark.perform_runs(client, scheduled_runs)
                except Exception as e:
                    menu.announce_check_command_error(
                        check_command, i_check_command, subindex, scheduled_runs, e
                    )
                    i_check_command += 1
                    continue
                for subindex, run_result in enumerate(results):
                    try:
                        marked = mark.perform_mark(run_result[3], check_command)
                        menu.announce_check_command(
                            check_command, i_check_command, subindex, run_result, marked
                        )
                    except Exception as e:
                        menu.announce_mark_error(
                            check_command,
                            i_check_command,
                            subindex,
                            scheduled_runs[subindex],
                            e,
                        )

                i_check_command += 1

            aspect_choice = menu.aspect_finish()
            if aspect_choice == "retry":
                is_retry = True
                continue

            i_aspect += 1
            is_retry = False
    return


if __name__ == "__main__":
    main()
