#!/usr/bin/env python
from flask import Flask, request, session, redirect, url_for, render_template
import json
import requests


app = Flask(__name__)
API_URL = 'http://127.0.0.1:8080'

def get_user_count():
    url = API_URL + '/users/'
    try:
        r = requests.get(url)
    except Exception as e:  # Gotta catch 'em all!
        return None

    result = r.json()
    return result['users']


def get_banner():
    url = API_URL + '/banner/'
    try:
        r = requests.get(url)
    except Exception as e:  # Gotta catch 'em all!
        return None

    result = r.json()
    return result['banner']


def set_banner(banner):
    url = API_URL + '/banner/'
    data = json.dumps({'banner': banner})
    try:
        r = requests.post(url, data=data)
    except Exception as e:  # Gotta catch 'em all!
        return None

@app.route("/")
def splash():
    user_count = get_user_count()
    banner = get_banner()
    return render_template('index.html', user_count=user_count, banner=banner)


@app.route('/set_banner/', methods=['POST'])
def banner():
    banner = request.values.get('banner', "")
    set_banner(banner)
    return redirect(url_for('splash'))


if __name__ == "__main__":
    app.run()
