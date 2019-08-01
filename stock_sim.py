import requests
import json
import pickle
import threading

watchList = {} #initial watchlist for first time loggin
positions = {}
wealth = []

def openWPickle(): #reassigns watchList to data in pickle file
    pickleIn = open("watchList.pickle", "rb")
    return pickle.load(pickleIn)

def saveWPickle(x): #dumps pickle file with watList data
    pickleOut = open("watchList.pickle", "wb")
    pickle.dump(x, pickleOut)
    pickleOut.close()

def openPPickle(): 
    pickleIn = open("positions.pickle", "rb")
    return pickle.load(pickleIn)

def savePPickle(x): 
    pickleOut = open("positions.pickle", "wb")
    pickle.dump(x, pickleOut)
    pickleOut.close()


try: #opens a pickle file if there is one, creates one otherwize
    watchList = openWPickle()
except (Exception) as e:
    saveWPickle(watchList)

try: 
    positions = openPPickle()
except (Exception) as e:
    savePPickle(watchList)


def updatePrices(): 
    print("updating prices")
    for x in list(watchList): 
        del watchList[x]
        x = x.lower()
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{x}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e")
        watchList[x.upper()] = "$" + str(response.json()["latestPrice"]) 

while True: 

    
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    updatePrices()
    print("Watch List: "+ str(watchList))
    print("Positions: " + str(positions))
    print("Wealth: " + wealth)


    userInput = input("ADD/REMOVE/BUY/SELL: ").lower() #checking user input
    if userInput == "add": 
        watchList.update({input("TICKER: ").upper() : 0})
        saveWPickle(watchList)
        
    elif userInput == "remove": 
        del watchList[input("TICKER: ").upper()]
        saveWPickle(watchList)
    elif userInput == "buy": 
        positions.update({input("TICKER: ").upper() : input("HOW MANY SHARES: ") + " shares"})
        savePPickle(positions)
    elif userInput == "sell": 
        del positions[input("TICKER: ").upper()]
        savePPickle(positions)
    elif userInput == "reset": 
        watchList = {}
        positions = {}
        saveWPickle(watchList)
        savePPickle(positions)
    else: 
        print("Invalid command")