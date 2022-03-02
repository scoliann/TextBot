'''
    TextBot Prerequisite Steps:

        1)  Create gmail account
        2)  Allow less secure apps (for smtp and imap):  https://www.google.com/settings/security/lesssecureapps
        
'''


# Do imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import imaplib
import email


class TextBot:


    # Define class variables
    d_provider_sms_emails = {
        'at&t': '@txt.att.net',
        'sprint': '@messaging.sprintpcs.com',
        't-mobile': '@tmomail.net',
        'verizon': '@vtext.com',
    }
    d_provider_mms_emails = {
        'at&t': '@mms.att.net',
        'sprint': '@pm.sprint.com',
        't-mobile': '@tmomail.net',
        'verizon': '@vzwpix.com',
    }


    def __init__(self, s_email, s_password):
        
        # Check that email is a gmail address
        assert '@gmail.com' in s_email, \
            f'\nError:\tEmail must be a gmail address: {s_email}'

        # Define instance variables
        self.s_email = s_email
        self.s_password = s_password

        # Log into smtp server
        self.o_smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.o_smtp_server.starttls()
        self.o_smtp_server.login(self.s_email, self.s_password)

        # Log into imap server
        self.o_imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
        self.o_imap_server.login(self.s_email, self.s_password)
        self.o_imap_server.select('inbox')


    def send_sms(self, s_phone_number, s_message):

	    # Send message
        for s_provider, s_email_suffix in self.d_provider_sms_emails.items():
            s_phone_email = f'{s_phone_number}{s_email_suffix}'
            self.o_smtp_server.sendmail(self.s_email, s_phone_email, s_message)


    def send_mms(self, s_phone_number, s_message, s_image_path):

        # Create message with text and image attachment
        o_message = MIMEMultipart()
        o_message.attach(MIMEText(s_message))
        with open(s_image_path, 'rb') as o_img_file:
            o_message.attach(MIMEImage(o_img_file.read()))

	    # Send message
        for s_provider, s_email_suffix in self.d_provider_mms_emails.items():
            s_phone_email = f'{s_phone_number}{s_email_suffix}'
            self.o_smtp_server.sendmail(self.s_email, s_phone_email, o_message.as_string())


    def get_emails(self, b_mark_seen=True):

        # Construct query to search inbox
        ls_email_suffixes = list(self.d_provider_sms_emails.values()) + list(self.d_provider_mms_emails.values())
        s_inbox_query = ''.join(' '.join([f'OR (FROM "{s_email_suffix}")' for s_email_suffix in ls_email_suffixes]).rsplit('OR ', 1)) + ' UNSEEN'

        # Search inbox and get list of email ids
        s_status_search, ls_email_id_blocks = self.o_imap_server.search(None, s_inbox_query)
        ls_email_ids = [s_email_id for s_block in ls_email_id_blocks for s_email_id in s_block.split()]

        # Iterate over email ids
        ld_emails = []
        for s_email_id in ls_email_ids:

            # Fetch email by id
            s_status_fetch, l_email_data = self.o_imap_server.fetch(s_email_id, '(RFC822)') 
            o_message = email.message_from_bytes(l_email_data[0][1])

            # Get email metadata
            s_email_from = o_message['from']
            s_email_to = o_message['to']
            s_email_subject = o_message['subject']
            s_email_body = o_message.get_payload()

            # Add email to list
            ld_emails.append({
                's_email_id': s_email_id,
                's_email_from': s_email_from,
                's_email_to': s_email_to,
                's_email_subject': s_email_subject,
                's_email_body': s_email_body,
            })

            # Mark message as unseen
            if not b_mark_seen:
                self.o_imap_server.uid('STORE', s_email_id, '-FLAGS', '\\Seen')

        # Return list of emails
        return ld_emails

