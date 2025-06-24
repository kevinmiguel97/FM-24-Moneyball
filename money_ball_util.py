import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import re

# Import created functions
import sys
sys.path.append(r'C:\Users\kevmi\Documents\FM 24 Moneyball\FM-24-Moneyball')

from money_ball_util import *

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Show all columns in pandas
pd.set_option('display.max_columns', 500) 



#____________________________________________________________________________________________________________
# Get transfer valuation estimation

def parse_transfer_value(val):
    if pd.isnull(val):
        return None

    # Remove dollar signs and spaces
    val = val.replace('£', '').replace(' ', '')

    # If it's a range like "850K-8.4M"
    if '-' in val:
        low_str, high_str = val.split('-')
        low = parse_single_value(low_str)
        high = parse_single_value(high_str)
        if low is not None and high is not None:
            return (low + high) * (6/10)
    else:
        return parse_single_value(val)

    return None  # fallback

# -----------------------------------------------------------------------------------------------------------

def parse_single_value(s):
    try:
        if s.endswith('M'):
            return float(s[:-1]) * 1_000_000
        elif s.endswith('K'):
            return float(s[:-1]) * 1_000
        else:
            return float(s)  # just in case it's a plain number
    except:
        return None

#____________________________________________________________________________________________________________
# Scatter plot function

def scatter_plot(df, x_metric, y_metric, z_metric, 
                 title, show_color_bar=False, show_name_label=True): 
    # Set text to 'name' if show_name_label is True, else empty string
    text_col = 'name' if show_name_label else None

    # Create plotly figure
    fig = px.scatter(
        df,
        x=x_metric,
        y=y_metric,
        color=z_metric,
        text=text_col,
        color_continuous_scale='RdYlGn',
        labels={z_metric: f'Color Scale ({z_metric})'},
        title=title,
        width=1200, 
        height=700    
    )

    # Format traces
    fig.update_traces(
        marker=dict(size=10), 
        textposition='top center',
        textfont=dict(size=10),
        customdata=df[['name', 'club']],  # Always pass 'name' for hovertemplate
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" +
            "<b>%{customdata[1]}</b><br><br>" +
            f"{x_metric}: " + "%{x}<br>" +
            f"{y_metric}: " + "%{y}<br>" +
            f"{z_metric}: " + "%{marker.color}<extra></extra>"
        )
    )

    fig.update_layout(
        title={
            'text': f'{title} ({len(df): ,.0f})',
            'x': 0.5,
            'xanchor': 'center'
        },
        coloraxis_colorbar=dict(title=z_metric),
        coloraxis_showscale=show_color_bar,  # Show or hide the color bar
        plot_bgcolor='darkgray',
        paper_bgcolor='darkgray',
        xaxis=dict(showgrid=True, gridcolor='white', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='white', zeroline=False)
    )

    fig.show()
