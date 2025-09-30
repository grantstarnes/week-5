import plotly.express as px
import pandas as pd

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

    age_order = pd.CategoricalDtype(categories=labels, ordered=True)
    grouped["AgeCategory"] = grouped["AgeCategory"].astype(age_order)

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