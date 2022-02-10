import logging
import asyncio

logging.basicConfig(filename="commands.log")

from telegram import Update
from telegram.ext import CallbackContext

from DailyReport.databases.notion_database import NotionDatabase

from DailyReport.utils.utils import remove_command_from_message
from DailyReport.utils.Either import Either, Left, Right


def EitherHandler(either: Either, update: Update, context: CallbackContext):
    if isinstance(either, Right):
        context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=either.context['message']
        )
    else:
        context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=either.context['message']
        )


class Commands:
    def __init__(
            self,
            notion: NotionDatabase
    ):
        self.notion = notion
        self.log = logging.getLogger("[Commands]")
        self.log.setLevel(level=logging.DEBUG)

    def start(self, update: Update, context: CallbackContext):
        either = self.notion.new_user({
            "telegram_id": update.message.from_user.id,
        })

        EitherHandler(either, update, context)

    def setRoot(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.set_user_info({
            "telegram_id": update.message.from_user.id,
            "root": msg
        })

        EitherHandler(either, update, context)

    def setNotion(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.set_user_info({
            "telegram_id": update.message.from_user.id,
            "integration": msg
        })

        EitherHandler(either, update, context)

    async def begin(self, update: Update, context: CallbackContext):
        self.log.info("1")
        either = await self.notion.init_user_root_notion_page({
            "telegram_id": update.message.from_user.id
        }, self.log)
        self.log.info("5")

        self.log.info(either)

        # EitherHandler(either, update, context)

    def rp(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.report({
            "telegram_id": update.message.from_user.id,
            "message": msg,
            "datetime": update.message.date
        })

        EitherHandler(either, update, context)

    # def todo(self, update: Update, context: CallbackContext):
    #     context.bot.send_message(
    #         chat_id=self.chat_id,
    #         text="Testing todo Command."
    #     )

        """
        {'update_id': 208513719, 'message': {'new_chat_members': [], 'supergroup_chat_created': False, 'channel_chat_created': False, 'photo': [], 'text': '/rp hello 123 ""aa 1 :: 12 : 😂', 'delete_chat_photo': False, 'caption_entities': [], 'entities': [{'type': 'bot_command', 'offset': 0, 'length': 3}], 'message_id': 634, 'new_chat_photo': [], 'date': 1644130630, 'chat': {'type': 'private', 'last_name': '김', 'first_name': '희찬', 'id': 2084891827, 'username': 'heechan_kim'}, 'group_chat_created': False, 'from': {'language_code': 'ko', 'last_name': '김', 'is_bot': False, 'first_name': '희찬', 'username': 'heechan_kim', 'id': 2084891827}}}
        """

        """
        시나리오 :
        /start
        /setToken
        /setRoot
        /begin
        """