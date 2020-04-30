from igbot import InstaBot
from credentials import username, password
import warnings
warnings.filterwarnings('ignore')
from credentials import test_username 

if __name__ == "__main__":

    #Initilize Bot
    bot = InstaBot(username, password)

    # Get unfollowers List
    bot.get_unfollowers()
    
    #Get Blue tick Following List
    bot.get_blue_tick_following()
    
    # Save DATA Locally
    # bot.persist_data()
