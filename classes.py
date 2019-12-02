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
    date = '0000-00-00 00:00:00'
    affairId = '000.00'
    title = 'none'
    dision = 'undef'
    yes = None
    no = None
    abstain = None
    novote = None
    session = None
    
    def __init__(self, i):
        self.idno = i
        self.yes = set()
        self.no = set()
        self.abstain = set()
        self.novote = set()
        
    def getDision(self):
        if len(self.yes) > len(self.no):
            return 'yes'
        if len(self.no) > len(self.yes):
            return 'no'
        return 'undef'

    def pivotal(self, p_yes, p_no, p_abstain, p_novote):
        return True

    def __str__(self):    
        out = str(self.idno)
        out += ' ' + self.dision
        out += ' yes:' + str(len(self.yes))
        out += ' no:' + str(len(self.no))
        out += ' abstain:' + str(len(self.abstain))
        out += ' novote:' + str(len(self.novote))
        return out
        