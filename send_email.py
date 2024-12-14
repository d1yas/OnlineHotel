import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "newkingg08@gmail.com"
receiver_email = "diyasdjumabaevv@gmail.com"
app_password = "pvrd qxfk sdsd znlf"

subject = "SMTP orqali yuborilgan xabar"
body = "Assalomu alaykum! Bu xabar SMTP orqali yuborildi."

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Xabar muvaffaqiyatli yuborildi!")
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")
finally:
    server.quit()
