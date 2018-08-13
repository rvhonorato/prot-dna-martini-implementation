Alist = [(e.split()[1], e.split()[0]) for e in open('Acontacts.lis').readlines()]
top = len(Alist)/10
print 'A', ','.join([e[0] for e in Alist[:top]])

Blist = [(e.split()[1], e.split()[0]) for e in open('Bcontacts.lis').readlines()]
top = len(Blist)/10
print 'B', ','.join([e[0] for e in Blist[:top]])
