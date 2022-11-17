from rushb.modules.modulemanager.ModuleManager import *
from rushb.modules.factory.ModuleFactory import *

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname:<8} {message}",
    style="{",
    filename="%slog" % __file__[:-2],
    filemode="a"),

def main():
    cfg_path = "C:/Users/Gjergji/Repos/rushbpy/modules.yml"
    module_manager = ModuleManger(cfg_path)
    module_manager.init()
    module_manager.run()
    module_manager.deinit()

if __name__ == "__main__":
    main()