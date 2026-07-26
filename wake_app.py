import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

STREAMLIT_URL = "https://creditpulse-ai-ow7sdnqsrbt6yf4ddtrxmc.streamlit.app/" 

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Optional: Spoof user agent to prevent cloud blocking
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"Navigating to {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        time.sleep(7)  # Give the main page wrapper time to load
        
        # 1. Streamlit clouds embed the actual app interface inside an iframe.
        # We must find the iframe and switch Selenium's focus inside it.
        try:
            print("Checking for Streamlit app iframe...")
            iframe = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            print("Successfully switched to app iframe context.")
        except Exception as iframe_err:
            print(f"Could not find or switch to iframe: {iframe_err}")
            print("Proceeding in default context...")

        # 2. Look for the wake-up button inside the iframe context
        try:
            print("Searching for the wake-up button...")
            # Streamlit button uses "Yes, get this app back up!" text exactly.
            wake_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'get this app back up')]"))
            )
            
            # Scroll to element to ensure it is in view before clicking
            driver.execute_script("arguments[0].scrollIntoView(true);", wake_button)
            time.sleep(1)
            
            wake_button.click()
            print("Success! Clicked the 'Yes, get this app back up!' button.")
            
            # Wait for the server spin-up animation to clear
            print("Waiting for app to spin up...")
            time.sleep(15) 
            
        except Exception as button_err:
            print("Wake up button not found. The app is likely already running!")
            
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        # Switch back to default content before quitting (good practice)
        try:
            driver.switch_to.default_content()
        except:
            pass
        driver.quit()
        print("Driver closed.")

if __name__ == "__main__":
    main()
