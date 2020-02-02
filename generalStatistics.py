#!/usr/bin/env python
# coding: utf-8

# In[2]:


import itertools as itt
import classes as vp
import parser
import simulator as sim
import plotly.graph_objects as go
import plot
import mathHelper as mh


# In[3]:


leg_49 = set(range(20))
leg_50 = set(range(20,39))

#load voting data in memory
sessions = parser.loadSessions()
data = parser.parseFiles(sessions, toParse=leg_50)
data_49 = parser.parseFiles(sessions, toParse=leg_49)
factions_size_49 = parser.loadFactionsSize(period='49')
factions_size_50 = parser.loadFactionsSize(period='50')


# In[18]:


def showVoteDist(votes):
    #histogramm of how many members votes yes, no, abstain per vote
    present = []
    absent = []
    for v in votes:
        s = len(v.yes) + len(v.no) + len(v.abstain)
        present.append(s)
        absent.append(len(v.novote))
    
    fig = go.Figure(data=[go.Histogram(x=present, histnorm='percent', marker_color='rgb(59,98,170)')])
    fig.update_layout(#title='Partisipation of National Council Members in 50th legislature',
                   xaxis_title='Number of Members Present for a Vote',
                   yaxis_title='Occurrence in %', height=500, width=900)
    fig.show()

    fig = go.Figure(data=[go.Histogram(x=absent, histnorm='percent')])
    fig.update_layout(#title='Partisipation of National Council Members in 50th legislature',
                   xaxis_title='Number of Members Absent for a Vote',
                   yaxis_title='Occurrence in %', height=500, width=900)
    fig.show()
showVoteDist(data.votes)


# In[6]:


def memberPartisipation(data):
    partisipation = dict()
    
    def update(key, i, d=partisipation):
        
        key = vp.faction_names[data.members[key].faction]
        
        if not key in d:
            d[key] = [0,0,0,0]
        else:
            d[key][i] += 1
    
    def presents(x):
        return sum(x[0:3]) / sum(x)
    
    
    for v in data.votes:
        for mem in v.yes:
            update(mem, 0)
        for mem in v.no:
            update(mem, 1)
        for mem in v.abstain:
            update(mem, 2)
        for mem in v.novote:
            update(mem, 3)  
    
    
    
    plot.bar_dict(partisipation, value=lambda x: presents(x) * 100, relativ= True, sort= True)
memberPartisipation(data)


# In[7]:


# creates bar chart for party unity in votes
def factionUnity(data):
    factionUnity = dict()
    for f in data.factionList:
        factionUnity[vp.faction_names[f]] = []
        
    for v in data.votes:
        for f in data.factionList:
            factionUnity[vp.faction_names[f]].append(v.unity(data.factionList[f], abstain=True))
    plot.bar_dict(factionUnity, value= lambda x: sum(x) / len(x) * 100, relativ=False, sort=True)
factionUnity(data)


# In[ ]:




