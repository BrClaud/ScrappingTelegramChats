from telethon import TelegramClient, events
from telethon import functions, types
from datetime import datetime
import csv, json
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import logging
from settings import API_ID,API_HASH,PHONE

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient(PHONE, API_ID, API_HASH)


async def scrap():
    dialogs = await client.get_dialogs() # получение диалогов
    groups = []
    i = 0
    for dialog in dialogs:
        if dialog.is_group == True:
            groups.append(dialog)
            print(i, ' - ', dialog.title)
            i += 1

    target_group = groups[int(input("введите номер группы:\n"))]
    print(target_group.name)
    all_participants = await client.get_participants(target_group)
    with open(f"members_'{target_group.title}'.csv", 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(['ID', 'Name', "Username"])
        for member in all_participants:
            if member.first_name:
                first_name = member.first_name
            else:
                first_name = ''
            if member.last_name:
                last_name = member.last_name
            else:
                last_name = ''
            if member.username:
                username = member.username
            else:
                username = ''
            name = (first_name+' '+last_name).strip()
            writer.writerow([member.id,name,username])
    print("тотальный успеx, парсинг удался")

def check():
    all_participants = []
    print("введите id пользователя и почту, каждый раз с новой строки")
    t = input() # убираем первую строчку
    while True:
        data = input().split()
        email = data[0]
        status = data[-1]
        un=''
        for i in range(1,len(data)-1):
            un+=data[i]
            if i-(len(data) - 2)!=0:
                un+=' '

        if status !='/':
            if un != "" and status == '+':
                all_participants.append([un,email,False])
        else:
            break

    # n = int(input("введите количество пользователей"))
    # print("введите id пользователя и почту, каждый раз с новой строки")
    # for i in range(n):
    #     un, email = input().split(maxsplit=1)
    #     if not (un == ""):
    #         all_participants.append([un,email,False])
    print(all_participants)
    members = []
    with open("members_'Community Digital Nova'23'.csv",'r',encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=',', lineterminator='\n')
        for row in reader:
            members.append(row[2])

    for i in range(len(all_participants)):
        for j in range(len(members)):
            if members[j] in all_participants[i][0]:
                all_participants[i][2] = True
    cnt = 0
    with open(f"data_members.csv",'w',encoding='utf-8') as file:
        writer = csv.writer(file,delimiter=',', lineterminator='\n')
        writer.writerow(['status','username','email'])

        # print("перешли в чат:\n")
        for i in range(len(all_participants)):
            if(all_participants[i][2]):
                writer.writerow(['+',all_participants[i][0], all_participants[i][1]])
        cnt = 0
        # print("не перешли в чат:\n")
        for i in range(len(all_participants)):
            if not (all_participants[i][2]):
                writer.writerow(['-', all_participants[i][0], all_participants[i][1]])




if __name__=="__main__":

    with client:
        client.loop.run_until_complete(scrap())
    check()
