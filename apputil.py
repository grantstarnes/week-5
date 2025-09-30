import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# update/add code below ...

# Exercise 1: Survival Patterns

def survival_demographics():
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
    # Compute survival rate by passenger class
    grouped = (
        df.groupby("Pclass")["Survived"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "survival_rate", "count": "n_passengers"})
    )

    # Create bar chart
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

    # Format survival rate as percentage on hover/text
    fig.update_traces(
        texttemplate="%{y:.1%}",
        textposition="outside"
    )
    fig.update_yaxes(tickformat=".0%", title="Survival Rate")

    return fig

# Exercise 2: Family Size and Wealth - Family Groups

def family_groups():
    # Create a new column for family size
    df["family_size"] = df["SibSp"] + df["Parch"] + 1  # +1 to include the passenger themselves

    # Compute survival rate by family size
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
    df["LastName"] = df["Name"].str.split(",").str[0]

    last_name_count = df["LastName"].value_counts()

    return last_name_count

# Exercise 2: Family Size and Wealth - Visualization

def visualize_families():
    # Get the grouped data
    grouped = family_groups()  # calls your existing function

    # Create line chart
    fig = px.line(
        grouped,
        x="family_size",
        y="avg_fare",
        color="Pclass",
        markers=True,  # show points on the line
        hover_data=["n_passengers", "min_fare", "max_fare"],
        title="Average Fare vs Family Size by Passenger Class",
        labels={
            "family_size": "Family Size",
            "avg_fare": "Average Fare",
            "Pclass": "Passenger Class"
        }
    )

    fig.update_layout(
        xaxis=dict(dtick=1),  # show each family size as a tick
        yaxis=dict(title="Average Fare ($)"),
        legend_title="Passenger Class"
    )

    return fig