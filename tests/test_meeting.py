# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for common properties of the message schemas."""

from meetbot_messages import MeetingCompleteV1, MeetingStartV1

MEETING_START = {
    "start_time": "2011-08-12T20:17:46+0000",
    "start_user": "dummy-user",
    "location": "#fedora-meeting:fedoraproject.org",
    "meeting_name": "epel",
}

MEETING_COMPLETE = {
    "start_time": "2023-08-12T20:17:46+0000",
    "start_user": "dummy-user",
    "end_time": "2023-08-12T20:45:59+0000",
    "end_user": "dudemcpants",
    "location": "#fedora-meeting:fedoraproject.org",
    "meeting_name": "epel",
    "url": (
        "https://meetbot-raw.test/fedora-meeting_matrix_fedoraproject-org/"
        "2023-08-12/epel.2023-08-12-20.17"
    ),
    "attendees": [
        {"name": "dummy-user", "lines_said": 23},
        {"name": "dudemcpants", "lines_said": 3},
        {"name": "stevebrown", "lines_said": 213},
    ],
    "logs": [
        {
            "log_type": "HTML Minutes",
            "log_url": (
                "https://meetbot-raw.test/fedora-meeting_matrix_fedoraproject-org/"
                "2023-08-12/epel.2023-08-12-20.17.html"
            ),
        },
        {
            "log_type": "HTML Full Log",
            "log_url": (
                "https://meetbot-raw.test/fedora-meeting_matrix_fedoraproject-org/"
                "2023-08-12/epel.2023-08-12-20.17.log.html"
            ),
        },
        {
            "log_type": "Text Minutes",
            "log_url": (
                "https://meetbot-raw.test/fedora-meeting_matrix_fedoraproject-org/"
                "2023-08-12/epel.2023-08-12-20.17.txt"
            ),
        },
        {
            "log_type": "Text Full Log",
            "log_url": (
                "https://meetbot-raw.test/fedora-meeting_matrix_fedoraproject-org/"
                "2023-08-12/epel.2023-08-12-20.17.log.txt"
            ),
        },
    ],
    "chairs": ["dummy-user", "dudemcpants", "joansmith"],
}


def test_meetbotMessage():
    """Assert meetbotMessage base class properties are correct"""
    message = MeetingStartV1(body=MEETING_START)

    assert message.app_name == "meetbot"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/meetbot.png"
    assert message.agent_name == "dummy-user"
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
    assert message.usernames == ["dummy-user"]
    assert message.url is None


def test_MeetingStartV1_test_str():
    expected_str = (
        "dummy-user started meeting 'epel' in #fedora-meeting:fedoraproject.org "
        "at 2011-08-12T20:17:46+0000"
    )
    message = MeetingStartV1(body=MEETING_START)
    message.validate()
    assert str(message) == expected_str


def test_MeetingStartV1_test_summary():
    expected_str = "Meeting 'epel' started in #fedora-meeting:fedoraproject.org"
    message = MeetingStartV1(body=MEETING_START)
    message.validate()
    assert message.summary == expected_str


def test_MeetingStartV1_test_agent_name():
    message = MeetingStartV1(body=MEETING_START)
    message.validate()
    assert message.agent_name == "dummy-user"


def test_MeetingStartV1_test_usernames():
    message = MeetingStartV1(body=MEETING_START)
    message.validate()
    assert message.usernames == ["dummy-user"]


def test_MeetingCompleteV1_test_str():
    expected_str = (
        "dudemcpants ended meeting 'epel' "
        "in #fedora-meeting:fedoraproject.org at 2023-08-12T20:45:59+0000\n"
        "\n"
        "# Attendees\n"
        "\n"
        "* dummy-user: 23 lines said\n"
        "* dudemcpants: 3 lines said\n"
        "* stevebrown: 213 lines said\n"
        "\n"
        "# Logs\n"
        "\n"
        "* [HTML Minutes](https://meetbot-raw.test/fedora-meeting_matrix_"
        "fedoraproject-org/2023-08-12/epel.2023-08-12-20.17.html)\n"
        "* [HTML Full Log](https://meetbot-raw.test/fedora-meeting_matrix_"
        "fedoraproject-org/2023-08-12/epel.2023-08-12-20.17.log.html)\n"
        "* [Text Minutes](https://meetbot-raw.test/fedora-meeting_matrix_"
        "fedoraproject-org/2023-08-12/epel.2023-08-12-20.17.txt)\n"
        "* [Text Full Log](https://meetbot-raw.test/fedora-meeting_matrix_"
        "fedoraproject-org/2023-08-12/epel.2023-08-12-20.17.log.txt)\n"
    )
    message = MeetingCompleteV1(body=MEETING_COMPLETE)
    message.validate()
    print(str(message))
    print(expected_str)
    assert str(message) == expected_str


def test_MeetingCompleteV1_test_summary():
    expected_str = "Meeting 'epel' in #fedora-meeting:fedoraproject.org finished"
    message = MeetingCompleteV1(body=MEETING_COMPLETE)
    message.validate()
    assert message.summary == expected_str


def test_MeetingCompleteV1_test_agent_name():
    message = MeetingCompleteV1(body=MEETING_COMPLETE)
    message.validate()
    assert message.agent_name == "dudemcpants"


def test_MeetingCompleteV1_test_usernames():
    message = MeetingCompleteV1(body=MEETING_COMPLETE)
    message.validate()
    assert message.usernames == ["dudemcpants", "dummy-user", "joansmith", "stevebrown"]
