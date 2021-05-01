import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendemail(email, link):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    me = "teenengineer3@gmail.com"
    server.login(me, password="abc")

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your One Time Password"
    msg['From'] = me
    msg['To'] = email
    html = '''
    <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
            <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Reshami Dhaga</a>
            </div>
            <p style="font-size:1.1em">Hi,</p>
            <p>Use the following link to complete your Sign Up procedures. link is valid for 5 minutes</p>
            <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">'''+link+'''</h2>
            <hr style="border:none;border-top:1px solid #eee" />
            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
            </div>
        </div>
    </div>'''
    body = MIMEText(html, 'html')
    msg.attach(body) 
    server.sendmail("", email, msg.as_string())
    server.quit() 


def generaterandomotp():
    otp = "".join([str(random.randint(0,9)) for i in range(4)])
    return otp



# def main():
#     email = input("Enter Email: ")
#     e = EmailValidation(email, GenerateRandomOTP())
#     e.SendEmail()
#     otp = input("Enter OTP: ")
#     if(e.ValidateEmail(otp)):
#         print("Valid OTP")
#     else:
#         print("Invalid OTP")

# if __name__ == "__main__":
#     main()
