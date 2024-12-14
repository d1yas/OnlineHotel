import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email yuborish funksiyasi
def send_booking_email(receiver_email, booking_details):
    sender_email = "onlinehotel.notifications@gmail.com"
    app_password = "pvrd qxfk sdsd znlf"
    
    subject = "Xonangiz muvaffaqiyatli bron qilindi!"
    body = (
        f"Assalomu alaykum!\n\n"
        f"✅ Siz muvaffaqiyatli xona bron qildingiz.\n\n"
        f"{booking_details}\n\n"
        f"Xizmatimizdan foydalanganingiz uchun rahmat! 😊"
    )
    
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
        print("✅ Email muvaffaqiyatli yuborildi!")
    except Exception as e:
        print(f"❗ Email yuborishda xatolik yuz berdi: {e}")
    finally:
        server.quit()
