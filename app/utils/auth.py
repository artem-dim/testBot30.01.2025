def is_user_allowed(user_id: int, allowed_users: set) -> bool:
    return user_id in allowed_users