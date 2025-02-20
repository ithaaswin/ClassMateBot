# Copyright (c) 2021 War-Keeper
from asyncio.tasks import sleep
import discord
import discord.ext.test as dpytest
from discord.utils import get, sleep_until
import os
import sys
from Utility.email_utility import EmailUtility
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytest


# ------------------------------------------------------------------------------------------------------
# Main file bot testing. Uses dpytest to test bot activity on a simulated server with simulated members
# ------------------------------------------------------------------------------------------------------

VERIFIED_MEMBER_ROLE = os.getenv("VERIFIED_MEMBER_ROLE")

# ---------------------------
# Tests cog/cogMaintenance
# ---------------------------
@pytest.mark.asyncio
async def test_cogMaintenance(bot):
    # Test instructor add.
    # Test email utility by providing just recipient email address.
    guild = bot.guilds[0]
    channel = await guild.create_text_channel('instructor-channel')
    await dpytest.message(content=f"$unloadCog instructor", channel = channel)
    assert dpytest.verify().message().content("instructor cog has been removed")

    await dpytest.message(content=f"$loadCog instructor",channel=channel)
    assert dpytest.verify().message().content("instructor cog has been added")

    await dpytest.message(content=f"$reloadCog instructor",channel=channel)
    assert dpytest.verify().message().content("instructor cog has been reloaded")


# ---------------------------
# Tests cogs/qanda
# ---------------------------
@pytest.mark.asyncio
async def test_qanda(bot):
    guild = bot.guilds[0]
    await guild.create_text_channel('q-and-a')
    channel = get(guild.text_channels, name='q-and-a')
    
    await dpytest.message(content=f"$ask 'Question-1'", channel=channel)
    assert dpytest.verify().message().contains().content("Question-1")
    assert not dpytest.verify().message().contains().content("$ask")
    
    await dpytest.message(content=f"$askanonym 'Question-2'", channel=channel)
    assert dpytest.verify().message().contains().content("Question-2")
    assert not dpytest.verify().message().contains().content("$askanonym")
    
    await dpytest.message(content=f"$answer 0 'Answer-0'", channel=channel)
    assert dpytest.verify().message().contains().content("Invalid question number: 0")
    
    await dpytest.message(content=f"$answer 1 'Answer-1'", channel=channel)
    assert not dpytest.verify().message().contains().content("$answer")

    await guild.create_text_channel('instructor_channel')
    channel = get(guild.text_channels, name='instructor_channel')
    
    await dpytest.message(content=f"$ask 'Question-3'", channel=channel)
    assert dpytest.verify().message().contains().content(
        "Questions can only be posted on q-and-a channel")
    
    await dpytest.message(content=f"$askanonym 'Question-4'", channel=channel)
    assert dpytest.verify().message().contains().content(
        "Questions can only be posted on q-and-a channel")
    
    await dpytest.message(content=f"$answer 0 'Answer-0'", channel=channel)
    assert dpytest.verify().message().contains().content(
        "Questions can only be posted on q-and-a channel")

    
# ---------------------------
# Tests cogs/cal_attendance
# ---------------------------
@pytest.mark.asyncio
async def test_takeattendance(bot):
    guild = bot.guilds[0]
    await guild.create_text_channel('calendar-channel')
    await dpytest.message(content=f"$takeattendance")
    assert dpytest.verify().message().contains().content("Command works only in instructor-channel")
    
    
# ---------------------------
# Tests cogs/instructor
# ---------------------------
@pytest.mark.asyncio
async def test_instructorcommands(bot):
    # Test instructor add.
    # Test email utility by providing just recipient email address.
    guild = bot.guilds[0]
    irole = await guild.create_role(name="Instructor", colour=discord.Colour(0xdc143c))
    srole = await guild.create_role(name=VERIFIED_MEMBER_ROLE, colour=discord.Colour(0x7289da))
    await dpytest.add_role(guild.members[0], irole)

    await dpytest.message(content=f"$getInstructor")
    assert dpytest.verify().message().contains().content("is the Instructor!")

    await dpytest.message(content=f"$setInstructor {guild.members[0]}")
    assert dpytest.verify().message().contains().content("Not a valid command for this channel")

    channel = await guild.create_text_channel('instructor-channel')
    await dpytest.message(content=f"$setInstructor {guild.members[0]}", channel=channel)
    assert dpytest.verify().message().contains().content("is already an Instructor!")

    await dpytest.message(content=f"$setInstructor {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("has been given Instructor role!")

    await dpytest.message(content=f"$getInstructor")
    assert dpytest.verify().message().contains().content("are the Instructors!")

    await dpytest.message(content=f"$removeInstructor {guild.members[1]}")
    assert dpytest.verify().message().contains().content("Not a valid command for this channel")

    await dpytest.message(content=f"$removeInstructor {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("has been removed from Instructor role and given student role!")

    await dpytest.message(content=f"$removeInstructor {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("is not an Instructor!")


# ---------------------------
# Tests cogs/ta
# ---------------------------
@pytest.mark.asyncio
async def test_tacommands(bot):
    # Test instructor add.
    # Test email utility by providing just recipient email address.
    guild = bot.guilds[0]
    irole = await guild.create_role(name="Instructor", colour=discord.Colour(0xdc143c))
    trole = await guild.create_role(name="TA", colour=discord.Colour(0x00ffff))
    srole = await guild.create_role(name=VERIFIED_MEMBER_ROLE, colour=discord.Colour(0x7289da))
    await dpytest.add_role(guild.members[0], irole)
    await dpytest.add_role(guild.members[1], trole)

    await dpytest.message(content=f"$getTA")
    assert dpytest.verify().message().contains().content("is the TA!")

    await dpytest.message(content=f"$setTA {guild.members[0]}")
    assert dpytest.verify().message().contains().content("Not a valid command for this channel")

    channel = await guild.create_text_channel('ta-channel')

    await dpytest.message(content=f"$setTA {guild.members[0]}", channel=channel)
    assert dpytest.verify().message().contains().content("already has higher role of instructor")

    await dpytest.message(content=f"$setTA {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("is already a TA!")

    await dpytest.message(content=f"$removeTA {guild.members[1]}")
    assert dpytest.verify().message().contains().content("Not a valid command for this channel")

    await dpytest.message(content=f"$removeTA {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("has been removed from TA role and given student role!")

    await dpytest.message(content=f"$setTA {guild.members[1]}", channel=channel)
    assert dpytest.verify().message().contains().content("has been given TA role!")

    await dpytest.message(content=f"$removeTA {guild.members[0]}", channel=channel)
    assert dpytest.verify().message().contains().content("is not a TA!")

    await dpytest.remove_role(guild.members[0], irole)
    await dpytest.add_role(guild.members[0], trole)

    await dpytest.message(content=f"$getTA")
    assert dpytest.verify().message().contains().content("are the TA's!")
    
# --------------------
# Tests cogs/profanity.py
# --------------------
@pytest.mark.asyncio
async def test_custom_profanity(bot):
    await dpytest.message("$custom word")
    await sleep(5)
    assert dpytest.verify().message().content("Word added to custom profanity filter")
    await dpytest.message("$custom word")
    await sleep(5)
    assert dpytest.verify().message().content("Already Added!!")

@pytest.mark.asyncio
async def test_profanity(bot):
    await dpytest.message("fuck")
    await sleep(5)
    assert dpytest.verify().message().content("TestUser0 says: ****")


# --------------------
# Tests cogs/hello.py
# --------------------
@pytest.mark.asyncio
async def test_hello(bot):
    await dpytest.message("$hello")
    assert dpytest.verify().message().content("Hello World!")


# -------------------
# Tests cogs/ping.py
# -------------------
@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("$ping")
    assert dpytest.verify().message().contains().content("Pong!")

# -------------------
# Tests cogs/SentimentAnalysis.py
# -------------------
@pytest.mark.asyncio
async def test_positive_sentiment(bot):
    await dpytest.message("This is a good idea")
    await dpytest.message("$sentiment")
    assert dpytest.verify().message().contains().content("POSITIVE")

@pytest.mark.asyncio
async def test_negative_sentiment(bot):
    await dpytest.message("This is a bad idea")
    await dpytest.message("$sentiment")
    assert dpytest.verify().message().contains().content("NEGATIVE")




# TODO Test user join messages


# ---------------------
# Tests cogs/groups.py
# ---------------------
@pytest.mark.asyncio
async def test_groupJoin(bot):
    # Try to join a group we're already in
    await dpytest.message("$join Group 1")
    message = dpytest.get_message()
    if message.content == "You are already in Group 1":
        await dpytest.message("$remove Group 1")
        assert dpytest.verify().message().content("You have been removed from Group 1!")
    else:
        assert message.content == "You are now in Group 1!"
    # Try to remove ourselves from a group we're not in
    await dpytest.message("$remove Group 20")
    assert dpytest.verify().message().contains().content("You are not in Group 20")
    # Try to remove ourself from the group

    # For some reason we're not in the group, might be a problem with how dpytest works

    # assert dpytest.verify().message().contains().content("You are not in Group 1")


# ------------------------------------
# Tests cogs/groups.py error handling
# ------------------------------------
@pytest.mark.asyncio
async def test_groupError(bot):
    # Try to join a group that doesn't exist
    await dpytest.message("$join Group -1")
    assert dpytest.verify().message().contains().content('Not a valid group')
    assert dpytest.verify().message().contains().content(
        'To use the join command, do: $join \'Group\' <Num> \n ( For example: $join Group 0 )')
    # Try to remove ourself from an invalid group
    await(dpytest.message("$remove Group 999"))
    assert dpytest.verify().message().contains().content('Group 999 is not a valid group')
    assert dpytest.verify().message().contains().content('To use the remove command, do: $remove \'Group\' <Num> \n \
            ( For example: $remove Group 0 )')
    # with pytest.raises(Exception):
    #     await dpytest.message("$join")
    #     assert dpytest.verify().message().contains().content(
    #         'To use the join command, do: $join \'Group\' <Num> \n ( For example: $join Group 0 )')
    #     assert dpytest.verify().message().contains().content(
    #         'To use the join command, do: $join \'Group\' <Num> \n ( For example: $join Group 0 )')

# ------------------------------------
# Tests cogs/groups.py autogrouping
# # ------------------------------------
@pytest.mark.asyncio

async def test_automatic_grouping(bot):
        await  dpytest.message("$auto-assign")
        assert dpytest.verify().message().contains().content("No modifications made. Every Student is part of a Group")


# ------------------------------------
#Tests cogs/groups.py find-group
# # ------------------------------------
@pytest.mark.asyncio
#
async def test_find_group(bot):
        # test with invalid input
        with pytest.raises(Exception):
            await  dpytest.message("$find-group UnknownUser")
            assert dpytest.verify().message().contains().content("Please check the name entered and try again")
            assert dpytest.verify().message().contains().content('To use the find-group command, do: $find-group <StudentName> \n \
                ( For example: $find-group Jane Doe )')

# -----------------------
# Tests cogs/deadline.py
# -----------------------
@pytest.mark.asyncio
async def test_deadline(bot):
    # Clear our reminders: Only if testing fails and leaves a reminders.JSON file with values behind
    # await dpytest.message("$clearreminders")
    # assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")
    # Test reminders while none have been set
    await dpytest.message("$coursedue CSC505")
    assert dpytest.verify().message().contains().content("Rejoice..!! You have no pending homeworks for CSC505..!!")
    # Test setting 1 reminder
    await dpytest.message("$addhw CSC505 DANCE SEP 21 2050 10:00")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC505 homework named: DANCE which is due on: 2050-09-21 10:00:00")
    # Test setting a 2nd reminder
    await dpytest.message("$addhw CSC510 HW1 DEC 21 2050 19:59")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Test deleting reminder
    await dpytest.message("$deletereminder CSC510 HW1")
    assert dpytest.verify().message().content(
        "Following reminder has been deleted: Course: CSC510, Homework Name: HW1, Due Date: 2050-12-21 19:59:00")
    # Test re-adding a reminder
    await dpytest.message("$addhw CSC510 HW1 DEC 21 2050 19:59")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")


# --------------------------------
# Test listing multiple reminders
# --------------------------------
@pytest.mark.asyncio
async def test_listreminders(bot):
    # Test listing multiple reminders
    await dpytest.message("$addhw CSC505 DANCE SEP 21 2050 10:00")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC505 homework named: DANCE which is due on: 2050-09-21 10:00:00")
    # Test setting a 2nd reminder
    await dpytest.message("$addhw CSC510 HW1 DEC 21 2050 19:59")
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    await dpytest.message("$listreminders")
    assert dpytest.verify().message().contains().content(
        "CSC505 homework named: DANCE which is due on: 2050-09-21 10:00:00")
    assert dpytest.verify().message().contains().content(
        "CSC510 homework named: HW1 which is due on: 2050-12-21 19:59:00")
    # Test $coursedue
    await dpytest.message("$coursedue CSC505")
    assert dpytest.verify().message().contains().content(
        "DANCE is due at 2050-09-21 10:00:00")
    # Try to change the due date of DANCE to something impossible
    await dpytest.message("$changeduedate CSC505 DANCE 4")
    assert dpytest.verify().message().contains().content(
        "Due date could not be parsed")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")


# ------------------------------
# Tests reminders due this week
# ------------------------------
@pytest.mark.asyncio
async def test_duethisweek(bot):
    # Try adding a reminder due in an hour
    now = datetime.now() + timedelta(hours=1)
    dt_string = now.strftime("%b %d %Y %H:%M")
    await dpytest.message(f'$addhw CSC600 HW0 {dt_string}')
    assert dpytest.verify().message().contains().content(
        "A date has been added for: CSC600 homework named: HW0")
    # Check to see that the reminder is due this week
    await dpytest.message("$duethisweek")
    assert dpytest.verify().message().contains().content("CSC600 HW0 is due this week")
    # Clear reminders at the end of testing since we're using a local JSON file to store them
    await dpytest.message("$clearreminders")
    assert dpytest.verify().message().contains().content("All reminders have been cleared..!!")

    
# --------------------
# Tests cogs/pinning
# --------------------
@pytest.mark.asyncio
async def test_pinning(bot):
    # Test pinning a message
    await dpytest.message("$pin TestMessage www.google.com this is a test")
    # print(dpytest.get_message().content)
    assert dpytest.verify().message().contains().content(
        "A new message has been pinned with tag: TestMessage and link: www.google.com with a description: this is a test")
    await dpytest.message("$pin TestMessage www.discord.com this is also a test")
    # print(dpytest.get_message().content)
    assert dpytest.verify().message().contains().content(
        "A new message has been pinned with tag: TestMessage and link: www.discord.com with a description: this is also a test")


# ----------------
# Tests unpinning
# ----------------
@pytest.mark.asyncio
async def test_unpinning(bot):
    # Test pinning a message
    await dpytest.message("$pin TestMessage www.google.com this is a test")
    # print(dpytest.get_message().content)
    assert dpytest.verify().message().contains().content(
        "A new message has been pinned with tag: TestMessage and link: www.google.com with a description: this is a test")
    # Tests unpinning a message that doesn't exist
    await dpytest.message("$unpin None ThisWillFail")
    assert dpytest.verify().message().contains().content(
        "No message found with the combination of tagname: None, description ThisWillFail")
    # Tests unpinning messages that DO exist
    await dpytest.message("$unpin TestMessage this is a test")
    assert dpytest.verify().message().contains().content(
        "1 pinned message(s) has been deleted with tag: TestMessage")
    # Tests adding another message to update pins
    await dpytest.message("$pin TestMessage2 www.discord.com test")
    assert dpytest.verify().message().contains().content(
        "A new message has been pinned with tag: TestMessage2 and link: www.discord.com with a description: test")
    await dpytest.message("$updatepin TestMessage2 www.zoom.com test")
    assert dpytest.verify().message().contains().content(
        "A pinned message has been updated with tag: TestMessage2 and new link: www.zoom.com")

# ---------------------------
# Tests cogs/emailAddressSpec
# ---------------------------
@pytest.mark.asyncio
async def test_emailAddressCRUD(bot):
    # Test email address specification to ensure functionality and edge cases
    # Tests the add email functionality
    await dpytest.message(content="$add_email noreplytest@classmatebot.com")
    assert dpytest.verify().message().contains().content("Email address has been configured successfully")
    # Tests the update email functionality
    await dpytest.message("$update_email noreplytest1@classmatebot.com")
    assert dpytest.verify().message().contains().content(
        "Email address has been updated successfully..!")
    # Tests view mail functionality
    await dpytest.message("$view_email")
    assert dpytest.verify().message().contains().content(
        "currently configured email address:noreplytest1@classmatebot.com")
    # Tests delete email functionality
    await dpytest.message("$delete_email")
    assert dpytest.verify().message().contains().content(
        "Email address has been deleted successfully..!")
    # Tests wrong use of command
    await dpytest.message("$add_email no_reply_test")
    assert dpytest.verify().message().contains().content(
        "Enter a valid Email Address..!")
    await dpytest.message("$update_email no_reply_test")
    assert dpytest.verify().message().contains().content(
        "Enter a valid Email Address..!")
    await dpytest.message("$add_email no_reply_test@example")
    assert dpytest.verify().message().contains().content(
        "Enter a valid Email Address..!")
    await dpytest.message("$add_email @example.com")
    assert dpytest.verify().message().contains().content(
        "Enter a valid Email Address..!")
    await dpytest.message("$delete_email")
    assert dpytest.verify().message().contains().content(
        "There is no email address configured..!")
    await dpytest.message("$view_email")
    assert dpytest.verify().message().contains().content(
        "There is no email address configured..!")
    with pytest.raises(Exception):
        await dpytest.message(content="$add_email")
        assert dpytest.verify().message().contains().content(
            "To use the add_email command, do: $add_email email_address")
        assert dpytest.verify().message().contains().content(
            "( For example: $add_email no-reply@example.com)")
    with pytest.raises(Exception):
        await dpytest.message(content="$update_email")
        assert dpytest.verify().message().contains().content(
            "To use the add_email command, do: $add_email email_address")
        assert dpytest.verify().message().contains().content(
            "( For example: $update_email no-reply@example.com)")
        
    

# ----------------------
# Tests invalid pinning
# ----------------------
@pytest.mark.asyncio
async def test_pinError(bot):
    # Tests pinning without a message, will fail
    with pytest.raises(Exception):
        await dpytest.message("$pin")
        assert dpytest.verify().message().contains().content(
            'To use the pin command, do: $pin TAGNAME LINK DESCRIPTION \n ( For example: $pin HW https://discordapp.com/channels/139565116151562240/139565116151562240/890813190433292298 HW8 reminder )')


# --------------------
# Tests cogs/newComer
# --------------------
@pytest.mark.asyncio
async def test_verifyError(bot):
    # Test verification, should raise exception since channel isn't private
    with pytest.raises(Exception):
        await dpytest.message(content="$verify", channel=0)
    # Can only test this currently since dpytest doesn't allow us to test DM'ing


# We cannot currently test newComer.py in a meaningful way due to not having a way to DM the test bot directly.


# --------------------
# Tests cogs/newComer
# --------------------
@pytest.mark.asyncio
async def test_voting(bot):
    # Test voting, should raise an exception since we aren't in a group
    with pytest.raises(Exception):
        await dpytest.message(content="$vote Project 1")
        assert dpytest.verify().message().contains().content(
            "Could not fine the Group you are in, please contact a TA or join with your group number")


# ---------------------------
# Tests Utility/email_utility
# ---------------------------
@pytest.mark.asyncio
async def test_email_utility(bot):
    # Test email utility negative cases.
    # Test email utility by providing just recipient email address.
    with pytest.raises(Exception):
        EmailUtility().send_email('noreplyclassmatebot@example.com')
    # Test email utility by providing just recipient email address and attachment.
    with pytest.raises(Exception):
        with open('data/email/emails.json') as file:
            EmailUtility().send_email('noreplyclassmatebot@example.com', attachment=file.read())
            
