import re

def fmt(sControl , *elements): # emulate printf
    print(sControl%(elements)) 

#test
##a=1
##b=2
##fmt("%s and %s" , a , b) --> "1 and 2"


def o(t , *isKeys): #--> s; convert `t` to a string. sort named keys.
    if type(t) != dict:
        return str(t)
    
    def fun(k , v):
        if not re.findall('[^_]'):
            return fmt(":%s %s",o(k),o(v))
    
    return '{' + ' '.join([str(len(t) > 0) , str(not isKeys) , str(map(t , o)) , str(sort(kap(t , fun)))]) + '}'

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
    




