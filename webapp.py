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

from tornado.web import Application, RequestHandler, HTTPError

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
    #   Be sure to bring this up. Is every request in Tornado an object,
    #   and can I guarantee that self.arguments in this call is always
    #   immutable for the duration of call?
    def getKeyOrError(self, arguments, key):
        if key in arguments.keys():
            return arguments['status'][0]
        raise HTTPError(400)

    def get(self, merchant_name):
        status = self.getKeyOrError(self.request.arguments, 'status')
        if merchant_name in dataDictionary.keys():
            self.write(dataDictionary[merchant_name][status])
        else:
            raise HTTPError(404)

app = Application([
    (r"/", MainHandler),
    (r"/v1/", APIHandler),
    (r"/v1/(.*)/deals", DealsHandler)
])
