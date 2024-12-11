#TENNIS DATA ANALYSIS
import streamlit as st
import pandas as pd
import mysql.connector
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#CONNECTING SQL WITH STREAMLIT PYTHON
connection= mysql.connector.connect(
 host= "localhost",
 user= "root",
 password="",
 database="tennis_project"
 )
mycursor = connection.cursor()

#SET PAGE NAME
st.set_page_config("TENNIS_SPORT_RADAR_APPLICATION")

#SET PROJECT TITLE
st.sidebar.title("TENNIS SPORTS RADAR API ANALYSIS")

#CREATING BUTTON FOR THE DASHBOARD
st.sidebar.title("NAVIGATION")
page = st.sidebar.radio("Select a Page:", ["COMPETITIONS ANALYSIS", "COMPLEXES ANALYSIS", "COMPETITOR ANALYSIS","SUMMARY"])



#COMPETITOR PAGE 
if page =="COMPETITOR ANALYSIS":
#CREATING HEADER
    st.markdown(
    """
    <h1 style="text-align: center; color: #005cbf; font-size: 36px; margin-top: -50px;">
        COMPETITOR PERFORMANCES ANALYSIS
    </h1>
    """,
    unsafe_allow_html=True
    )

#TO GIVE SPACE
    st.write("\n")

#CREATING DATAFRAME
    mycursor.execute("select * from competitor_table")
    data = mycursor.fetchall()
    df = pd.DataFrame(data,columns=mycursor.column_names)

#TOTAL COMPETITOR BY METRIC
    TOTAL_COMPETITOR = df["competitor_id"].count()
    st.sidebar.metric(label="TOTAL COMPETITOR", value=TOTAL_COMPETITOR)

#TOTAL COMPETITOR USING METRIC
    TOTAL_COUNTRY = df["country"].nunique()
    st.sidebar.metric(label="TOTAL COUNTRY",value=TOTAL_COUNTRY)

#CREATING QUERY FOR VIEW
    mycursor.execute("""SELECT competitor_table.name,competitor_ranking_table.rank,competitor_ranking_table.points
                FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id=competitor_ranking_table.competitor_id order by points DESC""")
    joined = mycursor.fetchall()
    df1 = pd.DataFrame(joined,columns=mycursor.column_names)

#SEARCH COMPETITOR BY NAME
    mycursor.execute("""SELECT competitor_table.competitor_id,competitor_table.name,competitor_table.country,competitor_table.country_code,
                 competitor_table.abbreviation,competitor_ranking_table.competitions_played,competitor_ranking_table.rank,
                 competitor_ranking_table.points FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id = competitor_ranking_table.competitor_id""")
    joined_tab1 = mycursor.fetchall()
    df2 = pd.DataFrame(joined_tab1,columns=mycursor.column_names)
    search_name = st.sidebar.text_input("Search for a competitor by name:")

#SLIDER FOR RANK WISE
    min_rank, max_rank = st.sidebar.slider("Select rank range", 1, 50, (1, 50))

# Apply filters: search by name and rank range
    filtered_df = df2.copy()
    if search_name:
         filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]

    filtered_df = filtered_df[(filtered_df['rank'] >= min_rank) & (filtered_df['rank'] <= max_rank)]

#DISPLAY THE FILTERED DATA
    st.dataframe(filtered_df, hide_index=True)

#TO GIVE SPACE
    st.write("\n")

#SELECT BOX FOR COUNTRY WISE PERFORMANCES
    country = st.selectbox("SELECT COUNTRY TO FILTER", df2['country'].unique())
    filtered = df2[df2['country'] == country]
    if country:
         st.dataframe(filtered,hide_index=True)

#TO GIVE SPACE
    st.write("\n")

#TOTAL COMPETITOR AND AVERAGE POINTS BY COUNTRY USING PIVOT TABLE
    pivot = df2.pivot_table(
       values="points",      
       index="country",     
       aggfunc=["count", "mean"]  
    )
    pivot.columns = ["Total Competitors", "Average Points"]
    st.write("       TOTAL COMPETITOR AND AVERAGE POINTS BY COUNTRY      ")
    st.dataframe(pivot.reset_index(),hide_index=True)

#MORE COMPETITIONS PLAYED
    mycursor.execute("""SELECT name,competitions_played,rank,country from (SELECT competitor_table.competitor_id,competitor_table.name,competitor_table.country,competitor_table.country_code,
                 competitor_table.abbreviation,competitor_ranking_table.competitions_played,competitor_ranking_table.rank,
                 competitor_ranking_table.points FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id = competitor_ranking_table.competitor_id) as joinntable ORDER BY competitions_played DESC LIMIT 2""")
    joined_tab2 = mycursor.fetchall()
    df3 = pd.DataFrame(joined_tab2,columns=mycursor.column_names)
    st.sidebar.write("MORE COMPETITIONS PLAYED")
    st.sidebar.dataframe(df3,hide_index=True)

#LOW RANK COMPETITOR
    mycursor.execute("""SELECT name,rank,points,country from (SELECT competitor_table.competitor_id,competitor_table.name,competitor_table.country,competitor_table.country_code,
                 competitor_table.abbreviation,competitor_ranking_table.competitions_played,competitor_ranking_table.rank,
                 competitor_ranking_table.points FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id = competitor_ranking_table.competitor_id) as joinntable ORDER BY points DESC LIMIT 3""")
    joined_tab2 = mycursor.fetchall()
    df3 = pd.DataFrame(joined_tab2,columns=mycursor.column_names)
    st.sidebar.write("TOP 3 RANK COMPETITORS")
    st.sidebar.dataframe(df3,hide_index=True)

#HIGH RANK COMPETITOR
    mycursor.execute("""SELECT name,rank,points,country from (SELECT competitor_table.competitor_id,competitor_table.name,competitor_table.country,competitor_table.country_code,
                 competitor_table.abbreviation,competitor_ranking_table.competitions_played,competitor_ranking_table.rank,
                 competitor_ranking_table.points FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id = competitor_ranking_table.competitor_id) as joinntable ORDER BY points ASC LIMIT 3""")
    joined_tab2 = mycursor.fetchall()
    df3 = pd.DataFrame(joined_tab2,columns=mycursor.column_names)
    st.sidebar.write("LOWEST 3 RANK COMPETITORS")
    st.sidebar.dataframe(df3,hide_index=True)

#TOP 3 COUNTRIES WITH POINTS
    mycursor.execute("""SELECT country,sum(points) as Total_points from (SELECT competitor_table.competitor_id,competitor_table.name,competitor_table.country,competitor_table.country_code,
                 competitor_table.abbreviation,competitor_ranking_table.competitions_played,competitor_ranking_table.rank,
                 competitor_ranking_table.points FROM competitor_table inner join competitor_ranking_table ON 
                 competitor_table.competitor_id = competitor_ranking_table.competitor_id) as joinntable group BY country 
                 ORDER BY Total_points DESC LIMIT 3""")
    joined_tab = mycursor.fetchall()
    df4 = pd.DataFrame(joined_tab,columns=mycursor.column_names)
    st.sidebar.write("TOP THREE COUNTRIES")
    st.sidebar.dataframe(df4, hide_index=True)



#VENUES AND COMPLEXES PAGE 
elif page == "COMPLEXES ANALYSIS":
#CREATING HEADER
       st.markdown(
    """
    <h1 style="text-align: center; color: #005cbf; font-size: 36px; margin-top: -50px;">
       COMPLEXES & VENUES ANALYSIS
    </h1>
    """,
    unsafe_allow_html=True
    )
       st.subheader("COMPLEXES & VENUES ANALYSIS")
       

#give space
       st.write("\n")

#CREATING DATAFRAME USING SQL QUERY
       mycursor.execute("""SELECT complexes_table.complex_id,complexes_table.complex_name,venues_table.venue_name,venues_table.city_name,
                     venues_table.country_name,venues_table.country_code,venues_table.timezone FROM venues_table 
                 inner join complexes_table ON venues_table.complex_id=complexes_table.complex_id""")
       data_1 = mycursor.fetchall()
       df_1 = pd.DataFrame(data_1,columns=mycursor.column_names)
       df_2 = pd.DataFrame(data_1,columns=mycursor.column_names)

#TOTAL COUNTRY USING METRIC
       TOTAL_COUNTRY = df_1["country_name"].nunique()
       st.sidebar.metric(label="TOTAL COUNTRY HAVING COMPLEX",value=TOTAL_COUNTRY)

#TOTAL COMPLEX USING METRIC
       TOTAL_COMPLEX = df_1["complex_name"].nunique()
       st.sidebar.metric(label="TOTAL COMPLEX",value=TOTAL_COMPLEX)

#TOTAL VENUE USING METRIC
       TOTAL_VENUE = df_1["venue_name"].nunique()
       st.sidebar.metric(label="TOTAL VENUE",value=TOTAL_VENUE)

#CREATING SELECTBOX FOR FILTERING COMPLEX
       complex = st.sidebar.selectbox("SELECT COMPLEX TO FILTER", ['None'] + list(df_2['complex_name'].unique()))
       if complex != 'None':
            df_2 = df_2[df_2['complex_name'] == complex]  
            st.dataframe(df_2, hide_index=True)
       else:
            st.dataframe(df_2, hide_index=True)  

#FILTERING DATA UISNG THE COMPLEX AND COUNTRY IN SAME DF2 TABLE
       TOTAL_VENUE = df_2["venue_name"].nunique()
       st.sidebar.metric(label="VENUE COUNT BY COMPLEX FILTER",value=TOTAL_VENUE)

#VENUES IN EACH COMPLEXES
       st.write("VENUES IN  EACH COMPLEXES")
       mycursor.execute(""" SELECT 
                             c.complex_name, 
                             COUNT(v.venue_name) AS venue_count
                             FROM venues_table v
                             JOIN 
                             complexes_table c 
                             ON 
                             v.complex_id = c.complex_id
                             GROUP BY 
                             c.complex_name order by venue_count DESC;
                        """)
       data_2 = mycursor.fetchall()
       df_2 = pd.DataFrame(data_2,columns=mycursor.column_names)
       st.dataframe(df_2,hide_index=True)

#GIVE TOPIC FOR THE DATAFRAME
       st.write("COMPLEXES IN EACH COUNTRY")

#COUNT OF COMPLEXES IN EACH COUNTRY   
       complex_counts_by_country = df_1.groupby('country_name')['complex_name'].nunique().reset_index()
       complex_counts_by_country = complex_counts_by_country.rename(columns={'complex_name': 'complex_count'})
       st.dataframe(complex_counts_by_country, hide_index=True)




#COMPETITIONS AND CATEGORIES PAGE
elif page == "COMPETITIONS ANALYSIS":
#CREATING HEADER
       st.markdown(
    """
    <h1 style="text-align: center; color: #005cbf; font-size: 36px; margin-top: -50px;">
        COMPETITIONS ANALYSIS
    </h1>
    """,
    unsafe_allow_html=True
    )
   

#CREATING DATAFRAME USING SQL QUERY
       mycursor.execute("""SELECT competitions_table.competition_id,categories1_table.category_id,competitions_table.competition_name,categories1_table.category_name,competitions_table.gender,competitions_table.parent_id,
                        competitions_table.type FROM competitions_table
                  INNER JOIN categories1_table ON competitions_table.category_id = categories1_table.category_id;""")
       out=mycursor.fetchall()   
       table1_data = pd.DataFrame(out,columns=mycursor.column_names)
       table2_data = pd.DataFrame(out,columns=mycursor.column_names)
       
#COMPETITIONS COUNT USING METRICS
       count_competitions = len(table1_data["competition_name"].unique())
       st.sidebar.metric(label="TOTAL_COMPETITIONS",value=count_competitions)


# Count OF EACH GENDER
       count_singles = table1_data[table1_data["type"] == "singles"].shape[0]
       count_doubles = table1_data[table1_data["type"] == "doubles"].shape[0]

#GENDER COUNT USING METRIC
       st.sidebar.metric(label="TOTAL TYPE SINGLES", value=count_singles)
       st.sidebar.metric(label="TOTALTYPE DOUBLES", value=count_doubles)

#FILTERING DATAFRAME USING GENDER
       gender= st.sidebar.selectbox("GENDER",["None"] + list(table1_data["gender"].unique()))

       type = st.sidebar.selectbox("TYPE",["None"] + list(table1_data["type"].unique()))

       if gender!="None":
            table1_data = table1_data[table1_data['gender'] == gender]
       else:
            table1_data = table1_data
            
#FILTERING DATAFRAME USING TYPE
       if type!="None":
            table1_data = table1_data[table1_data['type'] == type]
       else:
            table1_data = table1_data

#DISPLAY THE FILTERED GENDER AND TYPE
       st.dataframe(table1_data,hide_index=True)
   
#GIVE SPACE
       st.write("\n")

#GIVE TITLE FOR THE COUNTPLOT AND DISPLAY THE CHART
       st.write("TYPE PERCENTAGE")
       type_counts = table1_data["type"].value_counts()
       fig, ax = plt.subplots(figsize=(3, 3))
       ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
       ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
       st.pyplot(fig)



#SUMMARY PAGE 
elif page == "SUMMARY":
#CREATING HEADER
       st.markdown(
    """
    <h1 style="text-align: center; color: #005cbf; font-size: 36px; margin-top: -50px;">
         SUMMARY
    </h1>
    """,
    unsafe_allow_html=True
    )
       

#SUMMARY FOR ALL THE ANALYSIS
       
       st.subheader("COMPETITIONS ANALYSIS:")
       st.write("1. There were 5,794 competitions conducted in total")
       st.write("2. The numbers for singles(2,897) and doubles(2,885) events are nearly balanced, with a slight difference of 12 competitions.")
       st.write("3. Male participants (3,318) outnumber female participants (2,467) significantly, with minimal participation in mixed events.")
       st.write("""CONCLUSION: The competitions show balanced distribution between singles and doubles events but with a notable gap in male and female participation, 
                highlighting male dominance in the competitions.""")
       
       
       st.subheader("COMPLEXES & VENUES ANALYSIS:")
       st.write("1. 64 countries have tennis complexes")
       st.write("2. There are 459 complexes spread across the 64 countries.")
       st.write("3. The total number of venues is 619, indicating multiple venues per complex in many locations.")
       st.write("4. The National Tennis Center complex has the highest number of venues")
       st.write("5. The USA has the most complexes, with a total of 54 complexes")
       st.write(""" CONCLUSION: The USA leads in infrastructure, having the highest number of complexes,
                 while the National Tennis Center stands out with the maximum venue count, 
                showing significant capacity and importance.""")
       

       st.subheader("COMPETITOR PERFORMANCES ANALYSIS:")
       st.write("1. There are 1,000 total competitors spanning across 79 countries. ")
       st.write("""2. The highest-ranked competitor is Katerina Siniakova with 9,530 points.
                 The second-ranked competitor is Erin Routliffe with 8,165 points.
                """)
       st.write("3. The 500th-ranked competitor, Marc Polmans, has 104 points, reflecting the lower end of the competition spectrum.")
       st.write("""4. USA leads with 88,009 total points, dominating the competition.
                    Australia is in second place with 44,024 total points.""")
       st.write("""5. The USA has the highest number of competitors at 94.
                    The second-largest group of competitors represents the Neutral category, with 68 competitors. """)
       st.write("""CONCLUSION: The USA is the strongest in the competition with 88,009 points and 94 players, the highest number of competitors. 
                   Australia is in second place with 44,024 points but is far behind the USA, partly because fewer competitors participated. 
                   The top player,Katerina Siniakova, has 9,530 points, while the second player, Erin Routliffe, has nearly 1,200 points
                   less at 8,165.This shows a big gap between the first and second positions. The lowest-ranked player, Marc Polmans, 
                   has only 104 points, showing a wide difference in skill levels. The USA gives importance to tennis games, which helps them perform better 
                   and dominate the competition.""")




       
    






