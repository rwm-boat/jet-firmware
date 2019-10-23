from jet import Jet

def main():
    Jet1 = Jet(False)
    Jet2 = Jet(True)

    Jet1.zero()
    Jet2.zero()

    while(True):
        for x in range(-25,25):
            Jet1.dir_rq(x)
            Jet2.dir_rq(x)
        for y in range(25,-25):
            Jet1.dir_rq(y)
            Jet2.dir_rq(y)

if __name__ == "__main__":
    main()