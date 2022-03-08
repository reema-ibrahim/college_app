
import pandas as pd
import streamlit as st
import numpy as np

st.title("U Choose")
st.write("Where we rank schools for you based off your weighted prefences")

places = {
 'Pacific West': (41.852892, -117.15689),
 'Great Plains': (40.808291, -102.215833),
 'Midwest': (40.808291, -88.299063),
 'South East': (41.812686, -75.471863),
 'North East':(43.451894, -73.574247)
}

def c_distance(d, e, f, g):
     d=d*np.pi/180
     e=e*np.pi/180
     f=f*np.pi/180
     g=g*np.pi/180
     return (np.arccos((np.sin(e)*np.sin(g))+(np.cos(e)*np.cos(g)*(np.cos(abs(d-f)))))*(3958.8)) 

def my_mapping_function(r, in_min, in_max):
 out_min = 1
 out_max = 100
 return (r - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

user_cost_preference_min_choice = 1
user_cost_preference_max_choice = 20000
user_cost_weight = 10

user_act_score = 28
user_act_weight = 5

user_undergraduate_enrollment_choice = 20000
user_undergraduate_enrollment_weight = 7

user_location_choice = 'south east'
user_location_weight = 1

user_latitude_choice = -45
user_longitude_choice =  90

user_acceptance_rate_choice = .4
user_acceptance_rate_weight = 2

user_major_choice = 'Biology'

unchanged = pd.read_csv("college_db.csv")
changed = pd.read_csv("college_db.csv")

def c_distance(d, e, f, g):
     d=d*np.pi/180
     e=e*np.pi/180
     f=f*np.pi/180
     g=g*np.pi/180
     return (np.arccos((np.sin(e)*np.sin(g))+(np.cos(e)*np.cos(g)*(np.cos(abs(d-f)))))*(3958.8)) 

def my_mapping_function(r, in_min, in_max):
 out_min = 1
 out_max = 100
 return (r - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


majors=changed["majors"].apply(lambda x: x.split("\n"))
x = (majors.to_list())
y=np.concatenate([np.array(xi) for xi in x])
majors_array = np.unique(y)

changed = changed.drop(labels=['in state cost', '1st industry', '2nd industry','3rd industry', '4th industry', '5th industry', 'median earning wages', 'retention rate', 'student to faculty ratio'], axis=1)

with st.form('CollegeForm'):
 user_act_score = st.slider(label='Enter your ACT Score', min_value=1, max_value=36, key=1)
 user_act_weight = st.slider(label='How much does this score mean to you in your college search (0 not important and 10 most important)?', min_value=0, max_value=10, key=2)
 user_undergraduate_enrollment_choice = st.slider(label='Enter what undergrad enrollment size you want in a college.', min_value=unchanged['undergraduateenrollment'].min(), max_value=unchanged['undergraduateenrollment'].max(), key=3)
 user_undergraduate_enrollment_weight = st.slider(label='How much does undergrad enrollment size mean to you in your colleges search (0 not important and 10 most important)?', min_value=0, max_value=10, key=4)
 user_cost_preference_min_choice, user_cost_preference_max_choice = st.slider('Enter how much would you want to pay for college (min and max).', unchanged['outofstatecost'].min(), unchanged['outofstatecost'].max(), (unchanged['outofstatecost'].min(), unchanged['outofstatecost'].max()), key=5)
 user_cost_weight = st.slider(label='How much does college cost mean to you (0 not important and 10 most important)?', min_value=0, max_value=10, key=6)
 user_location_choice = st.selectbox("What region would you like to go to college in?", options=places.keys())
 user_location_weight = st.slider(label='How much does location mean to you in your college search (0 not important and 10 most important)?', min_value=0, max_value=10, key=7)
 user_major_choice = st.selectbox("Major Preference", options=majors_array)
 user_acceptance_rate_choice = st.slider(label='What acceptance rate would you like your desired college to have?', min_value=unchanged['acceptancerate'].min(), max_value=unchanged['acceptancerate'].max(), key=8)
 user_acceptance_rate_weight = st.slider(label='How much does acceptance rate mean to you in your college search (0 not important and 10 most important)?', min_value=0, max_value=10, key=9)
 
 submitted2 = st.form_submit_button('Submit')
if submitted2: 
 

 user_latitude_choice = places[user_location_choice][0]
 user_longitude_choice = places[user_location_choice][1]

 changed["undergraduateenrollment"].where(~(changed.undergraduateenrollment <= user_undergraduate_enrollment_choice), 
                                       other=changed["undergraduateenrollment"]/user_undergraduate_enrollment_choice , inplace=True)
 changed["undergraduateenrollment"].where(~(changed.undergraduateenrollment >= 10000), 
                                       other=10000/changed["undergraduateenrollment"], inplace=True)
 changed["undergraduateenrollment"]=changed["undergraduateenrollment"]*100


 changed["averageact"].where(~(changed.averageact <= user_act_score), 
                                   other=100, inplace=True)
 changed["averageact"].where(~(changed.averageact != 100), 
                                   other=(user_act_score/changed["averageact"])*100, inplace=True)


 changed["outofstatecost"].where(~(unchanged.outofstatecost <= user_cost_preference_min_choice),
                             other=unchanged["outofstatecost"]/user_cost_preference_min_choice, inplace=True)
 changed["outofstatecost"].where(~(unchanged.outofstatecost >= user_cost_preference_max_choice),
                             other=user_cost_preference_max_choice/unchanged["outofstatecost"], inplace=True)
 changed["outofstatecost"].where(~(changed.outofstatecost >1),
                             other=1, inplace=True)
 changed["outofstatecost"]=changed["outofstatecost"]*100


 changed["acceptancerate"].where(~(unchanged.acceptancerate <= user_acceptance_rate_choice),
                             other=unchanged["acceptancerate"]/user_acceptance_rate_choice, inplace=True)
 changed["acceptancerate"].where(~(unchanged.acceptancerate >= user_acceptance_rate_choice),
                             other=user_acceptance_rate_choice/unchanged["acceptancerate"], inplace=True)
 changed["acceptancerate"]=changed["acceptancerate"]*100


 def majors_function(collegename):
   majors=changed[changed["name"]==collegename]["majors"].apply(lambda x: x.split("\n"))
   for major in majors: 
     for i in major: 
       if i not in changed.columns:
         changed[i]=0
       changed.loc[changed[changed['name']==collegename].index.values[0], i]=1

 for college in changed['name']:
   majors_function(college)

 changed['distance'].where(~(changed.distance>0), other=(c_distance(user_longitude_choice, user_latitude_choice, changed['longitude '], changed['latitude'])), inplace=True)
 s = changed['distance'].min()
 y = changed['distance'].max()
 changed['distance'].where(~(changed.distance>0), other=(my_mapping_function(changed['distance'], y, s)), inplace=True)



 final_df=changed[changed[user_major_choice]==1]
 

 final_df['outofstatecost'] = final_df['outofstatecost']*user_cost_weight
 final_df['averageact'] = final_df['averageact']*user_act_weight
 final_df['undergraduateenrollment']= final_df['undergraduateenrollment']*user_undergraduate_enrollment_weight
 final_df['distance']=final_df['distance']*user_location_weight
 final_df['acceptancerate'] = final_df['acceptancerate']*user_acceptance_rate_weight


 final_df["pointscolumn"] = final_df['outofstatecost'] + final_df['averageact'] + final_df['undergraduateenrollment'] + final_df['distance'] + final_df['acceptancerate']
 final_df.sort_values(["pointscolumn"], axis=0, ascending=[False], inplace=True)

 user_colleges = final_df['name'].to_list()
 


 st.write("Your college reccomendations are...")

 for name in user_colleges:
   st.write(name)


