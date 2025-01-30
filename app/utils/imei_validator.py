def validate_imei(imei: str) -> bool:
    if not imei.isdigit() or len(imei) != 15:
        return False
    return True