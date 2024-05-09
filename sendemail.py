from flask import *
from flask_mail import *
from random import *
import os
app = Flask(__name__)
mail = Mail(app)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
  # Generate OTP without leading zeros

def verify(email):
    otp = randint(100000, 999999)
    email = email
    msg = Message('Your OTP for SecureAnon registration', sender='secureanon2024@gmail.com', recipients=[email])
    
    msg.body = f"""Dear User,

We are excited to have you join SecureAnon! To complete your registration, we need to verify your email address.

Your One-Time Passcode (OTP) for SecureAnon registration is: {otp}

Please enter this code within the next 10 minutes to complete your registration. If you did not request this OTP, please ignore this email.

Thank you for choosing SecureAnon. We look forward to helping you stay secure online.

Best regards,
The SecureAnon Team
"""
    
    mail.send(msg)
    print("verify")
    return otp

if __name__ == '__main__':
    with app.app_context():
        verify()
    app.run(debug=True)