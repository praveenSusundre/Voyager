from flask import Flask, render_template, request, redirect, url_for
import json
import pandas as pd
from math import ceil

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

def url_for_other_page(page, category):
    args = request.view_args.copy()
    args['page'] = page
    args['category'] = category
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/historicplace", methods=['POST', 'GET'], defaults={'page' : 1, 'category' : None})
@app.route("/historicplace/<category>/page/<int:page>")
def historicplace(page, category):
    places = pd.read_json('places_final.json', orient='columns')
    pl = []
    img = []
    names = []
    rates = []
    if request.method == 'POST':
        cat = request.form['category']
        print(cat)
        file1 = places[places['category'] == cat]
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

        start_index = sender(page, length)
        end_index = start_index + 10

        if end_index > length:
            end_index = length

        return render_template('historicaltemp.html', rates = rates[start_index:end_index], places = pl[start_index:end_index], images = img[start_index:end_index], names = names[start_index:end_index], pagination = pagination, category = cat)
    elif category != None:
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

        start_index = sender(page, length)
        end_index = start_index + 10

        if end_index > length:
            end_index = length

        return render_template('historicaltemp.html', rates = rates[start_index:end_index], places = pl[start_index:end_index], images = img[start_index:end_index], names = names[start_index:end_index], pagination = pagination, category = category)


@app.route("/placeinfo/<placename>")
def placeinfo(placename):
    places = pd.read_json('places_final.json', orient='columns')
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

    return render_template('moreinfo.html', rates = rates, places = places, images = images, names = names, city = city)

if __name__ == "__main__":
    app.run(debug=True)
