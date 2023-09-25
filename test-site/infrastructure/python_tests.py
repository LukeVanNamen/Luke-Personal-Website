import unittest
import requests
import subprocess
from urllib.request import urlopen

class TestFrontEndSite(unittest.TestCase):
    def test_web_app_running(self):
        try:
             r = requests.get("https://www.lukevannamen.com/#home")
        except:
            self.fail("Could not open web app. Not running, or crashed. Test Failed")

    def test_text(self):
        r = requests.get("https://www.lukevannamen.com/#home")
        page_src = r.text
 
        if page_src.find("Download Resume") < 0:
            self.fail("Resume not available")
        if page_src.find("Luke") < 0:
            self.fail("Can't find name")
        if page_src.find("Views") < 0:
            self.fail("Can't find views")
    
    def test_projects(self):
        r = requests.get("https://www.lukevannamen.com/#projects")
        page_src = r.text

        if page_src.find("Projects") < 0:
            self.fail("Can't find Projects")

    # We could also write a test that tests if the count value can be found in the site
    def test_find_count_value(self):
        r = requests.get("https://cwsqxbwez7.execute-api.us-east-1.amazonaws.com/Prod/counter").json()
        
        # Pull all text from the BodyText div
        visitor_count1 = r['Visitors']

        if(visitor_count1):
            print('\033[92m' + "PASS (VC Good)" + '\033[0m')
        else:
            print('\033[91m' + "FAIL (VC Good)" + '\033[0m')

    # We need to add one more test here to check if the counter value
    # is returned correctly if we call API
    def test_count_update(self):
        r = requests.get("https://cwsqxbwez7.execute-api.us-east-1.amazonaws.com/Prod/counter").json()
        
        # Pull all text from the BodyText div
        visitor_count1 = r['Visitors']

        # Define the command to execute using curl
        call_site = ['curl', '-s', "https://www.lukevannamen.com/#home"]
        subprocess.run(call_site, capture_output=False, text=True, stdout=subprocess.DEVNULL)

        r = requests.get("https://cwsqxbwez7.execute-api.us-east-1.amazonaws.com/Prod/counter").json()
        visitor_count2 = r['Visitors']

        if(visitor_count1 < visitor_count2):
            print('\033[92m' + "PASS (VC Increase)" + '\033[0m')
        else:
            print('\033[91m' + "FAIL (VC Increase)" + '\033[0m')

if __name__ == '__main__':
    unittest.main()
