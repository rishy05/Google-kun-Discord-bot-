from discord.ext import commands
import upload
import g_mail


client = commands.Bot(command_prefix='G ')

@client.event
async def on_ready():
    print("ready")


@client.command()
async def create(ctx, *, name):
    upload.auth()
    upload.create(name)


    await ctx.send('Done')

@client.command()
async def search(ctx, *, name):
    upload.auth()
    await ctx.send(upload.search(name))

@client.command()
async def send(ctx, to, *,msg ):
    g_mail.auth()
    g_mail.send_mail(to, msg)
    await ctx.send("Done!!")



client.run("SECRET")
