from rushb.modules.modulemanager.ModuleManager import *
from rushb.modules.factory.ModuleFactory import *

import argparse
import os

if __name__ == "__main__":
    initialized = False
    finished = False
    deinitialized = False
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-loglvl",
        metavar="--loglvl",
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

    logging.basicConfig(
        level=args.loglvl * 10,
        format="{asctime} {levelname:<8} {message}",
        style="{",
        filename="%slog" % __file__[:-2],
        filemode="a"),

    logging.getLogger().addHandler(logging.StreamHandler())

    cfg_path = args.cfg
    module_manager = ModuleManger(cfg_path)
    initialized = module_manager.init()

    if initialized:
        finished = module_manager.run()

    if finished:
        deinitialized = module_manager.deinit()
