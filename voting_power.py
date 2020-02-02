#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import os
import itertools as itt
import classes as vp
import PBI
import parser
import simulator as sim
import plotly.graph_objects as go
import plot
import mathHelper as mh


# In[2]:


#impirical voting power
#count how often a party in pivotal
#uses votes
def impVotingPower1(data):
    pivotal = dict()
    for f in data.factionList:
        count = 0
        for v in data.votes:
            if v.isPivotal(data.factionList[f]):
                count += 1
        pivotal[vp.faction_names.get(f,f)] = count
        
    n = sum(pivotal.values())
    
    for p in pivotal:
        pivotal[p] /= n
    
    return pivotal


# In[3]:


def profie(vote):
    profiles = dict()
    for f in vp.party_names:
        profiles[f] = vp.VoteProfile()
    
    for mem in vote.yes:
        profiles[vp.faction_names[members[mem].faction]].yes += 1
        
    for mem in vote.no:
        profiles[vp.faction_names[members[mem].faction]].no += 1
        
    for mem in vote.abstain:
        profiles[vp.faction_names[members[mem].faction]].abstain += 1
        
    for mem in vote.novote:
        profiles[vp.faction_names[members[mem].faction]].novote += 1
        
    for p in profiles:
        print(p + ' ' + str(profiles[p]))


# In[4]:


leg_49 = set(range(20))
leg_50 = set(range(20,39))

#load voting data in memory
sessions = parser.loadSessions()
data_50 = parser.parseFiles(sessions, toParse=leg_50)
data_49 = parser.parseFiles(sessions, toParse=leg_49)
factions_size_49 = parser.loadFactionsSize(period='49')
factions_size_50 = parser.loadFactionsSize(period='50')

#creating simulated voting data
simData_49 = sim.genData(factions_size_49, 5000)
simData_50 = sim.genData(factions_size_50, 5000)


# In[26]:


def groupedBar_Dict(dicts, names, log=False):
    data = []
    color = ['rgb(59,170,98)','rgb(59,98,170)','rgb(170,59,98)'][1:]
    
    for k, d in enumerate(dicts):
        l = []
        for i in d:
            l.append(d[i] * 100)
        
        #for i,item in enumerate(l):
         #   l[i] /= sum(l)
        #norm(l)
        data.append(go.Bar(name=names[k], x=list(d.keys()), y=l, marker_color=color[k]))

    fig = go.Figure(data=data)
    # ChagroupedBar_Dict([impVotingPower1(simData.votes, simData.factionList), impVotingPower1(data.votes, data.factionList), PBI.votingPower(factions_size_49)], ['sim','imp','50'])nge the bar mode
    if log:
        fig.update_layout(barmode='group', yaxis_type='log')
    else:
        fig.update_layout(barmode='group', width=900, height=500)
    fig.show()
    


# In[27]:


groupedBar_Dict([impVotingPower1(data_50), PBI.votingPower(factions_size_50)], ['Empirical Data', 'Banzhaf Index'])


# In[23]:


groupedBar_Dict([impVotingPower1(simData_50), impVotingPower1(data_50), PBI.votingPower(factions_size_50)], ['Simulated Data', 'Empirical Data', 'Banzhaf Index'])


# In[13]:


groupedBar_Dict([impVotingPower1(simData_49), impVotingPower1(data_49), PBI.votingPower(factions_size_49)], ['simulated data','empirical data','Banzhaf Index'])


# In[ ]:




