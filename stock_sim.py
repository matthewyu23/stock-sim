import requests
import json
import pickle
import threading

watchList = ["APPL", "MSFT", "AMZN"] #initial watchlist for first time loggin
positions = {}

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
    print("opened W pickle")
except (Exception) as e:
    saveWPickle(watchList)
    print("made a W pickle")

try: 
    positions = openPPickle()
    print("opened P pickle")
except (Exception) as e:
    savePPickle(watchList)
    print("made a P pickle")


while True: 
    print("Watch List: "+ str(watchList))
    print("Positions: " + str(positions))


    userInput = input("ADD/REMOVE/BUY/SELL: ").lower() #checking user input
    if userInput == "add": 
        watchList.append(input("TICKER: ").upper())
        saveWPickle(watchList)
    elif userInput == "remove": 
        watchList.remove(input("TICKER: ").upper())
        saveWPickle(watchList)
    elif userInput == "buy": 
        positions.update({input("TICKER: ").upper() : input("HOW MANY SHARES: ")})
        savePPickle(positions)
    elif userInput == "sell": 
        del positions[input("TICKER: ").upper()]
        savePPickle(positions)
    elif userInput == "reset": 
        watchList = []
        positions = {}
        saveWPickle(watchList)
        savePPickle(positions)
    else: 
        print("Invalid command")
    
    
                    




#response = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_520e6bf649924304a029ffc1d880fd0e")

#print(response.json())
