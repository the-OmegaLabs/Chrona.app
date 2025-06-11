import sys
import importlib.machinery
import importlib.util
import Frameworks.Logger as Logger
from dataclasses import dataclass
import traceback

@dataclass
class Configuation:
    IS_DEVMODE   = True             
    APP_PATH     = 'Sources/Chrona.py'    # fallback path

    IS_LOWGPU    = False           # disable animation
    UI_SCALE     = 1               # scale of UI
    UI_FPS       = 500             # animation fps
    UI_THEME     = 'dark' 
    UI_LOCALE    = 'zh'    
    UI_ANIMATIME = 500 
    UI_FAMILY    = '源流黑体 CJK'
    SET_USER     = 'root'
    SET_UID      = 0
    SET_MUTE     = False

class AppRuntime():
    def loadApp(self):
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

        self.target = self.loadApp()


def tracebackProcess(exception: Exception):
    tracelist = ''.join(traceback.format_exception(exception)).split('\n')

    try:
        for i in tracelist[:-1]:
            Logger.output(i, type=Logger.Type.ERROR)
    except:
        for i in tracelist[:-1]:
            print(f'FAIL: {i}')

if __name__ == "__main__":
    try:
        runtime = AppRuntime()
        runtime.target.Application(runtime.config)
    except Exception as e:
        tracebackProcess(e)
        
