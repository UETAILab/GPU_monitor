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