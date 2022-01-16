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
    Checks last valid count (due to bot cycling). Confirms that the bot is ready to use.
    """

    incorrect_emoji = "<a:heartlilac:931088577075482655>"

    # List of forbidden start/end characters
    char_arr = [".", ",", "!", "@", "#", "$", "%", "^", "&", ":", ";", "/", "*",
                "(", ")", "<", ">", "?", "{", "}", "[", "]", "\"", "'", "|", "_"]

    # Access JSON file for updating last count
    filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
    with open(filename, "r") as file1:
        data = json.load(file1)

    # Get counting channel history
    channel_hist = await client.get_channel(int(os.getenv("CHANNEL_ID"))).history(limit=float("inf")).flatten()

    # Create flag to avoid checking every message in the channel, only the last valid one
    checked_flag = False

    for msg in channel_hist:
        # Stop checking if last valid message has been checked
        if checked_flag:
            break

        split_arr = msg.content.split()
        if len(split_arr) != 0:
            expression = split_arr[0]

            result = evaluate(expression, data["curr_count"])[0]

            # If expression can be evaluated
            # If expression starts or ends with forbidden character
            evaluateable = result != float("-inf")
            with_fb = any(expression.startswith(fb_char) for fb_char in char_arr) or any(
                expression.endswith(fb_char) for fb_char in char_arr)

            # Message neither starts nor ends with forbidden character
            # If expression can be evaluated
            if evaluateable and (not with_fb):
                react_arr = msg.reactions

                for emo1 in react_arr:
                    # Only care about emoji sent by bot for checked flag
                    if emo1.me:
                        checked_flag = True

                        # Store 0 as last count if "incorrect" emoji is used, store result otherwise
                        if incorrect_emoji[-19:-1] == str(emo1.emoji.id):
                            data["curr_count"] = 0
                        else:
                            data["curr_count"] = result

    print(data["curr_count"])

    # Update JSON file
    with open(filename, "w") as file2:
        json.dump(data, file2, indent=4)

    # Confirmation message
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

    # Access JSON file for counting checked and verified sentences
    filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
    with open(filename, "r") as file1:
        data = json.load(file1)

    # Only react to other messages if they are sent in counting channel
    if message.channel.id == int(os.getenv("CHANNEL_ID")):
        # List of possible reactions
        emoji_list = ["<a:heartlilac:931088577075482655>",              # 0, incorrect
                      "<a:heartuntourablealbum:931059638223388702>",    # 1, correct
                      "<a:mitsparkles:931075919014141952>",             # 2, 69
                      "<a:heartonclejazz:931061570920931368>"           # 3, 10
                      "<a:heartyoudeservethis:931070978472153088>",     # 4, 20
                      "<a:heartdaysgoby:931059068662079488>",           # 5, 420
                      "<a:froggymit:931065352803209288>",               # 6, 30
                      "<:mituwu:931097521554604082>",                   # 7, 40
                      "<:mitlogo:931079481345601617>",                  # 8, 50
                      "<:mitdaisy:931252817417605190>",                 # 9, 60
                      "<:emmawaiting:931065882527027250>",              # 10, 70
                      "<:blushyhearts:931093478920814612>",             # 11, 80
                      "<:ahhh:931097728304443453>",                     # 12, 90
                      "<a:Ausar:931091601441308703>",                   # 13, 100
                      "<:onclejazz:931253711240564747>",                # 14, 200
                      "<:mitnumb:931254266243481660>",                  # 15, 300
                      "<:nortoncommander:931089415835619378>",          # 16, 400
                      "<:mitqt:931254665167908905>",                    # 17, 500
                      "<a:heartpulsing:931066370509119529>",            # 18, 600
                      "<a:mithug:931091404401279056>",                  # 19, 700
                      "<:heartato:931100200695660554>",                 # 20, 800
                      "<:mitsmile:931104285083725935>",                 # 21, 900
                      "<a:heartpride:931257165287673876>"               # 22, 1000
                      ]

        # List of forbidden start/end characters
        char_arr = [".", ",", "!", "@", "#", "$", "%", "^", "&", ":", ";", "/", "*",
                    "(", ")", "<", ">", "?", "{", "}", "[", "]", "\"", "'", "|", "_"]

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
                    evaluateable = evaluate(expression, data["curr_count"])[
                        0] != float("-inf")
                    with_fb = any(msg.content.startswith(fb_char) for fb_char in char_arr) or any(
                        msg.content.endswith(fb_char) for fb_char in char_arr)
                    author_verif = str(msg.author.id) == u_id

                    # Message does not start with forbidden character
                    # If expression can be evaluated and written by user in question
                    if evaluateable and (not with_fb) and author_verif:
                        react_arr = msg.reactions
                        for emo1 in react_arr:
                            # Only care about emoji sent by bot for total count
                            if emo1.me:
                                count_total += 1

                                # Increment correct count if "incorrect" emoji NOT used
                                if emoji_list[0][-19:-1] != str(emo1.emoji.id):
                                    count_correct += 1

            ct_str = f"• 𝗧𝗼𝘁𝗮𝗹 𝗰𝗼𝘂𝗻𝘁𝘀 𝗳𝗿𝗼𝗺 <@{u_id}>: {count_total}"
            cc_str = f"• 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗰𝗼𝘂𝗻𝘁𝘀 𝗳𝗿𝗼𝗺 <@{u_id}>: {count_correct}"
            sc_str = "𝗦𝘁𝗮𝗿𝘁 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗻𝗱 𝗵𝗮𝘃𝗲 𝗳𝘂𝗻! <:mitblowkiss:931219843963838565>"
            embed_m = discord.Embed()

            # Special case: user has never counted (avoiding ZeroDivisionError)
            if count_total == 0:
                ca_str_0 = f"• 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝘂𝗿𝗮𝗰𝘆 𝗼𝗳 <@{u_id}>: 𝗡/𝗔"
                stats_arr = [ct_str, cc_str, ca_str_0, sc_str]

            else:
                ca_str = f"• 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝘂𝗿𝗮𝗰𝘆 𝗼𝗳 <@{u_id}>: {round(count_correct / count_total * 100, 5)}%"
                stats_arr = [ct_str, cc_str, ca_str]

            embed_m.add_field(
                name="<:lilemma:931223678811770950> 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝘀𝘁𝗮𝘁𝘀",
                value="\n".join(stats_arr))

            await message.channel.send(embed=embed_m)

        else:
            msg_arr = message.content.split()
            if len(msg_arr) == 0:
                return

            # Evaluate first string before whitespace
            expression = message.content.split()[0]

            # If expression starts with forbidden character
            with_fb = any(expression.startswith(fb_char) for fb_char in char_arr) or any(
                expression.endswith(fb_char) for fb_char in char_arr)

            # Disregard if there are letters
            if (not any(char.isalpha() for char in expression)) and (not with_fb) and ("@" not in expression):
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
                        name="<a:heartbreakmit:931240957066764318> 𝗪𝗿𝗼𝗻𝗴 𝗰𝗼𝘂𝗻𝘁",
                        value=f"𝗢𝗵 𝗻𝗼! 𝗟𝗼𝗼𝗸𝘀 𝗹𝗶𝗸𝗲 <@{message.author.id}> 𝗺𝗲𝘀𝘀𝗲𝗱 𝘂𝗽 𝘁𝗵𝗲 𝘀𝗲𝗾𝘂𝗲𝗻𝗰𝗲.\n𝗧𝗵𝗲 𝗻𝗲𝘅𝘁 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝘀 𝟭! <:heartpinky:931246593527644190>")
                    await message.channel.send(embed=embed_m)

    # Update JSON file
    with open(filename, "w") as file2:
        json.dump(data, file2, indent=4)

    return


# Read secret token
client.run(os.getenv('DISCORD_TOKEN'))
