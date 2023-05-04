#!/bin/bash
cd "/apps/summary-bot/"

git pull

source ".venv/bin/activate"
pip install -U -q -r requirements.txt

cp scripts/summary_bot.service /etc/systemd/system/
cp scripts/summary_django.service /etc/systemd/system/

./manage.py collectstatic --noinput
./manage.py compilemessages > /dev/null
./manage.py migrate

systemctl daemon-reload
systemctl restart summary_bot
systemctl restart summary_django
echo "Finished"
