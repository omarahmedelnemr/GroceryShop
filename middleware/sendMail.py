import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_random_code():
    return str(random.randint(1000, 9999))

def send_email(recipient_email,messageHeader, messageBody):
    sender_email =  "omarahmedelnemr10@gmail.com"
    # sender_password = "dfch plgx hsrz xeso"
    sender_password = "wepd esuo ftkm dgxl"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = messageHeader

    # Attach the text message
    message.attach(MIMEText(messageBody))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")

recipient_email = "omarahmedelnemr16@gmail.com"

random_code = generate_random_code()

