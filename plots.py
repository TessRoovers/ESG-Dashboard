import csv
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st
import ast
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

entity_names = {
    'EPA': 'Environmental Protection Agency',
    'BLM': 'Bureau of Land Management',
    'Exxon': 'Exxon',
    'FERC': 'Federal Energy Regulatory Commission',
    'Corps': 'U.S. Army Corps of Engineers', 
    'FWS': 'U.S. Fish and Wildlife Service',
    'DOE': 'Department of Energy',
    'Sierra Club': 'Sierra Club',
    'Cal': 'California',
    'NHTSA':'National Highway Traffic Safety Administration',
    'Interior': 'U.S. Department of Interior',
    'NMFS': 'National Marine Fisheries Service',
    'Shell': 'Shell',
    'CEQ': 'Council on Environmental Quality',
    'the Forest Service': 'United States Forest Service'
}
    
entity_classes = {
        'EPA': 'Regulatory Authority',
        'BLM': 'Regulatory Authority',
        'Exxon': 'Corporate',
        'FERC': 'Regulatory Authority',
        'Corps': 'Regulatory Authority', 
        'FWS': 'Regulatory Authority',
        'DOE': 'Regulatory Authority',
        'Sierra Club': 'NGO',
        'Cal': 'Politics',
        'NHTSA': 'Regulatory Authority',
        'Interior': 'Regulatory Authority',
        'NMFS': 'Regulatory Authority',
        'Shell': 'Corporate',
        'CEQ': 'Regulatory Authority',
        'the Forest Service': 'Regulatory Authority'
    }


def timeline_bar(csv_file):
    df = pd.read_csv(csv_file)
    fig = go.Figure()
    color = 'rgb(178, 52, 39, 95)'
    totals = []
    
    for i, year in enumerate(df.columns[1:]):
        total = df[year].sum()
        totals.append(total)
        proportions = df[year] / total

        hovertext = []
        for entity, proportion in zip(df['Entity'], proportions):
            full_name = entity_names.get(entity, entity)
            hover_info = f'<b>{full_name}</b></br>Proportion: {proportion:.2f}<br>Year: {year}'
            hovertext.append(hover_info)

        fig.add_trace(go.Bar(
            x=proportions,
            y=df['Entity'],
            name=str(year),
            orientation='h',
            marker_color=color,
            hovertemplate="%{hovertext}<extra></extra>",
            hovertext=hovertext,
            ),
        )

    y_axis_range = [-0.5, len(df['Entity']) - 0.5]

    slider = dict(
        active=0,
        currentvalue={"prefix": "<b>Year:</b> "},
        pad={"t": 50},
        steps=[],
        font=dict(size=12)
    )

    for i, year in enumerate(df.columns[1:]):
        fig.update_traces(selector=dict(name=str(year)))
        total_frequency = totals[i]
        
        step = dict(
            method="update",
            args=[
                {"visible": [year == col for col in df.columns[1:]]},
                {"title.text": "<b>Entity Proportional Frequencies for "+str(year)+" (total: "+str(total_frequency)+")</b>"}
            ],
            value=str(year),
            label=str(year)
        )
        slider['steps'].append(step)

    fig.update_layout(
        barmode='group',
        sliders=[slider],
        height=1000,
        width=1200,
        margin=dict(l=100, r=100, t=100, b=100),
        yaxis=dict(range=y_axis_range, title="<b>Name of Entity</b>", ticksuffix="    ", tickmode='array', tick0=1, dtick=1, title_font=dict(size=20), tickfont=dict(size=16), automargin=True),
        xaxis=dict(range=[0,1], title="<b>Proportional Frequency</b>", title_font=dict(size=18), tickfont=dict(size=20)),
    )
    return fig


def bubble_chart(csv_file):
    df = pd.read_csv(csv_file)
    frequencies = defaultdict(dict)

    for _, row in df.iterrows():
        entity = row['Entity']
        for year in df.columns[1:]:
            if int(year) < 2004:
                continue
            else:
                frequencies[year][entity] = row[year]

    data = []
    legend_labels = list(set(entity_classes.values()))
    class_colors = {
        'Regulatory Authority': 'green',
        'Corporate': 'red',
        'NGO': 'blue',
        'Politics': 'yellow'
    }
    

    for year in frequencies:
        entities = []
        frequencies_year = []
        sizes = []
        color_values = []

        for entity in frequencies[year]:
            entities.append(entity)
            frequencies_year.append(frequencies[year][entity])
            sizes.append(frequencies[year][entity])
            
            entity_class = entity_classes.get(entity)
            if entity_class in class_colors:
                color_values.append(class_colors[entity_class])
        
        hovertext = []
        for i, entity in enumerate(entities):
            full_name = entity_names.get(entity, entity)
            hover_info = f'<b>{full_name}</b><br>Frequency: {frequencies_year[i]}<br>Year: {year}'
            hovertext.append(hover_info)
        
        data.append(
            go.Scatter(
                x=[year] * len(entities),
                y=entities,
                mode='markers',
                marker=dict(
                    size=sizes,
                    sizemode='diameter',
                    sizeref=350,
                    color=color_values,
                    opacity=0.5,
                    showscale=False,
                ),
                hovertemplate="%{hovertext}<extra></extra>",
                hovertext=hovertext,
                legendgroup='Entity Classes',
                showlegend=False,
                text=[entity_names.get(entity, entity) for entity in entities],
            )
        )

    legend_traces = []
    
    for label in legend_labels:
        color = class_colors[label]
        legend_trace = go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(size=10, color=color),
            showlegend=True,
            legendgroup=label,
            hoverinfo='none',
            name=label,
            opacity=0.5
        )
        legend_traces.append(legend_trace)
   
    data += legend_traces

    layout = go.Layout(
        xaxis=dict(title="<b>Year<b>", title_font=dict(size=20)),
        yaxis=dict(title="<b>Name of Entity<b>", type='category', ticksuffix="   ", title_font=dict(size=20)),
        height=1000,
        width=1200,
        margin=dict(l=100, r=100, t=100, b=100),
        hovermode='closest',
        showlegend=True,
    )

    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
        legend=dict(
            itemsizing='constant',
            title='<b> Entity Classes<b>',
            title_font=dict(size=18),
            bgcolor='rgba(255, 255, 255, 0.7)',
            bordercolor='gray',
            borderwidth=1,
            itemclick=False,
            itemdoubleclick=False,
            font=dict(size=16),
        ),
        margin=dict(l=100, r=100, t=100, pad=10),
    )

    for trace in data[:-len(legend_traces)]:
        fig.add_trace(trace)
    
    
    return fig

def lda(year):
    with open(f'./analysis_topics/lda_vis_{year}.0.html', 'r') as f:
        html_string = f.read()
        
    return html_string


def grouped_frequency(data_frame, country, year):
    filtered_data = data_frame[(data_frame['Country'] == country) & (data_frame['Year'] == year)]
    frequencies = []
    words = []

    for freq_list in filtered_data['Frequency']:
        if isinstance(freq_list, str):
            freq_list = ast.literal_eval(freq_list)
        
        if isinstance(freq_list, list) and len(freq_list) > 0 and isinstance(freq_list[0], tuple) and len(freq_list[0]) == 2:
            freq, word = zip(*freq_list)
            frequencies.extend(freq)
            words.extend(word)

    if len(words) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text='No words available for the selected country and year',
            xref='paper', yref='paper',
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14),
        )
    else:
        fig = go.Figure(
            data=go.Bar(
                x=words, 
                y=frequencies, 
                orientation='h'
            )
        )
        fig.update_layout(
            title=f'Top Words for {country} - {year}', 
            xaxis_title='Frequency', 
            yaxis_title='Word',
            width=1200,
            height=800,
            title_font=dict(size=18),
            font=dict(size=16)
        )
        
        fig.update_traces(
            marker=dict(color='rgb(178, 52, 39, 95)')
        )

    return fig

def world_map(csv_file):
    df = pd.read_csv(csv_file)

    # empty map
    world_map= folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(world_map)

    # for each coordinate, create circlemarker of user percent
    for i in range(len(df)):
            lat = df.iloc[i]['latitude']
            long = df.iloc[i]['longitude']
            radius=5
            popup_text = """Country : {}<br>
                        ESG-term : {}<br>
                        Link : {}<br"""
            popup_text = popup_text.format(df.iloc[i]['country'],
                                    df.iloc[i]['ESG-term'],
                                        df.iloc[i]['link']
                                    )
            folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
    
    # show the map
    return world_map
