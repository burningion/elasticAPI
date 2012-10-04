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
import schema

from datetime import timedelta

from tornado.web import Application, RequestHandler, HTTPError

def getAPIDescription():
    a = open("APIDescription.yaml")
    return yaml.load(a)

apiDescription = getAPIDescription()
allowableOptions = apiDescription['merchantapi']['options']
# dataDictionary = schema.get_data_from_yaml()[0]

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
    def get_key_or_error(self, arguments, key):
        if (key in arguments.keys()) and (arguments[key][0] in allowableOptions):
            return arguments['status'][0]
        raise HTTPError(400)

    def get(self, merchant_name):
        status = self.get_key_or_error(self.request.arguments, 'status')
        merchant = schema.get_company(merchant_name)

        if merchant:
            self.write(unicode(merchant[0][status]))
        else:
            raise HTTPError(404)

app = Application([
    (r"/", MainHandler),
    (r"/v1/", APIHandler),
    (r"/v1/(.*)/deals", DealsHandler)
])
