import os
from multiprocessing import Pool

from time import sleep
from random import randint

import sys
import datetime
import config as cfg



def callos(room, action, mode):
    torun = "python building_access.py " + room +" " + action+" " +mode 
    print(torun)
    os.system(torun)    


if __name__ == '__main__':

    pool = Pool()
    results = []

    if (len(sys.argv) != 3) :
        print("Error: Not enough args provided")
        print("Usage: python main.py   ENV ACTION")
        print("Environment available: PROD; TEST")
        print("Action available: ADD; DEL")
        exit()

    if  "TEST" in sys.argv:
        print('Test mode') 
        MODE = "TEST"
    elif "PROD" in sys.argv:
        print('Prod mode') 
        MODE = "PROD"
    else:
        MODE = "TEST"

    if "DEL" in sys.argv:
        print('Action Del') 
        ACTION = "DEL"
        resulthall = pool.apply_async(callos, args= ["HALL","DEL",MODE])
        results.append(resulthall)

        resulta = pool.apply_async(callos, args= ["A","DEL",MODE])
        results.append(resulta)
        
    elif "ADD" in sys.argv:
        print('Action add') 
        ACTION = "ADD"
        resulthall = pool.apply_async(callos, args= ["HALL","ADD",MODE])
        results.append(resulthall)

        resulta = pool.apply_async(callos, args= ["A","ADD",MODE])
        results.append(resulta)
        
        
    

    [result.wait() for result in results]
    print("DONE")
    sleep(10)
    # os.system("python main.py HALL ADD")
    # os.system("python main.py A ADD")

