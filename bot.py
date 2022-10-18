from redbox import EmailBox
from redbox.query import UNSEEN
from redmail import EmailSender
from time import sleep

USERNAME = "prison.b.net@gmail.com"
PASSWORD = "kannvepuazlqazba"


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

                if msg.subject.lower() == 'ping':
                    send(msg.from_, 'Pong!','I\'m alive!')
                    print('Pong => ', msg.from_)

        sleep(10)

    except KeyboardInterrupt:
        print('Working ended!')


if __name__ == '__main__':
    main()
