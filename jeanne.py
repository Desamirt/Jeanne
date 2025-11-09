import discord
from discord.ext import commands
from openai import OpenAI
import os
# -------------------------------
# 🔑 بارگذاری مقادیر از فایل .env
# -------------------------------

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -------------------------------
# ⚙️ تنظیم کلاینتها
# -------------------------------
client_oa = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True  # برای خواندن متن پیامها لازم است

bot = discord.Client(intents=intents)

# -------------------------------
# ✅ وقتی بات آنلاین میشود
# -------------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# -------------------------------
# 💬 واکنش به پیامهایی که با !gpt شروع میشوند
# -------------------------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    prefix = "!gpt "
    if not message.content.startswith(prefix):
        return

    prompt = message.content[len(prefix):].strip()

    if not prompt:
        await message.reply("بعد از !gpt یه چیزی هم بنویس 🙂")
        return

    async with message.channel.typing():
        try:
            response = client_oa.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant inside a Discord server. "
                            "Answer in the same language as the user. "
                            "Be concise but clear."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            answer = response.choices[0].message.content or "No response."

            if len(answer) > 1900:
                answer = answer[:1900] + " ..."

            await message.reply(answer)

        except Exception as e:
            print("❌ OpenAI error:", e)
            await message.reply("یه مشکلی در ارتباط با سرور پیش اومد 🤖")

# -------------------------------
# 🚀 اجرای بات
# -------------------------------
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
