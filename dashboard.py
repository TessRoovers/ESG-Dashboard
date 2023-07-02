import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plots
import streamlit.components.v1 as components
from streamlit_folium import folium_static

def main():
    st.set_page_config(
        page_title="ESG Dashboard",
        page_icon="./allenoveryicon.webp",
        layout="wide",
    )
    
    selected_option = "start"
    
    st.title("ESG Dashboard - Allen & Overy")
    st.subheader("Environmental, Social and Governance")
    st.markdown("---")
    st.write(" ")
    
    file1 = './analysis_entities/entities_timeline.csv'
    file2 = './analysis_words/groupedfrequencies.csv'
    file3 = './analysis_global/worldmap.csv'

    topics = {
            "About": ["The Project", "Allen & Overy", "Our Team"],  
            "ESG Entities": ["Proportional Frequencies", "Frequency & Clusters"],
            "ESG Topics": ["Topic Analysis", "Word Frequencies", "Global Map"],
        }
    
    st.sidebar.image("./allenovery.png")
    st.sidebar.title("Menu")
    
    for topic, subtopics in topics.items():
        with st.sidebar.expander(topic):
            for subtopic in subtopics:
                if st.checkbox(subtopic):
                    selected_option += subtopic

    if selected_option == "start":
        st.markdown("Welcome to the ESG Dashboard!  \nPlease select a topic from the menu to display.")
        st.markdown("---")
    
    # ESG Entities
    if "Proportional Frequencies" in selected_option:
        st.markdown("### ESG Entities: Proportional Frequencies")
        fig1 = plots.timeline_bar(file1)
        st.plotly_chart(fig1)
        st.markdown("---")
        st.markdown("&nbsp; ")

    if "Frequency & Clusters" in selected_option:
        st.markdown("### ESG Entities: Frequency & Clusters")
        fig2 = plots.bubble_chart(file1)
        st.plotly_chart(fig2)
        st.markdown("---")
        st.markdown("&nbsp; ")
        
        urls = pd.read_csv("./analysis_entities/entity_urls.csv")
        urls_link = urls.copy()
        
        for column in urls_link.columns:
            urls_link[column] = urls_link[column].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if isinstance(x, str) and x.startswith('http') else x)
        
        urls_link = urls_link.where(pd.notnull(urls_link), '-')
        
        entities = urls.index.tolist()
        entity_names = urls.iloc[1:, 0].values.tolist()
        
        st.markdown("### Documents with highest frequency per entity/year combination:")  
        for entity, entity_name in zip(entities, entity_names):
            with st.expander(f"**Documents for {entity_name}**"):
                years = urls.columns.tolist()
                years = years[1:]
                data = []
                
                for year in years:
                    url = urls_link.loc[entity, year]
                    data.append([year, url])
                    
                df = pd.DataFrame(data, columns=["Year", "Document"])
                st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)        
    
    # ESG Topics
    if "Topic Analysis" in selected_option:
        st.markdown("### ESG Topics: Topic Analysis")
        year = st.selectbox("Select a year:", list(range(2013, 2024)))
        html_string = plots.lda(year)
        components.html(html_string, height=1200, width=1200)
    
    # ESG Words
    if "Word Frequencies" in selected_option:
        st.markdown("### ESG Topics: Word Frequencies")
        
        df = pd.read_csv(file2)
        countries = df['Country'].unique()
        country = st.selectbox('Select country:', countries)
        filtered_data = df[df['Country'] == country]
        years = filtered_data['Year'].unique()
        years = [int(year) for year in years]
        year = st.slider('Select Year', min_value=int(min(years)), max_value=int(max(years)))
        
        fig3 = plots.grouped_frequency(filtered_data, country, year)
        st.plotly_chart(fig3)
        
        st.markdown("---")
        st.markdown("&nbsp; ")
    
    # ESG Global Map
    if "Global Map" in selected_option:
        st.markdown("### ESG Topics: Global Map")
        fig4 = plots.world_map(file3)
        folium_static(fig4, width=1200)
        st.markdown("---")
        st.markdown("&nbsp; ")
        
    # About
    if "The Project" in selected_option:
        st.markdown("### About: The Project")
        st.markdown("Our project revolves around leveraging data provided by Allen & Overy, a leading global law firm, to develop a groundbreaking solution for visualizing word frequencies in litigations related to Environmental, Social, and Governance (ESG) issues.\
            By harnessing the power of data analytics and visualization, we aim to provide valuable insights and assist legal professionals in understanding the key themes and patterns within ESG litigation cases.  \
            Through our innovative approach, we strive to contribute to the advancement of sustainable business practices and the pursuit of justice.")
        st.markdown("---")
        st.markdown("&nbsp; ")
        
    if "Allen & Overy" in selected_option:
        st.markdown("### About: Allen & Overy")
        st.markdown("Allen & Overy is a renowned global law firm with a rich history of excellence and innovation. \
            With a presence in major financial centers around the world, they are widely recognized for their exceptional legal expertise and commitment to client service. \
            Allen & Overy has been at the forefront of driving positive change in the legal industry, consistently adapting to evolving market dynamics and embracing cutting-edge technologies. \
            Their collaboration with our project showcases their dedication to leveraging data-driven insights for the benefit of their clients and the broader legal community.")
        st.markdown("---")
        st.markdown("&nbsp; ")
    
    if "Our Team" in selected_option:
        st.markdown("### About: Our Team")
        st.markdown("Our team comprises six students from the UvA: Salma, Quintijn, Tess, Max, Kayleigh, and Nabil. \
            All of us being AI students brought us together. \
            Together, we bring diverse backgrounds and expertise to the table, creating a dynamic and collaborative environment for our project.")
        st.markdown("---")
        st.markdown("&nbsp; ")


def hyperlink(url):
    if pd.notnull(url):
        return f'<a href="{url}" target="_blank">{url}</a>'
    else:
        return ''
        
if __name__ == "__main__":
    main()