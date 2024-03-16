from src.video_to_frames.frame_rate_config import FrameRateConfig

class VideoConversionConfig:
    def __init__(self, rgb_metadata: dict, client_schema: dict, blanket_statuses: list, distance_measures: list, frame_rate_config: FrameRateConfig, root_path:str, user_drive: str, local_export_path: str, remote_export_path: str):
        self.rgb_metadata = rgb_metadata
        self.client_schema = client_schema
        self.blanket_statuses = blanket_statuses
        self.distance_measures = distance_measures
        self.frame_rate_config = frame_rate_config
        self.root_path = root_path
        self.user_drive = user_drive
        self.local_export_path = local_export_path
        self.remote_export_path = remote_export_path