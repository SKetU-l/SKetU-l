import requests
import subprocess
import schedule
import time
import datetime
from dateutil import tz

UTC = tz.gettz('Etc/UTC')
IST = tz.gettz('Asia/Kolkata')

def update():
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()
    output = data[0]['h']
    author = data[0]['a']
    output = output.replace('&mdash; ', '')
    with open('README.md', 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if i == 12:
            lines[i] = '# ' + output + '\n'
            break

    with open('README.md', 'w') as file:
        file.writelines(lines)
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f'Todays quote by {author}'])
    subprocess.run(['git', 'push'])
    print("Prepended.")

def next_run():
    utc_time = datetime.datetime.now(UTC)
    ist_time = utc_time.astimezone(IST)
    target_time = ist_time.replace(hour=00, minute=00, second=0, microsecond=0)
    target_time_utc = target_time.astimezone(UTC)
    schedule.every().day.at(target_time_utc.strftime('%H:%M')).do(update)

next_run()
while True:
    schedule.run_pending()
    time.sleep(1)
