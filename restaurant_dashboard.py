import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Custom color scale for sentiments
# ... [Your imports remain unchanged]

# Custom color scale for sentiments
color_scale = {
    'Positive': 'green',
    'Negative': 'red',
    'Neutral': 'gray'
}

# Load the data
df = pd.read_excel('reviews.xlsx', engine='openpyxl')

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout
app.layout = html.Div(style={
    'backgroundImage': 'url(https://img.freepik.com/free-photo/abstract-luxury-blur-grey-color-gradient-used-as-background-studio-wall-display-your-products_1258-52609.jpg)',
    'backgroundSize': 'cover',
    'backgroundRepeat': 'no-repeat'
}, children=[
    dbc.Container([
        html.H1("Restaurant Review Analysis", className="text-center my-5", style={'color': 'black'}),
        
        dbc.Row([
            # Left side - 1/4th
            dbc.Col([
                dbc.Label("Select a Restaurant", style={'color': 'black'}),
                dcc.Dropdown(
                    id='restaurant-dropdown',
                    options=[{'label': restaurant, 'value': restaurant} for restaurant in df['Restaurant'].unique()],
                    value=None,
                    multi=False,
                ),
                html.Br(),  # Add some space
                html.P("A visual interface displaying real-time sentiment metrics on specific aspects or features of a topic, enabling users to quickly discern positive, negative, and neutral opinions. This dashboard aids in data-driven decision making by highlighting areas of concern and praise based on public feedback.", style={'color': 'black'})
            ], width=3),  # This sets the width to 1/4th
            
            # Right side - 3/4th
            dbc.Col([
                dcc.Graph(id='aspect-bar-graph', config={'displayModeBar': False}),
                html.Br(),
                html.P("_________________________________________________________BARCHART____________________________________________________________", style={'color': 'black'}),
                dcc.Graph(id='sentiment-pie-chart', config={'displayModeBar': False}),
                html.Br(),
                html.P("_________________________________________________________PIECHART___________________________________________________________", style={'color': 'black'}),
                dbc.Label("Select a Review", style={'color': 'black'}),
                dcc.Dropdown(
                    id='review-dropdown',
                    multi=False,
                ),
                html.Br(),
                dcc.Graph(id='review-aspect-bar-graph', config={'displayModeBar': False}),
                html.Br(),
                html.P("_________________________________________________________BARCHART____________________________________________________________", style={'color': 'black'}),
                dcc.Graph(id='review-sentiment-pie-chart', config={'displayModeBar': False}),
                html.Br(),
                html.P("_________________________________________________________PIECHART____________________________________________________________", style={'color': 'black'}),
            ], width=6)  # This sets the width to 3/4th
        ], className="mb-5"),
    ], fluid=True)
])

# ... [Your callback function and the running app code remain unchanged]



@app.callback(
    [Output('aspect-bar-graph', 'figure'),
     Output('sentiment-pie-chart', 'figure'),
     Output('review-dropdown', 'options'),
     Output('review-aspect-bar-graph', 'figure'),
     Output('review-sentiment-pie-chart', 'figure')],
    [Input('restaurant-dropdown', 'value'),
     Input('review-dropdown', 'value')]
)
def update_graphs(selected_restaurant,selected_review):
    filtered_df = df[df['Restaurant'] == selected_restaurant]
      # populate the review dropdown
    review_options = [{'label': review, 'value': review} for review in filtered_df['Review'].unique()]

    # Check if filtered_df is empty
    if filtered_df.empty:
        empty_bar = px.bar(title="No Data Available for Selected Restaurant")
        empty_pie = px.pie(title="No Data Available for Selected Restaurant")
        return empty_bar, empty_pie

    # Bar Chart
    sentiment_counts_dict = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    counts = filtered_df['Aspect Sentiment'].value_counts()
    for sentiment, count in counts.items():
        sentiment_counts_dict[sentiment] = count
    
    sentiments_to_include = [sentiment for sentiment, count in sentiment_counts_dict.items() if count > 0]
    sentiment_counts_dict = {sentiment: count for sentiment, count in sentiment_counts_dict.items() if count > 0}

    # If there are no sentiments to display, return an empty figure
    if not sentiments_to_include:
        return px.bar(title="No Sentiments to Display")

    sentiment_counts = pd.DataFrame(list(sentiment_counts_dict.items()), columns=['Aspect Sentiment', 'Count'])

    bar_fig = px.bar(
        sentiment_counts,
        x='Aspect Sentiment',
        y='Count',
        title='Aspect Analysis',
        color='Aspect Sentiment',
        color_discrete_map=color_scale
    )

    # Pie Chart
    pie_fig = px.pie(
        filtered_df,
        names='Overall Sentiment',
        title='Overall Sentiment Distribution',
        color='Overall Sentiment',
        color_discrete_map=color_scale
    )
    
    # Now, let's generate bar and pie charts for the selected review:
    review_df = filtered_df[filtered_df['Review'] == selected_review]

    # Aspect bar chart for the selected review
    sentiment_counts_dict = review_df['Aspect'].value_counts().to_dict()
    sentiment_counts = pd.DataFrame(list(sentiment_counts_dict.items()), columns=['Aspect', 'Count'])
    review_bar_fig = px.bar(
        sentiment_counts,
        x='Aspect',
        y='Count',
        title='Aspect Analysis for Selected Review',
        color='Aspect',
        color_discrete_map=color_scale
    )
    # Sentiment pie chart for the selected review
    overall_sentiment_counts_dict = review_df['Overall Sentiment'].value_counts().to_dict()
    review_pie_fig = px.pie(
        names=list(overall_sentiment_counts_dict.keys()),
        values=list(overall_sentiment_counts_dict.values()),
        title='Overall Sentiment for Selected Review',
        color_discrete_map=color_scale
    )


    return bar_fig, pie_fig, review_options, review_bar_fig, review_pie_fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

