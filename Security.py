from typing import Any, Awaitable, Callable, Dict
from aiogram import types
from aiogram  import BaseMiddleware
from aiogram.types import Message
class BannedUserMiddleware(BaseMiddleware):
 
    def __init__(self) -> None:
            self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
        ) -> Any:
            username = event.from_user.username
            if self.is_user_banned(username):
                await event.reply("You are banned and cannot use this bot.")
                return 
            return await handler(event, data)

    def is_user_banned(self, username: str) -> bool:
        # Implement your logic to check if the user is banned
        with open('banned_users.txt', 'r') as f:
            banned_users = [line.strip() for line in f.readlines()]
        return username in banned_users