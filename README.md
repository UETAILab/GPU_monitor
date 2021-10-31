# System monitor script

## Overview
This project contains script to run on DataCrunch.io to control usage of GPU servers

The script will add a cronjob to a server to 
+ Send report to a specified endpoint
+ Send alert email if gpu is not used

## Requirements
- Python 3.6 or above
- nvidia-smi installed on the machine

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

## Run on Datacrunch
To run on datacrunch, add a new startup script with the following content:

```
git clone https://github.com/UETAILab/GPU_monitor
cd GPU_monitor
cat <<EOT > run_monitor.sh
export MACHINE_ID=some_unique_id # the unique machine id, use to identify when send report to CALLBACK_URL
export GPU_MEMORY_THRESHOLD=100 # average threshold for alert
export CALLBACK_URL=http://localhost:5000/sysreport # callback url for machine info report
export SENDER_EMAIL_ADDRESS=uetailab.alert@gmail.com # sender email address
export SENDER_EMAIL_PASSWORD=uetailab@123 # sender email password
export RECIEVER_EMAIL_LIST="caohoangtung2001@gmail.com caohoangtung201@gmail.com 19020055@vnu.edu.vn" # Email alert list

current_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 $current_dir/tracker.py --machine_id $MACHINE_ID --gpu_memory_threshold $GPU_MEMORY_THRESHOLD --callback_url $CALLBACK_URL --sender_email_address $SENDER_EMAIL_ADDRESS --sender_email_password $SENDER_EMAIL_PASSWORD --receiver_email_list $RECIEVER_EMAIL_LIST
EOT

sh setup.sh
```
