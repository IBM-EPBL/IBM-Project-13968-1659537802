import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sendamail(to, sub):
    if(sub == "Registration Successful!"):
        c = "<strong>Hello!,</strong><br><h1> Welcome to VAST Plasma Donor Application</h1>You can use this application to: <br><ol><li>Check Eligibility</li><li>Save Health Card</li><li>View nearby Camps</li><li>Donate to emergencies</li><br>and many more!"
    elif(sub == "Health Card Updated Successfully"):
        c = "<strong>Hello!,</strong><br><h1>You can now view your updated information in your Dashboard!</h1>"
    else:
        c = "<strong>Hello!,</strong><br><h1>DONATE AND RESONATE!<h1>By agreeing to donate, you have agreed to the noble cause of saving a life!!<br> We sincerely thank you on behalf of everyone!<br>You can get the hospital details in your dashboard.<br><br><br>For further assistance, contact us via watson chat assistant."
    message = Mail(
        from_email='abhisheknarayan19006@cse.ssn.edu.in',
        to_emails=to,
        subject=sub,
        html_content=c)
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)