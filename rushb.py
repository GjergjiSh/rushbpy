from rushb.modulemanager.module_manager import ModuleManger

import argparse
import os
import logging

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-loglevel",
        metavar="--loglevel",
        type=int,
        default=3,
        help="Loglevel [0,5]")

    default_cfg_file = os.path.join(os.getcwd(), "modules.yml")
    parser.add_argument(
        "-cfg",
        metavar="--cfg",
        type=str,
        default=default_cfg_file,
        help="Module configuration file")

    args = parser.parse_args()

    filename = "%slog" % __file__[:-2]
    log_format = "{asctime} {levelname:<8} {message}"
    logging.basicConfig(
        level=args.loglevel * 10,
        format=log_format,
        style="{",
        handlers=[
            logging.FileHandler(filename),
            logging.StreamHandler()
        ]
    ),

    module_manager = ModuleManger(args.cfg)
    module_manager.init()
    module_manager.run()
    module_manager.deinit()
