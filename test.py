



def test(cycl):
   i =0
   while True:
        i+=1
        yield i//cycl+1

from itertools import cycle

cycle = cycle([0,1,2,3,4])



a =  test(5)
for i in range(20):
    print()



