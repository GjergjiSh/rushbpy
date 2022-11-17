from rushb.modules.modulemanager.ModuleManager import *
from rushb.modules.factory.ModuleFactory import *

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname:<8} {message}",
    style="{",
    filename="%slog" % __file__[:-2],
    filemode="w"),

def main():
    cfg_path = "C:/Users/Gjergji/Repos/rushbpy/modules.ymlx"
    module_manager = ModuleManger(cfg_path)
    module_manager.init()
    try:
        #pass
        module_manager.run()
    except KeyboardInterrupt:
        print("Exiting..")


if __name__ == "__main__":
    main()