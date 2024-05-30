# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: tictactoe
# Author: hikariatama
# Commands:
# .tictactoe
# ---------------------------------------------------------------------------------

__version__ = (2, 0, 1)

#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.dan.tatar/tictactoe_icon.png
# meta banner: https://mods.hikariatama.ru/badges/tictactoe.jpg
# meta developer: @hikarimods
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.2.10

import copy
import enum
from random import choice
from typing import List

from telethon.tl.types import Message
from telethon.utils import get_display_name

from .. import loader, utils
from ..inline.types import InlineCall

phrases = [
    "Your brain is just a joke... Use it!",
    "What a nice move...",
    "Try to overcome me!",
    "I'm irresistible, you have no chances!",
    "The clock is ticking... Hurry up.",
    "Don't act, stop to think!",
    "It was your choice, not mine...",
]

class Player(enum.Enum):
    x = 1
    o = 2

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o


MARKER_TO_CHAR = {
    None: " . ",
    Player.x: " x ",
    Player.o: " o ",
}


class Board:
    def __init__(self):
        self.dimension = 3
        self.grid = [
            [None for _ in range(self.dimension)] for _ in range(self.dimension)
        ]

        self.moves = {Player.x: [], Player.o: []}

    def print(self):
        print()
        for row in range(self.dimension):
            line = [
                MARKER_TO_CHAR[self.grid[row][col]] for col in range(self.dimension)
            ]
            print("%s" % "".join(line))

    def has_winner(self):
        # need at least 5 moves before x hits three in a row
        if len(self.moves[Player.x]) < 3 and len(self.moves[Player.o]) < 3:
            return None

        # check rows for win
        for row in range(self.dimension):
            unique_rows = set(self.grid[row])
            if len(unique_rows) == 1:
                value = unique_rows.pop()
                if value is not None:
                    return value

        # check columns for win
        for col in range(self.dimension):
            unique_cols = {self.grid[row][col] for row in range(self.dimension)}
            if len(unique_cols) == 1:
                value = unique_cols.pop()
                if value is not None:
                    return value

        # check backwards diagonal (top left to bottom right) for win
        backwards_diag = {self.grid[0][0], self.grid[1][1], self.grid[2][2]}
        if len(backwards_diag) == 1:
            value = backwards_diag.pop()
            if value is not None:
                return value

        # check forwards diagonal (bottom left to top right) for win
        forwards_diag = {self.grid[2][0], self.grid[1][1], self.grid[0][2]}
        if len(forwards_diag) == 1:
            value = forwards_diag.pop()
            if value is not None:
                return value

        # found no winner, return None
        return None

    def make_move(self, row, col, player):
        if self.is_space_empty(row, col):
            self.grid[row][col] = player
            self.moves[player].append((row, col))
            if len(self.moves[player]) > 3:
                old_row, old_col = self.moves[player].pop(0)
                self.grid[old_row][old_col] = None
        else:
            raise Exception("Attempting to move onto already occupied space")

    def is_space_empty(self, row, col):
        return self.grid[row][col] is None

    def get_legal_moves(self):
        choices = []
        for row in range(self.dimension):
            choices.extend(
                [row, col]
                for col in range(self.dimension)
                if (self.is_space_empty(row, col))
            )

        return choices

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        dp = Board()
        dp.grid = copy.deepcopy(self.grid)
        dp.moves = copy.deepcopy(self.moves)
        return dp


@loader.tds
class TicTacToeMod(loader.Module):
    """Play your favorite game in Telegram"""

    strings = {
        "name": "TicTacToe",
        "gamestart": (
            "🧠 <b>You want to play, let's play!</b>\n<i>Waiting for second"
            " player...</i>"
        ),
        "game_discarded": "Game is discarded",
        "wait_for_your_turn": "Wait for your turn",
        "no_move": "This cell is not empty",
        "not_your_game": "It is not your game, don't interrupt it",
        "draw": (
            "🧠 <b>The game is over! What a pity...</b>\n<i>🐉 The game ended with"
            " <b>draw</b>. No winner, no argument...</i>"
        ),
        "normal_game": (
            "🧠 <b>{}</b>\n<i>Playing with <b>{}</b></i>\n\n<i>Now is the turn of"
            " <b>{}</b></i>"
        ),
        "win": (
            "🧠 <b>The game is over! What a pity...</b>\n\n<i>🏆 Winner: <b>{}"
            " ({})</b></i>\n<code>{}</code>"
        ),
        "not_with_yourself": "You can't play with yourself!",
    }

    strings_ru = {
        "gamestart": (
            "🧠 <b>Поиграть захотелось? Поиграем!</b>\n<i>Ожидание второго игрока...</i>"
        ),
        "game_discarded": "Игра отменена",
        "wait_for_your_turn": "Ожидание хода",
        "no_move": "Эта клетка уже заполнена",
        "not_your_game": "Это не твоя игра, не мешай",
        "draw": (
            "🧠 <b>Игра окончена! Какая жалость...</b>\n<i>🐉 Игра закончилась"
            " <b>ничьей</b>. Нет победителя, нет спора...</i>"
        ),
        "normal_game": (
            "🧠 <b>{}</b>\n<i>Игра с <b>{}</b></i>\n\n<i>Сейчас ходит <b>{}</b></i>"
        ),
        "win": (
            "🧠 <b>Игра окончена! Какая жалость...</b>\n\n<i>🏆 Победитель: <b>{}"
            " ({})</b></i>\n<code>{}</code>"
        ),
        "not_with_yourself": "Ты не можешь играть сам с собой!",
        "_cmd_doc_tictactoe": "Начать новую игру в крестики-нолики",
        "_cls_doc": "Сыграй в крестики-нолики прямо в Телеграм",
    }

    async def client_ready(self, client, db):
        self._games = {}
        self._me = await client.get_me()

    async def _process_click(
        self,
        call: InlineCall,
        i: int,
        j: int,
        line: str,
    ):
        if call.from_user.id not in [
            self._me.id,
            self._games[call.form["uid"]]["2_player"],
        ]:
            await call.answer(self.strings("not_your_game"))
            return

        if call.from_user.id != self._games[call.form["uid"]]["turn"]:
            await call.answer(self.strings("wait_for_your_turn"))
            return

        if line != ".":
            await call.answer(self.strings("no_move"))
            return

        self._games[call.form["uid"]]["board"].make_move(
            i, j, self._games[call.form["uid"]]["mapping"][call.from_user.id]
        )

        self._games[call.form["uid"]]["turn"] = (
            self._me.id
            if call.from_user.id != self._me.id
            else self._games[call.form["uid"]]["2_player"]
        )

        if winner := self._games[call.form["uid"]]["board"].has_winner():
            await call.edit(
                self.strings("win").format(
                    (
                        get_display_name(await call._client.get_entity(self._me))
                        if winner == Player.x
                        else get_display_name(
                            await call._client.get_entity(
                                self._games[call.form["uid"]]["2_player"]
                            )
                        )
                    ),
                    winner.name,
                    "\n".join(
                        "".join(
                            MARKER_TO_CHAR[call]
                            for call in row
                        )
                        for row in self._games[call.form["uid"]]["board"].grid
                    ),
                )
            )
            self._games.pop(call.form["uid"])
            return

        if len(self._games[call.form["uid"]]["board"].get_legal_moves()) == 0:
            await call.edit(self.strings("draw"))
            self._games.pop(call.form["uid"])
            return

        await call.edit(
            self.strings("normal_game").format(
                get_display_name(self._me),
                get_display_name(
                    await call._client.get_entity(
                        self._games[call.form["uid"]]["2_player"]
                    )
                ),
                get_display_name(
                    await call._client.get_entity(
                        self._games[call.form["uid"]]["turn"]
                    )
                ),
            ),
            reply_markup=[
                [
                    {
                        "text": MARKER_TO_CHAR[cell],
                        "callback": self._process_click,
                        "args": (i, j, MARKER_TO_CHAR[cell].strip()),
                    }
                    for j, cell in enumerate(row)
                ]
                for i, row in enumerate(self._games[call.form["uid"]]["board"].grid)
            ],
        )

    async def tictactoe_cmd(self, message: Message):
        """Start a new game of tic-tac-toe"""
        if (
            message.is_private
            and message.chat_id != (await message.client.get_me()).id
        ):
            await utils.answer(message, self.strings("not_with_yourself"))
            return

        if message.chat_id in self._games:
            self._games.pop(message.chat_id)

        self._games[message.chat_id] = {
            "board": Board(),
            "turn": self._me.id,
            "mapping": {
                self._me.id: Player.x,
            },
        }

        await self.inline.form(
            self.strings("gamestart"),
            message=message,
            reply_markup=[],
            ttl=5 * 60,
        )
