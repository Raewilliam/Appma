import base64
import pyshorteners
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s = pyshorteners.Shortener()

app = Flask(__name__)

SCRAPPINGBEE_API_KEY = 'YOUR_SCRAPPINGBEE_API_KEY'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Initialize a headless Chrome browser with ScrappingBee
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--proxy-server={SCRAPPINGBEE_API_KEY}@proxy.scraperapi.com:8001')
        driver = webdriver.Chrome(options=options)

        # Navigate to the DoorDash login page
        driver.get('https://www.doordash.com/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-anchor-id="headerSignupButton"]')))

        # Click the sign in button
        driver.find_element(By.CSS_SELECTOR, 'button[data-anchor-id="headerLoginButton"]').click()

        # Enter the email address and click continue
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"]')))
        email_input = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email_input.send_keys(email)
        driver.find_element(By.CSS_SELECTOR, 'button[data-anchor-id="loginFormSubmitButton"]').click()

        # Enter the password and sign in
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[data-anchor-id="loginFormSubmitButton"]').click()

        # Wait for the orders page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-anchor-id="ordersWrapper"]')))

        # Get the session cookie and encode it
        cookie = driver.get_cookie('dd_sess')
        encoded_cookie = base64.urlsafe_b64encode(cookie['value'].encode('utf-8')).decode('utf-8')

        # Generate a shortened URL that redirects to the orders page with the session cookie appended
        orders_url = driver.current_url
        shortened_url = s.tinyurl.short(orders_url + '?dd_sess=' + encoded_cookie)

        # Close the browser
        driver.quit()

        # Return the shortened URL to the user
        return shortened_url

    else:
        # Render the login form template
        return '''
        <form method="post">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <br>
            <button type="submit">Submit</button>
        </form>
        '''

if __name__ == '__main__':
    app.run(debug=True)
