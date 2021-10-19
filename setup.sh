pip3 install -r requirements.txt
current_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/5 * * * * bash $current_dir/run_monitor.sh >> $current_dir/log.txt" >> mycron
#install new cron file
crontab mycron
rm mycron

crontab -l

echo "Done"