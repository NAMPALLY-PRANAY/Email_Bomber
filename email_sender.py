import smtplib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ur_email"
APP_PASSWORD = "cjrq bidk ghsp dfyp"#ur app password  

def select_files():
    """ Open file dialog to select multiple files for attachment. """
    file_paths = filedialog.askopenfilenames(title="Select Attachments")
    listbox.delete(0, tk.END)  
    for file in file_paths:
        listbox.insert(tk.END, file)  

def send_email():
    """ Sends an email with multiple attachments to multiple recipients. """
    try:
        num_times = int(entry_times.get())
        if num_times <= 0:
            messagebox.showerror("Error", "Enter a valid number of emails to send.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a numeric value.")
        return

    
    recipient_emails = entry_recipients.get().split(",")
    recipient_emails = [email.strip() for email in recipient_emails if email.strip()]

    if not recipient_emails:
        messagebox.showerror("Error", "Please enter at least one recipient email.")
        return

    
    email_subject = entry_subject.get().strip()
    email_body = text_body.get("1.0", tk.END).strip()

    if not email_subject or not email_body:
        messagebox.showerror("Error", "Subject and body cannot be empty.")
        return

    
    file_paths = list(listbox.get(0, tk.END))

    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  
    server.login(SENDER_EMAIL, APP_PASSWORD)

    for i in range(num_times):
        for recipient in recipient_emails:
            
            message = MIMEMultipart()
            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            message["Subject"] = email_subject

            
            message.attach(MIMEText(email_body, "plain"))

            
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={filename}")
                    message.attach(part)

            
            server.sendmail(SENDER_EMAIL, recipient, message.as_string())
            print(f"Email {i+1}/{num_times} sent to {recipient} successfully.")

    
    server.quit()
    messagebox.showinfo("Success", "Emails sent successfully!")


root = tk.Tk()
root.title("Email Sender with Multiple Recipients & Attachments")
root.geometry("500x550")


tk.Label(root, text="Enter recipient emails (comma separated):").pack()
entry_recipients = tk.Entry(root, width=50)
entry_recipients.pack()


tk.Label(root, text="Enter email subject:").pack()
entry_subject = tk.Entry(root, width=50)
entry_subject.pack()


tk.Label(root, text="Enter email body:").pack()
text_body = tk.Text(root, height=5, width=50)
text_body.pack()


tk.Label(root, text="Enter number of times to send email:").pack()
entry_times = tk.Entry(root)
entry_times.pack()


btn_select = tk.Button(root, text="Select Files", command=select_files)
btn_select.pack()


listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=60)
listbox.pack()


btn_send = tk.Button(root, text="Send Email", command=send_email, bg="green", fg="white")
btn_send.pack()


root.mainloop()