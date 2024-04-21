#86
#ngrok http http://localhost:8080
#java -jar selenium-server-4.19.1.jar standalone
#from bs4 import BeautifulSoup
from flask import Flask, jsonify
from selenium import webdriver
import threading
from seleniumbase import SB
from selenium.webdriver.common.by import By

import queue

#keep server = "http://localhost:4444/wd/hub"
#google VM IP internal edit: 10.146.0.3 on the same port
app = Flask(__name__)

result_queue = queue.Queue()

def scrape_website():
    try:
        print("All Modules are loaded")
        with SB(headless=True,undetectable=True, do_not_track=True,servername="http://10.128.0.2:4444/wd/hub",settings_file="selenium_base_config.py") as sb:
            print("Driver loaded")
            sb.open_new_tab()
            sb.switch_to_window(1)
            # Define the URL to scrape
            URL = "https://townwork.net/viewjob/jobid_7a0af0d4e77e6a82/"
            sb.open(URL)
            
            elem = sb.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[2]/h1')
            result_queue.put(elem.text)
            #sb.quit()
        # Capture or process scraped data here (not shown in this example)

    except Exception as e:
        print(f"Error during scraping: {str(e)}")

    

@app.route('/')
def index():
    return "Welcome to the Selenium Flask App!"

@app.route('/scrape')
def initiate_scraping():
    scraping_thread = threading.Thread(target=scrape_website)
    scraping_thread.start()
    #scraping_thread.join()
    element_text = result_queue.get()
    return jsonify({'element_text': element_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,threaded=False,processes=100)
#https://www.youtube.com/watch?v=2GkXFnDaadI&ab_channel=ThePythonOracle
