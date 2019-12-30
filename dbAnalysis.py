import pandas as pd


def create_drug_data():
    df = pd.read_csv("db/drugbank_all_drugbank_vocabulary.csv/drugbank vocabulary.csv", skiprows=1, sep=',')
    #  DrugBank ID - Accession Numbers - Common name - CAS - UNII - Synonyms Standard InChI Key
    drug_id_vs_common_name = {}
    common_name_vs_synonyms = {}
    for i in range(len(df)):
        if str(df.iloc[i, 5]).split('|')[0] != 'nan':
            drug_id_vs_common_name[df.iloc[i, 0]] = df.iloc[i, 2]
            common_name_vs_synonyms[df.iloc[i, 2]] = str(df.iloc[i, 5]).split('|')
    return [drug_id_vs_common_name, common_name_vs_synonyms]
