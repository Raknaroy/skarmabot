#   ____  _  __
#  / ___|| |/ /__ _ _ __ _ __ ___   __ _
#  \___ \| ' // _` | '__| '_ ` _ \ / _` |
#   ___) | . \ (_| | |  | | | | | | (_| |
#  |____/|_|\_\__,_|_|  |_| |_| |_|\__,_|
#
# Yet another carma bot for telegram
# Copyright (C) 2020 Nikita Serba. All rights reserved
# https://github.com/sandsbit/skarmabot
#
# SKarma is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# SKarma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with SKarma. If not, see <https://www.gnu.org/licenses/>.

from telegram import LabeledPrice

from telegram.ext import ConversationHandler

from skarma.utils.errorm import catch_error
from skarma.donate_info import DonateInfo

AMOUNT = range(1)

_donate_info = DonateInfo()


@catch_error
def donate_ask_d(update, context):
    return donate_ask(update, context, True)


@catch_error
def donate_ask(update, context, debug=False):
    enabled = _donate_info.test_enabled if debug else _donate_info.enabled

    if 'group' in update.effective_chat.type:
        update.message.reply_text('Увы, донатики работают только в личных сообщениях с ботом')
        return ConversationHandler.END

    if not enabled:
        update.message.reply_text('Увы, донатики пока недоступны, попробуйте позже!')
        return ConversationHandler.END

    update.message.reply_text('О, вы решили сделать донатик? Замечательно! Используйте /cancel для отмены операции.'
                              ' Сколько вы готовы нам пожертвовать? (введите число в долларах, без указания валюты'
                              ' в сообщении)')

    return AMOUNT


@catch_error
def donate_d(update, context):
    return donate(update, context, True)


@catch_error
def donate(update, context, debug=False):
    chat_id = update.effective_chat.id
    text = update.message.text

    enabled = _donate_info.test_enabled if debug else _donate_info.enabled
    payload = _donate_info.test_payload if debug else _donate_info.payload
    provider_token = _donate_info.test_provider_token if debug else _donate_info.provider_token
    start_parameter = _donate_info.test_start_parameter if debug else _donate_info.start_parameter

    assert enabled

    try:
        price = float(text.replace(',', '.'))
    except ValueError:
        update.message.reply_text('Эй, такого числа нет! Попробуйте снова')
        return AMOUNT

    if price < 1:
        update.message.reply_text('Слишком маленькая сумма, мы принимает донаты от $1. Попробуйте снова!')
        return AMOUNT
    elif price > 10000:
        update.message.reply_text('Ого, какотелей большой! Мы принимаем максимум $10,000. Попробуйте снова!')
        return AMOUNT

    title = "Уря, донатик!"
    description = "Проспонсируйте оплату сервера и кофе голодающему автору бота"
    currency = "USD"
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Donate", int(price * 100))]

    context.bot.send_invoice(chat_id, title, description, payload,
                             provider_token, start_parameter, currency, prices)

    return ConversationHandler.END


@catch_error
def cancel(update, _):
    update.message.reply_text('Оке(')

    return ConversationHandler.END


@catch_error
def finish_donate(update, _):
    update.message.reply_text("Пасиб за донат 🥰🥰")
