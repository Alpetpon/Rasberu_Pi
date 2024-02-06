# import asyncio
# from typing import Any, Callable, Dict, Awaitable
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject
#
# class SlowpokeMiddleware(BaseMiddleware):
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         await asyncio.sleep(40)
#         # Если в хэндлере сделать return, то это значение попадёт в result
#         print(f"Handler was delayed by {self.sleep_sec} seconds")
#         return await handler(event, data)