import os
import shutil
import np
import cv2

def move_png(log_file):
    with open(log_file, "r") as log_data:
        video_files = log_data.read().split("\n")

    for video in video_files:
        str_list = video.split("/")
        folder_name = "/".join(str_list[0:-1])
        video_filename = str_list[-1]
        output_folder = folder_name + "/" + "frames"

        if(video_filename.endswith("png")):
            print(f"moving {video_filename} to {output_folder}")

            if (not os.path.exists(output_folder)):
                os.makedirs(output_folder)

            try:
                shutil.move(video, output_folder)
            except Exception as e:
                print(f"{e}")
            
def create_corrupted_png(file_path):
    # Create a random numpy array (this will be treated as an image)
    image = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
    
    # Write the numpy array to a PNG file
    cv2.imwrite(file_path, image)
    
    # Now, let's manually corrupt the file by overwriting a part of it
    with open(file_path, "rb+") as file:
        file.seek(10)  # Move to an arbitrary position in the file
        file.write(b"corruption")  # Write some random data to corrupt the file