import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailValidation:
    def __init__(self, email, otp):
        self.email = email
        self.otp = otp

    def SendEmail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        me = "teenengineer3@gmail.com"
        server.login(me, password="abc")
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Your One Time Password"
        msg['From'] = me
        msg['To'] = self.email
        html = '''
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
            <div style="margin:50px auto;width:70%;padding:20px 0">
                <div style="border-bottom:1px solid #eee">
                <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Reshami Dhaga</a>
                </div>
                <p style="font-size:1.1em">Hi,</p>
                <p>Thank you for choosing Reshami Dhaga. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
                <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">'''+self.otp+'''</h2>
                <p style="font-size:0.9em;">Regards,<br />Reshami Dhaga</p>
                <hr style="border:none;border-top:1px solid #eee" />
                <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                <p>Reshami Dhaga Inc</p>
                </div>
            </div>
        </div>'''
        body = MIMEText(html, 'html')
        # message = "Subject: {0}\n\n{1}".format("Your One Time Password", body)
        msg.attach(body) 
        server.sendmail("", self.email, msg.as_string())
        server.quit() 

    def ValidateEmail(self, inputOtp):
        if( self.otp == inputOtp):
            return True
        return False

def GenerateRandomOTP():
    otp = "".join([str(random.randint(0,9)) for i in range(4)])
    return otp

def main():
    email = input("Enter Email: ")
    e = EmailValidation(email, GenerateRandomOTP())
    e.SendEmail()
    otp = input("Enter OTP: ")
    if(e.ValidateEmail(otp)):
        print("Valid OTP")
    else:
        print("Invalid OTP")

if __name__ == "__main__":
    main()