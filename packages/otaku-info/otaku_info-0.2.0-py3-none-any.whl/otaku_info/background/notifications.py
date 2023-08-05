"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of otaku-info.

otaku-info is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

otaku-info is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with otaku-info.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Dict, List
from puffotter.flask.base import db
from otaku_info.Config import Config
from puffotter.flask.db.TelegramChatId import TelegramChatId
from otaku_info.db.MediaUserState import MediaUserState
from otaku_info.db.MediaNotification import MediaNotification
from otaku_info.db.MangaChapterGuess import MangaChapterGuess
from otaku_info.db.MediaId import MediaId
from otaku_info.db.MediaItem import MediaItem
from otaku_info.db.NotificationSetting import NotificationSetting
from otaku_info.utils.enums import \
    MediaType, MediaSubType, ConsumingState, NotificationType


def send_new_manga_chapter_notifications():
    """
    Sends out telegram notifications for manga chapter updates
    :return: None
    """

    chats: Dict[int, TelegramChatId] = {
        x.user_id: x for x in TelegramChatId.query.all()
    }
    chapter_guesses: Dict[int, int] = {
        x.media_id_id: x.guess for x in MangaChapterGuess.query.all()
    }
    user_states: List[MediaUserState] = MediaUserState.query\
        .join(MediaId) \
        .join(MediaItem) \
        .filter(MediaItem.media_type == MediaType.MANGA)\
        .filter(MediaItem.media_subtype == MediaSubType.MANGA)\
        .filter(MediaUserState.consuming_state == ConsumingState.CURRENT)\
        .all()
    notifications: Dict[int, MediaNotification] = {
        x.media_user_state_id: x for x in MediaNotification.query.all()
    }
    notification_settings: Dict[int, NotificationSetting] = {
        x.user_id: x
        for x in NotificationSetting.query.filter_by(
            notification_type=NotificationType.NEW_MANGA_CHAPTERS
        ).all()
    }

    for user_state in user_states:

        settings = notification_settings.get(user_state.user_id)
        if settings is None or not settings.value:
            continue

        guess = chapter_guesses.get(user_state.media_id_id)
        notification = notifications.get(user_state.id)
        chat = chats.get(user_state.user_id)
        progress = user_state.progress

        if guess is None or chat is None:
            continue

        diff = guess - progress

        if diff <= 0:
            continue

        if notification is None:
            notification = MediaNotification(
                media_user_state=user_state, last_update=guess
            )
            db.session.add(notification)

        if guess != notification.last_update:

            notification.last_update = guess
            if user_state.score >= settings.minimum_score:

                title = user_state.media_id.media_item.title
                url = f"https://{Config.DOMAIN_NAME}/media/" \
                      f"{user_state.media_id.media_item_id}"
                chat.send_message(
                    f"New Chapter for {title}\n\n"
                    f"Chapter {progress}/{guess} (+{diff})\n\n"
                    f"{url}"
                )

    db.session.commit()
