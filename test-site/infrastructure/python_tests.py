import unittest
import requests
import pytest

class TestFrontEndSite(unittest.TestCase):
    def test_web_app_running(self):
        try:
             r = requests.get("https://www.lukevannamen.com/#home")
        except:
            self.fail("Could not open web app. Not running, or crashed. Test Failed")

    def test_text(self):
        r = requests.get("https://www.lukevannamen.com/#home")
        page_src = r.text
 
        if page_src.find("Greenside") < 0:
            self.fail("Can't find brand")
        if page_src.find("Luke") < 0:
            self.fail("Can't find name")
        if page_src.find("Views") < 0:
            self.fail("Can't find views")
    
    def test_projects(self):
        r = requests.get("https://www.lukevannamen.com/#projects")
        page_src = r.text

        if page_src.find("Projects") < 0:
            self.fail("Can't find Projects")

    # We need to add one more test here to check if the counter value
    # is returned correctly if we call API

    # We could also write a test that tests if the count value can be found in the site
    
        

if __name__ == '__main__':
    unittest.main()
