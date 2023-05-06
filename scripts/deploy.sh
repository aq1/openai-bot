#!/bin/bash
cd "/apps/openai-bot/"

git pull

source ".venv/bin/activate"
pip install -U -r requirements.txt

cp scripts/openai_dalle_bot.service /etc/systemd/system/
cp scripts/openai_summary_bot.service /etc/systemd/system/
cp scripts/openai_django.service /etc/systemd/system/

./manage.py collectstatic --noinput
./manage.py compilemessages > /dev/null
./manage.py migrate

systemctl daemon-reload
systemctl restart openai_dalle_bot
systemctl restart openai_summary_bot
systemctl restart openai_django
echo "Finished"
