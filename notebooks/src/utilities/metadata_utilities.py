def calculate_video_duration(video_fps: int, frame_count: int) -> int:
    """
        Get the video duration from fps and frame_count.
    """
    return frame_count // video_fps