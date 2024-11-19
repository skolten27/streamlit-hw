import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

def top_names_plot(df, year=2000, n=10, width=800, height=600, variable='count'):
    year_data = df[df['year'] == year].copy()
    year_data['overall_rank'] = year_data[variable].rank(method='min',ascending=False).astype(int)
    #rank the male names
    male_names = year_data[year_data['sex'] == 'M']
    top_male = male_names.sort_values(variable, ascending=False).head(n)
    top_male['sex_rank'] = range(1,n+1)
    #rank the female names
    female_names = year_data[year_data['sex'] == 'F']
    top_female = female_names.sort_values(variable, ascending=False).head(n)
    top_female['sex_rank'] = range(1,n+1)

    df = pd.concat[(top_male, top_female)]
    df.sort_values(variable, ascending=False, inplace=True)

    fig = px.bar(df, x='name', y=variable, color='sex',
                category_orders={"name": df['name'].tolist()},
                hover_data={'sex_rank': True, 'overall_rank': True, 'sex': False, 'name': False}) # Add custom hover
    fig.update_layout(title=f'Top {n} by sex names in {year}',
                      width=width, height=height)
    return fig