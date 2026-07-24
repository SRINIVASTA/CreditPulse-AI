import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Your exact deployment URL
STREAMLIT_URL = "https://creditpulse-ai-ow7sdnqsrbt6yf4ddtrxmc.streamlit.app/" 

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"Navigating to {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        time.sleep(5)  # Wait for page to initialize
        
        # Look for Streamlit's "Yes, get this app back up!" sleep button
        # This checks for the common button text elements Streamlit uses when sleeping
        try:
            wake_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Wake up') or contains(., 'get this app back up')]"))
            )
            wake_button.click()
            print("App was asleep! Clicked the wake-up button successfully.")
            time.sleep(10)  # Wait for it to spin up
        except:
            print("App is already awake or sleep button was not found. Excellent!")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
