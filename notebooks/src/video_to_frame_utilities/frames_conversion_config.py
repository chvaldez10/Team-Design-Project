class FrameConversionConfig:
    def __init__(self, video_path: str, video_id: str, frame_frequency: dict, new_fps: int, crop_coordinates: list, debug_mode: bool):
        self.video_path = video_path
        self.video_id = video_id
        self.frame_frequency = frame_frequency
        self.new_fps = new_fps
        self.crop_coordinates = crop_coordinates
        self.debug_mode = debug_mode
