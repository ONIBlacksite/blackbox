import discord
from discord.ext import commands

YOUR_AAR_CHANNEL_ID = 1188702656022184046  # Replace with the actual channel ID where AAR reports should be sent

class AAR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="submitaar")
    async def submit_aar(self, ctx):
        # Ask each portion of the AAR and delete the question once answered
        questions = [
            "After Action Report – **CLAN V. CLAN**",
            "DOA: **MONTH/DAY/YEAR**",
            "TOA: **TYPE OF ACTIVITY**",
            "POC: **PERSON OF CHARGE**",
            "OUT: **VICTORY/DEFEAT/TIE**",
            "\n__Personnel Attending__: – # of People",
            "\nOpposing Forces:",
            "\nLeft Early (^):",
            "\nJoined Late (!):",
            "\n__Event Log__: ",
            "\n__Event Comments__:",
            "\n**__What can be improved?__**",
            "\n**__MVP__:"
            "+ Good Communication",
            "– Complaining About Nades"
        ]

        responses = []

        for question in questions:
            message = await ctx.send(question)
            try:
                response = await self.bot.wait_for('message', timeout=300, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                responses.append((question, response.content))
                await message.delete()
            except discord.errors.NotFound:
                # Message may have been deleted by the user, ignore the error
                pass
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond. The AAR submission process has been canceled.")
                return

        # Create an embed for the AAR
        embed = discord.Embed(title="After Action Report", color=discord.Color.blue())

        for question, answer in responses:
            embed.add_field(name=question, value=answer, inline=False)

        # Send the embed to the specified channel
        aar_channel = self.bot.get_channel(YOUR_AAR_CHANNEL_ID)
        if aar_channel:
            await aar_channel.send(embed=embed)
            await ctx.send("Your After Action Report has been submitted successfully.")
        else:
            await ctx.send("AAR channel not found. Please contact the server administrator.")

def setup(bot):
    bot.add_cog(AAR(bot))
