import math

#line 32
#Summarize a stream of symbols.
class SYM:
    
    #no need to care about obj()
    
    ## line 35 function SYM.new(i)
    def __init__(self):
        self.n = 0 # basic
        self.has = {} # similar as before?
        # dict for keeping data
        
        self.most = 0 #the frequency of the most frequent object
        self.mode = None #there is no mode initially

    # line 40 function SYM.add(i,x)
    def add(self, x):
        if x != "?":
            self.n +=  1
            
            #if x already exists in current record, just add frequency of its occurance
            #otherwise, create a new key and its new value-1            
            if x in self.has.keys():
                self.has[x] += 1
            else:
                self.has[x] = 1
            
            
            #after each insertion, check whether the frequency of new record becomes the most frequent one
            #by comparing with 'most'
            if self.has[x] > self.most:
                self.most = self.has[x]
                self.mode = x

    # line 47 function SYM.mid(i,x)
    def mid(self):
        #here 'mid' stands for mode
        return self.mode

    # line 48 functon SYM.div(i,x,  fun, e)
    # fun() here should be an anonymous funciton
    #return the entropy
    def div(self, x):
        e = 0
        for key in self.has:
            p = self.has[key] / self.n
            p = p*(math.log2(p))
            e += p
        
        return -e
    
#line 53
#Summarizes a stream of numbers.
class NUM:
    ## line 55 function NUM.new(i)
    def __init__(self):
        self.n = 0 # basic
        
        self.mu = 0 # mean value of all
        self.m2 = 0 # standard deviation
        
        self.lo = math.inf # lowest value, initially set as MAX
        self.hi = -math.inf # highest seen, initially set as MIN

    # line 59 function NUM.add(i,x)
    # add `n`, update lo,hi and stuff needed for standard deviation
    def add(self, n):
        if n != "?":
            self.n +=  1
            
            d = n - self.mu
            
            self.mu += d/(self.n)
            self.m2 += d*(n - self.mu)
            
            self.lo = min(self.lo, n)
            self.hi = max(self.hi, n)

    # line 68 function NUM.mid(i,x)
    def mid(self):
        #here 'mid' stands for mean
        return self.mu

    # line 69 functon NUM.div(i,x)
    # return standard deviation using Welford's algorithm
    def div(self):
        if(self.m2 < 0 or self.n <2):
            return 0
        else:
            return pow((self.m2 / (self.n-1)), 0.5)