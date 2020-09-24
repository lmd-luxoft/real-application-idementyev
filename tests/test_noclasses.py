import pytest
import server.utils as utils
from datetime import datetime, timezone
import re


@pytest.fixture
def filename_len():
    value = utils.filename_len
    yield value


@pytest.fixture()
def filename_alphanum():
    name = utils.generate_string()
    yield name


@pytest.fixture()
def date_format_zero():
    in_date = 0.0
    out_date = utils.convert_date(in_date)
    yield out_date


@pytest.fixture()
def date_format_now():
    out_date = utils.convert_date(datetime.now().timestamp())
    yield out_date


class TestUtils:
    def test_filename_len(self, filename_len, filename_alphanum):
        """Should be 8"""
        assert filename_len == 8 and len(filename_alphanum) == filename_len

    def test_filename_alphanum(self, filename_alphanum):
        """Should consist only of alpha and numeric"""
        assert re.match(r'^[\w\d]+$', filename_alphanum)

    def test_date_format_zero(self, date_format_zero):
        """Should return properly formatted string for 0-time"""
        assert date_format_zero == '1970-01-01 00:00:00'

    def test_date_format_now(self, date_format_now):
        """Should return properly formatted string for now in UTC"""
        _format = '%Y-%m-%d %H:%M:%S'
        _tz = timezone.utc
        assert date_format_now == datetime.now(tz=_tz).strftime(_format)
