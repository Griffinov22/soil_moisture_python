import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv
import os
config = load_dotenv(".env")

smtp_server = "smtp.gmail.com"
port = 465
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASSWORD')

context = ssl.create_default_context()
date = datetime.now().strftime('%B %d, %Y @%I:%M %p')
time = datetime.now().strftime('%I:%M %p')

def send_email(score, me = sender_email, receiving_emails = None):
    if (receiving_emails is None):
      receiving_emails = [sender_email]

    if (score > 680):
        bg = 'firebrick'
        response = 'Your garden is dry! It needs water'
    elif (score > 620):
        bg = 'orange'
        response = 'Your garden is starting to dry up. Consider watering in the next couple hours'
    elif (score > 420):
        bg = 'green'
        response = 'Your garden is healthy and watered! Job well done.'
    else:
        bg = 'rebeccapurple'
        response = 'Your garden is drowning! Stop watering!'

    html = f"""
    <html>
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Garden Score</title>
      </head>
      <body>
        <div
          style="
            display: flex;
            justify-content: center;
            align-items: start end;
            min-height: 300px;
            padding: 10px;
            background: {bg};
            width: fit-content;
          "
        >
          <div style="border-radius: 10px; background-color: white; padding: 25px; margin-right: 10px">
            <h2>Moisture Score:</h2>
            <p><em style="font-weight: 900; font-size: 2.5rem">{score}</em> <sub>/710</sub></p>
            <i>This score ranges from 340-710</i>
          </div>
          <div style="border-radius: 10px; background-color: white; padding: 25px">
            <h2>Garden Score:</h2>
            <p>{response}</p>
            <p style="text-align:center;">{time}</p>
          </div>
        </div>
      </body>
    </html>
    """

    for i in range(len(receiving_emails)):
      msg = MIMEMultipart("alternative")
      msg['Subject'] = f'''Garden Test {date}'''
      msg["From"] = me
      msg["You"] = receiving_emails[i]

      pack = MIMEText(html, 'html')
      msg.attach(pack)

    with smtplib.SMTP_SSL(smtp_server,port) as server:
        try:
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiving_emails, msg.as_string())
            return 204
        except Exception as e:
            return 500
        finally:
            server.close()
            