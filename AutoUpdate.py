from telethon import TelegramClient, events
import requests,json
from datetime import datetime
from time import sleep
from asyncio import sleep
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import GetFullChannelRequest

## DO NOT CHANGE THIS DATA IT's retived from my.telegram.org
api_id = 925503
api_hash = 'b47d1ad4b832b79123af664781df4755'
##
client = TelegramClient('UserData', api_id, api_hash)


bot_id= "@SponserHelperBot"


client.start()


async def main():
    while True:
        try:
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

                        await client(GetBotCallbackAnswerRequest(
                            '@MTProxybot',
                            (MTProxybot_last_msg[0].id),
                            data=MTProxybot_last_msg[0].reply_markup.rows[0].buttons[1].data
                        ))

            print("================================")
            print("waiting two hour... ")
            await sleep(60*60*2)
            print("loop started after two hour... ")
            print("================================")
        except:
            print("ERROR HAPPEND")

with client:
    client.loop.run_until_complete(main())


