from igbot import InstaBot
from credentials import username_1, password_1
import warnings
from tkinter import *
warnings.filterwarnings('ignore')


# Note: UNCOMMENT ANY PART 1. For Working on GUI or 2. Working on development.


# FOR GENERATING RELEASE ==============================================================================================

root = Tk()
root.title("InstaBot")

def start_process():
    automate_label = Label(root, text="Bot Started for " + user_input.get() + ". See Command Prompt.").grid(row = 5, column = 0)
    bot = InstaBot(user_input.get(), pass_input.get())
    if(followCount.get() == 1):
        bot.get_followers_following()
        bot.get_blue_tick_following()
        bot.unfollow_unfollowers_by_search(50)
    elif(followCount.get() == 2):
        bot.follow(20, 5)
    
username_label = Label(root, text="Enter Username").grid(row = 0, column = 0)
user_input = Entry(root)
user_input.grid(row = 0, column = 1)
password_label = Label(root, text="Enter Password").grid(row = 1, column = 0)
pass_input = Entry(root, show="*")
pass_input.grid(row = 1, column = 1)
followCount = IntVar()
Radiobutton(root, text = "Unfollow Unfollwers", variable=followCount, value=1).grid(row=2, column= 0)
Radiobutton(root, text = "Follow More People", variable=followCount, value=2).grid(row=3, column= 0)
start_bot_butoon = Button(root, padx=50, pady=10, text="Automate!", command= start_process).grid(row = 4, column = 0)

root.mainloop()


# FOR DEVELOPMENT ======================================================================================================

#Initilize Bot
# bot = InstaBot(username_2, password_2)

# bot.get_followers_following()
# bot.get_unfollowers()
# bot.get_unfollowing()
# bot.get_blue_tick_following()

# Unfollow Unfollwers
# bot.follow(20, 5)
