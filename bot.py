from redbox import EmailBox
from redbox.query import UNSEEN
from redmail import EmailSender
from telethon import TelegramClient
from time import sleep
from datetime import datetime

USERNAME = "prison.b.net@gmail.com"
PASSWORD = "kannvepuazlqazba"

API_ID = 1029913
API_HASH = 'c89b062fb1b8ef18bc24a1e0c893f2ec'
OWNER = 181781214


box = EmailBox(
    host="imap.gmail.com", 
    port=993,
    username=USERNAME,
    password=PASSWORD)

sender = EmailSender(
    host="smtp.gmail.com", 
    port=587,
    username=USERNAME,
    password=PASSWORD)


bot = TelegramClient('client', API_ID, API_HASH).start()


def send(email:str, sub:str, text:str, attach:list=[]):
    sender.send(
    subject=sub,
    receivers=[email],
    text=text,
    attachments=attach)


def get_msgs():
    inbox = box["INBOX"]
    msgs = []
    for msg in inbox.search(UNSEEN):
        msg.read()
        msgs.append(msg)
    return msgs


def main():

    try:
        while True:

            msgs = get_msgs()

            for msg in msgs:
                sub = msg.subject.lower().split(' ')

                if sub[0] == 'ping':
                    send(msg.from_, 'Pong!','I\'m alive!')
                    print('Pong => ', msg.from_)
                
                elif sub[0] == 'get':
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    file_name = f'{sub[2]}_{now}.txt'
                    file = open(file_name, 'a')
                    for message in bot.iter_messages(sub[2], limit=int(sub[1])):
                        print(message.message)
                        file.write(message.message)
                        file.write('\n---------------------------------\n')
                    file.close()
                    send(msg.from_,
                        f'{sub[2]} messages from @{sub[2]}',
                        'Here is the file of messages: ',
                        [file_name])


        sleep(10)

    except KeyboardInterrupt:
        print('Working ended!')


if __name__ == '__main__':
    main()
