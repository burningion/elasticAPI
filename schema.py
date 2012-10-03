from elasticutils import get_es, S

mapping = {'companies': {'properties': {'company_name': {'type': 'string'}, 'active': {'type': 'string'}, 'inactive': {'type': 'string'},}}}

es = get_es(hosts='localhost:9200', default_indexes=['dealsindex'])

def create_and_insert():
    es.delete_index_if_exists('dealsindex')
    es.create_index('dealsindex', settings={'mapping': mapping})

    companies =  [{'company_name': 'homedepot', 'active': [{'20% off': 'ZYZZ', '50% off': 'REDDIT'}], 'inactive': [{'-10% off': 'DIVIDEBYZERO'}]}, 
                  {'company_name': 'lowes', 'active': [{'15% off': 'XCX', '100% off': 'HACKERNEWS'}], 'inactive': [{'Buy one get one': 'BOGO'}]},]

    for company in companies:
        es.index(company,'dealsindex','companies')
    
    es.refresh('dealsindex')

def get_company(companyname):
    basic_s = S().indexes('dealsindex').doctypes('companies').values_dict()
    return basic_s.filter(company_name=companyname)

