"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request, jsonify
from FlaskWebProject3 import app

#New
from pytrends.request import TrendReq
import json
keywords = ['Google', 'R']

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


#trigger the api with "/api/v1/GetResults" and with keys words in json format will recieve the output
@app.route('/api/v1/GetResults', methods=['POST'])
def api_all():
    req_data = request.get_json()
    language = req_data['SearchTags']
    splitedData=split(language, 5)
    jsondata={}
    for x in language:
        jsondata[x]=[]
    pytrend = TrendReq(hl='en-US', tz=360)
    #df = pd.DataFrame()
    for x in splitedData:
        try:
            pytrend.build_payload(kw_list=x,cat=0,timeframe='today 3-m',geo='TW',gprop='')
            data = pytrend.interest_over_time()
            #result = data.to_json(orient='index',date_format='iso') #,date_format='iso'
            #parsed = json.loads(result)
            #jsondata.append(data)
            for y in data.index:
                for columnName in x:
                    row={"date":y.strftime('%Y-%m-%d'),"Count":str(data[columnName][y])}#
                    oldData=jsondata[columnName]
                    oldData.append(row)
                    jsondata[columnName]=oldData
        except:   
            print("Oops!", sys.exc_info()[0], "occurred.")

    return jsonify(jsondata)


def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs
