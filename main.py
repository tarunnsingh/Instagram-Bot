from igbot import InstaBot
from credentials import username_1, password_1, username_2, password_2
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":

    #Initilize Bot
    bot = InstaBot(username_2, password_2)
    
    # bot.get_followers_following()
    # bot.get_unfollowers()
    # bot.get_unfollowing()
    # bot.get_blue_tick_following()
    
    # Unfollow Unfollwers
    bot.follow(10, 5)
