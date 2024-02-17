from aiogram.types import User, Chat

TEST_USER = User(
    id=123, is_bot=False, first_name='user', last_name='test',
    username='test_user', language_code='ru-RU', is_premium=None,
    added_to_attachment_menu=None, can_join_groups=None,
    can_read_all_group_messages=None, supports_inline_queries=None
)

TEST_CHAT = Chat(
    id=321, type='private', title=None, username=TEST_USER.username,
    first_name=TEST_USER.first_name, last_name=TEST_USER.last_name,
    is_forum=None, photo=None, active_usernames=None, available_reactions=None,
    accent_color_id=None, background_custom_emoji_id=None,
    profile_accent_color_id=None, profile_background_custom_emoji_id=None,
    emoji_status_custom_emoji_id=None, emoji_status_expiration_date=None,
    bio=None, has_private_forwards=None,
    has_restricted_voice_and_video_messages=None, join_to_send_messages=None,
    join_by_request=None, description=None, invite_link=None,
    pinned_message=None, permissions=None, slow_mode_delay=None,
    message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None,
    has_hidden_members=None, has_protected_content=None,
    has_visible_history=None, sticker_set_name=None, can_set_sticker_set=None,
    linked_chat_id=None, location=None
)
