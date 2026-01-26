from cml_client import CmlClient
from configuration import load_config


def main():
    config = load_config("configuration.json")
    client = CmlClient(config.cml.url, config.cml.username, config.cml.password)

    labs = client.list_labs()
    client.prep_lab_test(labs[0].id)
    return


if __name__ == "__main__":
    main()
