class FrameConversionConfig:
    def __init__(self, rooth_path:str, local_video_path: str, video_id: str, frame_frequency: dict, video_duration: int, new_fps: int, crop_coordinates: list, debug_mode: bool):
        self.root_path = rooth_path
        self.local_video_path = local_video_path
        self.video_id = video_id
        self.frame_frequency = frame_frequency
        self.video_duration = video_duration
        self.new_fps = new_fps
        self.crop_coordinates = crop_coordinates
        self.debug_mode = debug_mode

    def __str__(self):
        return f"FrameConversionConfig(root_path={self.root_path}, local_video_path={self.local_video_path}, video_id={self.video_id}, frame_frequency={self.frame_frequency}, new_fps={self.new_fps}, crop_coordinates={self.crop_coordinates}, debug_mode={self.debug_mode})"