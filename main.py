from igbot import InstaBot
from credentials import username_1, password_1, username_2, password_2
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":

    #Initilize Bot
    # bot_1 = InstaBot(username_1, password_1)
    bot = InstaBot(username_2, password_2)
    # Get unfollowers List
    # bot.get_unfollowers()
    
    #Get Blue tick Following List
    # bot.get_blue_tick_following()
    
    # Save DATA Locally
    # bot.persist_data()

    # Unfollow Unfollwers
    # bot_1.unfollow_unfollowers(50)
    bot.unfollow_unfollowers_bySearch(10)
