import platform
import subprocess
import threading
import psutil
import cpuinfo
import socket
import playsound

class SoundSystem:
    def getSpeakerVolume() -> int:
        if platform.system() == 'Windows':
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume_scalar = volume.GetMasterVolumeLevelScalar()

            return round(volume_scalar * 100)

        
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(["amixer", "get", "Master"])
                lines = output.decode().splitlines()

                for line in lines:
                    if "%" in line and "Mono:" in line or "Front Left:" in line or "Right:" in line:
                        parts = line.strip().split()
                        for part in parts:
                            if part.endswith("%") and part.startswith("["):
                                return int(part[1:-2]) if part.endswith("]%") else int(part[1:-1])
            except Exception as e:
                return None
            
    def playSound(path: str):
        threading.Thread(target=playsound.playsound, args=[path], daemon=True).start()
        

class HardwareInfo:
    def getCPU():
        info = cpuinfo.get_cpu_info()
        return {
            'brand': info.get('brand_raw', 'Unknown'),
            'arch': platform.machine(),
            'cores_physical': psutil.cpu_count(logical=False),
            'cores_logical': psutil.cpu_count(logical=True),
            'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
        }
    
    def getMemory():
        mem = psutil.virtual_memory()
        return {
            'total': f'{mem.total / (1024 ** 3):.2f} GB',
            'available': f'{mem.available / (1024 ** 3):.2f} GB',
            'used': f'{mem.used / (1024 ** 3):.2f} GB',
            'percent': f'{mem.percent} %'
        }

    def getDisk():
        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    'device': part.device,
                    'mountpoint': part.mountpoint,
                    'fstype': part.fstype,
                    'total': f'{usage.total / (1024 ** 3):.2f} GB',
                    'used': f'{usage.used / (1024 ** 3):.2f} GB',
                    'free': f'{usage.free / (1024 ** 3):.2f} GB',
                    'percent': f'{usage.percent} %'
                })
            except:
                pass
        return disks

    def getNetwork():
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        net_info = {}
        for iface_name, addrs in interfaces.items():
            net_info[iface_name] = {
                'is_up': stats[iface_name].isup if iface_name in stats else None,
                'speed': stats[iface_name].speed if iface_name in stats else None,
                'addresses': [addr.address for addr in addrs if addr.family == socket.AF_INET]
            }
        return net_info
    
    def getBattery():
        battery = psutil.sensors_battery()
        if not battery:
            return None
        return {
            'percent': f'{battery.percent} %',
            'plugged_in': battery.power_plugged,
            'time_left': f'{battery.secsleft // 60} min' if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'Unlimited'
        }