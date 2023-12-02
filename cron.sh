crontab -r
crontab -l > crontab_new
echo "*/5 * * * * python3 /home/ebianchi/tinyweb/tinyweather/main.py" >> crontab_new
crontab crontab_new
rm crontab_new
