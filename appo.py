import scrapingbee
from flask import Flask, request, render_template

# Set up the ScrapingBee client
client = scrapingbee.Client(api_key='your_api_key_here')

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form['email']
        password = request.form['password']

        # Use the ScrapingBee client to load the login page and enter the email and password
        response = client.get('https://www.doordash.com/login')
        response = client.post('https://www.doordash.com/login', data={'email': email, 'password': password})

        # Check if the login was successful
        if 'incorrect' in response.text:
            return render_template('login.html', error='Incorrect email or password')

        # Check if two-factor authentication is required
        if 'Verification Code' in response.text:
            return render_template('2fa.html')

        # Generate the unique token for the user
        token = generate_token(email)

        # Generate the orders link with the unique token
        orders_link = f'https://www.doordash.com/orders/{token}'

        # Send the orders link to the user's email
        send_email(email, orders_link)

        return render_template('orders.html', orders_link=orders_link)

    @app.route('/2fa', methods=['POST'])
    def twofa():
        email = request.form['email']
        password = request.form['password']
        code = request.form['code']

        # Use the ScrapingBee client to enter the two-factor authentication code
        response = client.post('https://www.doordash.com/login', data={'email': email, 'password': password, 'code': code})

        # Check if the login was successful
        if 'incorrect' in response.text:
            return render_template('2fa.html', error='Incorrect verification code')

        # Generate the unique token for the user
        token = generate_token(email)

        # Generate the orders link with the unique token
        orders_link = f'https://www.doordash.com/orders/{token}'

        # Send the orders link to the user's email
        send_email(email, orders_link)

        return render_template('orders.html', orders_link=orders_link)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
