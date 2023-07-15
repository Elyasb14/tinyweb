# ***tinyweb***

deploy on a raspberry pi with appropriate sensors using the following shell commands 

```bash
cd tinyweb
chmod +x deploy.sh
chmod +x cron.sh
sudo ./deploy.sh
./cron.sh
```
note that **cron.sh** deletes all existing cronjobs on the users account, you might have to modify these files if you are on a non debian based distro, and you will have to add correct paths in deploy.sh (keep in mind users). read scripts before blindly applying them