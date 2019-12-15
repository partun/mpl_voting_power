import itertools as itt
import plotly.graph_objects as go

faction_names = {'V': 'SVP', 'S': 'SP', 'RL': 'FDP', 'C': 'CVP', 'CE': 'CVP', 'G': 'GSP', 'BD': 'BDP', 'GL': 'GLP', '-': 'None'}
party_names = {'SVP', 'SP', 'FDP', 'CVP', 'GSP', 'BDP', 'GLP', 'None'}
party_order = {'SP': 1, 'GSP': 2, 'GLP': 3, 'CVP': 4, 'BDP': 5, 'FDP': 6, 'SVP': 7, 'None': 8}






#calulates Penrose-Banzhaf index (PBI) for parties with >=t votes for a winning coelition
#parties beeing dict form party key to number of seats
def PBI_votingPower(parties, t = 100):
    power = dict()
    #initialize voting power to zero
    for p in parties:
        power[p]  = 0
    
    #check for every party if it is pivotal for the empty subset
    for p in parties:
        if parties[p] >= t:
            power[p] += 1
    
    #iterate trought all subsets for size 1 to len(parties) + 1
    for i in range(1, len(parties) + 1):
        for partition in itt.combinations(parties.keys(), i):
            s = 0
            #sum all the votes in the partition
            for x in partition:
                s += parties[x]
                
            if s >= t:
                #the partition in winning
                for x in partition:
                    #check for all parties in the partion if they are pivotal
                    if s - parties[x] < t:
                        #party in pivotal add 1 to the power
                        power[x] += 1
                        
    #divid the power of each party by the number of subsets without this party
    for p in power:
        power[p] /= pow(2,len(parties) -1)
    return power



class KeyList:
    key = None
    value = None
    isSorted = False

    def __init__(self):
        self.key = []
        self.value = []

    def append(self, key, item):
        self.isSorted = False
        self.key.append(key)
        self.value.append(item)

    def extend(self, keys, items):
        assert(len(keys) == len(items))
        self.isSorted = False
        self.key.extend(keys)
        self.value.extend(items)  

    def sort(self, key= lambda x: x):
        temp = sorted(zip(self.value, self.key), key= lambda x: key(x[0]))
        self.key = [k for v, k in temp]
        self.value = [v for v, k in temp]
        self.isSorted = True

    def normalize(self, percent= False):
        t = sum(self.value)

        if percent:
            t *= 100

        for i, _ in enumerate(self.value):
            self.value[i] /= t

    def keyMap(self, f):
        self.key = list(map(f, self.value))
    
    def valueMap(self, f):
        self.value = list(map(f, self.value))

    def bar(self):
        fig = go.Figure([go.Bar(x=self.key, y=self.value)])
        fig.show()

    def __sizeof__(self):
        return len(self.key)

    def __str__(self):
        return str(list(zip(self.key, self.value)))

    def __iter__(self):
        return iter(zip(self.key, self.value))

#stores meta date of a session
#a session corresponds to one *.csv file
class Session:
    idno = 0
    year = '0000'
    no = '0'
    path = ''
    
    def __init__(self, idno, y, n, path):
        self.idno = idno
        self.year = y
        self.no = n
        self.path = path
        
    def __str__(self):
        return str(self.idno) + ' ' + self.path
    
    def __eq__(self, y):
        if isinstance(y, Session):
            return self.idno == y.idno
        else:
            return False
    
#stores data for a inividual national council member
class Member:
    idno = 0
    bioid = '0'
    name = 'none'
    faction = 'none'
    canton = 'none'
    birthdate = '0000-00-00'
    ismem = None
    
    def __init__(self, i):
        self.bioid = i
        self.ismem = []
    
    def __str__(self):
        f = self.faction
        if len(f) == 1:
            f += ' '
        return '#' + str(self.bioid) + ' ' + f + ' ' + self.canton + ' ' + self.name + ' c' + str(len(self.ismem))

    def __eq__(self, y):
        if isinstance(y, Member):
            return self.bioid == y.bioid
        else:
            return False
     
#stores data of a inivdual vote
class Vote:
    idno = 0
    date = '0000-00-00 00:00:00'
    affairId = '000.00'
    title = 'none'
    decision = 'undef'
    
    #set of member bioids
    yes = None #members voted yes
    no = None #members voted no
    abstain = None #members voted abstain
    novote = None #members not present for vote
    
    sessionId = 'none'
    session = None #ref to the session this vote was taken

    def __init__(self, i):
        self.idno = i
        self.yes = set()
        self.no = set()
        self.abstain = set()
        self.novote = set() 
        
    #returns the decison based on the yes/no set size    
    def getDecision(self):
        if len(self.yes) > len(self.no):
            return 'yes'
        if len(self.no) >= len(self.yes):
            return 'no'
        return 'undef'

    # -tests if party is pivotal for this vote
    # -party is set/list of members bioids
    # -party can contain members that were not national council members 
    #  at the time of the vote
    def isPivotal(self, party, abstain=True, novote=False, draw=False):
        p_yes = 0
        p_no = 0
        p_abstain = 0
        p_novote = 0

        for mem in party:
            if mem in self.yes:
                p_yes += 1
            elif mem in self.no:
                p_no += 1
            elif mem in self.abstain:
                p_abstain += 1
            elif mem in self.novote:
                p_novote += 1

        if not abstain:
            #do not consider members voted abstained
            p_abstain = 0
        if not novote:
            #not consider not present members
            p_novote = 0


        #decision was no
        if self.decision == 'no':
            new_yes = len(self.yes) + p_no + p_abstain + p_novote
            new_no = len(self.no) - p_no
            if new_yes > new_no:
                #can change vote pivotal
                return True
            elif new_no > new_yes:
                #can not change vote not pivotal
                return False
            else:
                #draw by default False
                return 'draw'
        
        #decision was yes
        if self.decision == 'yes':
            new_yes = len(self.yes) - p_yes
            new_no = len(self.no) + p_yes + p_abstain + p_novote
            if new_no > new_yes:
                return True
            elif new_yes > new_no:
                return False
            else:
                return 'draw'

    # -messure for how unifed the party was in this vote
    # -returns larges fraction of the party voted the same
    # -party is list/set of members bioids
    # -members not part of the national council at the time of the vote
    #  are not counted in any case
    def unity(self, party, abstain=True, novote=False):
        p_yes = 0
        p_no = 0
        p_abstain = 0
        p_novote = 0

        for mem in party:
            if mem in self.yes:
                p_yes += 1
            elif mem in self.no:
                p_no += 1
            elif mem in self.abstain:
                p_abstain += 1
            elif mem in self.novote:
                p_novote += 1
        
        if not abstain:
            #not consider abstain voters
            p_abstain = 0
    
        if not novote:
            #not consider abstain voters
            p_novote = 0

        p_max = max({p_yes, p_no, p_abstain, p_novote})
        p_sum = sum({p_yes, p_no, p_abstain, p_novote})

        if p_sum == 0:
            return 1

        return p_max / p_sum

    #enables print for Vote class    
    def __str__(self):
        out = str(self.sessionId) + '# '    
        out += str(self.idno)
        out += ' ' + self.decision
        out += ' yes:' + str(len(self.yes))
        out += ' no:' + str(len(self.no))
        out += ' abstain:' + str(len(self.abstain))
        out += ' novote:' + str(len(self.novote))
        return out

# class to store voter profile of a vote for a party
class VoteProfile:
    yes = 0
    no = 0
    abstain = 0
    novote = 0

    def __init__(self):
        self.yes = 0
        self.no = 0
        self.abstain = 0
        self.novote = 0

    def total(self):
        return self.yes + self.no + self.abstain + self.novote

    def partyVote(self, abstain=True, novote=False):
        out = 'None'
        t = -1

        if self.yes > t:
            out = 'yes'
            t = self.yes

        if self.no > t:
            out = 'no'
            t = self.no
        elif self.no == t:
            out = 'draw'

        if abstain and self.abstain > t:
            out = 'abstain'
            t = self.abstain
        elif abstain and self.abstain == t:
            out = 'draw'

        if novote and self.novote > t:
            out = 'novote'
            t = self.novote
        elif novote and self.novote == t:
            out = 'draw'

        return out

    def __str__(self):
        out = 'party vote: ' + self.partyVote()
        out += ' yes: ' + str(self.yes)
        out += ' no:' + str(self.no)
        out += ' abstain: ' + str(self.abstain)
        out += ' novote: ' + str(self.novote)
        out += ' total: ' + str(self.total())
        return out