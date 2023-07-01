import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plots
import streamlit.components.v1 as components

def main():
    
    st.set_page_config(
        page_title="ESG Dashboard",
        page_icon="./allenoveryicon.webp",
        layout="wide",
    )
    
    st.title("ESG Dashboard - Allen & Overy")
    st.subheader("Environmental, Social and Governance")
    st.write(" ")
    
    file1 = './analysis_entities/entities_timeline.csv'
    file2 = './analysis_words/groupedfrequencies.csv'

    topics = {
            "About": ["The Project", "Allen & Overy", "University of Amsterdam"],  
            "ESG Entities": ["Proportional Frequencies", "Frequency & Clusters"],
            "ESG Topics": ["Topic Analysis", "Word Frequencies"],
            "ESG Sentiment": ["Sentiment Analysis"],
        }
    
    st.sidebar.image("./allenovery.png")
    st.sidebar.title("Menu")
    
    selected_option=""
    
    for topic, subtopics in topics.items():
        with st.sidebar.expander(topic):
            for subtopic in subtopics:
                if st.button(subtopic):
                    selected_option=subtopic


    if selected_option == "":
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
    
    # ESG Sentiment
    if "Sentiment Analysis" in selected_option:
        st.markdown("### ESG Sentiment: Analysis")
        st.markdown("Coming soon.")
        st.markdown("---")
        st.markdown("&nbsp; ")
    
    # About
    if "The Project" in selected_option:
        st.markdown("### About: The Project")
        st.markdown("Information on this project: coming soon.")
        st.markdown("---")
        st.markdown("&nbsp; ")
        
    if "Allen & Overy" in selected_option:
        st.markdown("### About: Allen & Overy")
        st.markdown("Information on Allen & Overy: coming soon.")
        st.markdown("---")
        st.markdown("&nbsp; ")
    
    if "University of Amsterdam" in selected_option:
        st.markdown("### About: University of Amsterdam")
        st.markdown("Information on the UvA: coming soon.")
        st.markdown("---")
        st.markdown("&nbsp; ")
        
if __name__ == "__main__":
    main()