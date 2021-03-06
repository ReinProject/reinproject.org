from random import SystemRandom
from string import digits
from flask import Flask, request, redirect, session, render_template

application = Flask(__name__)
application.secret_key = ''.join(SystemRandom().choice(digits) for _ in range(32))

available_languages = ['en', 'lv', 'hi', 'fi', 'ru']

def get_language(headers):
    """
    Detect language using the HTTP Accept-Language header.
    """
    try:
        lang = session['reinproject-locale']
    except:
        lang = headers.get('Accept-Language')[:2]
        if lang not in available_languages:
            lang = 'en'
        session['reinproject-locale'] = lang
    return lang

def display(headers, template_name):
    """
    Wrapper around render_template for displaying localized page.
    """
    lang = get_language(headers)
    return render_template(lang + '/' + template_name)

@application.route('/')
def index():
    """Index page."""
    return display(request.headers, 'index.html')

@application.route('/<lang>')
def set_language(lang):
    """Choose language"""
    if lang in available_languages:
        session['reinproject-locale'] = lang
    return display(request.headers, 'index.html')


if __name__ == '__main__':
    application.run()
