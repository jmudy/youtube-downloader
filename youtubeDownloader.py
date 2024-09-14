from pytubefix.cli import on_progress
from pytubefix import YouTube
import os


def download_video(url: str, resolution: str, output_path: str) -> None:
    """
    Downloads a YouTube video with the specified resolution and saves it to the given output path.

    Args:
        url (str): The URL of the YouTube video to download.
        resolution (str): The resolution of the video stream to download (e.g., '1080p').
        output_path (str): The directory path where the downloaded video will be saved.

    Raises:
        Exception: If the video cannot be downloaded, prints an error message.
    """
    yt = YouTube(url, on_progress_callback=on_progress)

    try:  
        for idx, stream in enumerate(yt.streams):
            if stream.resolution == resolution:
                break    
        yt.streams[idx].download(output_path=output_path)
    except Exception as e:
        print(f"Could not download video: {str(e)}")


def main() -> None:
    """
    Main function to prompt the user for a YouTube URL, set up the output path,
    and initiate the video download process.
    """
    url = input("Enter the URL of the YouTube video: ")

    # Get the path to the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_directory, "downloads")  # "downloads" directory
    resolution = "1080p"

    print(f"The project directory is: {project_directory}")
    print(f"The files will be saved in: {output_path}")

    download_video(url, resolution, output_path)


if __name__ == "__main__":
    main()
