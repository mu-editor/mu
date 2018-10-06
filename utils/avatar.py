# Grab Gravatar images for the contributors listed in the GIT log.
import os
import subprocess
import shutil
import hashlib
import requests


def get_gravatar(email):
    """
    Given an email, attempt to get the gravatar image associated with it.
    """
    md5 = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = f"http://www.gravatar.com/avatar/{md5}?d=404&size=90"
    return requests.get(url, stream=True)


def get_github(username):
    """
    Given a GitHub username, attempt to get the user's avatar.
    """
    url = f"https://github.com/{username}.png"
    return requests.get(url, stream=True)


def get_gitlog():
    """
    Get unique tuples of username / email address from GIT log.
    """
    command = [
        "git",
        "log",
        '--pretty=format:%an|%ae',
    ]
    raw = subprocess.check_output(command,
                                  stderr=subprocess.STDOUT).decode('utf-8')
    lines = raw.split('\n')
    result = set()
    for line in lines:
        username, email = line.split('|')
        result.add((username, email))
    return tuple(result)

users = get_gitlog()
path = os.path.abspath(os.path.join('.git', 'avatar'))
if not os.path.exists(path):
    os.makedirs(path)

for (username, email) in users:
    print(f"Processing {username} {email}")
    if "users.noreply.github.com" in email:
        raw_username, _ = email.split("@")
        response = get_github(raw_username)
        _, mime = response.headers['content-type'].split('/')
    else:
        response = get_gravatar(email)
        _, mime = response.headers['content-type'].split('/')
    if response.status_code == 200:
        filename = os.path.join(path, f'{username}.{mime}')
        with open(filename, 'wb') as out_file:
            print(f"Writing to {filename}")
            shutil.copyfileobj(response.raw, out_file)
