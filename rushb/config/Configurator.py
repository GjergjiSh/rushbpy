import logging
import yaml


def read_config(config_path: str = "./modules.yml"):
    """ Read the module parameters from the configuration file """
    try:
        with open(config_path, "r") as stream:
            logging.info("Reading configuration file")
            yaml_file = yaml.safe_load(stream)
            return yaml_file
    except FileNotFoundError as e:
        logging.critical("Configuration file not found", exc_info=True)
        raise e


def configure_connection(config: dict) -> dict:
    """ Configure the connection mode and parameters """
    avail_selections = {1: "PUB", 2: "SUB", 3: "PUBSUB"}
    current_connection_type = f'Current connection type: {config["Connection"]["connection_type"]}'
    input_string = "Enter the connection type 1.PUB - Publisher 2.SUB - Subscriber 3.PUBSUB - Publisher and Subscriber"

    print("Connection configuration")
    selection = input(f"{current_connection_type}\n {input_string} ")
    if int(selection) in avail_selections:
        print(f"Selected connection type: {avail_selections[int(selection)]}")
        config["Connection"]["connection_type"] = avail_selections[int(selection)]
    else:
        print("Invalid selection")
        configure_connection(config)

    return config


def configure_modules(config: dict) -> dict:
    """ Configure the active modules and their parameters """
    module_names = [module["name"] for module in config["Modules"]]
    module_selections = {i: module for i, module in enumerate(module_names, 1)}
    current_modules = f'Current modules: {module_names}'

    # Select the modules to edit
    input_string = "Enter the modules to activate (separated by space starting from 1)"
    selection = input(f"{current_modules}\n {input_string} ")
    selections = selection.split(" ")
    for selection in selections:
        if int(selection) in module_selections:
            # Set the selected modules to active
            print(f"Selected module: {module_selections[int(selection)]}")
            config["Modules"][int(selection) - 1]["active"] = True

            # Get the module parameters
            module = config["Modules"][int(selection) - 1]

            # Edit the module parameters
            module_params = {key: value for key, value in module.items() if key not in ["name", "active"]}
            for param in module_params:
                current_value = f'Current value: {module_params[param]}'
                input_string = f"Enter the value for {param} : Current value {current_value} "
                parameter_selection = input(input_string)
                module_params[param] = parameter_selection
                # Update the module parameters in the config
                config["Modules"][int(selection) - 1][param] = module_params[param]
        else:
            print("Invalid selection")
            configure_modules(config)

    # Set all other modules to inactive
    for module in config["Modules"]:
        if module["name"] != module_selections[int(selection)]:
            module["active"] = False

    return config


def update_config(config: dict, config_path: str = "./modules.yml"):
    """ Update the configuration file """
    try:
        with open(config_path, "w") as stream:
            logging.info("Updating configuration file")
            # Dump the connection parameters
            yaml.dump(config, stream)
    except FileNotFoundError as e:
        logging.critical("Configuration file not found", exc_info=True)
        raise e


if __name__ == "__main__":
    cfg_path = "C:/Users/Gjergji/Repos/rushbpy/modules.yml"
    cfg = read_config(cfg_path)
    cfg = configure_connection(cfg)
    cfg = configure_modules(cfg)
    update_config(cfg, cfg_path)
    print(cfg)
