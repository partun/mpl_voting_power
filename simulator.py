import random
import parser
import classes

#simulate voting data were faction vote randomly
#data has the same structure as the data returned form parser.py

#generates faction member lists with number of members according to faction_size
def genFactions(faction_size):
    t = 0
    simFaction = dict()

    for name, count in faction_size.items():
        simFaction[name] = list(range(t, t+count))
        t += count
    
    return simFaction

#generates a member id to member maping that can be use to determine the faction coresponding to a member id
def genMembers(factionList):
    members = dict()

    for f in factionList:
        for mem in factionList[f]:
            members[mem] = classes.Member(mem)
            members[mem].faction = f
    return members


#generates vote array containing n votes where each faction votes randomly yes/no
def genVotes(simFaction, n, unity=1):
    simVotes = []
    
    for i in range(n):
        vote = classes.Vote(i)
        
        for faction in simFaction:
            withFaction = []
            againstFaction = []
            
            for mem in simFaction[faction]:
                if random.random() < unity:
                    withFaction.append(mem)
                else:
                    againstFaction.append(mem)
                    
            if random.randint(0,1) == 0:
                #faction votes yes
                vote.yes.update(withFaction)
                vote.no.update(againstFaction)
            else:
                #fation votes no
                vote.no.update(withFaction)
                vote.yes.update(againstFaction)
        
        vote.decision = vote.getDecision()
        simVotes.append(vote)
        
    return simVotes

#generates voting data with n votes
def genData(faction_size, n, unity = 1):
    simData = parser.VotingData()

    simData.factionList = genFactions(faction_size)
    simData.votes = genVotes(simData.factionList, n, unity=unity)
    simData.members = genMembers(simData.factionList)

    return simData