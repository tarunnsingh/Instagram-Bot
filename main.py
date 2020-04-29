import InstaBot from igbot
from credentials import username, password

if __name__ == "__main__":

    #Initilize Bot
    bot = InstaBot(username, password)

    #Get Blue tick Following List
    bot.get_blue_tick_following()
