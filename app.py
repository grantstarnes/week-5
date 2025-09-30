import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write("Did first class passengers have a higher survival rate than second and third class passengers overall?")

'''

# Titanic Visualization 1

'''

# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write("The result from the last_names function does not agree with that of the family_groups function. The last_names function simply counts" \
" the number of occurrences of each last name in the dataset, while the family_groups function identifies families based on last names and counts " \
"the number of passengers in each family. The problem arises when multiple families can share the same last name, leading to an overcount in " \
"the last_names function compared to the more accurate family grouping in the family_groups function.")

'''
# Titanic Visualization 2
'''
# Generate and display the figure
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