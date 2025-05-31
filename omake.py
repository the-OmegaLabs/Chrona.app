make = {
    'Sources/example.py': 'Releases/example.app',
}

















import os
import sys
import py_compile
import Frameworks.Logger as Logger

def build_project(build_map: dict[str, str]):
    Logger.output('Starting project build...')
    total = len(build_map)

    for idx, (src, dst) in enumerate(build_map.items(), start=1):
        if not os.path.exists(src):
            Logger.output(f"[{idx}/{total}] Source file not found: {src}, skipping...", type=Logger.Type.ERROR)
            sys.exit(1)

        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            py_compile.compile(src, cfile=dst, doraise=True)
            Logger.output(f"[{idx}/{total}] {src} -> {dst}", type=Logger.Type.INFO)
        except py_compile.PyCompileError as e:
            Logger.output(f"[{idx}/{total}] Syntax error in {src}:\n{e}", type=Logger.Type.ERROR)
            sys.exit(1)

    Logger.output('Project build complete.')

if __name__ == "__main__":
    build_project(make)


