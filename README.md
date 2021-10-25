# System monitor script

## Overview
This project contains script to run on DataCrunch.io to control usage of GPU servers

The script will add a cronjob to a server to 
+ Send report to a specified endpoint
+ Send alert email if gpu is not used

## How to run
```
git clone https://github.com/UETAILab/GPU_monitor
cd GPU_monitor
bash setup.sh
```

## Customize
To customize your running arguments, before running `setup.sh`, navigate to `run_monitor.sh` and modify the arguments.

Available arguments:
- **MACHINE_ID**: The id of the machine. Use as an identifier to the callback server
- **GPU_MEMORY_THRESHOLD**: The minimum average gpu threshold to trigger mail alert (If average gpu usage drop below this value, send the email to recievers)
- **CALLBACK_URL**: The callback url to send recurring system monitor report
- **SENDER_EMAIL_ADDRESS**: The sender gmail account used to send alert email. (Note: The gmail address must enable unsafe apps in order for mails to be sent)
- **SENDER_EMAIL_PASSWORD**: The sender gmail account password
- **RECIEVER_EMAIL_LIST**: List of reciever email addresses, seperated by a whitespace
