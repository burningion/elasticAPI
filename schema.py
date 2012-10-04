import glob
import yaml

from elasticutils import get_es, S

# def create_mapping():
#      a = open('schema/deals.yaml')
#      b = yaml.load(a)
#      a.close()
#      return b

#mapping = create_mapping()
#fileformat = [{'company_name': 'homedepot', 'active': [{'20% off': 'ZYZZ', '50% off': 'REDDIT'}], 'inactive': [{'-10% off': 'DIVIDEBYZERO'}]}, 
#             {'company_name': 'lowes', 'active': [{'15% off': 'XCX', '100% off': 'HACKERNEWS'}], 'inactive': [{'Buy one get one': 'BOGO'}]},]
mapping = {'companies': {'properties': {'company_name': {'type': 'string'}, 'active': {'type': 'string'}, 'inactive': {'type': 'string'},}}}

es = get_es(hosts='localhost:9200', default_indexes=['dealsindex'])

def get_data_from_yaml():
    data = {}
    dataList = []
    a = glob.iglob("data/*.yaml")
    for file in a:
        b = open(file)
        c = yaml.load(b)
        dataList.append(c)
        b.close()
    # Elasticsearch wants a list of dictionaries, hence the conversion
    return dataList

def create_and_insert():
    es.delete_index_if_exists('dealsindex')
    es.create_index('dealsindex', settings={'mapping': mapping})

    companies = get_data_from_yaml()

    for company in companies:
        print company
        es.index(company,'dealsindex','companies')
    
    es.refresh('dealsindex')

def get_company(companyname):
    basic_s = S().indexes('dealsindex').doctypes('companies').values_dict()
    
    return basic_s.filter(company_name=companyname)
