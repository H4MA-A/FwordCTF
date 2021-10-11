from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/877707596855910490/uqAInqGESUybVebz_LLxuNp-yzP5hXD7kAFFPQ2ZGn2Nl3xjlY4IYHCSzeE-jsT7C_Fv', content='Webhook Message')
response = webhook.execute()