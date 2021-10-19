import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import DEFAULT_EMAIL_HEADER, DEFAULT_EMAIL_CONTENT

def send_alert_mail(sender_email, sender_password, receiver_email, gpu_stats):
    #The mail addresses and password
    sender_address = "caohoangtung201@gmail.com"
    sender_pass = "38361067"
    receiver_address = "caohoangtung2001@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    message["Subject"] = DEFAULT_EMAIL_HEADER
    message.attach(
        MIMEText(
            f"""
                {DEFAULT_EMAIL_CONTENT}
                Thông tin GPU đây thưa các ngài
                {gpu_stats}
            """, 
            "plain"
        )
    )
    
    session = smtplib.SMTP("smtp.gmail.com", 587) # use gmail with port
    session.starttls()
    session.login(sender_email, sender_password) 
    
    text = message.as_string()
    
    session.sendmail(sender_email, receiver_email, text)

    session.quit()
    return True

# if __name__ == "__main__":
#     send_alert_mail()