import cv2
import os

def create_video_from_png(png_folder:str, output_video_path:str, fps:int=10):
    png_files = [filename for filename in os.listdir(png_folder) if filename.endswith(".png")]
    
    if not png_files:
        print(f"No PNG files found in the folder '{png_folder}'.")
        return

    png_files.sort()

    first_image = cv2.imread(os.path.join(png_folder, png_files[0]))
    height, width, _ = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for png_file in png_files:
        img_path = os.path.join(png_folder, png_file)
        img = cv2.imread(img_path)
        out.write(img)

    out.release()
    cv2.destroyAllWindows()
    
    print(f"Video successfully created at '{output_video_path}'.")