import requests
import json
import pickle

watchList = {} #initial watchlist for first time loggin
positions = {}
money = [0, 10000]

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

def openMPickle(): 
    pickleIn = open("money.pickle", "rb")
    return pickle.load(pickleIn)

def saveMPickle(x): 
    pickleOut = open("money.pickle", "wb")
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

try: 
    money = openMPickle()
except (Exception) as e:
    saveMPickle(money)


def updatePrices(): 
    print("updating prices")
    for x in list(watchList): 
        del watchList[x]
        x = x.lower()
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{x}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e")
        watchList[x.upper()] = "$" + str(response.json()["latestPrice"]) 

def calculateInvested(): 
    print("updating wealth")
    money[0] = 0
    for x in list(positions): 
        if len(positions) > 0: 
            x = x.lower()
            money[0] = money[0] + float(positions[x.upper()]) * float(requests.get(f"https://cloud.iexapis.com/stable/stock/{x}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"])
while True: 

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    updatePrices()
    calculateInvested()
    print("Watch List: "+ str(watchList))
    print("Positions: " + str(positions))
    print("Invested: " + str(round(money[0], 2)))
    print("Uninvested: " + str(round(money[1], 2)))


    userInput = input("ADD/REMOVE/BUY/SELL: ").lower() #checking user input
    if userInput == "add": 
        watchList.update({input("TICKER: ").upper() : 0})
        saveWPickle(watchList)
        
    elif userInput == "remove": 
        del watchList[input("TICKER: ").upper()]
        saveWPickle(watchList)
    elif userInput == "buy": 
        toBuy = input("TICKER: ")
        numberOfSharesToBuy = input("HOW MANY SHARES: ")
        try: 
            transaction = float(numberOfSharesToBuy) * float(requests.get(f"https://cloud.iexapis.com/stable/stock/{toBuy.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"])
        except (Exception): 
            continue
        if transaction <= money[1]: 
            money[1] = money [1] - transaction
            saveMPickle(money)
            try: 
                positions[toBuy.upper()] = str(int(positions[toBuy.upper()]) + int(numberOfSharesToBuy))
                savePPickle(positions)
            except (Exception): 
                positions.update({toBuy.upper() : numberOfSharesToBuy})
                savePPickle(positions)
    elif userInput == "sell": 
        toSell = input("TICKER: ")
        numberOfSharesToSell = input("Shares: ")
        try: 
            if int(numberOfSharesToSell) <= int(positions[toSell.upper()]): 
                transaction = float(numberOfSharesToSell) * float(requests.get(f"https://cloud.iexapis.com/stable/stock/{toSell.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"])
                money[0] = money[0] - transaction
                money[1] = money[1] + transaction
                saveMPickle(money)
                positions[toSell.upper()] = str(int(positions[toSell.upper()]) - int(numberOfSharesToSell))
                if positions[toSell.upper()] == "0": 
                    del positions[toSell.upper()]
                savePPickle(positions)
        except (Exception): 
            print("You don't own this stock")
    elif userInput == "reset": 
        watchList = {}
        positions = {}
        money = [0, 10000]
        saveWPickle(watchList)
        savePPickle(positions)
        saveMPickle(money)
    else: 
        print("Invalid command")