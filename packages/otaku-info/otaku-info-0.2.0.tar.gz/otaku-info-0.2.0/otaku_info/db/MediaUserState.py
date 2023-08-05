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

from typing import Dict, Any, Optional
from puffotter.flask.base import db
from puffotter.flask.db.User import User
from puffotter.flask.db.ModelMixin import ModelMixin
from otaku_info.db.MediaId import MediaId
from otaku_info.utils.enums import ConsumingState


class MediaUserState(ModelMixin, db.Model):
    """
    Database model that keeps track of a user's entries on external services
    for a media item
    """

    __tablename__ = "media_user_states"
    """
    The name of the database table
    """

    __table_args__ = (
        db.UniqueConstraint(
            "media_id_id",
            "user_id",
            name="unique_media_user_state"
        ),
    )
    """
    Makes sure that objects that should be unique are unique
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    media_id_id: int = db.Column(
        db.Integer,
        db.ForeignKey(
            "media_ids.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the media ID referenced by this user state
    """

    media_id: MediaId = db.relationship(
        "MediaId",
        backref=db.backref(
            "media_user_states", lazy=True, cascade="all,delete"
        )
    )
    """
    The media ID referenced by this user state
    """

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False
    )
    """
    The ID of the user associated with this user state
    """

    user: User = db.relationship(
        "User",
        backref=db.backref(
            "media_user_states", lazy=True, cascade="all,delete"
        )
    )
    """
    The user associated with this user state
    """

    progress: Optional[int] = db.Column(db.Integer, nullable=True)
    """
    The user's current progress consuming the media item
    """

    score: Optional[int] = db.Column(db.Integer, nullable=True)
    """
    The user's score for the references media item
    """

    consuming_state: ConsumingState \
        = db.Column(db.Enum(ConsumingState), nullable=False)
    """
    The current consuming state of the user for this media item
    """

    def __json__(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models
                                 will be included or if they're limited to IDs
        :return: A dictionary representing the model's values
        """
        data = {
            "id": self.id,
            "media_id_id": self.media_id_id,
            "user_id": self.user_id,
            "progress": self.progress,
            "score": self.score,
            "consuming_state": self.consuming_state.value
        }
        if include_children:
            data["media_id"] = self.media_id.__json__(include_children)
            data["user"] = self.user.__json__(include_children)
        return data
