import csv
import os
import spacy
from collections import defaultdict
import re
import pandas as pd
import plotly.graph_objects as go
import requests


def preprocess():
    """
    Code used to preprocess .txt files and apply NER analysis with SpaCy.
    Iterates through year-based folders and computes NER statistics for each year.
    Output is saved to file: ./YEAR_ner_statistics.txt
    """
    input_folders = ["1990", "1992", "1994", "1997", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2023", "2022"]
    excluded_labels = ["CARDINAL", "ORDINAL", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "GPE", "LOC"]

    nlp = spacy.load('en_core_web_lg')
    nlp.max_length = 5000000

    all_ner_stats = defaultdict(int)

    for input_folder in input_folders:
        input_folder_path = os.path.join("../data/", input_folder)

        ner_stats = defaultdict(int)

        for file_name in os.listdir(input_folder_path):
            if file_name.endswith(".txt"):
                input_file = os.path.join(input_folder_path, file_name)

                try:
                    with open(input_file, "r") as f:
                        text = f.read()
                except:
                    print("Error occurred in processing of the file:", file_name)
                    continue

                cleaned_text = preprocess_text(text)
                
                if len(cleaned_text) > nlp.max_length:
                    print(f"Text length exceeds maximum limit for file {input_file}.")
                    continue

                doc = nlp(cleaned_text)

                for entity in doc.ents:
                    if entity.label_ not in excluded_labels:
                        ner_stats[entity.text] += 1
                        all_ner_stats[entity.text] += 1
                

        output_file = os.path.join('./', f"{input_folder}_ner_statistics.txt")
        with open(output_file, 'w') as f:
            for entity, frequency in ner_stats.items():
                f.write(f"NER: {entity}\tFrequency: {frequency}\n")

        print(f"NER statistics for {input_folder} saved to {output_file}")


def preprocess_text(text):
    """
    Code used to preprocess individual text files.
    Output is the tokenized and cleaned text file.
    """
    tokens = text.split()
    cleaned_tokens = []

    i = 0
    while i < len(tokens):
        if tokens[i].endswith("..."):
            split_word = tokens[i]
            while i < len(tokens) - 1 and not tokens[i + 1].endswith("..."):
                i += 1
                split_word += tokens[i]
            cleaned_tokens.append(split_word)
        else:
            cleaned_tokens.append(tokens[i])
        i += 1

    cleaned_text = " ".join(cleaned_tokens)
    return cleaned_text


def combined_data():
    """
    Computes top 50 most common entities throughout all years.
    Uses .txt files generated by preprocess() and creates one csv file.
    """
    input_folder_path = "./"
    output_file = './output/output_data.csv'
    top_50 = './output/top_50.csv'

    all_ner_stats = defaultdict(int)

    for file_name in os.listdir(input_folder_path):
        if file_name.endswith(".txt"):
            input_file = os.path.join(input_folder_path, file_name)

            with open(input_file, "r") as f:
                lines = f.readlines()
                    
                for line in lines:
                    match = re.match(r'NER:\s*(.*?)\s*Frequency:\s*(\d+)', line)
                    
                    if match:
                        word = match.group(1)
                        frequency = int(match.group(2))
                        if word not in all_ner_stats:
                            all_ner_stats[word] = frequency
                        else:
                            all_ner_stats[word] += frequency

                
    with open(output_file, 'w', newline='') as o:
        writer = csv.writer(o, escapechar="\\")
        writer.writerow(['NER', 'Frequency'])
        
        for word, frequency in all_ner_stats.items():
            writer.writerow([word, frequency])
        
        print("Succesfully saved data to output.")
        
    sorted_entities = sorted(all_ner_stats.items(), key=lambda x: x[1], reverse=True)[:50]
    with open(top_50, 'w', newline='') as t:
        writer = csv.writer(t, escapechar="\\")
        writer.writerow(['NER', 'Frequency'])
        for word, frequency in sorted_entities:
            writer.writerow([word, frequency])
        
        print("Succesfully saved top 50 to output.")


entity_vars = {
        'EPA': ['EPA', 'Environmental Protection Agency'], # Regulatory Authority
        'BLM': ['BLM', 'Bureau of Land Management', 'Bureau Of Land Managament'], # Regulatory Authority
        'Exxon': ['Exxon', 'ExxonMobil'], # Corporate
        'FERC': ['FERC', 'Federal Energy Regulatory Commission'], # Regulatory Authority
        'Corps': ['Corps', 'U.S. Army Corps of Engineers', 'US Corps', 'U.S. Corps', 'US Army Corps of Engineers', 'Corps of Engineers'], # Regulatory Authority
        'FWS': ['FWS', 'U.S. Fish and Wildlife Service', 'US Fish and Wildlife Service', 'Fish and Wildlife Service'], # Regulatory Authority
        'DOE': ['DOE', 'Department of Energy'], # Regulatory Authority
        'Sierra Club': ['Sierra Club', 'SierraClub'], # NGO
        'Cal': ['Cal', 'California'], # Politics
        'NHTSA': ['NHTSA', 'National Highway Traffic Safety Administration'], # Regulatory Authority
        'Interior': ['Interior', 'U.S. Department of Interior', 'US Department of Interior', 'Department of Interior'], # Regulatory Authority
        'NMFS': ['NMFS', 'National Marine Fisheries Service'], # Regulatory Authority
        'Shell': ['Shell', 'RDS', 'Royal Dutch Shell', 'SOC', 'Shell Oil Company', 'Shell plc.', 'Shell plc'], # Corporate
        'CEQ': ['CEQ', 'Council on Environmental Quality'], # Regulatory Authority
        'the Forest Service': ['the Forest Service', 'Forest Service', 'FS', 'USFS', 'United States Forest Service'] # Regulatory Authority  
    }


def gather_stats():
    """
    Generates csv file of frequencies for top 15 entities (+variations) through time.
    Iterates through output files from preprocess() to create dictionary of counts.
    Saves output in csv file.
    """
    entity_stats = defaultdict(dict)

    for file_name in os.listdir('.'):
        if file_name.endswith('.txt') and re.match(r'\d{4}_ner_statistics\.txt', file_name):
           year = re.search(r'(\d{4})', file_name).group(1)
    
        with open(file_name, 'r') as f:
            lines = f.readlines()

            year_entity_stats = {entity: 0 for entity in entity_vars}

            for line in lines:
                match = re.match(r'NER:\s*(.*?)\s*Frequency:\s*(\d+)', line)
                if match:
                    word = match.group(1)
                    frequency = int(match.group(2))

                    for entity, variations in entity_vars.items():
                        if any(variation.lower() in word.lower() for variation in variations):
                            year_entity_stats[entity] += frequency

            for entity, frequency in year_entity_stats.items():
                entity_stats[entity][year] = frequency

    sorted_entities = sorted(entity_stats.keys(), key=lambda x: sum(entity_stats[x].values()), reverse=True)

    csv_file_path = './output/entities_timelinedata.csv'
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Entity'] + sorted(entity_stats[sorted_entities[0]].keys()))

        for entity in sorted_entities:
            row = [entity] + [entity_stats[entity].get(year, 0) for year in sorted(entity_stats[entity].keys())]
            writer.writerow(row)


def get_documents(year):
    """
    Finds document with highest frequency for each entity in given year.
    Returns dictionary with the file names. 
    """
    entities = list(entity_vars.keys())
    entity_documents = {entity: '' for entity in entities}
    entity_counts = {entity: 0 for entity in entities}
    
    folder_path = f"../data/{year}"
 
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for entity in entities:
                    entity_variations = entity_vars[entity]
                    entity_count = 0
                    for variation in entity_variations:
                        count = text.count(variation)
                        entity_count += count
                        if entity_count > entity_counts[entity]:
                            entity_counts[entity] = entity_count
                            entity_documents[entity] = file_name
            
    return entity_documents


def doc_overview(output_file):
    """
    Uses get_documents() to create csv file for all entity/year combinations.
    Output displays documents with highest frequency for entity in year.
    """
    entities = list(entity_vars.keys())
    years = range(2004, 2024)
    entity_documents = {year: get_documents(year) for year in years}

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Entity'] + list(years)
        writer.writerow(header)
        
        for entity in entities:
            row = [entity]
            for year in years:
                document = entity_documents[year][entity]
                row.append(document)
            writer.writerow(row)


def valid_url(url):
    """
    Tests whether a given url is valid.
    """  
    response = requests.head(url)
    return response.status_code == requests.codes.ok


def get_url(name):
    """
    Matches file name (string) to valid url or None.
    Dictionary of manual_urls is changed manually (invalid urls).
    Returns valid url or None.
    """
    manual_urls = {
        '2014-13726.txt': 'http://www.gpo.gov/fdsys/pkg/FR-2014-06-18/pdf/2014-13726.pdf',
        '2016-24215.txt': 'https://www.govinfo.gov/content/pkg/FR-2016-11-18/pdf/2016-24215.pdf',
        '2014-18742.txt': 'https://www.govinfo.gov/content/pkg/FR-2014-08-07/pdf/2014-18742.pdf',
        '20210526_8918_judgment-1.txt': 'http://climatecasechart.com/wp-content/uploads/sites/16/non-us-case-documents/2021/20210526_8918_judgment-1.pdf',
        '2011-20740.txt': 'https://www.govinfo.gov/content/pkg/FR-2011-09-15/pdf/2011-20740.pdf',
        '20191113_8918_reply.txt': 'http://climatecasechart.com/wp-content/uploads/sites/16/non-us-case-documents/2019/20191113_8918_reply.pdf',
        '2010-3851.txt': 'https://www.govinfo.gov/content/pkg/FR-2010-03-26/pdf/2010-3851.pdf'
    }
    
    if name.strip("'") in manual_urls:
        return manual_urls[name]
    
    url = None
    year = name[:4]
    
    if year.isnumeric():
        base_url = 'http://climatecasechart.com/wp-content/uploads/sites/16/case-documents/year'
        url = base_url.replace('year', year) + '/' + name.replace('.txt', '.pdf')

        try:
            if not valid_url(url):
                url = None
        except:
            url = None
    
    return url


def doc_url(input_file, output_file):
    """
    Finds url's for each file name (string).
    Adds valid url's to cell or leaves invalid url's emtpy.
    Output is saved to csv file.
    """        
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        header = rows[0]
        output_rows = [header]
        
        for row in rows[1:]:
            output_row = row.copy()
            for i, cell in enumerate(row):
                if i > 0 and cell.endswith('.txt'):
                    url = get_url(cell.strip("'"))
                    output_row[i] = url
            output_rows.append(output_row)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output_rows)
        
    # Invalid url's for:
    #   ''                              -> None entries
    #   '2014-13726.txt'                -> EPA, 2014
    #   '2016-24215.txt'                -> EPA, 2016
    #   '2014-18742.txt'                -> CAL, 2014 + NHTSA, 2014
    #   '20210526_8918_judgment-1.txt'  -> Shell, 2021
    #   '2011-20740.txt',               -> EPA + NHTSA + SHELL, 2011
    #   '20191113_8918_reply.txt'       -> Shell, 2019
    #   '2010-3851.txt'                 -> DOE + the Forest Service + Shell, 2010 
        
        
if __name__ == '__main__':
   doc_url('./entity_docnames.csv', './entity_urls.csv')

"""
**METHODE**

1. Preprocessen txt data -> preprocess() en preprocess_text()
    - Opslaan dictionary van entities + frequencies per jaar.
    - Format: "NER: <entity> Frequency: <frequency>" in .txt file.
2. Top 50 meestvoorkomende entities verzamelen -> combined_data()
    - Alle unieke entities in dict opslaan + itereren door year files voor optellen frequencies.
3. Handmatig non-entities verwijderen uit csv bestand.
    - Verwijderde entities: 
        Court, NEPA, Fed, Project, State, ESA, Congress, Commission, 
        GHG, /i255, CEQA, EA, Service, Plaintiff, Federal Defendants, F. Supp, Board,
        CAA, /47, LLC, ...
    - Top 15 samenstellen.
    - Acts + Statements uitgefilterd:
        'EIS': ['EIS', 'Environmental Impact Statement'],
        'APA': ['APA', 'Administrative Procedure Act'],
        'USCA': ['USCA', 'United States Code Annotated'],
        'FOIA': ['FOIA', 'Freedom of Information Act'],
        'FEIS': ['FEIS', 'Final Environmental Impact Statement'],
4. Opstellen dictionary met variaties van entities (zie entity_vars) en labels.
    - Regulatory Authority: 11x
    - Corporate:             2x
    - NGO:                   1x
    - Politics:              1x
5. Itereren door year_ner_statistics.txt files en frequencies per entity per jaar optellen -> gather_stats().
6. Output csv file voor datavisualisatie opstellen -> entities_timeline.csv
7. Opstellen overzicht documenten met hoogste frequentie voor elke entity per jaar:
    - doc_overview(): csv bestand met bestandsnamen (strings)
    - doc_url(): csv bestand met url's op basis van doc_overview() csv-bestand
"""