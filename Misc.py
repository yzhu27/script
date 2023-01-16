# Misc support functions
import math

## Numerics 

Seed = 937162211

# n ; a integer lo..hi-1
def rint(lo, hi):
    return math.floor(0.5 + rand(lo, hi))

# n; a float "x" lo<=x < x
def rand(lo, hi):
    lo = lo or 0
    hi = hi or 1
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

# num. return `n` rounded to `nPlaces`
def rnd(n, nPlaces):
    mult = 10^(nPlaces or 3)
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
def sort(t:list, fun):
    return sorted(t, key=fun)

# ss; return list of table keys, sorted
def keys(t:list):
    return sorted(kap(t, lambda k, _:k))