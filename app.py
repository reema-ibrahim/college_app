import pandas as pd
import streamlit as st
import numpy as np
import os

print(os.getcwd())


places = {
  'pacific west': (41.852892, -117.15689),
  'great plains': (40.808291, -102.215833),
  'midwest': (40.808291, -88.299063),
  'south east': (41.812686, -75.471863),
  'north east':(43.451894, -73.574247)
}

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


#unchanged = pd.read_csv(os.getcwd() + "/college_db.csv", sep='delimiter', header=None)
#changed = pd.read_csv(os.getcwd() + "/college_db.csv", sep='delimiter', header=None)

unchanged = pd.read_csv("college_db.csv", sep='delimiter', header=None)
changed = pd.read_csv("college_db.csv", sep='delimiter', header=None)


changed = changed.drop(labels=['in state cost', '1st industry', '2nd industry','3rd industry', '4th industry', '5th industry', 'median earning wages', 'retention rate', 'student to faculty ratio'], axis=1)



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

with st.form('CollegeForm'):
  user_act_score = st.slider(label='ACT Score', min_value=1, max_value=36, key=1)
  user_act_weight = st.slider(label='ACT Weight', min_value=0, max_value=10, key=2)
  user_undergraduate_enrollment_choice = st.slider(label='Undergrad Enrollment Size', min_value=unchanged['undergraduateenrollment'].min(), max_value=unchanged['undergraduateenrollment'].max(), key=3)
  user_undergraduate_enrollment_weight = st.slider(label='Undergrad Enrollment Size Weight', min_value=0, max_value=10, key=4)
  user_cost_preference_min_choice, user_cost_preference_max_choice = st.slider('Cost', unchanged['outofstatecost'].min(), unchanged['outofstatecost'].max(), (unchanged['outofstatecost'].min(), unchanged['outofstatecost'].max()), key=5)
  user_cost_weight = st.slider(label='Cost Weight', min_value=0, max_value=10, key=6)
  #user_location_choice = st.selectbox("Select State", options=stateslist) 
  user_location_choice = st.selectbox("Select Region", options=places.keys())
  user_location_weight = st.slider(label='ACT Weight', min_value=0, max_value=10, key=7)
  user_major_choice = st.text_input("Major Preference")
  user_acceptance_rate_choice = st.slider(label='Acceptance Rate', min_value=unchanged['acceptancerate'].min(), max_value=unchanged['acceptancerate'].max(), key=8)
  user_acceptance_rate_weight = st.slider(label='Acceptance Rate Weight', min_value=0, max_value=10, key=9)
  
  submitted2 = st.form_submit_button('Submit')
if submitted2: 
  

  user_latitude_choice = places[user_location_choice][0]
  user_longitude_choice = places[user_location_choice][1]


  changed["undergraduateenrollment"].where(~(changed.undergraduateenrollment <= user_undergraduate_enrollment_choice), 
                                        other=changed["undergraduateenrollment"]/user_undergraduate_enrollment_choice , inplace=True)
  changed["undergraduateenrollment"].where(~(changed.undergraduateenrollment >= 10000), 
                                        other=10000/changed["undergraduateenrollment"], inplace=True)
  changed["undergraduateenrollment"]=changed["undergraduateenrollment"]*100

  # changed["averageact"].where(~(changed.averageact <= user_act_score), 
  #                                       other=100, inplace=True)
  # changed["averageact"].where(~(changed.averageact != 100), 
  #                                       other=changed["averageact"]/user_act_score, inplace=True)
  changed["averageact"].where(~(changed.averageact <= user_act_score), 
                                    other=100, inplace=True)
  changed["averageact"].where(~(changed.averageact != 100), 
                                    other=(user_act_score/changed["averageact"])*100, inplace=True)


  # changed["outofstatecost"].where(~(changed.outofstatecost <= user_cost_preference_min_choice), 
  #                                       other=0, inplace=True)
  # changed["outofstatecost"].where(~(changed.outofstatecost >= user_cost_preference_max_choice), 
  #                                       other=0, inplace=True)
  # changed["outofstatecost"].where(~(changed.outofstatecost != 0), 
  #                                       other=100, inplace=True)

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

  # changed["location"].where(~(changed.location == user_location_choice), 
  #                                       other=100, inplace=True)
  # changed["location"].where(~(changed.location != 100), 
  #                                       other=0, inplace=True)


  def majors_function(collegename):
    majors=changed[changed["name"]==collegename]["majors"].apply(lambda x: x.split("\n"))
    for major in majors: 
      for i in major: 
        if i not in changed.columns:
          changed[i]=0
        changed.loc[changed[changed['name']==collegename].index.values[0], i]=1

  for college in changed['name']:
    majors_function(college)


  #changed['distance'].where(~(changed.distance>0), other=(c_distance(user_longitude, user_latitude, changed['longitude'], changed['latitude'])), inplace=True)
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
  st.write(final_df)
 

