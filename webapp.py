# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.
#
# Run with:
#
#   $ gunicorn -k egg:gunicorn#tornado webapp:app
#
import yaml
import glob

from datetime import timedelta

from tornado.web import Application, RequestHandler

def getAPIDescription():
    a = open("APIDescription.yaml")
    return yaml.load(a)

def getData():
    data = {}
    a = glob.iglob("data/*.yaml")
    for file in a:
        b = open(file)
        c = yaml.load(b)
        data.update(c)
        b.close()
    return data

apiDescription = getAPIDescription()
dataDictionary = getData()

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

class APIHandler(RequestHandler):
    def get(self):
        self.write(apiDescription)

class DealsHandler(RequestHandler):
    def get(self, merchant_name):
        status = self.request.arguments['status'][0]
        self.write(dataDictionary[merchant_name][status])

app = Application([
    (r"/", MainHandler),
    (r"/v1/", APIHandler),
    (r"/v1/(.*)/", DealsHandler)
])
