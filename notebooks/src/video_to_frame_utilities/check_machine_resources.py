import psutil

class NotEnoughFreeSpace(Exception):
    """Exception raised when there is not enough free space on the drive."""
    pass

# It's good practice to define constants like this at the module level.
MINIMUM_FREE_SPACE_GB = 75

def get_drive_storage(user_drive: str) -> dict:
    """
    Retrieves the storage information for a given drive on macOS.
    """
    try:
        # For macOS, user_drive would be a path like "/Volumes/MyDrive" or simply "/"
        drive_usage = psutil.disk_usage(user_drive)
        return {
            'path': user_drive,
            'total_space_GB': drive_usage.total / (1024**3),
            'used_space_GB': drive_usage.used / (1024**3),
            'free_space_GB': drive_usage.free / (1024**3),
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"Path {user_drive} not found.")

def check_drive_usage(user_drive: str):
    """
    Checks if the free space on the drive is above a minimum threshold.
    """
    drive_info = get_drive_storage(user_drive)

    if drive_info["free_space_GB"] < MINIMUM_FREE_SPACE_GB:
        raise NotEnoughFreeSpace(f"Not enough free space on Drive {user_drive}. Minimum {MINIMUM_FREE_SPACE_GB} GB required.")