# Importing streamlit and apputil modules
import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# The question I was curious about regarding the first dataset is:
st.write("Did first class passengers have a higher survival rate than second and third class passengers overall?")

'''

# Titanic Visualization 1

'''

# Generate and display the figure
# fig1 contains the bar chart I created to visualize survival rates by passenger class, pulled from apputil.py and my visualize_demographic function
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

# This is my thought regarding the difference between the last_names and family_groups functions
st.write("The result from the last_names function does not agree with that of the family_groups function. The last_names function simply counts" \
" the number of occurrences of each last name in the dataset, while the family_groups function identifies families based on last names and counts " \
"the number of passengers in each family. The problem arises when multiple families can share the same last name, leading to an overcount in " \
"the last_names function compared to the more accurate family grouping in the family_groups function.")

'''
# Titanic Visualization 2

Question the Visualization is based on: Does ticket price increase with family size across all classes (first, second, and third)?
'''

# Generate and display the figure
# fig2 contains the line chart I created to visualize ticket price by family size, pulled from apputil.py and my visualize_families function
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)