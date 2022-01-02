import json
import os
import discord


def evaluate(exp, curr_count):
    """
    Safely evaluates the mathematical expression in the message.

    Parameters
    ==========
    - exp

        Expression to be verified

    - curr_count

        The current count

    Returns
    =======
    [

        - number: Evaluation result of expression (if valid), -infinity otherwise,
        - boolean value: whether the expression evaluates to current_count + 1

    ]
    """

    # Disregard expressions with letters
    if any(char.isalpha() for char in exp):
        return [float("-inf"), False]

    # Replace exponentiation, multiplication and division signs with Pythonic equivalents
    temp = exp.replace("^", "**").replace("×", "*").replace("÷", "/")

    # Perform the calculation
    try:
        result = eval(temp)
    except:
        return [float("-inf"), False]

    # Check if current expression evaluates to 1 more than curr_count
    return [result, result == curr_count + 1]


client = discord.Client()


@client.event
async def on_ready():
    """
    Confirms that the bot is ready to use.
    """

    print('Logged in')
    return


@client.event
async def on_message(message):
    """
    Handles stuff upon the arrival of a message

    Parameters
    ==========
    - message

        Newest message
    """

    # Don't check message if written by self
    if message.author == client.user:
        return

    # Access JSON file for counting sentences checked and verified
    filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
    with open(filename, "r") as file1:
        data = json.load(file1)
        file1.close()

    # Set counting channel using tailwhip!set
    if message.content.startswith('tailwhip!set'):
        # This is the setting part
        data["channel"] = message.channel.id

        # Confirmation message
        embed_m = discord.Embed()
        embed_m.add_field(
            name="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘀𝗲𝘁 <:mitlogo:923878289427279892>",
            value=f"𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝘁 𝘁𝗼 <#{message.channel.id}>. 𝗚𝗲𝘁 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗻𝗱 𝗵𝗮𝘃𝗲 𝗳𝘂𝗻! <:mituwu:924101386071851008>")
        await message.channel.send(embed=embed_m)

    # Only react to other messages if they are sent in counting channel
    if message.channel.id == data["channel"]:
        # Unset counting channel using tailwhip!unset
        if message.content.startswith('tailwhip!unset'):
            # This is the unsetting part
            data["channel"] = 0

            # Confirmation message
            embed_m = discord.Embed()
            embed_m.add_field(
                name="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘂𝗻𝘀𝗲𝘁 <a:mitfrogskip:924101595791233075>",
                value=f"𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗶𝘀 𝗻𝗼 𝗹𝗼𝗻𝗴𝗲𝗿 <#{message.channel.id}>. 𝗨𝘀𝗲 `tailwhip!set` 𝗶𝗻 𝗮 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝗼 𝘀𝗲𝘁 𝗶𝘁 𝗳𝗼𝗿 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴. <:mitfrog:923878290689753148>")
            await message.channel.send(embed=embed_m)

        # List of possible reactions
        emoji_list = ["<a:tidesheart:923876187338592306>",              # 0, incorrect
                      "<a:untourablealbumheart:923876065670234164>",    # 1, correct
                      "<a:mitsparkles:924101093980528650>",             # 2, 69
                      "<a:onclejazzheart:923876017251160094>"           # 3, 10
                      "<a:youdeservethisheart:923876695516282931>",     # 4, 20
                      "<a:daysgobyheart:923876397464829992>",           # 5, 420
                      "<a:mitfrog:924101595329888287>",                 # 6, 30
                      "<:mituwu:924101386071851008>",                   # 7, 40
                      "<:mitlogo:923878289427279892>",                  # 8, 50
                      "<:mitdaisy:923878289410506802>",                 # 9, 60
                      "<:emmawaiting:924511130838245446>",              # 10, 70
                      "<:blushyhearts:923878290387771402>",             # 11, 80
                      "<a:ashestoashes:925332671461228624>",            # 12, 90
                      "<a:Ausar:925986282830725170>",                   # 13, 100
                      "<:onclejazz:923877566819991563>",                # 14, 200
                      "<:mitnumb:923877630506328085>",                  # 15, 300
                      "<:mitsunglasses:923877630846066708>",            # 16, 400
                      "<:mitqt:923878289033019392>",                    # 17, 500
                      "<a:pulsingheart:923890933391564810>",            # 18, 600
                      "<a:mithug:923878945651298304>",                  # 19, 700
                      "<:mitwhistle:923878289083359264>",               # 20, 800
                      "<:mitsmile:923878289423102002>",                 # 21, 900
                      "<a:prideheart:923877371231207484>"               # 22, 1000
                      ]
        
        # List of forbidden starting characters
        char_arr = [".", ",", "!", "@", "#", "$", "%", "^", "&", "*", ":", ";", "<", ">", "/", "?", "{", "}", "[", "]", "\"", "'", "|", "/"]

        # See stats using tailwhip!user <@user>; user parameter is optional
        if message.content.startswith('tailwhip!user'):
            # Determine whose stats to analyse
            u_id = ""
            msg_arr = message.content.split()
            if len(msg_arr) == 1:
                u_id = str(message.author.id)
            elif msg_arr[1][:2] == "<@":
                u_id = msg_arr[1][3:21]
            else:
                return

            # Initialise counting stats
            count_total = 0
            count_correct = 0

            # Read entire channel history
            channel_hist = await message.channel.history(limit=float("inf")).flatten()
            for msg in channel_hist:
                split_arr = msg.content.split()
                if len(split_arr) != 0:
                    expression = split_arr[0]
                    
                    # If expression can be evaluated
                    # If expression starts with forbidden character
                    # If message is written by user in question
                    evaluateable = evaluate(expression, data["curr_count"])[0] != float("-inf")
                    starts_with_fb = any(msg.content.startswith(fb_char) for fb_char in char_arr)
                    author_verif = str(msg.author.id) == u_id

                    # Message does not start with forbidden character
                    # If expression can be evaluated and written by user in question
                    if evaluateable and (not starts_with_fb) and author_verif:
                        react_arr = msg.reactions
                        for emo1 in react_arr:
                            # Only care about emoji sent by bot for total count
                            if emo1.me:
                                count_total += 1
                                for emo2 in emoji_list[1:]:
                                    # Only care about "correct" emoji sent by bot for correct count
                                    if emo2[-19:-1] == str(emo1.emoji.id):
                                        count_correct += 1
                                        break
                                break

            ct_str = f"• 𝗧𝗼𝘁𝗮𝗹 𝗰𝗼𝘂𝗻𝘁𝘀 𝗳𝗿𝗼𝗺 <@{u_id}>: {count_total}"
            cc_str = f"• 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗰𝗼𝘂𝗻𝘁𝘀 𝗳𝗿𝗼𝗺 <@{u_id}>: {count_correct}"
            sc_str = "𝗦𝘁𝗮𝗿𝘁 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗻𝗱 𝗵𝗮𝘃𝗲 𝗳𝘂𝗻! <:mitkiss:923877937923637269>"
            embed_m = discord.Embed()

            # Special case: user has never counted (avoiding ZeroDivisionError)
            if count_total == 0:
                ca_str_0 = f"• 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝘂𝗿𝗮𝗰𝘆 𝗼𝗳 <@{u_id}>: 𝗡/𝗔"
                stats_arr = [ct_str, cc_str, ca_str_0, sc_str]
                
            else:
                ca_str = f"• 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝘂𝗿𝗮𝗰𝘆 𝗼𝗳 <@{u_id}>: {round(count_correct / count_total * 100, 5)}%"
                stats_arr = [ct_str, cc_str, ca_str]
                
            embed_m.add_field(
                    name="<:lilemma:926078630386364436> 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝘀𝘁𝗮𝘁𝘀",
                    value="\n".join(stats_arr))

            await message.channel.send(embed=embed_m)

        else:
            # Evaluate first string before whitespace
            expression = message.content.split()[0]
            
            # If expression starts with forbidden character
            starts_with_fb = any(message.content.startswith(fb_char) for fb_char in char_arr)

            # Disregard if there are letters
            if (not any(char.isalpha() for char in expression)) and (not starts_with_fb) and ("@" not in expression) and ("?" not in expression):
                # Check using evaluate and check for user repeat counting
                result = evaluate(expression, data["curr_count"])

                if result[1] and data["last_user"] != message.author.id:
                    data["last_user"] = message.author.id
                    emoji = emoji_list[1]
                    data["curr_count"] = result[0]
                    if data["curr_count"] == 69:
                        emoji = emoji_list[2]
                    if data["curr_count"] == 10:
                        emoji = emoji_list[3]
                    elif data["curr_count"] == 20:
                        emoji = emoji_list[4]
                    elif data["curr_count"] == 30:
                        emoji = emoji_list[6]
                    elif data["curr_count"] == 40:
                        emoji = emoji_list[7]
                    elif data["curr_count"] == 420:
                        emoji = emoji_list[5]
                    elif data["curr_count"] == 50:
                        emoji = emoji_list[8]
                    elif data["curr_count"] == 60:
                        emoji = emoji_list[9]
                    elif data["curr_count"] == 70:
                        emoji = emoji_list[10]
                    elif data["curr_count"] == 80:
                        emoji = emoji_list[11]
                    elif data["curr_count"] == 90:
                        emoji = emoji_list[12]
                    elif data["curr_count"] == 100:
                        emoji = emoji_list[13]
                    elif data["curr_count"] == 200:
                        emoji = emoji_list[14]
                    elif data["curr_count"] == 300:
                        emoji = emoji_list[15]
                    elif data["curr_count"] == 400:
                        emoji = emoji_list[16]
                    elif data["curr_count"] == 500:
                        emoji = emoji_list[17]
                    elif data["curr_count"] == 600:
                        emoji = emoji_list[18]
                    elif data["curr_count"] == 700:
                        emoji = emoji_list[19]
                    elif data["curr_count"] == 800:
                        emoji = emoji_list[20]
                    elif data["curr_count"] == 900:
                        emoji = emoji_list[21]
                    elif data["curr_count"] == 1000:
                        emoji = emoji_list[22]
                        
                    await message.add_reaction(emoji)

                else:
                    # Send "incorrect" emoji
                    await message.add_reaction(emoji_list[0])

                    # Reset all data except for counting channel
                    data["curr_count"] = 0
                    data["last_user"] = 0

                    embed_m = discord.Embed()
                    embed_m.add_field(
                        name="<a:mitexclaimed:924105720293646367> 𝗪𝗿𝗼𝗻𝗴 𝗰𝗼𝘂𝗻𝘁",
                        value=f"𝗢𝗵 𝗻𝗼! 𝗟𝗼𝗼𝗸𝘀 𝗹𝗶𝗸𝗲 <@{message.author.id}> 𝗺𝗲𝘀𝘀𝗲𝗱 𝘂𝗽 𝘁𝗵𝗲 𝘀𝗲𝗾𝘂𝗲𝗻𝗰𝗲.\n𝗧𝗵𝗲 𝗻𝗲𝘅𝘁 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝘀 𝟭𝟢! <:pinkyheart:924100914695000104>")
                    await message.channel.send(embed=embed_m)

    # Update JSON file
    with open(filename, "w") as file2:
        json.dump(data, file2, indent=4)
        file2.close()

    return


# Read secret token
client.run(os.getenv('DISCORD_TOKEN'))
