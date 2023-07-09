from flask import Flask, request, make_response,render_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly
import json

app = Flask(__name__)

@app.route('/')
def index():
    attention = pd.read_csv('static/attention.csv')
    attention['Date'] = pd.to_datetime(attention['Date'])
    attention.head(3)
    max_encoder_length = 13
    encoder_indices = list(range(max_encoder_length))
    attention.rename(
        {str(index):index for index in encoder_indices}, 
        axis=1, inplace=True
    )



    attention_date_aligned = pd.DataFrame(attention[['FIPS', 'Date']])
    for i in range(max_encoder_length):
        attention_date_aligned[i] = attention[i].shift(
            periods=i-max_encoder_length, fill_value=0
        )

    attention_date_aligned['weekday'] = attention_date_aligned.Date.dt.dayofweek


    attention_date_aligned_summed = attention_date_aligned.groupby('Date')[
        encoder_indices
    ].aggregate('sum').reset_index()

    attention_date_aligned_mean = attention_date_aligned.groupby('Date')[
        encoder_indices
    ].aggregate('mean').reset_index()



    import holidays
    # Select country
    us_holidays = holidays.US()


    start_date = pd.to_datetime('2021-11-8')
    end_date = pd.to_datetime('2021-12-29')


    df = pd.read_csv('static/predictions.csv')
    df = df.groupby(['Date'])[['Cases', 'Predicted_Cases']].aggregate('sum').reset_index()
    df['Date'] = df['Date'].apply(pd.to_datetime)
    df['holiday'] = df['Date'].apply(us_holidays.get)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    df1 = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    fig.add_trace(
        go.Scatter(x=df1['Date'], y=df1['Cases'], name='Ground Truth', line=dict(color='blue')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df1['Date'], y=df1['Predicted_Cases'], name='Prediction', line=dict(color='green')),
        secondary_y=False,
    )

    df2 = attention_date_aligned_mean[
        (attention_date_aligned_mean['Date'] >= start_date) & (attention_date_aligned_mean['Date'] <= end_date)
    ]

    fig.add_trace(
        go.Scatter(x=df2['Date'], y=df2[12], name='Attention Weight', line=dict(color='grey'), mode='lines'),
        secondary_y=True
    )

    holiday_cases = df1[~df1['holiday'].isna()]

    fig.add_trace(
        go.Scatter(x=holiday_cases['Date'], y=holiday_cases['Cases'], mode='markers', marker=dict(size=10, color='red'), name='Holiday'),
        secondary_y=False,
    )

    train_end = pd.to_datetime('2021-11-29')
    y_train = df1[df1['Date'] == train_end]['Cases'].values[0]

    fig.add_annotation(
        x=train_end, y=y_train, text='Train ends', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black',
        ax=40, ay=-120, align='center'
    )

    validation_end = pd.to_datetime('2021-12-14')
    y_validation = df1[df1['Date'] == validation_end]['Cases'].values[0]

    fig.add_annotation(
        x=validation_end, y=y_validation, text='Validation ends', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black',
        ax=40, ay=-160, align='center'
    )

    fig.update_layout(
        xaxis=dict(
            tickformat="%Y-%m-%d",
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks="outside",
            tickwidth=2,
            tickcolor='black'
        ),
        yaxis=dict(
            title='Daily Cases',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks="outside",
            tickwidth=2,
            tickcolor='black'
        ),
        yaxis2=dict(
            title='Avg. α(t, n, 1)',
            overlaying='y',
            side='right',
            range=[0, 0.5],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks="outside",
            tickwidth=2,
            tickcolor='black',
        ),
        legend=dict(orientation='h', x=0, y=1.2),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white',
        showlegend=True,
        legend_bgcolor='rgba(255, 255, 255, 0.5)',
        legend_bordercolor='black',
        legend_borderwidth=2,
    )

    fig.update_yaxes(
        tickformat=".3s",
        rangemode='tozero',
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=2,
        secondary_y=False,
    )

    fig.update_yaxes(
        tickformat=".3f",
        range=[0, 0.5],
        showgrid=False,
        secondary_y=True,
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("GPCE-frontend.html", graphJSON=graphJSON)




if __name__ == '__main__':
     app.run(debug=True)