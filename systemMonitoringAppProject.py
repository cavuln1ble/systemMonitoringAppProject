import psutil
import time
from psutil._common import bytes2human
from tabulate import tabulate

def cpuUsage():
    return psutil.cpu_percent(percpu=True)

def memUsage():
    mem = psutil.virtual_memory()
    return {
        "total": bytes2human(mem.total),
        "available": bytes2human(mem.available),
        "percent": mem.percent,
        "used": bytes2human(mem.used),
        "free": bytes2human(mem.free)
    }

def diskUsage():
    disk = psutil.disk_usage("/")
    return {
        "total": bytes2human(disk.total),
        "used": bytes2human(disk.used),
        "free": bytes2human(disk.free)
    }

def netUsage():
    netio = psutil.net_io_counters()
    return {
        "upload": bytes2human(netio.bytes_sent),
        "download": bytes2human(netio.bytes_recv)
    }

def procMonitor():
    processes = []
    for proc in psutil.process_iter(["pid", "name", "memory_percent", "cpu_percent"]):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            continue
    processes.sort(key=lambda x: x["cpu_percent"], reverse=True)
    return processes

def displaySystemMonitor():
    procs = procMonitor()

    cpu_usage = cpuUsage()
    cpuTable = []
    for i in range(len(cpu_usage)):
        cpuTable.append([f'CPU {i+1}', cpu_usage[i]])
    print(tabulate(cpuTable, headers=['CPU', 'CPU usage']))
    
    mem_usage = memUsage()
    memTable = []
    for proc in procs:
        memTable.append([proc['name'], mem_usage['percent']])
    print(tabulate(memTable, headers=['Process', 'Memory Usage']))

displaySystemMonitor()  
    
