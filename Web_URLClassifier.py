import requests
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from BeautifulSoup import BeautifulSoup
import httplib
from flask import url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("home.html", title = 'Home')

@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        #URL from input
        URL = request.form['URL']

        response = requests.get(URL)
        #Check if Site Available
        if response.status_code == 200:
            #Scraping
            html = response.content
            soup = BeautifulSoup(html)
            text_analyze = (soup.find('title'))
        elif response.status_code == 500:
            return redirect(url_for('/error'))
    return render_template("classify.html", data_URL=URL, data_Text=text_analyze)

@app.route('/error', methods=['POST'])
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
