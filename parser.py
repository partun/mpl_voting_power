import csv
import classes

class VotingData:
    votes = None
    members = None
    factionList = None

    def __init__(self):
        self.votes = []
        self.members = dict()
        self.factionList = dict()

#loads all the session form sessions.csv
def loadSessions(file = 'sessions.csv', csv_data_dir = './csv_data'):
    #load session data form sessions.csv
    sessions = [] #list of all the sessions
    with open(file) as sessions_csv:
        sessionno = 0
        csv_reader = csv.reader(sessions_csv, delimiter=',')
        for l in csv_reader:
            sessions.append(classes.Session(sessionno, l[1], l[2], csv_data_dir + '/' + l[3]))
            sessionno += 1
    return sessions

#load the size of each faction form factions.csv 
#the avoids the problem that the faction member list contain all members that were part of the faction in some session
#so the length of the member list can be higher then the actual member count of a faction.
def loadFactionsSize(file = 'factions.csv', period='50'):
    factions_count = dict()
    with open(file) as factions_csv:
        csv_reader = csv.reader(factions_csv, delimiter=',')
        l = next(csv_reader)
        periodIndex = None
        for i,item in enumerate(l):
            if item == period:
                periodIndex = i
                break
        if periodIndex == None:
            #could not fined period
            return None
            
        l = next(csv_reader)
        while True:
            try:
                factions_count[l[0]] = int(l[periodIndex])
                l = next(csv_reader)
            except StopIteration:
                break

        t = 200 - sum(factions_count.values())
        if t > 0:
            factions_count['None'] = t

        
        return factions_count


#list of members for each faction
def genFactions(members):
    factions = dict()
    for mem in members:
        f = members[mem].faction
        if f in factions:
            factions[f].append(members[mem].bioid)
        else:
            factions[f] = [members[mem].bioid]
    return factions

#counts members that were part of each fation a some point in parsed data
def genFactionSize(factions):
    factions_size = dict()
    for f in factions:
        factions_size[f] = len(factions[f])
        
    return factions_size

#parses information about the members
def parseMems(r, session, members):
    #members = dict()
    posIdMap = []
    line = next(r)
    start = 0
    end = 0
    for i, item in enumerate(line):
        if item == 'CouncillorId':
            start = i+1
            break
    
    line = next(r)
    
    #enumerate ID
    for i, item in enumerate(line[start:]):
        if item == '':
            end = i + start
            break
            
        posIdMap.append(item)
        if not item in members:
            members[item] = classes.Member(item)
        (members[item].ismem).append(session.idno)

    ''' 
    #enumerate bioid
    line = next(r)    
    for i,item in enumerate(line[start:end]):
        members[posIdMap[i]].bioid = item
    '''
    
    #enumerate name
    line = next(r)
    for i,item in enumerate(line[start:end]):
        #print(i), print(item)
        members[posIdMap[i]].name = item
        
    #skip line (this line only shows members are part of national council)
    next(r)
    #enumerate faction membership
    line = next(r)
    for i,item in enumerate(line[start:end]):
        members[posIdMap[i]].faction = item 
        
    #enumerate canton
    line = next(r)
    for i,item in enumerate(line[start:end]):
        members[posIdMap[i]].canton = item
        
    #enumerate birthdata
    line = next(r)
    for i,item in enumerate(line[start:end]):
        members[posIdMap[i]].birthdate = item

    return

#parses information about the votes
def parseVotes(r, s, votes):
    l = next(r)
    voters = []
    #votes = []
    voteno = 0
    start = 0
    while l[0] != 'VoteDate':
        l = next(r)
        start += 1
    
    #voters contains all the voters in a session
    endVotes = 0
    for i, item in enumerate(l[12:]):
        if item != 'Decision':
            voters.append(item)
        else:
            endVotes = i + 12
            break
    #print(len(voters))
    
    g = set()
    l = next(r)
    
    
    #need to handle:
    vote_none = '' #member was not yet or is no longer a national coucil member
    vote_yes = 'Ja'
    vote_no = 'Nein'
    vote_novote = ['Entschuldigt', 'Hat nicht teilgenommen']
    vote_abstain = 'Enthaltung'
    vote_pres = 'Der Präsident stimmt nicht'
    decision_set = {'yes', 'no'}
    
    
    while True:
        try:
            #store vote meta data
            v = classes.Vote(voteno)
            v.date = l[0]
            v.affairId = l[4]
            v.title = l[5]
            v.session = s
            v.sessionId = s.idno
            #store how each member voted by adding the members bioid to the yes/no/abstain/noset set
            for i, item in enumerate(l[12:endVotes]):
                if item == vote_none:
                    pass
                elif item == vote_yes:
                    v.yes.add(voters[i])
                elif item == vote_no:
                    v.no.add(voters[i])
                elif item == vote_abstain:
                    v.abstain.add(voters[i])
                elif item in vote_novote:
                    v.novote.add(voters[i])
                elif item == vote_pres:
                    pass
                else:
                    print('err vote: ' + item)
            
            #store decision data as stored in file and compare with calculated decision value
            v.decision = l[endVotes].lower()
            
            if v.decision != v.getDecision() or (not v.decision in decision_set):
                v.decision = 'err: \"' + v.decision + '\"' 
            votes.append(v)
            voteno += 1
            l = next(r)
        except StopIteration:
            break  


#parses all the session data files
#to parse can limit the session to parse
def parseFiles(sessions, toParse = {}): 
    data = VotingData()

    for s in sessions:
        if s.idno in toParse or len(toParse) == 0:
            with open(s.path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                print('-', end='')
                #print(str(key) + '. reading ... ' + csv_file.name)
                #parseFile(csv_reader)
                parseMems(csv_reader, s, data.members)
                parseVotes(csv_reader, s, data.votes)
                csv_file.close


    data.factionList = genFactions(data.members)

    return data