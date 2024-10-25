import smtplib
import os
from tkinter import Tk, Label, Entry, Button, Text, END, filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(sender_email, sender_password, to_emails, cc_emails, bcc_emails, subject, body, smtp_server, smtp_port, attachment_paths):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_emails
    msg['Cc'] = cc_emails
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Add attachments if any
    for attachment in attachment_paths:
        filename = os.path.basename(attachment)
        attachment_part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as f:
            attachment_part.set_payload(f.read())
        encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attachment_part)

    recipients = to_emails.split(',') + cc_emails.split(',') + bcc_emails.split(',')

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


def open_file_dialog():
    filename = filedialog.askopenfilename()
    if filename:
        attachment_list.append(filename)
        attachment_box.insert(END, filename + "\n")


def send_email_gui():
    sender_email = sender_entry.get()
    # jicg rsgy heug uxub
    sender_password = password_entry.get()
    to_emails = to_entry.get()
    cc_emails = cc_entry.get()
    bcc_emails = bcc_entry.get()
    subject = subject_entry.get()
    body = body_text.get("1.0", END)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    send_email(sender_email, sender_password, to_emails, cc_emails, bcc_emails, subject, body, smtp_server, smtp_port, attachment_list)


# Set up GUI using Tkinter
root = Tk()
root.title("Email Sender")
root.geometry("550x550")

# Labels and Entries
Label(root, text="Sender Email").grid(row=0, column=0)
sender_entry = Entry(root, width=50)
sender_entry.grid(row=0, column=1)

Label(root, text="Password").grid(row=1, column=0)
password_entry = Entry(root, show="*", width=50)
password_entry.grid(row=1, column=1)

Label(root, text="To (Recipients)").grid(row=2, column=0)
to_entry = Entry(root, width=50)
to_entry.grid(row=2, column=1)

Label(root, text="CC").grid(row=3, column=0)
cc_entry = Entry(root, width=50)
cc_entry.grid(row=3, column=1)

Label(root, text="BCC").grid(row=4, column=0)
bcc_entry = Entry(root, width=50)
bcc_entry.grid(row=4, column=1)

Label(root, text="Subject").grid(row=5, column=0)
subject_entry = Entry(root, width=50)
subject_entry.grid(row=5, column=1)

Label(root, text="Body").grid(row=6, column=0)
body_text = Text(root, height=10, width=50)
body_text.grid(row=6, column=1)

# Attachments
Label(root, text="Attachments").grid(row=7, column=0)
attachment_list = []
attachment_box = Text(root, height=5, width=50)
attachment_box.grid(row=7, column=1)

Button(root, text="Add Attachment", command=open_file_dialog).grid(row=8, column=1)

# Send Button
send_button = Button(root, text="Send Email", command=send_email_gui)
send_button.grid(row=9, column=1)

root.mainloop()
