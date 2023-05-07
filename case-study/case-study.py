import pandas as pd, numpy as np, plotly.express as px
from IPython.display import *
from ipywidgets import *
import streamlit as st
px.defaults.template = 'seaborn'
col_names = {
    "experience" : ["jonathan", "gender", "major", "year", 
                    "stat_experience", "stat_course", "stat_confidence", 
                    "cs_experience", "cs_course", "cs_confidence",
                    "scaffolding_helpful", "learn_modes", "demonstrate_modes", "mode_preference", 
                    "bank_learn", "bank_like",
                    "pose_learn", "pose_like"],
    "feedback" : ["enjoy_lab", "lecture_help", "present_mode", "discussion_helpful"],
    "welcome" : ["gender", "year", "major", "math_experience", "first_coding", "first_stats", "code_comfortable", "prepared", "succeed", "section_mode"]
}

readable_names = {
    "experience" : {
        "jonathan" : "My GSI is Jonathan",
        "gender" : "Gender",
        "major" : "Major",
        "year" : "Year",
        "stat_experience" : "I have previous Statistics Experience",
        "stat_course" : "Previous Stats Courses taken",
        "stat_confidence" : "Confidence in Stats",
        "cs_experience" : "I have previous Computer Science Experience",
        "cs_course" : "Previous CS Courses taken",
        "cs_confidence" : "Confidence in CS",
        "scaffolding_helpful" : "Scaffolding is Helpful",
        "learn_modes" : "I learn best by",
        "demonstrate_modes" : "I prefer to demonstrate my knowledge by",
        "mode_preference" : "I prefer multiple modes of presentation",
        "bank_learn" : "I learn from Banking Education",
        "bank_like" : "I like Banking Education",
        "pose_learn" : "I learn from Problem Posing Education",
        "pose_like" : "I like Problem Posing Education"
    },
    "feedback" : {
        "enjoy_lab" : "I enjoy the labs",
        "lecture_help" : "Lectures help me learn",
        "present_mode" : "I prefer this mode of presentation",
        "discussion_helpful" : "Discussions are helpful"
    },
    "welcome" : {
        "gender" : "Gender",
        "year" : "Year",
        "major" : "Major",
        "math_experience" : "Math Experience",
        "first_coding" : "First Coding",
        "first_stats" : "First Stats",
        "code_comfortable" : "Comfortable with Coding",
        "prepared" : "Background Prepared me for Data 8",
        "succeed" : "I will Succeed in Data 8",
        "section_mode" : "Prefered Section Mode"
    }
}

titles = {
    "experience" : "Data 8 Experience Survey",
    "feedback" : "Feedback Survey",
    "welcome" : "Welcome Survey"
}
@st.cache_data
def load_sheet():
    sheets = pd.read_excel("https://docs.google.com/spreadsheets/d/e/2PACX-1vTaoSrGe7BpMFvXFQnn02_HUt7t3pTWAAl1ny_A4zNkszerHWZHReQ0YkDK58qJ8_G83ih9IVqmm0IO/pub?output=xlsx", sheet_name = None)
    experience = sheets["Experience"].iloc[:, np.arange(1, 19)]
    feedback = sheets["Feedback"]
    welcome = sheets["Welcome"]
    experience.columns = col_names["experience"]
    feedback.columns = col_names["feedback"]
    welcome.columns = col_names["welcome"]
    data = {"experience" : experience, "feedback" : feedback, "welcome" : welcome}
    return data
data = load_sheet()

survey_type = st.selectbox(
    "Select Survey",
    options=list(titles.keys()),
    index=0,
    format_func=lambda x: titles[x]
)

table = data[survey_type]

column = st.selectbox(
    "Select Column",
    options=list(readable_names[survey_type].keys()),
    index=1,
    format_func=lambda x: readable_names[survey_type][x]
)
category = table[column].dtype == "object"
if category:
    category_counts = table[column].value_counts().reset_index()
    category_counts.columns = [column, 'Frequency']
    fig = px.bar(category_counts, x=column, y='Frequency', text='Frequency', color = column, text_auto=True)
    fig.update_layout(title=titles[survey_type], xaxis_title=readable_names[survey_type][column], yaxis_title="Frequency")
    
else:    
    fig = px.histogram(table, x=column, color = column, 
                        title=titles[survey_type], labels=readable_names[survey_type],
                        nbins=len(table[column].unique())+1,
                        range_x=(0, table[column].max() + 1),
                        text_auto=True)
    
fig.update_traces(textposition='outside')

st.markdown("## Histogram")
st.plotly_chart(fig)
st.markdown("## Responses")
st.dataframe(table)
st.markdown("## Statistics")
st.markdown(f"#### Count: {table[column].count()}")
if not category:
    st.markdown(f"#### Mean: {table[column].mean()}")
    st.markdown(f"#### Median: {table[column].median()}")
    st.markdown(f"#### Min: {table[column].min()}")
    st.markdown(f"#### Max: {table[column].max()}")

try:
    pass    
except:
    pass