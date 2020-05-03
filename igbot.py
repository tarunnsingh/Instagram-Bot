from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import glob
import json
import time
from datetime import datetime

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
        self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]").click()
        self.isLoggedIn = True

    def print_names(self, names):
        for i, name in enumerate(names):
            print("{}. {}".format(i + 1, name))

    def get_names(self, listname):
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
        print("{}======================>".format(listname))
        self.print_names(names)
        return names

    def get_unfollowers(self):
        if(not self.isLoggedIn):
            self._login()
        print("Getting Unfollowers for {}".format(self.username))
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}/')]".format(self.username)).click()
        sleep(2)
        self.followers = self.get_names('followers')
        self.following = self.get_names('following')
        self.persist_data_general('followers', self.followers)
        self.persist_data_general('following', self.following)
        unfollowers_names = [
            name for name in self.following if name not in self.followers]
        print("Unfollowers=====================================>")
        self.print_names(unfollowers_names)
        self.unfollowers = unfollowers_names
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[1]/div/a").click()
        sleep(2)

    def get_blue_tick_following(self):
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
        self.print_names(names)

    def persist_data(self):
        directory = self.username
        parent_dir = "./data/"
        self.path = os.path.join(parent_dir, directory)

        if(self.unfollowers != None and self.blue_tick_following != None):
            fname = self.path + '/unfollowers.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(self.unfollowers))
            txtfile.close()

            fname = self.path + '/bt_following.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(self.blue_tick_following))
            txtfile.close()

    def persist_data_general(self, filename, list_data):
        directory = self.username
        parent_dir = "./data/"
        self.path = os.path.join(parent_dir, directory)

        if list_data != None:
            fname = self.path + '/' + filename + '.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(list_data))
            txtfile.close()



    def unfollow_unfollowers(self, count):
        local_usernames_list = [ f.name for f in os.scandir("./data") if f.is_dir() ]
        if self.username in local_usernames_list : 
            print("Local data available for {}".format(self.username))
            path = os.path.join('./data', self.username)
        else:
            print("No local data available for {}".format(self.username))
            quit()
        
        unf = open(path + "/unfollowers.txt", 'r')
        self.unfollowers = (unf.read()).strip("][").replace("'", "").split(", ")
        
        btf = open(path + "/bt_following.txt", 'r')
        self.blue_tick_following = (btf.read()).strip("][").replace("'", "").split(", ")
        
        print("{} has {} Unfollwers and {} BT Following.".format(self.username, len(self.unfollowers), len(self.blue_tick_following)))

        if count > 50 :
            print("Set count to unfollow less than 50")
            quit()
        else:
            self.to_unfollow_list = [user for user in self.unfollowers if user not in self.blue_tick_following][:count]
            print("Following accounts will be unfollowed: {}".format(self.to_unfollow_list))
            # capture_time = str(datetime.now()).replace(' ', '@')
            filename = 'to_unfollow_list'
            self.persist_data_general(filename, self.to_unfollow_list)
            
            if(not self.isLoggedIn):
                self._login()
            self.driver.find_element_by_xpath("//a[contains(@href, '/{}/')]".format(self.username)).click()
            sleep(5)
            self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
            sleep(4)
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
            last_ht, ht = 0, 1
            while (last_ht != ht):
                sleep(2)
                last_ht = ht
                ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
            for name in self.to_unfollow_list:
                print("Now Unfollowing: {}".format(name))
                link = scroll_box.find_element_by_xpath("//a[text()='{}']".format(name))
                print(link.text)
                div_parent_1 = link.find_element_by_xpath("..")
                div_parent_2 = div_parent_1.find_element_by_xpath("..")
                div_parent_3 = div_parent_2.find_element_by_xpath("..")
                div_parent_4 = div_parent_3.find_element_by_xpath("..")
                div_required = div_parent_4.find_element_by_xpath("//div[2]")
                following_button_clicked = div_required.find_element_by_xpath("//button[text()='Following']").click()
                sleep(2)
                self.driver.find_element_by_xpath("//button[text()='Unfollow']").click()
                sleep(2)
                print("Successfully Unfollowed {}".format(name))

    def unfollow_unfollowers_bySearch(self, count):
        local_usernames_list = [ f.name for f in os.scandir("./data") if f.is_dir() ]
        if self.username in local_usernames_list : 
            print("Local data available for {}".format(self.username))
            path = os.path.join('./data', self.username)
        else:
            print("No local data available for {}".format(self.username))
            quit()
        
        unf = open(path + "/unfollowers.txt", 'r')
        self.unfollowers = (unf.read()).strip("][").replace("'", "").split(", ")
        
        btf = open(path + "/bt_following.txt", 'r')
        self.blue_tick_following = (btf.read()).strip("][").replace("'", "").split(", ")
        
        print("{} has {} Unfollwers and {} BT Following.".format(self.username, len(self.unfollowers), len(self.blue_tick_following)))

        if count > 50 :
            print("Set count to unfollow less than 50")
            quit()
        else:
            if(not self.isLoggedIn):
                self._login()
            for user in self.unfollowers:
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