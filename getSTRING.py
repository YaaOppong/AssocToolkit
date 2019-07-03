from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd

def getMapIdentifiers(loci_id_col):
    string_api_url = "http://string-gamma.org/api"
    output_format = "tsv"
    method = "get_string_ids"
    params = {
        "identifiers" : "\r".join(loci_id_col), # your protein list
        "species":83332, # species NCBI identifier 
        "limit":1, # only one (best) identifier per input protein
        "echo_query":1, # see your input identifiers in the output
        #"caller_identity" : "LSHTM" # your app nam
    }
    request_url = string_api_url + "/" + output_format + "/" + method
    try:
        response = requests.post(request_url, params=params)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit()
    return(response)

def ParseIdentifiers(response):
    lines=response.text.strip().split("\n")
    columns=lines.pop(0).split('\t')
    id_df= pd.DataFrame(columns=columns)
    for line in lines:
        l = line.split("\t")
        id_df=id_df.append(dict(zip(id_df.columns, l)), ignore_index=True)
    return(id_df)

def getNetworkInteractions(STRING_IDs):
    STRING_api_url='https://string-db.org/api/'
    request_url = STRING_api_url 
    request_url += 'tsv/'
    request_url += 'interaction_partners?identifiers=%s' % "%0d".join(STRING_IDs) 
    request_url += "&species=83332"
    #request_url += "&" + "limit=" + str(limit)
    try:
        response = requests.post(request_url, params=params)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit()
    return(reponse)

def ParseNetwork(response):
    lines=response.text.strip().split("\n")
    columns=lines.pop(0).split('\t')
    nw_df= pd.DataFrame(columns=columns)
    for line in lines:
        l = line.split("\t")
        nw_df=nw_df.append(dict(zip(nw_df.columns, l)), ignore_index=True)
    return(nw_df)


def getLociIDs(results_df):
    results_df=pd.read_csv(results,',')
    Loci_IDs=results_df['Loci_name']
    out=[]
    for name in Loci_IDs:
        newname=name.split('-')
        for splitname in newname:
            out.append(splitname)
    #LociIDs=LociIDs.str.split('-')
    return(out)


def getLociAnnotationsDF(results_df, outfile):
    Loci_IDs= getLociIDs(results_df)
    id_response=getMapIdentifiers(Loci_IDs)
    id_df=ParseIdentifiers(id_response)
    id_df.to_csv(outfile, sep='\t', mode='w')
    return(id_df)

###BELOW FUNCTIONS NEED TO BE TROUBLESHOOTED- THEY DONT APPEAR TO OUTPUT INTERACTIONS ONLY PROPERTIES (SAME AS ABOVE)
def getNetworkInteractionsDF(results_df):
    Loci_IDs= getLociIDs(results_df)
    results_df=pd.read_csv(results,',')
    companions=results_df['Companions']
    id_response=getMapIdentifiers(Loci_IDs)
    id_df=ParseIdentifiers(id_response)
    stringIds=id_df['stringId']
    nw_response=getNetworkInteractions(stringIds)
    nw_df=ParseNetwork(nw_response)
    return(nw_response)

def getInteractionsDF(results_df, out_file):
    nw_interactions_df = getNetworkInteractionsDF(results_df)
    nw_interactions_df.to_csv(outfile, header=None, index=None, sep='\t', mode='w')



