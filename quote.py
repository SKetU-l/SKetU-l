import requests
import subprocess

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

update()