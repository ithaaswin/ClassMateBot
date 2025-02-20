# Copyright (c) 2021 War-Keeper
"""
This File contains commands for voting on projects,
displaying which groups have signed up for which project.
"""
import csv
import discord
from discord.ext import commands
import os


class Voting(commands.Cog):
    """
        Class provides various methods to manage voting of multiple groups.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vote', help='Used for voting for Project 2 and 3, \
    To use the vote command, do: $vote \'Project\' <Num> \n \
    (For example: $vote project 0)', pass_context=True)
    async def vote(self, ctx, arg='Project', arg2='-1'):
        """
            vote for the given project by adding the user to it.

            Parameters:
                ctx: used to access the values passed through the current context.
                arg: the name of the project.
                arg2: the number of the project.

            Returns:
                adds the user to the given project or returns an error if the project is invalid or
                the user is not in a valid group.

        """
        # load the groups from the csv
        groups = load_groups()
        # load the projects from the csv
        projects = load_projects()

        # get the arguments for the project to vote on
        project_num = arg.upper() + ' ' + arg2

        # get the name of the caller
        member_name = ctx.message.author.display_name.upper()

        # initialize which group the member in in
        member_group = '-1'

        # check which group the member is in
        for key in groups.keys():
            if member_name in groups[key]:
                member_group = key
                print(member_group)

        # error handle if member is not in a group
        if member_group == '-1':
            await ctx.send(
                "Could not fine the Group you are in,"
                " please contact a TA or join with your group number")
            raise commands.UserInputError

        # if the project is a valid option
        if project_num in projects:

            # check if project has more than 6 groups voting on it
            if len(projects[project_num]) == 6:
                await ctx.send('A Project cannot have more than 6 Groups working on it!')
                return

            # check if you have already voted for another group
            for key in projects.keys():
                if member_group in projects[key]:
                    print(member_group)
                    await ctx.send('You already voted for ' + key.title())
                    return

            # add the group to the project list
            projects[project_num].append(member_group)
            await ctx.send(member_group + ' has voted for ' + project_num.title() + '!')
            print_projects(projects)

        # error handling
        else:
            await ctx.send('Not a valid Project')
            await ctx.send('Used for voting for Project 2 and 3, To use the vote command, '
                           'do: $vote \'Project\' <Num> \n (For example: $vote project 0)')

    @vote.error
    async def vote_error(self, ctx, error):
        """
            this handles errors related to the vote command
        """
        if isinstance(error, commands.UserInputError):
            await ctx.send('To join a group, use the join command, do: $vote \'Project\' <Num> \n \
            ( For example: $vote Project 0 )')

    @commands.command(name='projects', help='print projects with groups assigned to them',
                      pass_context=True)
    @commands.dm_only()
    async def projects(self, ctx):
        """
            prints the list of current projects.

            Parameters:
                ctx: used to access the values passed through the current context.

            Returns:
                prints the list of current projects.

        """
        projects = load_projects()
        overall = ''
        for key in projects.keys():
            if key != 'PROJECT_NUM':
                s = ''
                temp = projects[key]
                for num in temp:
                    s += num + ', '
                if s != '':
                    overall += key + ': ' + s[:-2] + '\n'
                else:
                    overall += key + ': \n'
        await ctx.send(overall)


def load_projects() -> dict:
    """
        Used to load the Project from the csv file into a dictionary.
    """
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dir)
    os.chdir('data')
    os.chdir('server_data')
    with open('Project_mapping.csv', mode='r') as infile:
        reader = csv.reader(infile)
        student_pools = {
            rows[0].upper(): [rows[1].upper(), rows[2].upper(), rows[3].upper(), rows[4].upper(),
                              rows[5].upper(), rows[6].upper()] for rows in reader}
    for key in student_pools.keys():
        student_pools[key] = list(filter(None, student_pools[key]))

    return student_pools


def print_projects(projects):
    """
        Used to print the Projects to the csv file.
    """
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dir)
    os.chdir('data')
    os.chdir('server_data')
    with open('Project_mapping.csv', mode='w', newline="") as outfile:
        writer = csv.writer(outfile)
        for key in projects.keys():
            while len(projects[key]) < 6:
                projects[key].append(None)
            writer.writerow([key] + projects[key])


def load_groups() -> dict:
    """
        Used to load the groups from the csv file into a dictionary.
    """
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dir)
    os.chdir('data')
    os.chdir('server_data')
    with open('groups.csv', mode='r') as infile:
        reader = csv.reader(infile)
        group = {rows[0].upper(): [rows[1].upper(), rows[2].upper(), rows[3].upper(), rows[4].upper(),
                                   rows[5].upper(), rows[6].upper()] for rows in reader}

    for key in group.keys():
        group[key] = list(filter(None, group[key]))

    return group


def print_groups(group):
    """
        Used to print the groups to the csv file.
    """
    with open('./data/server_data/groups.csv', mode='w', newline="") as outfile:
        writer = csv.writer(outfile)
        for key in group.keys():
            while len(group[key]) < 6:
                group[key].append(None)
            writer.writerow([key] + group[key])


def setup(bot):
    """
        add the file to the bot's cog system.
    """
    bot.add_cog(Voting(bot))


