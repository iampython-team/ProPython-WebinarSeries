
from string import Template
import smtplib
import credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_contacts(filename):
    names=[]
    emails=[]
    with open(filename,encoding='utf-8') as contact_file:
        for contact in contact_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
        return names,emails

def get_msg_template(filename):
    with open(filename,encoding='utf-8') as msg_template_file:
        message=msg_template_file.read()
    return Template(message)


def main():

    names,emails=get_contacts('contacts.txt')
    message_template=get_msg_template('messages.txt')

    # setup the SMTP server 
    server=smtplib.SMTP(credentials.HOST_NAME,credentials.PORT)
    server.ehlo()
    server.starttls()
    server.login(credentials.ADDRESS,credentials.PASSWORD)

    for name,email in zip(names,emails):
        # create message 
        msg=MIMEMultipart()
        message=message_template.substitute()
        #setup the message parameters
        msg['From']=credentials.ADDRESS
        msg['To']=email
        msg['Subject']='Automated Email sending by Pythoner'
        msg.attach(MIMEText(message,'plain'))
        server.send_message(msg)
        del msg
    server.quit()


main()
    


