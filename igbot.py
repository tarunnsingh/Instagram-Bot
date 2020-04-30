from time import sleep
from selenium import webdriver
import os

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath(
            "//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath(
            "//input[@name=\"password\"]").send_keys(password)
        self.driver.find_element_by_xpath(
            "//button[@type=\"submit\"]").click()
        sleep(10)
        self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Not Now')]").click()

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
        print("Getting Unfollowers for {}".format(self.username))
        self.driver.find_element_by_xpath(
            "//a[contains(@href, '/{}/')]".format(self.username)).click()
        sleep(2)
        self.followers = self.get_names('followers')
        self.following = self.get_names('following')
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
        os.mkdir(self.path)

        if(self.unfollowers != None and self.blue_tick_following != None):
            fname = self.path + '/unfollowers.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(self.unfollowers))
            txtfile.close()

            fname = self.path + '/bt_following.txt'
            txtfile = open(fname, 'w')
            txtfile.write(str(self.blue_tick_following))
            txtfile.close()


    def remove_unfollowers(self):
        to_remove = [name for name in self.unfollowers if name not in self.blue_tick_following]
        to_remove = to_remove[:25]
