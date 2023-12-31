# ESG-Dashboard
Environmental, Social and Governance Dashboard

Welcome to the ESG Dashboard project!

This project was developed as part of the course 'Tweedejaarsproject' by students of the Bachelor programme Artificial Intelligence (University of Amsterdam).
The aim of this project was to create a dashboard for the law firm Allen & Overy, displaying results of Natural Language Processing (NLP) applied to legal documents.

## Description
This ESG Dashboard is a web-based dashboard that provides visualizations and analysis of Environmental, Social, and Governance (ESG) legal data. 
It aims to provide insights and facilitate decision-making related to ESG topics to the associates of Allen & Overy.

## Features
- Information about the project, Allen & Overy, and University of Amsterdam;
- Frequency and clusters analysis of ESG entities;
- Topic analysis of ESG topics;
- Word frequencies of ESG topics;
- A global map of ESG document distribution;
- Proportional frequencies of ESG entities.

### Dashboard Files
This repository includes the following files required for the dashboard:
- `dashboard.py`: Contains the dashboard initialisation.
- `plots.py`: Includes the code for figure generation.

### Data Files
The repository includes the following data files that are used for visualizations:
- `/analysis_entities/entities_timeline.csv`: ESG Entities data source.
- `/analysis_entities/entity_urls.csv`: ESG Entities data source -> hover information (URLs to documents).
- `/analysis_topics/lda_vis_{year}.0.html`: ESG Topics visualization source.
- `/analysis_words/groupedfrequencies.csv`: ESG Words data source.
- `/analysis_global/worldmap.csv`: ESG Global Map data source.

### Misc. Files
Other files that provide background insight into the project and intermediate process steps are:
- `/preprocessing/doc_scraper.ipynb`: Code used to webscrape legal documents.
- `/analysis_entities/{year}_ner_statistics.txt`: Year-based dictionaries for entity frequencies.
- `/analysis_entities/entity_docnames.csv`: Data file with document names for highest frequency entity/year combination.
- `/analysis_entities/ner.py`: Code used for Named Entity Recognition.
- `/analysis_topics/lda.ipynb`: Code used for LDA topic modelling.
- `/analysis_words/wordfrequencies.ipynb`: Code used for word frequency analysis.
- `/analysis_global/worldmap.ipynb`: Code used for the geomap.

## Usage
To use the ESG Dashboard:
1. Clone or download the repository.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Run the Streamlit application using the command `streamlit run dashboard.py`.
4. Access the dashboard through the provided URL.
