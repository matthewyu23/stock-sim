import requests
import json
import pickle
import os
try: 
    import termcolor
except (Exception): 
    os.system("pip3 install termcolor")
    import termcolor

watchList = {} #initial watchlist for first time loggin
positions = {}
money = [0, 10000]
inputError = False
insufficientFunds = False
insufficientShares = False
forceRefresh = False

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
    print("Updating prices...")
    for x in list(watchList): 
        del watchList[x]
        x = x.lower()
        response = requests.get(f"https://cloud.iexapis.com/stable/stock/{x}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e") 
        change = requests.get(f"https://cloud.iexapis.com/stable/stock/{x}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["changePercent"]
        if change >= 0: 
            change = "+" + format(change*100, ".2f")
        else: 
            change = format(change*100, ".2f")
        watchList[x.upper()] = "$" + format(response.json()["latestPrice"], ".2f") + ", " + change + "%"

def calculateInvested(): 
    print("Updating wealth...")
    money[0] = 0
    for x in list(positions): 
        if len(positions) > 0: 
            money[0] = money[0] + float(positions[x.upper()]) * float(requests.get(f"https://cloud.iexapis.com/stable/stock/{x.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"])


def coloredList(myList): 
    listPrint = ""
    for x in myList: 
        tickerChange = requests.get(f"https://cloud.iexapis.com/stable/stock/{x.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["change"]
        if tickerChange < 0: 
            if myList == positions: 
                if myList[x] == "1": 
                    share = " share"
                else: 
                    share = " shares"
                listPrint = listPrint + termcolor.colored(x + ": " + str(myList[x]) + share, "red") + " | "
            else: 
                listPrint = listPrint + termcolor.colored(x + ": " + str(myList[x]), "red") + " | "
        else: 
            if myList == positions: 
                if myList[x] == "1": 
                    share = " share"
                else: 
                    share = " shares"
                listPrint = listPrint + termcolor.colored(x + ": " + str(myList[x]) + share, "green") + " | "
            else: 
                listPrint = listPrint + termcolor.colored(x + ": " + str(myList[x]), "green") + " | "
    return listPrint[:len(listPrint)-3]

def bold(x): 
    return termcolor.colored(x, attrs=["bold"])

while True: 
    if not (inputError or insufficientFunds or insufficientShares) or forceRefresh == True: 
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        updatePrices()
        calculateInvested()
        forceRefresh = False
    coloredWatchList = coloredList(watchList)
    coloredPositionList = coloredList(positions)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    if inputError: 
        termcolor.cprint("Input error", "red" , attrs=["bold", "underline"])
        inputError = False
    if insufficientFunds: 
        termcolor.cprint("Insufficient funds", "red" , attrs=["bold", "underline"])
        insufficientFunds = False
    if insufficientShares: 
        termcolor.cprint("Insufficient shares", "red" , attrs=["bold", "underline"])
        insufficientShares = False
    print(bold("Watch List: ") + coloredWatchList)
    print(bold("Positions: ") + coloredPositionList)
    print(bold("Invested: ") + str("$" + format(money[0], ".2f")))
    print(bold("Cash: ") + str("$" + format(money[1], ".2f")))
    net = ((money[0] + money [1])/10000) - 1
    if net < 0: 
        net = format(net, ".2f")
        net = net  + "%"
        coloredNet = termcolor.colored(net, "red")
    else: 
        net = "+" + format(net, ".2f") + "%"
        coloredNet = termcolor.colored(net, "green")
    print(bold("Net: ") +  coloredNet)

    userInput = input("\nADD/REMOVE/BUY/SELL/REFRESH: ").lower() #checking user input
    if userInput == "add": 
        try: 
            ticker = input("TICKER: ")
            temp = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"]
            watchList.update({ticker.upper() : 0})
            saveWPickle(watchList)
        except (Exception): 
            inputError = True
            continue
        
    elif userInput == "remove": 
        try: 
            ticker = input("TICKER: ")
            temp = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"]
            del watchList[ticker.upper()]
            saveWPickle(watchList)
        except (Exception): 
            inputError = True
            continue
    elif userInput == "buy": 
        toBuy = input("TICKER: ")
        numberOfSharesToBuy = input("HOW MANY SHARES: ")
        try: 
            transaction = float(numberOfSharesToBuy) * float(requests.get(f"https://cloud.iexapis.com/stable/stock/{toBuy.lower()}/quote?token=pk_520e6bf649924304a029ffc1d880fd0e").json()["latestPrice"])
        except (Exception): 
            inputError = True
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
        else: 
            insufficientFunds = True
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
            else: 
                insufficientShares = True
        except (Exception): 
            inputError = True
            continue
    elif userInput == "reset": 
        watchList = {}
        positions = {}
        money = [0, 10000]
        saveWPickle(watchList)
        savePPickle(positions)
        saveMPickle(money)
    elif userInput == "refresh": 
        forceRefresh = True
    else: 
        inputError = True