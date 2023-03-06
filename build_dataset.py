import requests
import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name')
args = parser.parse_args()

name = args.name


url="https://api.mercadolibre.com/sites/"+name+"/search?q=tv%204k&limit=50&offset="

#items = resultados#[0:6]
def arre_df(url,paging):
    consulta = requests.get(url+str(50*paging)).json()

    if consulta!={}:
        items = consulta['results']

        res_filtered = list(filter(lambda x: x['condition']=='new',items))
        variables = ['id','title','price','domain_id','condition','attributes']
        res = [dict(((key, item[key]) for key in variables)) for item in res_filtered]

        brand =[list(filter(lambda x: x['id']=='BRAND',res_1['attributes'])) for res_1 in res]
        brand_2 = [marca[0]['value_name'] for marca in brand]

        variables_2 = ['id','title','price','domain_id']
        tbl_fin = [[item[key] for key in variables_2] for item in res]
        df = pd.DataFrame(tbl_fin,columns=['item_id','title','price','domain_id'])
        df['brand']=brand_2
        return(df)


base_final = [arre_df(url,i) for i in range(10)]
base_final = pd.concat(base_final)
base_final.to_csv("data_set.csv",index=False)

