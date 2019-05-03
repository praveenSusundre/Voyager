from flask import Flask, render_template, request, redirect, url_for
import json
import pandas as pd
from math import ceil
from bs4 import BeautifulSoup
from requests import get
from googlesearch import search

app = Flask(__name__)

PER_PAGE = 10


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge = 2, left_current = 2,
                    right_current = 5, right_edge = 2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or (num > self.page - left_current - 1 and num < self.page + right_current) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

def sender(page, length):
    if page == 1:
        return 0
    else:
        val = 10*(page-1)
        if(val >= length):
            return 0
        else:
            return val

def fetch_img(query):

    image_type="ActiOn"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"

    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    soup = BeautifulSoup(get(url,headers=header).text,'html.parser')

    a = soup.find("div",{"class":"rg_meta"})
    link =json.loads(a.text)["ou"]

    return link

app.jinja_env.globals['fetch_img'] = fetch_img

def url_for_other_page(page, category, state):
    args = request.view_args.copy()
    args['page'] = page
    args['category'] = category
    args['state'] = state
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/historicplace", methods=['POST', 'GET'], defaults={'page' : 1, 'category' : 'all', 'state': 'all'})
#@app.route("/historicplace/<category>/<s/page/<int:page>", defaults = {'state': 'all'})
#@app.route("/historicplace/all/<state>/page/<int:page>", defaults = {'category': 'all'})
@app.route("/historicplace/<category>/<state>/page/<int:page>")
def historicplace(page, category, state):
    places = pd.read_json('places_final.json', orient='columns')
    pl = []
    img = []
    names = []
    rates = []
    states = []
    if request.method == 'POST':
        cat = request.form['category']
        state = request.form['state']
        if cat != 'all':
            file0 = places[places['category'] == cat]
        else:
            file0 = places
        if state != 'all':
            file1 = file0[file0['state_name'] == state]
        else:
            file1 = file0

        file2 = file1.sort_values('rating',ascending = False)
        length = len(file2) #count
        pagination = Pagination(page, PER_PAGE, length)

        for place in file2['place_info']:
            pl.append(place)
        for place in file2['place_image']:
            img.append(place)
        for place in file2['place_name']:
            names.append(place)
        for place in file2['rating']:
            rates.append(place)
        for place in file2['state_name']:
            states.append(place)

        start_index = sender(page, length)
        end_index = start_index + 10

        if end_index > length:
            end_index = length

        return render_template('historicaltemp.html',states = states, rates = rates[start_index:end_index],
                                places = pl[start_index:end_index], images = img[start_index:end_index],
                                names = names[start_index:end_index], pagination = pagination, category = cat, state = state)

    elif category != 'all' and state == 'all':

        file1 = places[places['category'] == category]
        file2 = file1.sort_values('rating',ascending = False)
        length = len(file2) #count
        pagination = Pagination(page, PER_PAGE, length)

        for place in file2['place_info']:
            pl.append(place)
        for place in file2['place_image']:
            img.append(place)
        for place in file2['place_name']:
            names.append(place)
        for place in file2['rating']:
            rates.append(place)
        for place in file2['state_name']:
            states.append(place)

        start_index = sender(page, length)
        end_index = start_index + 10

        if end_index > length:
            end_index = length

        return render_template('historicaltemp.html', states = states, rates = rates[start_index:end_index],
                                places = pl[start_index:end_index], images = img[start_index:end_index],
                                names = names[start_index:end_index], pagination = pagination, category = category, state = state)

    elif category == 'all' and state == 'all':

            file2 = places.sort_values('rating',ascending = False)
            length = len(file2) #count
            pagination = Pagination(page, PER_PAGE, length)

            for place in file2['place_info']:
                pl.append(place)
            for place in file2['place_image']:
                img.append(place)
            for place in file2['place_name']:
                names.append(place)
            for place in file2['rating']:
                rates.append(place)
            for place in file2['state_name']:
                states.append(place)

            start_index = sender(page, length)
            end_index = start_index + 10

            if end_index > length:
                end_index = length

            return render_template('historicaltemp.html', states = states, rates = rates[start_index:end_index],
                                    places = pl[start_index:end_index], images = img[start_index:end_index],
                                    names = names[start_index:end_index], pagination = pagination, category = category, state = state)

    elif category == 'all' and state != 'all':

            file1 = places[places['state_name'] == state]
            file2 = file1.sort_values('rating',ascending = False)
            length = len(file2) #count
            pagination = Pagination(page, PER_PAGE, length)

            for place in file2['place_info']:
                pl.append(place)
            for place in file2['place_image']:
                img.append(place)
            for place in file2['place_name']:
                names.append(place)
            for place in file2['rating']:
                rates.append(place)
            for place in file2['state_name']:
                states.append(place)

            start_index = sender(page, length)
            end_index = start_index + 10

            if end_index > length:
                end_index = length

            return render_template('historicaltemp.html', states = states, rates = rates[start_index:end_index],
                                    places = pl[start_index:end_index], images = img[start_index:end_index],
                                    names = names[start_index:end_index], pagination = pagination, category = category, state = state)


@app.route("/placeinfo/<placename>")
def placeinfo(placename):

    pl = []
    img = []
    name = []
    rates = []
    states = []
    h_names = []


    places = pd.read_json('places_final.json', orient='columns')
    places1 = pd.read_json('places_final.json', orient='columns')
    file1 = places[places['place_name'] == placename]
    file2 = file1.sort_values('rating',ascending = False)

    for place in file2['place_info']:
        places = place
    for place in file2['place_image']:
        images = place
    for place in file2['place_name']:
        names = place
    for place in file2['rating']:
        rates = place
    for place in file2['city_name']:
        city = place


    same_city = places1[places1['city_name'] == city]
    same_city0 = same_city[same_city['place_name'] != placename]
    same_city1 = same_city0.sort_values('rating',ascending = False)


    for place in same_city1['place_name']:
        name.append(place)
    for place in same_city1['place_image']:
        img.append(place)

    hotel = pd.read_csv('Hotel.csv')
    hotel1 = hotel[hotel['city'] == city.capitalize()]

    for place in hotel1['property_name']:
        h_names.append(place)

    # to search
    query = names + ' ' + city + ' reviews'

    for j in search(query, tld="co.in", num=10, stop=1, pause=2):
        print(j)

    page = get(str(j))

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all(class_='quote')
    rev = soup.find_all(class_='partial_entry')


    return render_template('moreinfo.html', rates = rates, places = places, images = images,
                            names = names, city = city, same_city = name, image = img
                            , h_names = h_names, title = title, rev = rev)

if __name__ == "__main__":
    app.run(debug=True)
