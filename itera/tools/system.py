import psutil
import subprocess

def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)

def system_info() -> dict:
    """Retrieve detailed system information (CPU, RAM, Disk, Battery)."""
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu": {
            "logical": psutil.cpu_count(logical=True),
            "physical": psutil.cpu_count(logical=False),
            "usage_percent": psutil.cpu_percent(interval=1),
        },
        "ram": {
            "usage_percent": ram.percent,
            "total_gb": bytes_to_gb(ram.total),
        },
        "disk": {
            "usage_percent": disk.percent,
            "total_gb": bytes_to_gb(disk.total),
            "used_gb": bytes_to_gb(disk.used),
            "free_gb": bytes_to_gb(disk.free),
        },
        "battery": (
            {
                "percent": psutil.sensors_battery().percent,
                "charging": psutil.sensors_battery().power_plugged,
            }
            if psutil.sensors_battery()
            else None
        ),
    }

def run_command(cmd: str) -> str:
    """Execute a shell command and return its output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr
