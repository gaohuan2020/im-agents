import uuid


def create_meeting_card(title, date, time, attendees):
    meeting_id = "1234567890"
    card = {
        "config": {
            "update_multi": True
        },
        "card_link": {
            "url": ""
        },
        "i18n_elements": {
            "zh_cn": [{
                "tag": "markdown",
                "content": f"{title}",
                "text_align": "left",
                "text_size": "normal",
                "icon": {
                    "tag": "standard_icon",
                    "token": "submit-feedback_outlined",
                    "color": "grey"
                }
            }, {
                "tag": "markdown",
                "content":
                f"{date} {time} - {time.split(':')[0]}:{int(time.split(':')[1])+30:02d} (GMT+8)",
                "text_align": "left",
                "text_size": "normal",
                "icon": {
                    "tag": "standard_icon",
                    "token": "time_outlined",
                    "color": "grey"
                }
            }, {
                "tag": "person_list",
                "persons": attendees,
                "size": "small",
                "lines": 1,
                "show_avatar": True,
                "show_name": True,
                "icon": {
                    "tag": "standard_icon",
                    "token": "group_outlined",
                    "color": "grey"
                }
            }, {
                "tag":
                "action",
                "layout":
                "default",
                "actions": [{
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "编辑日程信息"
                    },
                    "type": "default",
                    "width": "default",
                    "size": "medium",
                    "value": {
                        "action_type": "edit_meeting",
                        "meeting_id": meeting_id
                    }
                }, {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "确认创建日程"
                    },
                    "type": "primary",
                    "width": "default",
                    "size": "medium",
                    "value": {
                        "action_type": "create_meeting",
                        "meeting_id": meeting_id,
                        "title": title,
                        "date": date,
                        "time": time,
                        "attendees": attendees
                    }
                }]
            }]
        },
        "i18n_header": {
            "zh_cn": {
                "title": {
                    "tag": "plain_text",
                    "content": "为您智能创建了一个会议日程，请确认："
                },
                "subtitle": {
                    "tag": "plain_text",
                    "content": ""
                },
                "template": "orange",
                "ud_icon": {
                    "tag": "standard_icon",
                    "token": "calendar_colorful"
                }
            }
        }
    }
    return card
