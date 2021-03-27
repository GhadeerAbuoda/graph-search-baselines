from read_csv import CSVData
from graph_search import build_SPARQL_query, build_SPARQL_query_row



def entity_relation_type(dataframe):

    relations = dataframe[dataframe.subject.str.contains('http://www.wikidata.org/entity') & dataframe.object.str.contains('http://www.wikidata.org/entity') & ~(dataframe.predicate.str.contains('P31')) ]
    entities = dataframe[dataframe.subject.str.contains('http://www.wikidata.org/entity') & dataframe.predicate.str.contains('label')]
    row_entity = set.intersection(set(entities.subject), set(relations.subject))
    #print(list(row_entity)[0])
    types = dataframe[dataframe.subject.str.contains(str(list(row_entity)[0])) & dataframe.object.str.contains('http://www.wikidata.org/entity') & (dataframe.predicate.str.contains('P31')) ] # instance of
    print(list(types.object)[0])

    return relations, entities, row_entity, types


def find_in_wiki(filename, row=''):
    filename = filename.replace('.csv', '')
    dfObj = CSVData('/Users/dewet/Downloads/SemTab2020_Table_GT_Target/Round1/temp/0AWSOW3R.csv',',')
    #print(dfObj.get_instance(0)) ##  identifier 
    #print(dfObj.get_instances())

    (rows, cols) = dfObj.data.shape
    #print(rows)
    #print(cols)
    for row in range(1, rows):
        #print(row)
        row_values = dfObj.data.iloc[row, :]
        df_results = build_SPARQL_query_row(list(row_values))
        #df1 = build_SPARQL_query(["An Unearthly Child", "Barbara Wright", 'Mervyn Pinfield'])
        if df_results is not None:
            #print(df_results.head())
            entity_relation_type(df_results)
        else:
            print("no results")

filename = '/Users/dewet/Downloads/SemTab2020_Table_GT_Target/Round1/temp/0AWSOW3R.csv'
find_in_wiki(filename)