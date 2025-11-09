import discord
from openai import OpenAI

# -------------------------------
# -------------------------------
DISCORD_TOKEN = "MTQzNjY2Njk5NDg4MjY0NjAzNg.GwNEBm.RZQdINmNNIGciVJRDo7hnTOOGXfrfp9Oegp1ew"
OPENAI_API_KEY = "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"

# -------------------------------
# -------------------------------
client_oa = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True  # برای خواندن متن پیام‌ها لازم است

bot = discord.Client(intents=intents)


# -------------------------------
# -------------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")


# -------------------------------
# -------------------------------
@bot.event
async def on_message(message: discord.Message):
    # خودِ بات را نادیده بگیر
    if message.author.bot:
        return

    # فقط پیام‌هایی که با !gpt شروع می‌شوند
    prefix = "!gpt "
    if not message.content.startswith(prefix):
        return

    # متن بعد از !gpt را بگیر
    prompt = message.content[len(prefix):].strip()

    if not prompt:
        await message.reply("بعد از !gpt یه چیزی هم بنویس 🙂")
        return

    # نشون بده بات داره فکر می‌کنه
    async with message.channel.typing():
        try:
            # درخواست به مدل OpenAI
            response = client_oa.chat.completions.create(
                model="gpt-4.1-mini",  # در صورت نیاز می‌تونی مدل رو عوض کنی
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

            # محدودیت 2000 کاراکتر دیسکورد
            if len(answer) > 1900:
                answer = answer[:1900] + " ..."

            await message.reply(answer)

        except Exception as e:
            print("❌ OpenAI error:", e)
            await message.reply("یه مشکلی در ارتباط با سرور پیش اومد 🤖")


# -------------------------------
# -------------------------------
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
