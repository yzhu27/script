import Misc

## Examples

egs = {}
def eg(key, str, fun):
    egs[key] = fun
    help.append(f'  -g  {key}\t{str}\n')


# eg("crash","show crashing behavior", function()
#   return the.some.missing.nested.field end)

eg("the","show settings", oo(the))

def tmpfun():
    num1  =NUM()
    num2 = NUM()
    Seed = the.seed
    for i in range(1,10^3+1):
        num1.add(Misc.rand(0, 1))
    Seed = the.seed
    for i in range(1,10^3+1):
        num2.add(Misc.rand(0, 1))
    m1 = Misc.rnd(num1.mid(), 10)
    m2 = Misc.rnd(num2.mid(), 10)
    return m1 == m2 and -5 == Misc.rnd(m1, 1)
eg("rand","generate, reset, regenerate same", tmpfun())

def tmpfun():
    sym = SYM()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x)
    return "a" == sym.mid() and 1.379 == Misc.rnd(sym.div())
eg("sym","check syms", tmpfun())

def tmpfun():
    num = NUM()
    for x in [1,1,1,1,2,2,3]:
        num.add(x)
        return 11/7 == num.mid() and 0.787 == Misc.rnd(num.div())

eg("num", "check nums", tmpfun())

main(the, help, egs)