from rushb.modules.modulemanager.ModuleManager import *
from rushb.modules.factory.ModuleFactory import *


def main():
    cfg_path = "C:/Users/Gjergji/Repos/rushbpy/modules.yml"
    module_manager = ModuleManger(cfg_path)
    module_manager.init()
    try:
        #pass
        module_manager.run()
    except KeyboardInterrupt:
        print("Exiting..")


if __name__ == "__main__":
    main()