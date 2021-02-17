        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await eor(usr, "`Couldn't fetch user.`")
        return

    await eor(usr, "`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await eor(usr, NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await eor(
            usr,
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}",
        )
    else:
        await eor(usr, f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@telebot.on(admin_cmd(outgoing=True, pattern="users ?(.*)"))
@errors_handler
async def get_users(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await eor(show, mentions)
    except MessageTooLongError:
        await eor(show, "Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="Users in {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await eor(event, "`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await eor(event, str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await eor(event, str(err))
        return None

    return user_obj


CMD_HELP.update(
    {
        "admin": ".promote <username/reply> <custom rank (optional)>\
\nUse - : Provides admin rights to the person in the chat.\
\n\n.demote <username/reply>\
\nUse - : Revokes the person's admin permissions in the chat.\
\n\n.ban <username/reply> <reason (optional)>\
\nUse - : Bans the person off your chat.\
\n\n.unban <username/reply>\
\nUse - : Removes the ban from the person in the chat.\
\n\n.mute <username/reply> <reason (optional)>\
\nUse - : Mutes the person in the chat, works on admins too.\
\n\n.unmute <username/reply>\
\nUse - : Removes the person from the muted list.\
\n\n.admins\
\nUse - : Retrieves a list of admins in the chat.\
\n\n.users or .users <name of member>\
\nUse - : Retrieves all (or queried) users in the chat.\
\n\n.setgppic <reply to image>\
\nUse - : Changes the group's display picture."
    }
)
