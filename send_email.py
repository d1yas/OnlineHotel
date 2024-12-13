# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# # Elektron pochta ma'lumotlari
# sender_email = "newkingg08@gmail.com"  # O'zingizning emailingiz
# receiver_email = "diyasdjumabaevv@gmail.com"  # Qabul qiluvchi email
# app_password = "pvrd qxfk sdsd znlf"  # Gmail app password
#
# # Xabar mazmuni
# subject = "SMTP orqali yuborilgan xabar"
# body = "Assalomu alaykum! Bu xabar SMTP orqali yuborildi."
#
# # MIME xabar yaratish
# msg = MIMEMultipart()
# msg["From"] = sender_email
# msg["To"] = receiver_email
# msg["Subject"] = subject
#
# msg.attach(MIMEText(body, "plain"))
#
# try:
#     # SMTP serverga ulanish
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()  # TLS ulanishini boshlash
#     server.login(sender_email, app_password)  # Hisobga kirish
#     server.sendmail(sender_email, receiver_email, msg.as_string())  # Xabar yuborish
#     print("Xabar muvaffaqiyatli yuborildi!")
# except Exception as e:
#     print(f"Xatolik yuz berdi: {e}")
# finally:
#     server.quit()  # Serverdan chiqish
