import pandas as pd  
import plotly.express as px  
import streamlit as st  

st.set_page_config(page_title="Alumni System Dashboard", page_icon=":mortar_board:", layout="wide")

@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("alumini_data.csv")  
    return df

df = get_data_from_csv()

st.sidebar.header("Please Filter Here:")

name = st.sidebar.multiselect(
    "Select Name:",
    options=df["Name"].unique(),
    default=[]
)

platform = st.sidebar.multiselect(
    "Select Platform:",
    options=df["Platform"].unique(),
    default=[]
)

search_button = st.sidebar.button("Search")

if search_button:
    query_string = ""
    if name:
        query_string += "`Name` == @name"
    if platform:
        if query_string:
            query_string += " & "
        query_string += "`Platform` == @platform"

    df_selection = df.query(query_string) if query_string else df  

    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop()  

    st.title(":mortar_board: Alumni System Dashboard")
    st.markdown("##")

    total_participants = int(df_selection.shape[0])  

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Total Participants:")
        st.subheader(f"{total_participants:,}")

    st.markdown("""---""")

    points_by_name = df_selection.groupby("Name")["Points"].sum().reset_index()
    
    # Bar chart for all participants
    fig_points = px.bar(
        points_by_name,
        x="Name",
        y="Points",
        title="<b>Points by Alumni</b>",
        color="Points",
        color_continuous_scale="blues",
        template="plotly_white",
    )
    
    fig_points.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )
    
    st.plotly_chart(fig_points, use_container_width=True)

    # Bar chart for top 5 alumni based on points
    top_5 = points_by_name.nlargest(5, "Points")
    fig_top5 = px.bar(
        top_5,
        x="Name",
        y="Points",
        title="<b>Top 5 Alumni by Points</b>",
        color="Points",
        color_continuous_scale="oranges",
        template="plotly_white",
    )
    
    fig_top5.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
    )
    
    st.plotly_chart(fig_top5, use_container_width=True)

    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
else:
    st.info("Please select your filters and click 'Search' to see the data.")
