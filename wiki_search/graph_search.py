import requests
import pandas as pd



def build_SPARQL_query_row(col_names):
    query= """ CONSTRUCT { """ 
    if col_names:
        main_triple = " ?item0 ?p0 '" + col_names[0] + "'" + "@en." +"\n"
        main_triple+= " ?item0 wdt:P31 ?itemType0." +"\n" 
    triples=""
    relations=""
    triples_lst = []
    relations_lst=[]
    optionals = ""
    for i in range(1,len(col_names)):
        triple = " ?item" + str(i)+ " ?p"+ str(i)+ " '" + col_names[i] + "'" + "@en." +"\n"
        triple+= " ?item"+ str(i)+ " wdt:P31 ?itemType"+ str(i) +" .\n" 
        triples_lst.append(triple)
        relation = "?item0 ?p1"+str(i) +" ?item"+ str(i)+" .\n"
        relations += relation
        relations_lst.append(relation)
        triples+=triple
    
    query+=main_triple+ triples + relations +"}\n" +" where {"
    query+=main_triple 
    for t, r in zip(triples_lst, relations_lst):
        optionals +="\n optional{"
        optionals += t +" "+ r +" }\n"

    #query+=triples + relations
    query+=optionals
    query+="}"
    #print(query)

    try:
        r = requests.get("https://query.wikidata.org/sparql",
                         params={'format': 'json', 'query': query},
                         headers={'User-Agent': 'agent123'},
                         timeout=12)
        results = r.json().get('results').get("bindings")
        #print("results", results)
        rows = []
        for prop in results:
            if 'subject' in prop and prop.get('subject').get('value') is not None:
                rows.append([prop.get('subject').get('value'),prop.get('predicate').get('value'),prop.get('object').get('value') ])
            
        if len(results) != 0:
            output = pd.DataFrame(rows, columns=['subject','predicate','object'], dtype=str)
        else:
            output = None
    except Exception as e: 
        print(e)
        output = None
    
    return output



def build_SPARQL_query(col_names):
    query= """ CONSTRUCT { """ 
    if col_names:
        main_triple = " ?item0 ?p0 '" + col_names[0] + "'" + "@en." +"\n"
        main_triple+= " ?item0 wdt:P31 ?itemType0." +"\n" 
    triples=""
    relations=""
    for i in range(1,len(col_names)):
        triple = " ?item" + str(i)+ " ?p"+ str(i)+ " '" + col_names[i] + "'" + "@en." +"\n"
        triple+= " ?item"+ str(i)+ " wdt:P31 ?itemType"+ str(i) +" .\n" 
        relations += "?item0 ?p1"+str(i) +" ?item"+ str(i)+" .\n"
        triples+=triple

    query+=main_triple+ triples + relations +"}\n" +" where {"
    query+=main_triple + "\n optional{"
    query+=triples + relations
    query+="} }"
    #print(query)

    try:
        r = requests.get("https://query.wikidata.org/sparql",
                         params={'format': 'json', 'query': query},
                         headers={'User-Agent': 'agent123'},
                         timeout=12)
        results = r.json().get('results').get("bindings")
        #print("results", results)
        rows = []
        for prop in results:
            if 'subject' in prop and prop.get('subject').get('value') is not None:
                rows.append([prop.get('subject').get('value'),prop.get('predicate').get('value'),prop.get('object').get('value') ])
            
        if len(results) != 0:
            output = pd.DataFrame(rows, columns=['subject','predicate','object'], dtype=str)
        else:
            output = None
    except Exception as e: print(e)
    #print(len(output))
    return output

