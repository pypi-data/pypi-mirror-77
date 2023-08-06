import logging
from datetime import datetime, time, date
from typing import Optional, Any
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
import pytz
from django.utils.dateparse import parse_datetime as django_parse_datetime
from django.utils.dateparse import parse_date as django_parse_date

logger = logging.getLogger(__name__)

TRUE_VALUES = (
    'true',
    '1',
    'yes',
)

FALSE_VALUES = (
    'none',
    'null',
    'false',
    '0',
    'no',
)


def parse_bool(v, default: Optional[bool] = None, exceptions: bool = True) -> Optional[bool]:
    """
    Parses boolean value
    :param v: Input string
    :param default: Default value if exceptions=False
    :param exceptions: Raise exception on error or not
    :return: bool
    """
    if not exceptions:
        logger.warning('jutil.parse.parse_bool(..., exceptions=False) is deprecated, use parse_bool_or_none')
    if isinstance(v, bool):
        return v
    s = str(v).lower()
    if s in TRUE_VALUES:
        return True
    if s in FALSE_VALUES:
        return False
    if exceptions:
        msg = _("%(value)s is not one of the available choices") % {'value': v}
        raise ValidationError(msg)
    return default


def parse_datetime(v: str, default: Optional[datetime] = None, tz: Any = None, exceptions: bool = True) -> Optional[datetime]:
    """
    Parses ISO date/datetime string to timezone-aware datetime.
    Supports YYYY-MM-DD date strings where time part is missing.
    Returns always timezone-aware datetime (assumes UTC if timezone missing).
    :param v: Input string to parse
    :param default: Default value to return if exceptions=False
    :param tz: Default pytz timezone or if None then use UTC as default
    :param exceptions: Raise exception on error or not
    :return: datetime with timezone
    """
    if not exceptions:
        logger.warning('jutil.parse.parse_datetime(..., exceptions=False) is deprecated, use parse_datetime_or_none')
    try:
        t = django_parse_datetime(v)
        if t is None:
            t_date: Optional[date] = django_parse_date(v)
            if t_date is None:
                raise ValidationError(_(
                    "“%(value)s” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.") % {
                                          'value': v})
            t = datetime.combine(t_date, time())
        if tz is None:
            tz = pytz.utc
        return t if t.tzinfo else tz.localize(t)
    except Exception:
        if exceptions:
            raise ValidationError(_("“%(value)s” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.") % {'value': v})
        return default


def parse_bool_or_none(v: str) -> Optional[bool]:
    """
    Parses boolean value, or returns None if parsing fails.
    :param v: Input string
    :return: bool or None
    """
    if isinstance(v, bool):
        return v
    s = str(v).lower()
    if s in TRUE_VALUES:
        return True
    if s in FALSE_VALUES:
        return False
    return None


def parse_datetime_or_none(v: str, tz: Any = None) -> Optional[datetime]:
    """
    Parses ISO date/datetime string to timezone-aware datetime.
    Supports YYYY-MM-DD date strings where time part is missing.
    Returns timezone-aware datetime (assumes UTC if timezone missing) or None if parsing fails.
    :param v: Input string to parse
    :param tz: Default pytz timezone or if None then use UTC as default
    :return: datetime with timezone or None
    """
    try:
        t = django_parse_datetime(v)
        if t is None:
            t_date: Optional[date] = django_parse_date(v)
            if t_date is None:
                return None
            t = datetime.combine(t_date, time())
        if tz is None:
            tz = pytz.utc
        return t if t.tzinfo else tz.localize(t)
    except Exception:
        return None
