import plotly.graph_objects as go
import plotly.express as px
import mathHelper as mh

def hist(data):
    fig = go.Figure(data=[go.Histogram(x=data, histnorm='percent')])
    fig.show()

#colors = ['rgb(0, 154, 46)', 'rgb(255, 0, 0)', 'rgb(6, 60, 255)','rgb(255, 135, 0)', 'rgb(42, 232, 2)', 'rgb(255, 220, 0)', 'rgb(190, 239, 0)']
faction_color = ['#009A2E', '#FF0000', '#063CFF', '#FF8700', '#2AE802', '#FFDC00', '#BEEF00']

def factionBar(x, y):
    fig = go.Figure([go.Bar(x=x, y=y, marker_color=faction_color)])
    fig.show()

# prints bar chart form dict d
# key function applied to the dict keys
# value function applied to the dict items
# if relativ is true the average is substracted form all values
# if sort is true values are sorted by value
# sortkey function can modify sort key
def bar_dict(d, key= lambda x: x, value= lambda x: x, relativ= False, sort=False, sortKey= lambda x: x, xlable='', ylable='', titel=''):
    x = []
    y = []
    
    for k in d:
        x.append(key(k))
        y.append(value(d[k]))
    
    if relativ:
        mean = mh.mean(y)
        y = list(map(lambda x: x - mean, y))

    if sort:
        temp = sorted(zip(x, y), key= lambda x: sortKey(x[1]))
        x = [k for k, _ in temp]
        y = [v for _, v in temp]
    
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title=titel,
                   xaxis_title=xlable,
                   yaxis_title=ylable)
    fig.show()