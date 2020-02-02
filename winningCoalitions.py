#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools as itt
import classes as vp
import PBI
import parser
import simulator as sim
import plotly.graph_objects as go
import plot
import mathHelper as mh


# In[2]:


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


# In[3]:


# find the wining coelition for all the votes
# needs member dict
def allWinningC(data, ids=False):
    coelitions = dict()
    
    for i in range(1, len(vp.party_names) + 1):
        for p in itt.combinations(vp.party_names, i):
            key = list(p)
            key.sort(key=lambda x: vp.party_order[x])
            if ids:
                coelitions[', '.join(key)] = []
            else:
                coelitions[','.join(key)] = 0
    
    for i, v in enumerate(data.votes):
        try:
            #change to lists vot ids instead
            if ids:
                coelitions[', '.join(winningC(data, v))].append(i)
            else:
                coelitions[','.join(winningC(data, v))] += 1
        except KeyError:
            print(v)
            print(i)
        
    return coelitions
    
    
#returns winning coelition for a vote
def winningC(data, vote):
    profiles = dict()
    for f in vp.party_names:
        profiles[f] = vp.VoteProfile()
    
    for mem in vote.yes:
        f = data.members[mem].faction
        profiles[vp.faction_names.get(f,f)].yes += 1
        
    for mem in vote.no:
        f = data.members[mem].faction
        profiles[vp.faction_names.get(f,f)].no += 1
        
    for mem in vote.abstain:
        f = data.members[mem].faction
        profiles[vp.faction_names.get(f,f)].abstain += 1
        
    for mem in vote.novote:
        f = data.members[mem].faction
        profiles[vp.faction_names.get(f,f)].novote += 1
        
    out = list()
    
    for p in profiles:
        if profiles[p].partyVote(abstain=False) == vote.decision:
            out.append(p)
    
    out.sort(key=lambda x: vp.party_order[x])
    return out
        
    


# In[20]:


#displays a histogram of all winning coelitions
def coelitions(data, simpleName = False, normalize=False, cut=0, ele=0, order=True):
    l = list(filter(lambda x: x[1] > cut, allWinningC(data).items()))
    if order:
        l.sort(key=lambda x: x[1], reverse=True)
    
    x = []
    y = []
    
    for i in l:
        if simpleName and (i[0] in coelition_names):
            x.append(coelition_names[i[0]])
        else:
            x.append(i[0])
        y.append(i[1])
    
    if normalize:
        #normalize data
        mh.norm(y, percet=True)
    
    print(sum(y))
    print(len(y))
    
    #plot.hist(y)
    
    if ele != 0:
        x = x[:ele]
        y = y[:ele]
        
    #print(y[:40])
    print(sum(y[:ele]))
    
    
    
    fig = go.Figure([go.Bar(x=x, y=y, marker_color='rgb(59,98,170)')])
    fig.update_layout(#title='Average High and Low Temperatures in New York',
                   #xaxis_title='winning Coalitions',
                   yaxis_title='Occurrence in %',
                    width=1200, height=700)
    fig.show()

#simpler names for coelitions
coelition_names = {'SP,GSP,GLP,CVP,BDP,FDP': 'against SVP',
                  'GLP,CVP,BDP,FDP,SVP': 'against left',
                  'SP,GSP,GLP,CVP,BDP,FDP,SVP': 'unanimous',
                  'CVP,BDP,FDP,SVP': 'center right',
                  'SP,GSP,GLP,CVP,BDP': 'center left',
                  'CVP, FDP, SVP': 'right and CVP',
                  'BDP, FDP, SVP': 'right and BDP',
                  'SP, GSP, GLP, BDP, FDP': 'center left'}


# In[21]:


coelitions(data_50, normalize=True, cut=1, ele=40, simpleName=False)


# In[22]:


coelitions(simData_50, normalize=True, cut=1, ele=64, simpleName=False, order=False)


# In[13]:


coelitions(data_49, normalize=True, cut=1, ele=40, simpleName=False)


# In[17]:


coelitions(simData_49, normalize=True, cut=1, ele=64, simpleName=False, order=False)


# In[ ]:




