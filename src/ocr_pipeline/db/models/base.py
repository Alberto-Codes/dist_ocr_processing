"""Constants and type annotations for an SQLAlchemy-based ORM setup.

This module provides reusable constants and type annotations for defining
mapped columns in SQLAlchemy models. It also includes system defaults
like user information and timestamps.
"""

import datetime
import os
import uuid
from typing import Optional

from sqlalchemy import DECIMAL, Column, DateTime, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated

# Constants
DEFAULT_USER = "system"
"""str: The default username used if the 'USERNAME' environment variable 
is not set."""

DEFAULT_VALID_TO = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
"""datetime: The far future timestamp used as a default validity expiration."""

HOSTNAME = os.getenv("COMPUTERNAME", "UnknownHost")
"""str: The hostname of the machine, defaulting to 'UnknownHost' if unavailable."""

CURRENT_USER = os.getenv("USERNAME", DEFAULT_USER)
"""str: The current username derived from the 'USERNAME' environment variable, 
falling back to the default user.
"""

CURRENT_TIME = datetime.datetime.now()
"""datetime: The current timestamp when the script is executed."""

# Type Annotations
str_20 = Annotated[str, mapped_column(Column(String(20)))]
"""Annotated[str]: A mapped column with a maximum length of 20 characters."""

str_50 = Annotated[str, mapped_column(Column(String(50)))]
"""Annotated[str]: A mapped column with a maximum length of 50 characters."""

str_100 = Annotated[Optional[str], mapped_column(Column(String(100)))]
"""Annotated[Optional[str]]: A mapped column with a maximum length of 
100 characters. This field can also be null.
"""

str_36 = Annotated[str, mapped_column(Column(String(36)))]
"""Annotated[str]: A mapped column with a maximum length of 36 characters."""

str_2000 = Annotated[float, mapped_column(Column(DECIMAL(11, 2)))]
"""Annotated[float]: A mapped column for a decimal value with a precision of 
11 digits and 2 digits after the decimal point.
"""

int_small = Annotated[SmallInteger, mapped_column(Column(SmallInteger))]
"""Annotated[SmallInteger]: A mapped column for a small integer value."""


# Base Classes
class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models.

    This class serves as the foundational base for all ORM models that
    interact with the database. It uses SQLAlchemy's `DeclarativeBase`
    as its parent class.
    """

    pass


class OnlineBase(DeclarativeBase):
    """Specialized base class for online-related SQLAlchemy ORM models.

    This class extends the functionality of `DeclarativeBase` for
    online-specific database tables and models. It can be used to
    distinguish between general-purpose and online-focused database
    models in a modular architecture.
    """

    pass


class CommonBase:
    """Common attributes for SQLAlchemy ORM models.

    This class provides a reusable set of common fields for database models.
    """

    id: Mapped[str_36] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime.datetime] = mapped_column(default=CURRENT_TIME)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=CURRENT_TIME, onupdate=CURRENT_TIME
    )
    created_by: Mapped[str_50] = mapped_column(default=CURRENT_USER)
    updated_by: Mapped[str_50] = mapped_column(default=CURRENT_USER)
    is_current: Mapped[bool] = mapped_column(default=True)
    valid_from: Mapped[datetime.datetime] = mapped_column(default=CURRENT_TIME)
    valid_to: Mapped[datetime.datetime] = mapped_column(default=DEFAULT_VALID_TO)
    row_source: Mapped[Optional[str_100]] = mapped_column(default=HOSTNAME)
    row_source_id: Mapped[Optional[str_36]] = mapped_column(nullable=True)


class BaseModel(Base, CommonBase):
    """Abstract base model for SQLAlchemy ORM models.

    Combines the functionality of `Base` and `CommonBase` to serve as a
    foundational class for all models in the database.
    """

    __abstract__ = True


class OnlineModel(OnlineBase, CommonBase):
    """Abstract base model for online-specific SQLAlchemy ORM models.

    Combines the functionality of `OnlineBase` and `CommonBase` to serve
    as a foundational class for online-focused database models.
    """

    __abstract__ = True
