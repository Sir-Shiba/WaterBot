import discord
import random
import asyncio

token = open('token.txt', 'r').read()
client = discord.Client()
dactive = []

def tophierarcy(author):
    return sorted([tup for tup in dactive if tup[0] == author], key=lambda x: x[1], reverse = True)[0]

async def drink(ctx, weight, hours, drank=0):
    ounce = int(weight * (2/3))
    if drank > ounce:
        await ctx.channel.send('Drank more than daily needs already :O')
    else:
        ounce -= drank
        bottles = int(ounce/17) + 1
        interval_min = (hours * 60)/bottles
        interval_sec = (hours * 3600)/bottles
        message = 'drink 17 ounces of water (1 bottle/ 2 cups) in the next {} minute(s)'.format(int(interval_min))

        if ctx.author.id not in [tup[0] for tup in dactive]:
            dactive.append([ctx.author.id, 0])
            order = 0
        else:
            await ctx.channel.send('Active Iteration Found: Performing Override')
            embed = discord.Embed(title='New Iteration : ', color=discord.Colour.from_rgb(252, 0, 59))
            await ctx.author.send(embed=embed)
            a = tophierarcy(ctx.author.id)
            dactive.remove(a)
            order = a[1] + 1
            dactive.append([a[0], order])

        await ctx.channel.send('Hydration Monitor Initated Sucessfully: You are drinking {} bottle(s) of water in {} hour(s)'.format(bottles, hours))

    while ounce > 0 and order == tophierarcy(ctx.author.id)[1]:
        ounce -= 17
        embed = discord.Embed(title='Hydration Monitor', description=message, color=0x00eaff)
        await ctx.author.send(embed=embed)
        if ounce < 0:
            file = discord.File('Kibosummer.png', filename = 'Kibosummer.png')
            embed = discord.Embed(title='Congrats', description='You reached your daily water needs! Good job Hyrdohomie :)', color=0x00eaff)
            embed.set_image(url="attachment://Kibosummer.png")
            await ctx.author.send(file=file,embed=embed)
        await asyncio.sleep(interval_sec)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('>help for commands'))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(ctx):

    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name} {ctx.author.id} {ctx.guild.id}: {ctx.content}")
    def command(cmd, desc, use, example ):
        return '\n{:<20}{}\n\t{:<10}{}'.format(cmd, desc, use, example)


    if (str(ctx.content.lower()) == '>help'):
        
        message = '{:<20}\n{:<20}{}'.format('**List of Commands:**', '**>help:**', 'displays commands')
        message += command('**>game:**', 'matchmaking tool', 'usage:', '>game [name of game] [number of other people]')
        message += command('**>poll:**', 'polling tool', 'usage:', '>poll "question" [choice] [choice] [etc]')
        message += command('**>?**', '8-ball', 'usage:', '>? [question]')
        message += command('**>water:**', 'hydration reminder bot', 'usage:', '>water [body weight in pounds] [hours til sleep] [ounces drank already]')
        embed= discord.Embed(title='Commands', description=message, color=0x00eaff)
        await ctx.channel.send(embed=embed)

    elif (str(ctx.content.lower()).startswith('>game')) and len(ctx.content.lower().split()) > 2 and ctx.content.lower().split()[-1].isdigit():
        game = ' '.join(ctx.content.split()[1:-1])
        num = int(ctx.content.lower().split()[-1])
        
        message = '{} is looking for **{}** other(s) to play **{}**'.format(ctx.author.name, num, game)
        embed = discord.Embed(title='Game Queue', description=message, color=0x00eaff)
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction('🎮')

        users = []
        temp = 0
        users.append(ctx.author)

        def check(payload):
            return payload

        while temp != num:
            payload = await client.wait_for("raw_reaction_add", check=check)
            # print(payload)
            print(payload.member.name)
            newid = payload.message_id
            user = payload.member
            print(newid, msg.id)
            if user not in users and user.name != msg.author.name:
                users.append(user)
                temp += 1
        message1 = ' '.join([person.mention for person in users])
        message2 = '**Everyone is ready to play {}**'.format(game)
        embed = discord.Embed(title='Match Found', description=message2, color=0x00eaff)
        msg1 = await ctx.channel.send(message1)
        msg2 = await ctx.channel.send(embed=embed)

    elif (str(ctx.content.lower()).startswith('>poll')) and len(ctx.content.lower().split()) > 2:
        try:
            question = ctx.content.split('\"', 1)[1].split('\"')[0]
            emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']
            choices = ''.join(ctx.content.split('"{}"'.format(question))).split()[1:]
            choice_string = '\n'
            for i in range(len(choices)):
                choice_string += '{}: {}\n'.format(emojis[i],choices[i])
            message = '**Question:** {} {}'.format(question, choice_string)
            embed = discord.Embed(title='Poll', description=message, color=0x00eaff)
            msg = await ctx.channel.send(embed=embed)
            for i in range(len(choices)):
                await msg.add_reaction(emojis[i])
        finally:
            pass

    elif (str(ctx.content.lower()).startswith('>?')) and len(ctx.content.lower().split()) > 1:
        try:
            one = 'One hundo percent yes'
            two = 'Its a coin flip'
            tre = 'Duh'
            fou = 'You already know the answer'
            fiv = 'Too disturbing to answer'
            six = 'Yes, totally'
            sev = 'Why are you even asking this'
            eig = 'Nope'
            nin = 'The opposite of yes'
            ten = 'One hundo percent no'
            ele = 'My guess is as good as your\'s'
            box = [one, two, tre, fou, fiv, six, sev, eig, nin, ten, ele]
            answer = random.choice(box)
            embed = discord.Embed(title='The Great Kirbo Says:', description=answer, color=0x00eaff)
            msg = await ctx.channel.send(embed=embed)
        finally:
            pass

    elif (str(ctx.content.lower()).startswith('>water')):
        # try: 
        weight = int(ctx.content.split()[1])
        hour = int(ctx.content.split()[2])

        if int(weight) < 0 or int(hour) < 0:
            raise ValueError
        elif len(ctx.content.split()) == 4:
            sub = int(ctx.content.split()[3])
            if (int(ctx.content.split()[3])) < 0:
                raise ValueError
            await drink(ctx, weight, hour, sub)
        elif len(ctx.content.split()) == 3:
            await drink(ctx, weight, hour)
        else:
            raise ValueError
        # except:
        #     await ctx.channel.send('Invalid: Must be in the form: >water [weight] [hours til sleep] [optional: ounces drank already]')
        # finally:
        #     pass

    elif (str(ctx.content.lower()).startswith('>stop')):
        if ctx.author in dactive:
            dactive.remove(ctx.author)

    elif (str(ctx.content.lower()).startswith('>dab')):
        file = discord.File('dab.png', filename = 'dab.png')
        embed = discord.Embed(color=0x00eaff)
        embed.set_image(url="attachment://dab.png")
        await ctx.channel.send(file=file, embed=embed)

    elif (str(ctx.content.lower()).startswith('>gentleman')):
        file = discord.File('gentleman.png', filename = 'gentleman.png')
        embed = discord.Embed(color=0x00eaff)
        embed.set_image(url="attachment://gentleman.png")
        await ctx.channel.send(file=file, embed=embed)

    elif (str(ctx.content.lower()).startswith('>kirby')):
        file = discord.File('kirby.jpg', filename = 'kirby.jpg')
        embed = discord.Embed(color=0x00eaff)
        embed.set_image(url="attachment://kirby.jpg")
        await ctx.channel.send(file=file, embed=embed) 

client.run(token)

