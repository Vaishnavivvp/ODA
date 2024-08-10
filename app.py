import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from preprocessor import preprocess
import helper
from utils import (
    fetch_medal_tally, country_year_list, data_over_time,
    most_successful
)

# Load data and preprocess
df = pd.read_csv(r'C:\Users\User\Desktop\VaiSh miniproject\Olympics-Data-Analysis-with-Deployment-main\data\athlete_events.csv')
region_df = pd.read_csv(r'C:\Users\User\Desktop\VaiSh miniproject\Olympics-Data-Analysis-with-Deployment-main\data\noc_regions.csv')

df = preprocess(df, region_df)
years, available_countries = country_year_list(df)  # Rename the list of countries to available_countries to avoid conflict


# Streamlit sidebar and menu
st.sidebar.title("Olympics Analysis")

# Display image in the sidebar
image_path = r'C:\Users\User\Desktop\VaiSh miniproject\Olympics-Data-Analysis-with-Deployment-main\img.png'
st.sidebar.image(image_path, use_column_width=True)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", available_countries)

    medal_tally = fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown("<h1 style='text-align: center; font-size: 60px;'><em>Overall Medal Tally </em></h1>", unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'><em>Medal Tally in {selected_year} Olympics </em></h1>", unsafe_allow_html=True)
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'><em>{selected_country} Overall Performance </em></h1>", unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'><em>{selected_country} Performance in {selected_year} Olympics</em></h1>", unsafe_allow_html=True)
    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    st.sidebar.header("Overall Analysis")

    # Top statistics
    editions = df['Year'].nunique()
    hosts = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    nations = df['region'].nunique()
    athletes = df['Name'].nunique()

    # Use st.markdown with HTML tags for center alignment and increased font size
    st.markdown("<h1 style='text-align: center; font-size: 60px;'><em>Top Statistics </em></h1>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(hosts)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    # Participating nations over the years
    st.title("Participating Nations Over the Years")
    nations_over_time = data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Year', y='count')
    st.plotly_chart(fig)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    # Events over the years
    st.title("Events Over the Years")
    events_over_time = data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='count')
    st.plotly_chart(fig)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    # Athletes over the years
    st.title("Athletes Over the Years")
    athletes_over_time = data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Year', y='count')
    st.plotly_chart(fig)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    # Heatmap of sports and events over leap years
    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    # Most successful athletes
    st.title("Most Successful Athletes")
    sport_selected = st.selectbox("Select a Sport", df['Sport'].unique().tolist() + ['Overall'])
    top_athletes = most_successful(df, sport_selected)
    st.table(top_athletes)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    
    # Replace NaN values with 0 in pt DataFrame
    pt.fillna(0, inplace=True)
    
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

elif user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)  # Call function from helper module
    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
    st.pyplot(fig)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)