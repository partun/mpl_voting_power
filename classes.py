#one file per national council session
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
    bioid = 0
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
    dision = 'undef'
    yes = None
    no = None
    abstain = None
    novote = None
    session = None
    
    def _init__(self, idno):
        self.ifno = idno
        self.yes = set()
        self.no = set()
        self.abstain = set()
        self.novote = set()
        
    def setVotes(self, votes, idMap):
        for i, v in enumerate(votes):
            if v == 'Ja':
                self.yes.add(idMap[i])
            elif v == 'Nein':
                self.no.add(idMap[i])
            elif v == 'Enthaltung':
                self.abstain.add(idMap[i])
            else:
                self.novote.add(idMap[i])
        
    def pivotal(self, p_yes, p_no, p_abstain, p_novote):
        return true 
        
    def __str__(self):
        return self.idno + self.dision + ' yes:' + str(len(self.yes)) + ' no:' + str(len(self.no)) + ' abstain:' + str(len(self.abstain)) + ' novote:' + str(len(self.novote))
        