import discord
from discord.ext import tasks, commands
from datetime import datetime
import os

# === CONFIGURATION ===
TOKEN = os.environ["TOKEN"]  # Get token from environment variable
GUILD_ID = 1389792196470902916  # Replace with your actual server ID
CHANNEL_ID = 1395362484767952947  # Replace with your voice channel ID

# === RP CALENDAR CONFIG ===
START_DATE = datetime(2025, 7, 1)  # When RP time began
RP_MONTHS = [
    "Virelion", "Kastrel", "Obrex", "Tristane", "Cendris",
    "Zulnar", "Marneth", "Joltrix", "Aendral", "Dravenhall"
]
MONTHS_PER_YEAR = 10

# === BOT SETUP ===
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === RP DATE CALCULATION ===
def get_rp_date():
    now = datetime.utcnow()
    delta_days = (now - START_DATE).days
    rp_month_index = delta_days
    rp_year = rp_month_index // MONTHS_PER_YEAR
    month_name = RP_MONTHS[rp_month_index % MONTHS_PER_YEAR]
    return f"📅 RP Date: 1 {month_name}, Year {rp_year}"

# === EVENTS ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    update_rp_time.start()

# === AUTO UPDATE TASK ===
@tasks.loop(hours=1)
async def update_rp_time():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found.")
        return

    channel = guild.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Voice channel not found.")
        return

    rp_date_str = get_rp_date()
    try:
        await channel.edit(name=rp_date_str)
        print(f"🕒 Channel updated: {rp_date_str}")
    except Exception as e:
        print(f"⚠️ Failed to edit channel name: {e}")

# === COMMANDS ===
@bot.command(name="rpdate")
async def rp_date(ctx):
    rp_date_str = get_rp_date()
    await ctx.send(rp_date_str)

# === RUN BOT ===
bot.run(TOKEN)
