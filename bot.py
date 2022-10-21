# Import Libraries
from cgitb import html
from re import findall
from time import sleep
from textwrap import wrap
from os import remove, mkdir
from datetime import datetime
from shutil import make_archive, rmtree

from redbox import EmailBox
from redmail import EmailSender
from redbox.query import UNSEEN

from telethon import TelegramClient
from telethon.sessions import StringSession



# Define Privates 
USERNAME = "prison.b.net@gmail.com"  # Bot email address
PASSWORD = "kannvepuazlqazba"        # Bot email password

API_ID = 1029913 # API_id
API_HASH = 'c89b062fb1b8ef18bc24a1e0c893f2ec' # API_hash
SESSION = '1BJWap1wBu0jAJFZnR_C-HSf2H_yXf-PzpEE48Hf3JLpq0X_E2EkSnb5GuqXQdTRASjGIy0QULhUaYi37_hXgG2vr2Fs9cVzhVsdlQyuWSvT3mxEP5D7Og5xA49xAeuND0QsTVHiQAMzYjlDp8wpy5a6USCIAqV88JgeF2KJ1spz5kkPOZWwKso0L0j3mjCE3v_vmKCP0HIn9hUteMg5PvrqC3y_091bwHyPnaLK4jPZZR4zA27ko6FsxwnePqhlwEZA4dHFisewrL0v8FCQRSxHt8D8EB1RCZgPCBPn_XDI_FOKlVvsIH1-vC8vY-bbSTts4Jxb2OZcAurT4M7FlPpoWF7EXXBY='
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
bot = TelegramClient(StringSession(SESSION), API_ID, API_HASH).start()

# Bypass asynco client
bot_sync = bot.loop.run_until_complete


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
    print('Ready to response...')

    # Define a counter for use in file names
    counter = 1

    # Define a inifity loop to response email's
    while True:

        # Define a try-except option for error's
        try:
            # Get unread messages
            msgs = get_msgs()

            for msg in msgs:
                # Split subject to easy find command's
                sub = msg.subject.lower().split(' ')

                # Define the help command
                if sub[0] == 'help':
                    help = open('help.html').read()
                    send('Prison Break Tutorial', receivers=[msg.from_], html=help)
                    print('Help => ', msg.from_)


                # Define get messages command (owner only)
                elif sub[0] == 'get' and msg.from_.split('<')[1][:-1] == OWNER:
                    print('Getting messages...')

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
                        text = 'Dear ' + msg.from_.split('<')[0] + 'Here is the file of messages: ',
                        attachments=[file_name])
                    
                    # Remove the file
                    remove(file_name)
                    
                    print(f'{sub[1]} messages from @{sub[2]}', 'to', msg.from_)


                # Define Mtproto proxy command
                elif sub[0] in ['mtproto', 'mtproxy']:
                    print('Getting proxies...')

                    channels = ['hack_proxy', 'NetAccount']

                    # Make a standard name for file by date and time of now
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    file_name = f'mtproto_{now}_{counter}.txt'
                    

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

                    # Send the file of proxies
                    send('Mtproto porxies',
                        receivers=[msg.from_],
                        text = 'Dear ' + msg.from_.split('<')[0] + 'Here is the proxies: ',
                        attachments=[file_name])
                    
                    # Remove the file
                    remove(file_name)
                    
                    print('sent mtproto to', msg.from_)


                # Define HTTP config command
                elif sub[0] == 'config':
                    print('Getting configs...')

                    channels = ['mypremium98', 'NetAccount', 'injector2', 'barcode_tm', 'Free_Nettm']

                    # Make a standard name for file and folder by date and time of now
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    name = f'config_{now}_{counter}'
                    
                    counter += 1

                    # Make folder
                    mkdir(name)

                    # Write proxies to file
                    for channel in channels:

                        # Make sub-folder
                        mkdir(name+'/'+channel)

                        for message in bot.iter_messages(channel, limit=20):

                            if message.file is not None and message.file.name is not None:
                                if message.file.name[-3:] in ['.hc', 'ehi']:
                                    bot_sync(message.download_media(
                                        name+'/'+channel+'/'+message.file.name))
                            
                    make_archive(f'{name}', 'zip',name)

                    # Send the file of configs
                    send('HTTP Config',
                        receivers=[msg.from_],
                        text = 'Dear ' + msg.from_.split('<')[0] + 'Here is the configs: ',
                        attachments=[f'{name}.zip'])
                    
                    # Remove the folder
                    rmtree(f'/{name}', ignore_errors=True)
                    
                    print('sent config to', msg.from_)
                

                # Define V2ray server command
                elif sub[0] in ['v2ray', 'vmess', 'vless', 'trojan']:
                    print('Getting servers...')

                    channels = ['v2rayng_org', 'NetBox2', 'freelancer_gray']

                    # Make a standard name for file by date and time of now
                    now = str(datetime.now())[:16].replace(':','-').replace(' ','_')
                    file_name = f'v2ray_{now}_{counter}.txt'
                    

                    counter += 1

                    # Open the file
                    file = open(file_name, 'w')

                    # Write servers to file
                    for channel in channels:
                        for message in bot.iter_messages(channel, limit=30):
                            servers = findall(r'((vmess://|trojan://|vless://)[a-z0-9A-Z=%@#-&/:\.]+)(\s|\n)?',message.message)

                            for server in servers:
                                file.write(server[0])

                                # Write a line between messages
                                file.write('\n\n' + '-'*60 + '\n\n')

                    # Close the file
                    file.close()

                    # Send the file of servers
                    send('V2ray servers',
                        receivers=[msg.from_],
                        text = 'Dear ' + msg.from_.split('<')[0] + 'Here is the V2ray servers: ',
                        attachments=[file_name])
                    
                    # Remove the file
                    remove(file_name)
                    
                    print('sent v2ray to', msg.from_)


                # Define APK link command
                elif sub[0] == 'apk':
                    print(f'Sending {sub[1]}')

                    # Define APK file links
                    drive = {
                        'injector': 'https://drive.google.com/file/d/1Wc5ocL4feKtN1oIIenU6SGxlFdImDddS',
                        'plugin'  : 'https://drive.google.com/file/d/1D4aJ8xSQfl45bvXEM5S3L5LEaOfX3Hlp',
                        'custom'  : 'https://drive.google.com/file/d/1ir2qfJija1NxFBzubLikPd5BHBqg9GXS',
                        'v2ray'   : 'https://drive.google.com/file/d/1Gj_jeOaAqwLDqtoQU_9DiXLY1gvucT06'}
                    
                    bayan = {
                        'injector': 'https://bayanbox.ir/download/6811170076719809389/HTTP-Injector-5.7.1-apkcombo.com',
                        'plugin'  : 'https://bayanbox.ir/download/4310901268947379443/V2Ray-plugin-for-HTTP-Injector-v1.5.1-apkpure.com.apk',
                        'custom'  : 'https://bayanbox.ir/download/8623657524937065235/HTTP-Custom-AIO-Tunnel-VPN-v3.10.28-apkpure.com.apk',
                        'v2ray'   : 'https://bayanbox.ir/download/2407425016960915312/v2rayNG-v1.7.4-apkpure.com'}
                    
                    if sub[1] in drive and sub[1] != 'plugin':
                        html = f'<p>Dear <b>{msg.from_.split("<")[0]}</b>\nHere is the APK links:</p><p></p>\
                            <p><b><a href="{drive[sub[1]]}">Download from Google Drive</a></b></p>\
                                <p><b><a href="{bayan[sub[1]]}">Download from Bayan Box</a></b></p>'

                        if sub[1] == 'injector':
                            html = html + f'<br><p><b><a href="{drive["plugin"]}">V2ray-Plugin Download from Google Drive</a></b></p>\
                                <p><b><a href="{bayan["plugin"]}">V2ray-Plugin Download from Bayan Box</a></b></p></br>'

                        # Send the APK file
                        send(f'APK {sub[1]}',
                            receivers=[msg.from_],
                            html=html)
                        
                        print(f'sent {sub[1]} to', msg.from_)
                


        # Define the Keyboard Interrupt detector to stop the bot
        except KeyboardInterrupt:
            print('\n\n|-----Bot stoped-----|')
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
