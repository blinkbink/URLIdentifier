import requests
from flask import Flask
from flask import render_template
from flask import request
from BeautifulSoup import BeautifulSoup
import re
from Reader import dataset, feature_set, no_of_items

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html", title = 'Home')

@app.route('/classify', methods=['POST'])
def classify():
    URL = request.form['URL']
    response = requests.get(URL)

    if request.method == 'POST' and response.status_code == 200:

        #Scraping
        html = response.content
        soup = BeautifulSoup(html)
        text_analyze = (soup.find('title') or soup.find('paragraph'))

        #Replace Tag
        item_text = str(text_analyze).replace("<title>", "").replace("</title>","").replace("&amp;", "")

        #Calculate
        def calc_prob(word, category):
            if word not in feature_set or word not in dataset[category]:
                return 0
            return float(dataset[category][word]) / no_of_items[category]

        def weighted_prob(word, category):
            # probability of a word - calculated by calc_prob
            basic_prob = calc_prob(word, category)

            # total_no_of_appearances - in all the categories
            if word in feature_set:
                tot = sum(feature_set[word].values())
            else:
                tot = 0

            # Weighted probability formula
            weight_prob = ((1.0 * 0.5) + (tot * basic_prob)) / (1.0 + tot)
            return weight_prob

        def test_prob(test, category):
            # Split the test data
            split_data = re.split('[^a-zA-Z][\'][ ]', test)

            data = []
            for i in split_data:
                if ' ' in i:
                    i = i.split(' ')
                    for j in i:
                        if j not in data:
                            data.append(j.lower())
                elif len(i) > 2 and i not in data:
                    data.append(i.lower())

            p = 1
            for i in data:
                p *= weighted_prob(i, category)
            return p

        def naive_bayes(test):
            results = {}
            for i in dataset.keys():
                cat_prob = float(no_of_items[i]) / sum(no_of_items.values())

                test_prob1 = test_prob(test, i)

                results[i] = test_prob1 * cat_prob

            return results

        result = naive_bayes(item_text)

        if result['1'] > result['-1']:
            status = "Positif"
        else:
            status = "Negativ"

        return render_template("classify.html", data_URL=URL, data_Text=item_text, data_result=status, respon=response.status_code)

    elif response.status_code == 500:
        return render_template("error.html", respon="Internal Error")
    elif response.status_code == 404:
        return render_template("error.html", respon="Site Not Found")
    elif response.status_code == 403:
        return render_template("error.html", respon="Forbidden, Access Denied")
    elif response.status_code == 400:
        return render_template("error.html", respon="Bad Request")

if __name__ == '__main__':
    app.run()