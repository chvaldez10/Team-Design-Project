class FrameConversionConfig:
    def __init__(self, root_path: str, export_path: str, local_video_path: str, video_id: str, frame_frequency: dict, video_duration: int, old_fps: int, new_fps: int, crop_coordinates: list, debug_mode: bool, frame_limit: int):
        self.root_path = root_path
        self.export_path = export_path
        self.local_video_path = local_video_path
        self.video_id = video_id
        self.frame_frequency = frame_frequency
        self.video_duration = video_duration
        self.old_fps = old_fps
        self.new_fps = new_fps
        self.crop_coordinates = crop_coordinates
        self.debug_mode = debug_mode
        self.frame_limit = frame_limit

    def __str__(self):
        attrs = vars(self)
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in attrs.items())
        return f"{self.__class__.__name__}({attrs_str})"