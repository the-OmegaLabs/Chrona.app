import sys
import importlib.machinery
import importlib.util
import Frameworks.Logger as Logger
from dataclasses import dataclass

@dataclass
class Configuation:
    IS_DEVMODE   = True             
    APP_PATH     = 'Sources/chrona.py'    # fallback path

    IS_LOWGPU    = False           # disable animation
    UI_SCALE     = 1               # scale of UI
    UI_FPS       = 200             # animation fps
    UI_THEME     = 'dark' 
    UI_LOCALE    = 'zh'    
    UI_ANIMATIME = 500
    UI_FAMILY    = '源流黑体 CJK'
    SET_USER     = 'root'
    SET_UID      = 1000
    SET_MUTE     = False           # disable sound play

class AppRuntime():
    def getApp(self):
        if sys.argv[-1].endswith('.py'):
            spec = importlib.util.spec_from_file_location("loaded_module", self.config.APP_PATH)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        
        elif sys.argv[-1].endswith('.app'):
            loader = importlib.machinery.SourcelessFileLoader("loaded_module", self.config.APP_PATH)
            module = loader.load_module()

        else:
            Logger.output('Unsupported executable format', type=Logger.Type.ERROR)
            exit()

        return module

    def __init__(self):
        self.config = Configuation()

        if self.config.IS_DEVMODE:
            Logger.output(f"Launching app: {self.config.APP_PATH}", type=Logger.Type.INFO)

        if self.config.IS_LOWGPU:
            self.config.UI_ANIMATIME = 0

        self.target = self.getApp()


if __name__ == "__main__":
    runtime = AppRuntime()
    runtime.target.Application(runtime.config)