#!/usr/bin/env python3
from jet import Jet
import time

def main():
    Jet1 = Jet(False)
    Jet2 = Jet(True)

    Jet1.zero()
    Jet2.zero()

    # while(True):
    #     for x in range(-25,25,1):
    #         Jet1.dir_rq(x)
    #         Jet2.dir_rq(x)
    #         time.sleep(0.1)
    #     for y in range(25,-25,-1):
    #         Jet1.dir_rq(y)
    #         Jet2.dir_rq(y)
    #         time.sleep(0.1)
    #     Jet1.rb_rq('down')
    #     Jet2.rb_rq('down')
    #     time.sleep(1)
    #     Jet1.rb_rq('up')
    #     Jet2.rb_rq('up')

if __name__ == "__main__":
    main()
