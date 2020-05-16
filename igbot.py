from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import os
import glob
import json
import time
from datetime import datetime
import sys
from random import randrange
from tqdm import tqdm

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.isLoggedIn = False
        
    def _login(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath(
            "//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath(
            "//input[@name=\"password\"]").send_keys(self.password)
        self.driver.find_element_by_xpath(
            "//button[@type=\"submit\"]").click()
        sleep(10)
        try:
            self.driver.find_element_by_xpath(
                "//button[contains(text(), 'Not Now')]").click()
        except:
            print("No Not Now Button!")
        self.isLoggedIn = True
        
        print("Logged in to: {}".format(self.username))
        
        # REACHES THE HOME PAGE FOR A USER

    def _print_names(self, names):
        for i, name in enumerate(names):
            print("{}. {}".format(i + 1, name))

    def _get_names(self, listname):
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}')]".format(listname)).click()
        sleep(4)
        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while (last_ht != ht):
            sleep(2)
            last_ht = ht
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [title.text for title in links if title.text != '']
        sleep(2)
        self.driver.refresh()
        sleep(2)
        print("{} count: {}".format(listname, len(names)))
        return names

    def _read_list(self, listname):
        local_usernames_list = [ f.name for f in os.scandir("./data") if f.is_dir() ]
        if self.username in local_usernames_list : 
            print("Local data available for {}".format(self.username))
            path = os.path.join('./data', self.username)
            list_opened = open(path + "/" + listname + ".txt", 'r')
            req_list = (list_opened.read()).strip("][").replace("'", "").split(", ")
            print("Read from Local Data => {} count: {}".format(listname, len(req_list)))
            return req_list
        else:
            print("No local data available for {}".format(self.username))
            quit()

    def _persist_data(self, filename, list_data):
        directory = self.username
        parent_dir = "./data/"
        self.path = os.path.join(parent_dir, directory)

        if(not os.path.isdir(self.path)):
            os.mkdir(path)

        if list_data != None:
            fname = self.path + '/' + filename + '.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(list_data))
            txtfile.close()
        else :
            print("{} is empty list.".format(list_data))

    def get_followers_following(self):
        if(not self.isLoggedIn):
            self._login()
        print("Getting Followers and Following...")
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}/')]".format(self.username)).click()
        sleep(2)
        self.followers = self._get_names('followers')
        self.following = self._get_names('following')
        self._persist_data('followers', self.followers)
        self._persist_data('following', self.following)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a/svg/path").click()
        sleep(4)

    def get_unfollowers(self):
        self.followers = self._read_list('followers')
        self.following = self._read_list('following')
        self.unfollowers = [ name for name in self.following if name not in self.followers]
        print("Unfollowers count: {}".format(len(self.unfollowers)))
        self._persist_data('unfollowers', self.unfollowers)

    def get_unfollowing(self):
        self.followers = self._read_list('followers')
        self.following = self._read_list('following')
        self.unfollowing = [ name for name in self.followers if name not in self.following]
        print("Unfollowing count: {}".format(len(self.unfollowing)))
        self._persist_data('unfollowing', self.unfollowing)

    def get_blue_tick_following(self):
        if(not self.isLoggedIn):
            self._login()
        print("Getting Blue-Tick Following for {}".format(self.username))
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}/')]".format(self.username)).click()
        sleep(2)
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/following')]").click()
        sleep(4)
        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while (last_ht != ht):
            sleep(2)
            last_ht = ht
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scroll_box)
        spans = scroll_box.find_elements_by_xpath("//span[text()='Verified']")
        names = []
        for span in spans:
            div = span.find_element_by_xpath('..')
            link = div.find_element_by_tag_name('a')
            names.append(link.text)
        self.blue_tick_following = names
        print("BT Following count: {}".format(len(self.blue_tick_following)))
        self._persist_data('bt_following', self.blue_tick_following)
        self.driver.refresh()
        sleep(4)
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a/svg/path").click()
        sleep(4)



    def unfollow_unfollowers_by_search(self, count):
        self.unfollowers = self._read_list('unfollowers')
        self.blue_tick_following = self._read_list('bt_following')
        self.unfollowed_success = self._read_list('unfollowed_success')
        # self.to_unfollow = self.unfollowers # Unfollows Blue Ticks also
        self.to_unfollow = [ name for name in self.unfollowers 
                                if name not in self.blue_tick_following
                                and name not in self.unfollowed_success][:count]
        print("Following people will be Unfollowed: ")
        self._print_names(self.to_unfollow)
        self._persist_data('to_unfollow', self.to_unfollow)
        
        self.unfollowed_success = []

        if count > 50 :
            print("Set count to unfollow less than 50")
            quit()
        else:
            if(not self.isLoggedIn):
                self._login()
            for i, user in enumerate(self.to_unfollow):
                sleep(2)
                searchbox = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]").click()
                entered_username = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(user)
                sleep(4)
                once_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                twice_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                sleep(2)
                self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div").click()
                sleep(2)
                self.driver.find_element_by_xpath("//button[text()='Unfollow']").click()
                print("{}. Successfully Unfollowed {}".format(i, user))
                self.unfollowed_success.append(user)
            
            self._persist_data('unfollowed_success', self.unfollowed_success)
    

    def follow(self, user_count, follow_count):
        if(not self.isLoggedIn):
            self._login()
        if((user_count < 1 or user_count > 10) and user_count*follow_count > 120):
            print("Set the follow user count in proper range! [ < 120]")
            quit()
        followed = 0
        follow_count_per_user = user_count/follow_count
        self.followers = self._read_list('followers')
        self._print_names(self.followers)
        for user in self.followers[:user_count]:
            try:
                n = follow_count_per_user
                sleep(2)
                searchbox = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]").click()
                entered_username = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(user)
                sleep(4)
                once_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                twice_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                sleep(2)
                self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
                sleep(4)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
                last_ht, ht = 0, 1
                while (last_ht != ht and n > 0):
                    sleep(2)
                    last_ht = ht
                    targets = scroll_box.find_elements_by_xpath("//button[text()='Follow']")
                    for i, target in enumerate(targets):
                        if(not i):
                            continue
                        target.click()
                        followed = followed + 1
                        n = n -1
                        sleep(randrange(4) + 1)
                    ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
                    
                print("Followed {} people.".format(followed))
                self.driver.refresh()
                sleep(4)
            except:
                print("Skipping user {}".format(user))
    
    def random_like(self):
        if(not self.isLoggedIn):
            self._login()
        self.followers = self._read_list('followers')
        self._print_names(self.followers)
        for user in self.followers:
            try:
                sleep(2)
                searchbox = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]").click()
                entered_username = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(user)
                sleep(4)
                once_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                twice_enter = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                sleep(2)
                self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
                sleep(4)
                scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
                last_ht, ht = 0, 1
                while (last_ht != ht and n > 0):
                    sleep(2)
                    last_ht = ht
                    links = scroll_box.find_elements_by_tag_name('a')
                    names = [title.text for title in links if title.text != '']
                    for i, target in enumerate(names):
                        if(not i):
                            continue
                        sleep(2)
                        sb = self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]").click()
                        eu = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(user)
                        sleep(4)
                        oe = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                        te = self.driver.find_element_by_xpath("//input[@placeholder=\"Search\"]").send_keys(Keys.ENTER)
                        sleep(2)
                    ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
                    
                print("Followed {} people.".format(followed))
                self.driver.refresh()
                sleep(4)
            except:
                print("Skipping user {}".format(user))


            
            