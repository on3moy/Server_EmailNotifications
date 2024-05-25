import smtplib # For emailing capabilities
from email.message import EmailMessage # For emailing capabilities

# SMTP Information
RELAY = 'IP ADDRESS'
PORT = 'SOME PORT NUMBER'

# Test email information
SENDER = 'PythonBIServer-noreply@company.com'
RECIPIENTS = ['moy.patel@company.com', 'moi@company.com']
SUBJECT = 'Automated Python Test Email'
MESSAGE = f'''
Hi!

This is a test email from ServerA generated from a Python Script.

Please disregard

'''

# Create a function to send out email 
def send_email(sender, recipient, subject, message):
        '''
        Function inputs sender, recipient, subject, and message to
        send an email from SMTP Server.
        '''
        email = EmailMessage()
        email['From'] = sender
        email['To'] = recipient
        email['Subject'] = subject
        email.set_content(message)
        smtp = smtplib.SMTP(RELAY, port=PORT)
        # smtp.starttls()
        # print(smtp.starttls())
        smtp.sendmail(sender,recipient,email.as_string())
        smtp.quit()

# If statement ensure only test information is sent if directly called upon.
if __name__ == '__main__':
    try:
        print('\n')
        print('Initiating process of sending out test emails')
        print(f'Sender: {SENDER}')
        print(f'Recipients: {RECIPIENTS}')
        send_email(SENDER, RECIPIENTS, SUBJECT, MESSAGE)
    except Exception as e:
        print(e)