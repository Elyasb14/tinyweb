crontab -l > crontab_new
echo "* * * * * sleep 0s && python3 /home/ebianchi/tinyweb/tinyweather/main.py" >> crontab_new
echo " * * * * * sleep 30s && python3 /home/ebianchi/tinyweb/tinyweather/main.py" >> crontab_new
crontab crontab_new
rm crontab_new
