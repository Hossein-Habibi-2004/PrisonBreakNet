
# Import Libraries

from redbox import EmailBox
from redbox.query import UNSEEN
from redmail import EmailSender

from os import remove
from re import findall
from time import sleep
from textwrap import wrap
from datetime import datetime

from telethon import TelegramClient



# Define Privates 
USERNAME = "prison.b.net@gmail.com"  # Bot email address
PASSWORD = "kannvepuazlqazba"        # Bot email password

API_ID = 1029913 # API_id
API_HASH = 'c89b062fb1b8ef18bc24a1e0c893f2ec' # API_hash
OWNER = 'mmdchenar@gmail.com' # Owner email


# Connect to Gmail
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

send = sender.send

# Connect to Telegram
bot = TelegramClient('client', API_ID, API_HASH).start()


# Define a function for read inbox and return the unread messages
def get_msgs():
    inbox = box["INBOX"] 
    msgs = []

    for msg in inbox.search(UNSEEN):
        msg.read()
        msgs.append(msg)

    return msgs


# Define the main function
def main():

    # Define a inifity loop to response email's
    while True:
        # Define a counter for use in file names
        counter = 1

        # Define a try-except option for error's
        try:
            # Get unread messages
            msgs = get_msgs()

            for msg in msgs:
                # Split subject to easy find command's
                sub = msg.subject.lower().split(' ')

                # Define the Ping-Pong option
                if sub[0] == 'ping':
                    send('Pong!', receivers=[msg.from_], text="I'm alive!")
                    print('Pong => ', msg.from_)
                
                # Define option to get messages from a Telegram channel
                elif sub[0] == 'get':
                    # Make a standard name for file by date and time of now
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    file_name = f'{sub[2]}_{now}_{counter}.txt'
                    
                    counter += 1

                    # Open the file
                    file = open(file_name, 'w')

                    # Write messages to file
                    for message in bot.iter_messages(sub[2], limit=int(sub[1])):

                        # Wraping the messages to better view
                        wrap_list = wrap(message.message, 50)
                        wrap_text = '\n'.join(wrap_list)

                        file.write(wrap_text)

                        # Write a line between messages
                        file.write('\n\n' + '-'*60 + '\n\n')

                    # Close the file
                    file.close()

                    # Send the file of messages
                    send(f'{sub[1]} messages from @{sub[2]}',
                        receivers=[msg.from_],
                        text = 'Here is the file of messages: ',
                        attachments=[file_name])
                    
                    # Remove the file
                    remove(file_name)
                    
                    print(f'{sub[1]} messages from @{sub[2]}', 'to', msg.from_)
                

                elif sub[0] in ['mtproto', 'mtproxy']:

                    channels = ['hack_proxy', 'NetAccount']

                    # Make a standard name for file by date and time of now
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    file_name = f'mtproxy_{now}_{counter}.txt'
                    
                    counter += 1

                    # Open the file
                    file = open(file_name, 'w')

                    # Write proxies to file
                    for channel in channels:
                        for message in bot.iter_messages(channel, limit=30):
                            proxies = findall(
                                r'((https://t\.me/|tg://)proxy\?server=.+&port=[0-9]{0,5}&secret=[a-z0-9A-Z_]+)(\s|\n)?',
                                message.message)

                            for proxy in proxies:
                                file.write(proxy[0])

                                # Write a line between messages
                                file.write('\n\n' + '-'*60 + '\n\n')

                    # Close the file
                    file.close()

                    # Send the file of messages
                    send('Mtproto porxies',
                        receivers=[msg.from_],
                        text = 'Here is the proxies: ',
                        attachments=[file_name])
                    
                    # Remove the file
                    remove(file_name)
                    
                    print('sent mtproto to', msg.from_)



        # Define the Keyboard Interrupt detector to stop the bot
        except KeyboardInterrupt:
            print('Bot stoped!')
            break
        

        # Define an except to pass other error's to continue bot if get an error 
        # except Exception as error:
        #     print(error)
        # except:
        #     pass
        
        sleep(10)


# Start the bot

if __name__ == '__main__':
    main()
