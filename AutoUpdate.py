from telethon import TelegramClient, events
import requests,json
from datetime import datetime
from time import sleep
from asyncio import sleep
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from datetime import datetime, timedelta

TimeTable = [ #enter your timetable below first number is hour and second is minute
    [9,32],
    [10,32],
    [11,32],
    [12,32],
    [13,20],
    [14,32],
    [15,32],
    [16,32],
    [17,32],
    [18,32],
    [19,32],
    [20,32],
    [21,32],
    [22,32],
    [23,32],
    [0,32],
]
bot_id= "@SponserHelperBot"






## DO NOT CHANGE THIS DATA IT's retived from my.telegram.org
api_id = 925503
api_hash = 'b47d1ad4b832b79123af664781df4755'
##
client = TelegramClient('UserData', api_id, api_hash)

client.start()

current_day = -1 # flag to build time table daily
Current_Time_Table = []
async def main():
    global  current_day
    global  Current_Time_Table
    while True:
        # try:
            current_time_in_utc = datetime.utcnow()
            iran_time = current_time_in_utc + timedelta(hours=3,minutes=30)

            if(iran_time.strftime("%d") != current_day):
                print("RE PRODUCE TIME TABLE")
                current_day = iran_time.strftime("%d")
                for time in TimeTable:
                    Current_Time_Table.append([time[0],time[1],1]) #hour , minute , flagCHecked
            current_hour = int(iran_time.strftime("%H"))
            current_minute = int(iran_time.strftime("%M"))
            Flag_LET_GET_STATS = 0
            for index,time in enumerate(Current_Time_Table, start=0):
                if(current_hour == time[0]):
                    if(time[2]): #flag is true it's mean must check
                        if(current_minute >= time[1]):
                            Flag_LET_GET_STATS =1
                            break
            if(not(Flag_LET_GET_STATS)):
                print("WE ARE NOT IN TIME TABLE, iran time:",iran_time.strftime("%H:%M")," we wait 3minute and then try again")
                await sleep(60 * 3)
                continue

            print("================================")
            print("try to get proxies tag...")
            await client.send_message('@MTProxybot', '/myproxies')
            await sleep(3)
            MTProxybot_last_msg = await client.get_messages('@MTProxybot', limit=1,
                        offset_date=None,
                        offset_id=0,
                        max_id=0,
                        min_id=0,
                        add_offset=0)
            print("all tags recived...")
            if("You didn't create any proxy yet." in MTProxybot_last_msg[0].message):
                print("you must create a tag from : @MTProxybot \n we kill our self ... :)")
                exit(200)
            if(not('Here is the list of all proxies you created:' in MTProxybot_last_msg[0].message)):
                print("we think another robot in process... we wait 10 second...")
                await sleep(10)
                continue
            if('Here is the list of all proxies you created:' in MTProxybot_last_msg[0].message):
                MTProxybot_last_msg_temp = MTProxybot_last_msg[0]
                print("recivieng stats...")
                for row in MTProxybot_last_msg_temp.reply_markup.rows:
                    for button in row.buttons:
                        print("===================")
                        print("recivieng stats of ",button.text)
                        message_response_click = await client(GetBotCallbackAnswerRequest(
                            '@MTProxybot',
                            (MTProxybot_last_msg[0].id),
                            data=button.data
                        ))
                        # MTProxybot_last_msg = await client.get_messages('@MTProxybot', limit=1,
                        #                                                 offset_date=None,
                        #                                                 offset_id=0,
                        #                                                 max_id=0,
                        #                                                 min_id=0,
                        #                                                 add_offset=0)
                        MTProxybot_last_msg = await client.get_messages('@MTProxybot', ids=MTProxybot_last_msg[0].id)
                        MTProxybot_last_msg = [MTProxybot_last_msg]
                        if(len(MTProxybot_last_msg[0].reply_markup.rows) == 3):
                            message_response_click = await client(GetBotCallbackAnswerRequest(
                                '@MTProxybot',
                                (MTProxybot_last_msg[0].id),
                                data=MTProxybot_last_msg[0].reply_markup.rows[1].buttons[0].data
                            ))
                        if(len(MTProxybot_last_msg[0].reply_markup.rows) == 2):
                            message_response_click = await client(GetBotCallbackAnswerRequest(
                                '@MTProxybot',
                                (MTProxybot_last_msg[0].id),
                                data=MTProxybot_last_msg[0].reply_markup.rows[0].buttons[1].data
                            ))
                        await sleep(2)
                        MTProxybot_last_msg = await client.get_messages('@MTProxybot', ids=MTProxybot_last_msg[0].id)
                        MTProxybot_last_msg = [MTProxybot_last_msg]
                        if('Stats for proxy with tag'in MTProxybot_last_msg[0].message):
                            print("stats forwarding started... ",button.text)
                            await client.forward_messages(bot_id, MTProxybot_last_msg[0].id, MTProxybot_last_msg[0].peer_id.user_id)
                            print("stats forwarding end... ",button.text)
                            print("stats recived... ",button.text)
                        else:
                            print("-no stats exist",button.text)

                        # set flagChecked to zero and it's mean we do not try anymore on this time
                        Current_Time_Table[index][2] = 0
                        await client(GetBotCallbackAnswerRequest(
                            '@MTProxybot',
                            (MTProxybot_last_msg[0].id),
                            data=MTProxybot_last_msg[0].reply_markup.rows[0].buttons[1].data
                        ))
        # except:
        #     print("ERROR HAPPEND")

with client:
    client.loop.run_until_complete(main())


