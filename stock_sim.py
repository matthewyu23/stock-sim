import pygame
import requests
import json
import pickle

pygame.init()
done = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))

watchList = ["APPL", "MSFT", "AMZN"] #initial watchlist for first time loggin


def openPickle(): #reassigns watchList to data in pickle file
    pickleIn = open("watchList.pickle", "rb")
    return pickle.load(pickleIn)

def savePickle(x): #dumps pickle file with watList data
    pickleOut = open("watchList.pickle", "wb")
    pickle.dump(x, pickleOut)
    pickleOut.close()


try: #opens a pickle file if there is one, creates one otherwize
    watchList = openPickle()
    print("opened pickle")
except (Exception) as e:
    savePickle(watchList)
    print("made a pickle")


print(watchList)

while not done: 

    pygame.display.set_caption('Stock Sim') 

    for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                savePickle(watchList)
                done = True
                    
                    


    
    

    pygame.display.flip() 
    screen.fill((0, 0, 0))
    clock.tick(15)



#response = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_520e6bf649924304a029ffc1d880fd0e")

#print(response.json())