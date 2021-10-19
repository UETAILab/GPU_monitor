import subprocess as sp
import psutil
import logging
import argparse
import json
import requests
from mail import send_alert_mail
from utils import run_task_with_retries
import time
import datetime


def get_self(s):
    return s


def get_first(s):
    return int(s.split()[0])


"""
The config to parse into nvidia-smi
"""
GPU_UTILS = [
    ["name", "name", get_self],
    ["total_memory", "memory.total", get_first],
    ["used_memory", "memory.used", get_first],
    ["free_memory", "memory.free", get_first],
    ["gpu_utilization", "utilization.gpu", get_first],
    ["memory_utilization", "utilization.memory", get_first]
]


def get_single_gpu_info_from_output(gpu_info_output):
    """
    Get info of gpu string
    Example input: 'GeForce RTX 2080 Ti, 11019 MiB, 0 MiB, 11019 MiB, 1 %, 0 %'
    Example output: {
        "name": "GeForce RTX 2080 Ti", 
        "total_memory": "11019 MiB", 
        "used_memory": "0 MiB", 
        "free_memory": "11019 MiB",
        "gpu_utilization": "1 %",
        "memory_utilization": "0 %"
    }
    """
    values = gpu_info_output.split(", ")
    return {
        util[0]: util[2](values[idx])
        for idx, util in enumerate(GPU_UTILS)
    }


def get_gpu_info():
    """
    Get list of gpu and their info
    """
    GPU_UTILS_COMMAND = f"nvidia-smi --query-gpu={','.join([util[1] for util in GPU_UTILS])} --format=csv"

    gpu_info_outputs = sp.check_output(GPU_UTILS_COMMAND.split()).decode("ascii").split("\n")[1:-1]

    return [get_single_gpu_info_from_output(gpu_info_output) for gpu_info_output in gpu_info_outputs]


def get_cpu_info():
    """
    Get the cpu usage in percentage per cpu cores
    Example output: [7.9, 9.3, 9.1, 30.0, 8.8, 7.0, 9.8, 62.6]
    """
    return psutil.cpu_percent(interval=1, percpu=True)


def get_disk_info():
    """
    Get system disk usage information
    """
    disk_memory = psutil.disk_usage("/")
    return {
        "total_memory": disk_memory.total / 2**30,
        "used_memory": disk_memory.used / 2**30,
        "free_memory": disk_memory.free / 2**30
    }


def get_machine_full_info():
    """
    Get every information of system, including public ip address, cpu usage, gpu usage
    """
    try:
        gpu_info = get_gpu_info()
    except Exception as e:
        gpu_info = None
        logging.exception(e)
    
    try:
        cpu_info = get_cpu_info()
    except Exception as e:
        cpu_info = None
        logging.exception(e)

    try:
        disk_info = get_disk_info()
    except Exception as e:
        disk_info = None
        logging.exception(e)

    return {
        "gpu_info": gpu_info,
        "cpu_info": cpu_info,
        "disk_info": disk_info
    }


def send_report(id, data, callback_url):
    """
    Send report to another server
    """
    logging.info("Sending" , json.dumps(data, indent=4))
    requests.post(
        callback_url,
        json={
            "id": id,
            "data": data
        }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--machine_id", type=str, default="default_id", help="The machine id used to identify on the management system")
    parser.add_argument("--gpu_memory_threshold", type=int, default=100, help="Send alert when memory usage <= gpu_memory_threshold")
    parser.add_argument("--callback_url", type=str, default="http://localhost:5000/sysreport", help="The endpoint to callback in cronjob")
    parser.add_argument("--sender_email_address", type=str, default="uetailab.alert@gmail.com", help="Alert sender email address")
    parser.add_argument("--sender_email_password", type=str, default="uetailab@123", help="Alert sender email password")
    parser.add_argument("--receiver_email_list", nargs="+", type=str, default=["caohoangtung2001@gmail.com", "caohoangtung201@gmail.com"], help="List of alert receiver")
    parser.add_argument("--alert_freeze_time", type=int, default=5, help="Time in second between mail sending (use to prevent blocked from target mail server)")
    
    args = parser.parse_args()

    print(f"=== {datetime.datetime.now()} ===")

    print("TRACKER ARGS", vars(args))
    
    data = get_machine_full_info()
    

    gpu_info = data.get("gpu_info")
    if gpu_info is not None:
        gpu_details = json.dumps(gpu_info, indent=4)
        usage = sum([gpu.get("used_memory") for gpu in gpu_info]) / len(gpu_info)
        if usage <= args.gpu_memory_threshold:
            for receiver_email in args.receiver_email_list:
                """Send alert email if gpu is inactive"""
                print(f"Sending alert mail {args.sender_email_address} -> {receiver_email}")
                result = run_task_with_retries(
                    send_alert_mail, 
                    (args.sender_email_address, args.sender_email_password, receiver_email, gpu_details) 
                )
                if result is not None:
                    print(f"Alert mail sent {args.sender_email_address} -> {receiver_email}")

                time.sleep(args.alert_freeze_time)

    send_report(
        id=args.machine_id,
        data=data,
        callback_url=args.callback_url
    )

    print("="*20, "\n")
    