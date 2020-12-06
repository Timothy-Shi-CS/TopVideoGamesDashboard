__author__ = 'Timothy Shi'

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv("vgsales.csv")

attributeNames = {
    'NA_Sales': 'North America Sales (millions)',
    'EU_Sales': 'Europe Sales (millions)',
    'JP_Sales': 'Japan Sales (millions)',
    'Other_Sales': 'Total Sales in other places (millions)',
    'Global_Sales': 'Global Sales (millions)',
    'Rank': 'Rank',
    'Name': 'Name',
    'Platform': 'Platform',
    'Year': 'Year',
    'Genre': 'Genre',
    'Publisher': 'Publisher'
}


app.layout = html.Div(children=[
    # html.H1('Timothy Shi CSE 332 Lab 5'),
    html.Div([
        html.Div([
            dcc.Graph(
                id='parallel_coordinates',
            )
        ],
                style={
                    'display': 'inline-block',
                    'width': '75%'
                }
        ),
        html.Div([
                dcc.Graph(
                    id="pie_chart",
                )
            ],
                style={
                    'display': 'inline-block',
                    'width': '25%'
                }
        )
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id="histogram",
            )
        ],
            style={
                'display': 'inline-block',
                'width': '49%'
            }
        ),
        html.Div([
            dcc.Graph(id="scatterplot")
        ],
            style={
                'display': 'inline-block',
                'width': '49%'
            }
        ),
    ]),
])


def make_parallel_coordinates(c_df):
    figure = px.parallel_coordinates(
        c_df,
        dimensions=['Global_Sales', 'NA_Sales', 'EU_Sales', 'Other_Sales', 'Rank',
                    'JP_Sales', 'Year'],
        color='Rank',
        title='Parallel Coordinates Display',
        labels={"Global_Sales": "Global Sales (Millions)", "EU_Sales": "Europe Sales (Millions)",
                "NA_Sales": "North America Sales (Millions)", "Other_Sales": "Other Countries Sales (Millions)",
                "Rank": "Rank", "JP_Sales": "Japan Sales (Millions)", "Year": "Year"}
    )
    figure.update_layout(
        title_x=0.5,
        margin=dict(b=10),
        height=275,
    )
    return figure


def make_histogram(c_df):
    hist = px.histogram(
        title='Best Selling Video Games by Platform',
        data_frame=c_df,
        x='Platform',
        nbins=40,
        labels={
            'Platform': attributeNames['Platform'],
        }
    )
    hist.update_layout(
        title_x=0.5,
        # margin=dict(t=50),
        height=425
    )
    return hist


def make_pie_chart(c_df):
    filtered_df = c_df.filter(items=['Genre']).values.tolist()
    genre = ['Action', 'Sports', 'Shooter', 'Role-Playing', 'Platform', 'Others']
    num_games = [0] * 6
    for i in range(len(filtered_df)):
        if filtered_df[i][0] == 'Action':
            num_games[0] += 1
        elif filtered_df[i][0] == 'Sports':
            num_games[1] += 1
        elif filtered_df[i][0] == 'Shooter':
            num_games[2] += 1
        elif filtered_df[i][0] == 'Role-Playing':
            num_games[3] += 1
        elif filtered_df[i][0] == 'Platform':
            num_games[4] += 1
        else:
            num_games[5] += 1

    pie_chart = px.pie(
        title='Best Selling Games by Genre',
        labels=genre,
        values=num_games,
        names=genre,
        hole=.5,
    )
    pie_chart.update_layout(
        title_x=0.5,
        margin=dict(b=0, l=0),
        height=275
    )
    return pie_chart


def make_scatter_plot(c_df):
    scatterplot = px.scatter(
        data_frame=c_df,
        x='NA_Sales',
        y='EU_Sales',
        hover_name="Name",
        hover_data=["Platform", "Publisher", "Genre", "Year"],
        color='Genre',
        size='Global_Sales',
        title=attributeNames['NA_Sales'] + ' VS. ' + attributeNames['EU_Sales'],
        labels={
            'NA_Sales': attributeNames['NA_Sales'],
            'EU_Sales': attributeNames['EU_Sales'],
            'Global_Sales': attributeNames['Global_Sales'],
        }
        # log_y=True,
    )
    scatterplot.update_layout(
        title_x=0.5,
        margin=dict(l=0),
        height=425
    )
    return scatterplot


def parallel_coordinates_df(c_df, pc_restyleData):
    pc_df = c_df
    if 'dimensions[0].constraintrange' in pc_restyleData:
        min_global = pc_restyleData['dimensions[0].constraintrange'][0][0]
        max_global = pc_restyleData['dimensions[0].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['Global_Sales'] >= min_global) & (pc_df['Global_Sales'] <= max_global)]

    if 'dimensions[1].constraintrange' in pc_restyleData:
        min_na = pc_restyleData['dimensions[1].constraintrange'][0][0]
        max_na = pc_restyleData['dimensions[1].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['NA_Sales'] >= min_na) & (pc_df['NA_Sales'] <= max_na)]

    if 'dimensions[2].constraintrange' in pc_restyleData:
        min_eu = pc_restyleData['dimensions[2].constraintrange'][0][0]
        max_eu = pc_restyleData['dimensions[2].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['EU_Sales'] >= min_eu) & (pc_df['EU_Sales'] <= max_eu)]

    if 'dimensions[3].constraintrange' in pc_restyleData:
        min_other = pc_restyleData['dimensions[3].constraintrange'][0][0]
        max_other = pc_restyleData['dimensions[3].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['Other_Sales'] >= min_other) & (pc_df['Other_Sales'] <= max_other)]

    if 'dimensions[4].constraintrange' in pc_restyleData:
        min_rank = pc_restyleData['dimensions[4].constraintrange'][0][0]
        max_rank = pc_restyleData['dimensions[4].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['Rank'] >= min_rank) & (pc_df['Rank'] <= max_rank)]

    if 'dimensions[5].constraintrange' in pc_restyleData:
        min_jp = pc_restyleData['dimensions[5].constraintrange'][0][0]
        max_jp = pc_restyleData['dimensions[5].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['JP_Sales'] >= min_jp) & (pc_df['JP_Sales'] <= max_jp)]

    if 'dimensions[6].constraintrange' in pc_restyleData:
        min_year = pc_restyleData['dimensions[6].constraintrange'][0][0]
        max_year = pc_restyleData['dimensions[6].constraintrange'][0][1]
        pc_df = pc_df.loc[(pc_df['Year'] >= min_year) & (pc_df['Year'] <= max_year)]

    return pc_df


@app.callback(
    Output(component_id='parallel_coordinates', component_property='figure'),
    Input(component_id='parallel_coordinates', component_property='restyleData'),
    Input(component_id='scatterplot', component_property='selectedData'),
    Input(component_id='scatterplot', component_property='relayoutData'),
    Input(component_id='pie_chart', component_property='clickData'),
    Input(component_id='histogram', component_property='clickData')
)
def update_parallel_coordinates(parallel_coordinates_restyle, scatterplot_selected, scatterplot_relayout,
                                pie_chart_click, histogram_click):
    copy_df = df
    ctx = dash.callback_context
    # print(ctx.inputs)
    # print("Success")
    if ctx.inputs['parallel_coordinates.restyleData'] is not None:
        copy_df = parallel_coordinates_df(copy_df, parallel_coordinates_restyle[0])
    if ctx.inputs['pie_chart.clickData'] is not None:
        # print(pie_chart_click['points'][0]['label'])
        label = pie_chart_click['points'][0]['label']
        if label == 'Others':
            copy_df = copy_df.loc[(copy_df['Genre'] == 'Racing') | (copy_df['Genre'] == 'Puzzle') |
                                       (copy_df['Genre'] == 'Misc') | (copy_df['Genre'] == 'Simulation') |
                                       (copy_df['Genre'] == 'Fighting') | (copy_df['Genre'] == 'Adventure') |
                                       (copy_df['Genre'] == 'Strategy')]
        else:
            copy_df = copy_df.loc[(copy_df['Genre'] == label)]
        # print(copy_df.loc[(copy_df['Genre'] == label)])
    if ctx.inputs['histogram.clickData'] is not None:
        # print(ctx.inputs['histogram.clickData'])
        platform = histogram_click['points'][0]['x']
        copy_df = copy_df.loc[(copy_df['Platform'] == platform)]
    if ctx.inputs['scatterplot.relayoutData'] is not None:
        if 'xaxis.range[0]' in scatterplot_relayout:
            copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_relayout['xaxis.range[0]']) &
                                  (copy_df['NA_Sales'] <= scatterplot_relayout['xaxis.range[1]']) &
                                  (copy_df['EU_Sales'] >= scatterplot_relayout['yaxis.range[0]']) &
                                  (copy_df['EU_Sales'] <= scatterplot_relayout['yaxis.range[1]'])]
    if ctx.inputs['scatterplot.selectedData'] is not None:
        copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_selected['range']['x'][0]) &
                              (copy_df['NA_Sales'] <= scatterplot_selected['range']['x'][1]) &
                              (copy_df['EU_Sales'] >= scatterplot_selected['range']['y'][0]) &
                              (copy_df['EU_Sales'] <= scatterplot_selected['range']['y'][1])]

    return make_parallel_coordinates(copy_df)


@app.callback(
    Output(component_id='histogram', component_property='figure'),
    Input(component_id='parallel_coordinates', component_property='restyleData'),
    Input(component_id='scatterplot', component_property='selectedData'),
    Input(component_id='scatterplot', component_property='relayoutData'),
    Input(component_id='pie_chart', component_property='clickData'),
)
def update_histogram(parallel_coordinates_restyle, scatterplot_selected, scatterplot_relayout, pie_chart_click):
    copy_df = df
    ctx = dash.callback_context
    if ctx.inputs['pie_chart.clickData'] is not None:
        label = pie_chart_click['points'][0]['label']
        if label == 'Others':
            copy_df = copy_df.loc[(copy_df['Genre'] == 'Racing') | (copy_df['Genre'] == 'Puzzle') |
                                  (copy_df['Genre'] == 'Misc') | (copy_df['Genre'] == 'Simulation') |
                                  (copy_df['Genre'] == 'Fighting') | (copy_df['Genre'] == 'Adventure') |
                                  (copy_df['Genre'] == 'Strategy')]
        else:
            copy_df = copy_df.loc[(copy_df['Genre'] == label)]
    if ctx.inputs['parallel_coordinates.restyleData'] is not None:
        copy_df = parallel_coordinates_df(copy_df, parallel_coordinates_restyle[0])
    if ctx.inputs['scatterplot.relayoutData'] is not None:
        if 'xaxis.range[0]' in scatterplot_relayout:
            copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_relayout['xaxis.range[0]']) &
                                  (copy_df['NA_Sales'] <= scatterplot_relayout['xaxis.range[1]']) &
                                  (copy_df['EU_Sales'] >= scatterplot_relayout['yaxis.range[0]']) &
                                  (copy_df['EU_Sales'] <= scatterplot_relayout['yaxis.range[1]'])]
    if ctx.inputs['scatterplot.selectedData'] is not None:
        copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_selected['range']['x'][0]) &
                              (copy_df['NA_Sales'] <= scatterplot_selected['range']['x'][1]) &
                              (copy_df['EU_Sales'] >= scatterplot_selected['range']['y'][0]) &
                              (copy_df['EU_Sales'] <= scatterplot_selected['range']['y'][1])]
    return make_histogram(copy_df)


@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='parallel_coordinates', component_property='restyleData'),
    Input(component_id='scatterplot', component_property='selectedData'),
    Input(component_id='scatterplot', component_property='relayoutData'),
    Input(component_id='histogram', component_property='clickData'),
)
def update_pie_chart(parallel_coordinates_restyle, scatterplot_selected, scatterplot_relayout, histogram_click):
    copy_df = df
    ctx = dash.callback_context
    # print(ctx.inputs)
    if ctx.inputs['histogram.clickData'] is not None:
        # print(ctx.inputs['histogram.clickData'])
        platform = histogram_click['points'][0]['x']
        copy_df = copy_df.loc[(copy_df['Platform'] == platform)]
    if ctx.inputs['parallel_coordinates.restyleData'] is not None:
        # print(parallel_coordinates_restyle[0])
        copy_df = parallel_coordinates_df(copy_df, parallel_coordinates_restyle[0])
    # print(ctx.inputs)
    if ctx.inputs['scatterplot.relayoutData'] is not None:
        # print(scatterplot_relayout)
        if 'xaxis.range[0]' in scatterplot_relayout:
            copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_relayout['xaxis.range[0]']) &
                                  (copy_df['NA_Sales'] <= scatterplot_relayout['xaxis.range[1]']) &
                                  (copy_df['EU_Sales'] >= scatterplot_relayout['yaxis.range[0]']) &
                                  (copy_df['EU_Sales'] <= scatterplot_relayout['yaxis.range[1]'])]
    if ctx.inputs['scatterplot.selectedData'] is not None:
        # print(scatterplot_selected['range']['x'][0])
        copy_df = copy_df.loc[(copy_df['NA_Sales'] >= scatterplot_selected['range']['x'][0]) &
                              (copy_df['NA_Sales'] <= scatterplot_selected['range']['x'][1]) &
                              (copy_df['EU_Sales'] >= scatterplot_selected['range']['y'][0]) &
                              (copy_df['EU_Sales'] <= scatterplot_selected['range']['y'][1])]
    return make_pie_chart(copy_df)


@app.callback(
    Output(component_id='scatterplot', component_property='figure'),
    Input(component_id='parallel_coordinates', component_property='restyleData'),
    Input(component_id='histogram', component_property='clickData'),
    Input(component_id='pie_chart', component_property='clickData'),
)
def update_scatterplot(parallel_coordinates_restyle, histogram_click, pie_chart_click):
    copy_df = df
    ctx = dash.callback_context
    if ctx.inputs['histogram.clickData'] is not None:
        # print(ctx.inputs['histogram.clickData'])
        platform = histogram_click['points'][0]['x']
        copy_df = copy_df.loc[(copy_df['Platform'] == platform)]
    if ctx.inputs['parallel_coordinates.restyleData'] is not None:
        # print(parallel_coordinates_restyle[0])
        copy_df = parallel_coordinates_df(copy_df, parallel_coordinates_restyle[0])
    # print(ctx.inputs)
    if ctx.inputs['pie_chart.clickData'] is not None:
        label = pie_chart_click['points'][0]['label']
        if label == 'Others':
            copy_df = copy_df.loc[(copy_df['Genre'] == 'Racing') | (copy_df['Genre'] == 'Puzzle') |
                                  (copy_df['Genre'] == 'Misc') | (copy_df['Genre'] == 'Simulation') |
                                  (copy_df['Genre'] == 'Fighting') | (copy_df['Genre'] == 'Adventure') |
                                  (copy_df['Genre'] == 'Strategy')]
        else:
            copy_df = copy_df.loc[(copy_df['Genre'] == label)]
    return make_scatter_plot(copy_df)


if __name__ == '__main__':
    app.run_server(debug=True)
