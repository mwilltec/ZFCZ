import pandas as pd
import plotly.express as px 
import streamlit as st
import plotly.graph_objects as go
import io 

@st.cache(allow_output_mutation=True)
def load_data():
    with open('datapolice.xlsx', 'rb') as f:
        data = pd.read_excel(io.BytesIO(f.read()))
    return data

df0 = load_data()
df0.columns = [column.replace(" ", "_") for column in df0.columns]
print(df0)
st.set_page_config(page_title="Danger Zones in San Francisco",
                    page_icon=":warning:",
                    layout="wide"
)
st.dataframe(df0)

#----- SIDEBAR -----
st.sidebar.header("Please Filter Here:")
dayofweek = st.sidebar.multiselect(
    "Select the WeekDay of the Incident:",
    options=df0["Incident_Day_of_Week"].unique(),
    default=df0["Incident_Day_of_Week"].unique()
)

year = st.sidebar.multiselect(
    "Select the year of the Incident:",
    options=df0["Incident_Year"].unique(),
    default=df0["Incident_Year"].unique()
)

category = st.sidebar.multiselect(
    "Select the category of the incident:",
    options=df0["Incident_Category"].unique(),
    default=df0["Incident_Category"].unique()
)

df0_selection = df0.query(
     "Incident_Day_of_Week == @dayofweek & Incident_Year == @year & Incident_Category == @category"
)

#----- MAINPAGE -----
st.title(":warning: San Francisco Danger Zones")
st.markdown("##")

# TOP KPIs
total_areas_of_vulnerability = int(df0_selection["Areas_of_Vulnerability,_2016"].sum())
total_current_police_districts = int(df0_selection["Current_Police_Districts"].sum())
total_current_supervisor_districts = int(df0_selection["Current_Supervisor_Districts"].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Areas of Vulnerability:")
    st.subheader(f"{total_areas_of_vulnerability:}")
with middle_column:
    st.subheader("Total Current Police Districts:")
    st.subheader(f"{total_current_police_districts}")
with right_column:
    st.subheader("Total Current Supervisor Districts:")
    st.subheader(f"{total_current_supervisor_districts}")

st.markdown("---")

# AREAS OF VULNERABILITY BY CATEGORY (BAR CHART)
areas_of_vulnerability_by_category = ( 
    df0_selection.groupby(by=["Incident_Category"]).sum()[["Areas_of_Vulnerability,_2016"]].sort_values(by="Areas_of_Vulnerability,_2016")
)
fig_vulnerability_category = px.bar(
    areas_of_vulnerability_by_category,
    x="Areas_of_Vulnerability,_2016",
    y=areas_of_vulnerability_by_category.index, 
    orientation="h",
    title="<b>Areas of vulnerability by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(areas_of_vulnerability_by_category),
    template="plotly_white",
)
fig_vulnerability_category.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_vulnerability_category)

#----- MAPA -----
def generar_mapa_interactivo(df0):
    data = [
        go.Scattermapbox(
            lat=df0['Latitude'],
            lon=df0['Longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=df0['Intersection']
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiYTAxNTcwOTI3IiwiYSI6ImNsaXhscDR0NzA3cGgzY281N3huZmwxaGgifQ.aEzV7kQCmfkzxXrz1EGCgQ',
            bearing=0,
            center=dict(
                lat=df0['Latitude'].mean(),
                lon=df0['Longitude'].mean()
            ),
            pitch=0,
            zoom=12
        ),
    )

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig, use_container_width=True)

#----- APP WEB DEL MAPA -----
def main():
    st.title('San Francisco Crime Zones')

    generar_mapa_interactivo(df0)

if __name__ == '__main__':
    main()




















