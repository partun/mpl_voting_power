import itertools as itt
#calculates Penrose-Banzhaf index (PBI) for parties with >=t votes for a winning coalition
#parties beeing dict form party key to number of seats
#t is the min number of votes needed for a winning coalition
def votingPower(parties, t = 100, v=False):
    power = dict()
    countPivotal = 0

    #initialize power to zero
    for p in parties:
        power[p] = 0
    
    #iterate over all subsets
    for i in range(1, len(parties) + 1):
        for partition in itt.combinations(parties.keys(), i):
            s = 0
            #sum all the votes in the partition
            for x in partition:
                s += parties[x]

            if v:
                print(partition, s)
                
            if s >= t:
                #the partition in winning
                for p in partition:
                    #check for all parties in the partion if they are pivotal
                    if s - parties[p] < t:
                        #party in pivotal add 1 to the power
                        countPivotal += 1
                        power[p] += 1

    if v:
        print(countPivotal)
                      
    if countPivotal > 0:
        #divide the power of each party by the number of subsets without this party
        for p in power:
            power[p] /= countPivotal
    
    return power
