import discord
import requests
import json

bot = discord.Bot()

redeem_for_all = bot.create_group("redeem_for_all", "Redeem gift codes for all", guild_ids=[742405919249268767, 742269996071387238])

@redeem_for_all.command(name="genshin", description="Redeem for all for Genshin Impact", guild_ids=[742405919249268767, 742269996071387238])
async def genshin(ctx: discord.ApplicationContext, code: str):
    with open('users.json', 'r') as file:
        users = json.load(file)

    embed=discord.Embed(title=f"Genshin Impact Code Redemption", description=f"Redeeming code `{code}`", color=0x666666)
    embed.set_footer(text="Gamer/Hacker", icon_url="https://static.wikia.nocookie.net/houkai-star-rail/images/a/a8/Profile_Picture_Silver_Wolf_-_Opening.png/revision/latest?cb=20241023022201")

    # Claim for the author first
    user = [u for u in users if u['discord_id'] == ctx.author.id]
    if not user:
        embed.add_field(name=f"Error", value=f"{ctx.author.mention} - I don't have your credit card details yet", inline=False)
    else:
        user = user[0]
        response = genshin_redeem(code, user)
        result = json.loads(response.text)
        status = get_status(result['retcode'])
        embed.add_field(name=f"{user['user_id']}", value=f"<@!{user['discord_id']}> - "+status, inline=False)
        print(f"{result}")
    # End for author claim

    # Claim for the rest
    for user in users:
        if(user['discord_id'] == ctx.author.id):
            continue

        response = genshin_redeem(code, user)
        result = json.loads(response.text)
        status = get_status(result['retcode'])

        embed.add_field(name=f"{user['user_id']}", value=f"<@!{user['discord_id']}> - "+status, inline=False)
        print(f"{result}")
    await ctx.respond(embed=embed)

def genshin_redeem(code, user):
    return requests.get(
        'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey',
        cookies=user['cookies'],
        params={'uid': user['user_id'],
                'region': 'os_asia',
                'lang': 'en',
                'cdkey': code,
                'game_biz': 'hk4e_global',
                'sLangKey': 'en-us'
                })

def get_status(retcode):
    status = ''
    match retcode:
        case 0:
            status = 'OK'
        case -2017:
            status = 'Already redeemed'
        case -2003:
            status = 'Invalid Code'
        case -1071:
            status = 'Session invalid, resend cookies'
        case _:
            status = 'Error, checking logs for details'
    
    return status

def setup(bot):
    bot.add_application_command(redeem_for_all)
    print("Redeem for all module - Loaded")