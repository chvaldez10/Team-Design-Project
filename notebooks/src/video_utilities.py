import cv2
import os

# reload for module caching
from importlib import reload
import src.id_utilities
reload(src.id_utilities)

# import custom functions
from src.id_utilities import get_alias

def create_video_from_png(png_folder: str, output_video_path: str, fps: int = 10):
    """
    Creates a video from a series of PNG images in a specified folder.

    Args:
    png_folder (str): Path to the folder containing PNG images.
    output_video_path (str): Path where the output video will be saved.
    fps (int, optional): Frames per second of the output video. Default is 10.

    Returns:
    None. Outputs a video file at the specified path.
    """
    try:
        png_files = sorted([f for f in os.listdir(png_folder) if f.endswith('.png')])
        if not png_files:
            print(f"No PNG files found in the folder '{png_folder}'.")
            return

        first_image = cv2.imread(os.path.join(png_folder, png_files[0]))
        if first_image is None:
            raise IOError(f"Failed to read the first image from '{png_folder}'.")

        height, width, _ = first_image.shape
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        with cv2.VideoWriter(output_video_path, fourcc, fps, (width, height)) as out:
            for png_file in png_files:
                img = cv2.imread(os.path.join(png_folder, png_file))
                if img is None:
                    raise IOError(f"Failed to read '{png_file}' from '{png_folder}'.")
                out.write(img)

        print(f"Video successfully created at '{output_video_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_video_properties(mp4_file: str) -> tuple:
    """
    Extracts properties from an MP4 video file.

    Args:
    mp4_file (str): The path to the MP4 file.

    Returns:
    tuple: A tuple containing the number of frames, frames per second (FPS),
           and the length of the video in seconds. Returns None if an error occurs.

    Raises:
    Exception: Any exception that occurs while processing the video file.
    """
    try:
        video = cv2.VideoCapture(mp4_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        number_of_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = number_of_frames / fps
        video.release()
        return number_of_frames, fps, length
    except Exception as e:
        print(f"{type(e).__name__} occurred while processing {mp4_file}: {e}")
        return None

def add_video_properties(metadata: dict, camera: str) -> dict:
    """
    Enhances patient metadata with video properties and alias based on camera type.

    Args:
    metadata (dict): A dictionary of patient metadata.
    camera (str): The type of camera used ('rgb' or 'thermal').

    Returns:
    dict: The enriched metadata with added video properties and aliases.
    """
    enriched_metadata = []

    for patient_id, patient_info in enumerate(metadata):
        try:
            video_path = patient_info.get("local path")
            if not video_path:
                raise ValueError(f"Missing 'local path' for patient ID {patient_info['ID']}")

            frames, fps, length_in_seconds = get_video_properties(video_path)
            alias = get_alias(patient_info, camera)

            patient_info.update({
                "frames": frames,
                "old fps": fps,
                "length": length_in_seconds,
                "alias": alias
            })

            enriched_metadata.append(patient_info)

        except Exception as e:
            print(f"Error processing patient ID {patient_info['ID']}: {e}")

    return enriched_metadata