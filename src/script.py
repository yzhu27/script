'''
---                                           __      
---                           __             /\ \__   
---     ____    ___    _ __  /\_\    _____   \ \ ,_\  
---    /',__\  /'___\ /\`'__\\/\ \  /\ '__`\  \ \ \/  
---   /\__, `\/\ \__/ \ \ \/  \ \ \ \ \ \L\ \  \ \ \_ 
---   \/\____/\ \____\ \ \_\   \ \_\ \ \ ,__/   \ \__\
---    \/___/  \/____/  \/_/    \/_/  \ \ \/     \/__/
---                                    \ \_\          
---                                     \/_/          
'''

import re
import sys
import math

the =  {}
help = '''
script.lua : an example script with help text and a test suite
(c)2022, Tim Menzies <timm@ieee.org>, BSD-2

USAGE:   script.lua  [OPTIONS] [-g ACTION]

OPTIONS:
  -d  --dump  on crash, dump stack = false
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211

ACTIONS:
'''




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
    def div(self):
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
        self.hi = -math.inf # highest value, initially set as MIN

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





# Misc support functions

## Numerics 

Seed = 937162211

# n ; a integer lo..hi-1
def rint(lo, hi):
    return math.floor(0.5 + rand(lo, hi))

# n; a float "x" lo<=x < x
def rand(lo, hi):
    global Seed
    lo = lo or 0
    hi = hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

# num. return `n` rounded to `nPlaces`
def rnd(n, nPlaces=3):
    mult = 10**nPlaces
    return math.floor(n * mult + 0.5) / mult


## Lists

# Note the following conventions for `map`.
# - If a nil first argument is returned, that means :skip this result"
# - If a nil second argument is returned, that means place the result as position size+1 in output.
# - Else, the second argument is the key where we store function output.

# t; map a function `fun`(v) over list (skip nil results)
def map(t:dict, fun):
    u = {}
    for k, v in t.items():
        u[k]=fun(v)
    return u

# t; map function `fun`(k,v) over list (skip nil results)
def kap(t:dict, fun):
    u = {}
    for k, v in t.items():
        u[k]=fun(k, v)
    return u

# t; return `t`,  sorted by `fun` (default= `<`)
def sort(t:list, fun = None):
    return sorted(t, key=fun)

# ss; return list of table keys, sorted
def keys(t:list):
    return sorted(kap(t, lambda k, _:k))





## Strings



def fmt(sControl , *elements): # emulate printf
    return (sControl%(elements)) 
#test
##a=1
##b=2
##print(fmt("%s and %s" , a , b)) #--> "1 and 2"


def o(t , *isKeys): #--> s; convert `t` to a string. sort named keys.
    if type(t) != dict:
        return str(t)
    
    def fun(k , v):
        if not re.findall('[^_]' , k):
            return fmt(":%s %s",o(k),o(v))
    
    return ' '.join([str(len(t) > 0) and str(not isKeys) and str(map(t , o)) or str(sort(kap(t , fun)))])

def oo(t):
    print(o(t))
    return t

def coerce(s):
    def fun(s1):
        if s1 == 'true':
            return True
        if s1 == 'false':
            return False 
        return s1.strip()
    if s.isdigit():
        return int(s)
    try:
        tmp = float(s)
        return tmp
    except ValueError:
        return fun(s)
    




### Main


def settings(s):  # --> t;  parse help string to extract a table of options
    t = {}
    # match the contents like: '-d  --dump  on crash, dump stack = false'
    res = r"[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)"
    m = re.findall(res, s)
    for key, value in m:
        t[key] = coerce(value)
    return t
# test
# print(settings(help)) --> {'dump': False, 'go': 'data', 'help': False, 'seed': 937162211}

# Update settings from values on command-line flags. Booleans need no values


def cli(t, list):
    slots = list[1:]
    # search the key and value we want to update
    for slot, v in t.items():
        # give each imput slot an index(begin from 0)
        for n, x in enumerate(slots):
            # match imput slot with the.keys: x == '-e' or '--eg'
            if x == ('-'+slot[0]) or x == ('--'+slot):
                v = str(v)
                # we just flip the defeaults
                if v == 'True':
                    v = 'false'
                elif v == 'False':
                    v = 'true'
                else:
                    v = slots[n+1]
                t[slot] = coerce(v)
    return t



def main(options, help, funs, *k):
    saved = {}
    fails = 0
    for k, v in cli(settings(help), sys.argv).items():
        options[k] = v
        saved[k] = v
    if options['help']:
        print(help)
    

    else:
        for what, fun in funs.items():
            if options['go'] == 'all' or what == options['go']:
                for k, v in saved.items():
                    options[k] = v
                if fun() == False:
                    fails += 1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)



## Examples

egs = {}
def eg(key, str, fun):
    global help
    egs[key] = fun
    help = help + f'  -g  {key}\t{str}\n'



if __name__=='__main__':
    
# eg("crash","show crashing behavior", function()
#   return the.some.missing.nested.field end)
    def thefun():
        global the
        return oo(the)
    eg("the","show settings", thefun)

    def randfun():
        global Seed
        num1  =NUM()
        num2 = NUM()
        Seed = the['seed']
        for i in range(1,10^3+1):
            num1.add(rand(0, 1))
        Seed = the['seed']
        for i in range(1,10^3+1):
            num2.add(rand(0, 1))
        m1 = rnd(num1.mid(), 10)
        m2 = rnd(num2.mid(), 10)
        return m1 == m2 and .5 == rnd(m1, 1)
    eg("rand","generate, reset, regenerate same", randfun)

    def symfun():
        sym = SYM()
        for x in ["a","a","a","a","b","b","c"]:
            sym.add(x)
        return "a" == sym.mid() and 1.379 == rnd(sym.div())
    eg("sym","check syms", symfun)

    def numfun():
        num = NUM()
        for x in [1,1,1,1,2,2,3]:
            num.add(x)
        return 11/7 == num.mid() and 0.787 == rnd(num.div())

    eg("num", "check nums", numfun)


    main(the, help, egs)