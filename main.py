from cml_client import CmlClient
from configuration import load_config
from menu import Menu


def main():
    config = load_config("configuration.json")
    client = CmlClient(config.cml.url, config.cml.username, config.cml.password)
    menu = Menu()

    chosen_lab_id = menu.choose_labs(client.list_labs())

    print(f"User chose lab {chosen_lab_id}")
    client.prep_lab_test(chosen_lab_id)

    menu.console.clear()
    menu.console.line(2)

    for sub_criterion in config.sub_criteria:
        menu.announce_sc(f"{sub_criterion.sc_id} - {sub_criterion.name}")
        for aspect in sub_criterion.aspects:
            menu.announce_aspect(aspect)
    return


if __name__ == "__main__":
    main()
