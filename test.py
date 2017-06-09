
from __future__ import print_function
import base64
import email.mime.text
import os
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

#授權範圍
SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.send']

CLIENT_SECRET_FILE = 'test.json' #OAuth 2.0 用戶端 ID
CREDENTIAL_FILE = 'test.json' # 服務帳戶金鑰 管理服務帳戶
#https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount
APPLICATION_NAME = 'hikidiary-1496310174324'
MANUAL_AUTH = True

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    if MANUAL_AUTH:
        flags.noauth_local_webserver=True
except ImportError:
    flags = None    

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.send']

class PythonGmailAPI:
    def __init__(self):
        pass

    def gmail_send(self, sender_address, to_address, subject, body):
        print('Sending message, please wait...')
        message = self.__create_message(sender_address, to_address, subject, body)
        credentials = self.__get_credentials()
        service = self.__build_service(credentials)
        raw = message['raw']
        raw_decoded = raw.decode("utf-8")
        message = {'raw': raw_decoded}
        message_id = self.__send_message(service, 'me', message)
        print('Message sent. Message ID: ' + message_id)


    def __get_credentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
      
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)
        store = Storage(credential_path)
        credentials = store.get()
        
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)
            
        return credentials

    def __create_message(self, sender, to, subject, message_text):
      """Create a message for an email.
      Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
      Returns:
        An object containing a base64url encoded email object.
      """
      message = email.mime.text.MIMEText(message_text, 'plain', 'utf-8')
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject
      encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes())}
      return encoded_message

    def __send_message(self, service, user_id, message):
      """Send an email message.
      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.
      Returns:
        Sent Message ID.
      """
      message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
      return message['id']

    def __build_service(self, credentials):
        """Build a Gmail service object.
        Args:
            credentials: OAuth 2.0 credentials.
        Returns:
            Gmail service object.
        """
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build('gmail', 'v1', http=http)
        

def main():
    sender_address = 'hikintnucsie@gmail.com'
    to_address = 'lucylai0102@gmail.com'
    subject = 'test'
    body = 'test success'
    PythonGmailAPI().gmail_send(sender_address, to_address, subject, body)

if __name__ == '__main__':
    main()
