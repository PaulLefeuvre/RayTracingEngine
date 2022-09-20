import multiprocessing
import os
import math
import time

def check_prime(val):
    print("{} - check".format(val))
    if(val == 2):
        return val
    elif(val == 1 or val%2 == 0):
        return 0
    else:
        for i in range(3, math.floor(val/2.0), 2):
            if(val%i == 0):
                return 0
        return val

primes = []

if __name__ == "__main__":
    # input list
    mylist = range(1000)

    # creating a pool object
    p = multiprocessing.Pool(7)

    # map list to target function
    result = p.map_async(check_prime, mylist)
    for value in result.get():
        if(value != 0):
            primes.append(value)
        print("{} - print".format(value))

    p.close()
    p.join()
    print(primes)
