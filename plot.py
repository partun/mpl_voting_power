import plotly.graph_objects as go
import plotly.express as px

def hist(data):
    fig = go.Figure(data=[go.Histogram(x=data)])
    fig.show()

#olors = ['rgb(0, 154, 46)', 'rgb(255, 0, 0)', 'rgb(6, 60, 255)','rgb(255, 135, 0)', 'rgb(42, 232, 2)', 'rgb(255, 220, 0)', 'rgb(190, 239, 0)']
faction_color = ['#009A2E', '#FF0000', '#063CFF', '#FF8700', '#2AE802', '#FFDC00', '#BEEF00']

def factionBar(x, y):
    fig = go.Figure([go.Bar(x=x, y=y, marker_color=faction_color)])
    fig.show()