class FrameConversionConfig:
    def __init__(self, rooth_path:str, local_video_path: str, video_id: str, frame_frequency: dict, new_fps: int, crop_coordinates: list, debug_mode: bool):
        self.root_path = rooth_path
        self.local_video_path = local_video_path
        self.video_id = video_id
        self.frame_frequency = frame_frequency
        self.new_fps = new_fps
        self.crop_coordinates = crop_coordinates
        self.debug_mode = debug_mode