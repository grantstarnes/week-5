# importing plotly express and pandas
import plotly.express as px

import pandas as pd

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# Exercise 1: Survival Patterns

def survival_demographics():
    '''
    First, we create bins and labels for age categories. Then, we use pd.cut to categorize ages into these bins. Next, we group the DataFrame by passenger
    class (Pclass), sex (Sex), and age category (AgeCategory) to compute survival statistics, such as the number of passengers, number of survivors, and
    survival rate. Finally, we return the grouped DataFrame sorted by Pclass, Sex, and AgeCategory.
    '''
    bins = [0,12,19,59,float('inf')]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    
    df["AgeCategory"] = pd.cut(
        df["Age"],
        bins=bins,
        labels=labels,
        right=True
    )

    grouped = (
        df.groupby(["Pclass", "Sex", "AgeCategory"])
        .agg(
            n_passengers = ("Survived", "size"),
            n_survivors = ("Survived", "sum"),
            survival_rate = ("Survived", "mean")
        )
        .reset_index()
    )

    age_group = pd.CategoricalDtype(categories=labels, ordered=True)
    grouped["AgeCategory"] = grouped["AgeCategory"].astype(age_group)

    grouped = grouped.sort_values(by=["Pclass", "Sex", "AgeCategory"]).reset_index(drop=True)

    return grouped

# Exercise 1: Survival Patterns - Visualization (Bar Chart)

def visualize_demographic():
    '''
    This function simply creates a bar chart to visualize survival rates by passenger class using plotly. It groups the data by passenger class and
    calculates the survival rate for each class, and then creates a bar chart with appropriate labels and formatting. The x-axis represents passenger class,
    and the y-axis represents the survival rate.
    '''
    
    grouped = (
        df.groupby("Pclass")["Survived"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "survival_rate", "count": "n_passengers"})
    )

    
    fig = px.bar(
        grouped,
        x="Pclass",
        y="survival_rate",
        text="survival_rate",
        color="Pclass",
        color_continuous_scale="Blues",
        title="Survival Rate by Passenger Class",
        labels={"Pclass": "Passenger Class", "survival_rate": "Survival Rate"}
    )

    
    fig.update_traces(
        texttemplate="%{y:.1%}",
        textposition="outside"
    )
    fig.update_yaxes(tickformat=".0%", title="Survival Rate")

    return fig

# Exercise 2: Family Size and Wealth - Family Groups

def family_groups():
    '''
    This function calculates family sizes and their associated ticket prices. It creates a new column "family_size" by summing the number of 
    siblings/spouses (SibSp) and parents/children (Parch) for each passenger, adding one to include the passenger themselves. Then, it groups 
    the DataFrame by passenger class (Pclass) and family size (family_size) to compute statistics such as the number of passengers, average fare, 
    minimum fare, and maximum fare. Finally, it returns the grouped DataFrame sorted by Pclass and family size.
    '''
    
    df["family_size"] = df["SibSp"] + df["Parch"] + 1 

    
    grouped = (
        df.groupby(["Pclass", "family_size"])
        .agg(
            n_passengers = ("PassengerId", "size"),
            avg_fare = ("Fare", "mean"),
            min_fare = ("Fare", "min"),
            max_fare = ("Fare", "max")
        )
        .reset_index()
    )

    grouped = grouped.sort_values(["Pclass", "family_size"]).reset_index(drop=True)

    return grouped

# Exercise 2: Family Size and Wealth - Last Names

def last_names():
    '''
    This function extracts last names from the "Name" column and counts the number of occurrences per last name.
    It creates a new column, "LastName", by splitting the "Name" string at the comma and taking the first part, the last name [0 index].
    Then, it uses the value_counts() method to count how many times each last name appears in the dataset.
    Finally, it returns a Series with last names as the index and their counts as values.
    '''
    df["LastName"] = df["Name"].str.split(",").str[0]

    last_name_count = df["LastName"].value_counts()

    return last_name_count

# Exercise 2: Family Size and Wealth - Visualization

def visualize_families():
    '''
    This function creates a line chart to visualize the relationship between family size and average ticket fare, segmented by passenger class.
    It first calls the family_groups function to get the grouped DataFrame containing family sizes and their associated ticket prices.
    Then, it uses plotly to create a line chart with family size on the x-axis and average fare on the y-axis, with different lines for each
    passenger class (Pclass).
    '''
    grouped = family_groups()

    
    fig = px.line(
        grouped,
        x="family_size",
        y="avg_fare",
        color="Pclass",
        markers=True,  
        hover_data=["n_passengers", "min_fare", "max_fare"],
        title="Average Fare vs Family Size by Passenger Class",
        labels={
            "family_size": "Family Size",
            "avg_fare": "Average Fare",
            "Pclass": "Passenger Class"
        }
    )

    fig.update_layout(
        xaxis=dict(dtick=1),  
        yaxis=dict(title="Average Fare ($)"),
        legend_title="Passenger Class"
    )

    return fig