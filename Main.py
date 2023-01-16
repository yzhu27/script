import re
import sys
from Strings import coerce

the = {}
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

def settings(s): # --> t;  parse help string to extract a table of options
  t = {}
  #match the contents like: '-d  --dump  on crash, dump stack = false'
  res = r"[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)"
  m = re.findall(res , s)
  for key , value in m:
      t[key] = coerce(value)
  return t
#test
##print(settings(help)) --> {'dump': False, 'go': 'data', 'help': False, 'seed': 937162211}

#Update settings from values on command-line flags. Booleans need no values
def cli(t , list):
  slots = list[1:]
  #search the key and value we want to update
  for slot , v in t.items():            
      #give each imput slot an index(begin from 0)
      for n , x in enumerate(slots):
          # match imput slot with the.keys: x == '-e' or '--eg'
          if x == ('-'+slot[0]) or x == ('--'+slot):
              v = str(v)
              #we just flip the defeaults
              if v == 'True':
                  v = 'false'
              elif v == 'False':
                  v = 'true'
              else:
                  v = slots[n+1]
              t[slot] = coerce(v)
  return t

#test
## input python3 Main.py -d in cmd 
## --> {'dump': True, 'go': 'data', 'help': False, 'seed': 937162211}
if __name__ == '__main__':
  list_of_argument = sys.argv
  the = settings(help)
  the = cli(the , list_of_argument)
  print(the)