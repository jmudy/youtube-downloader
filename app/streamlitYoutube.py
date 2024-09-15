import streamlit as st
from pytubefix.cli import on_progress
from pytubefix import YouTube
import os
import re
from pathlib import Path
import platform

def get_youtube_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    
    Args:
        url (str): The full URL of the YouTube video.
    
    Returns:
        str: The video ID extracted from the URL.
    """
    # Regular expression to extract video ID
    pattern = r"(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]+)"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None

def get_thumbnail_url(video_id: str) -> str:
    """
    Returns the URL of the YouTube video thumbnail based on the video ID.
    
    Args:
        video_id (str): The ID of the YouTube video.
    
    Returns:
        str: The URL of the thumbnail image.
    """
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

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
        st.error(f"Could not download video: {str(e)}")

def get_downloads_folder() -> Path:
    """
    Obtiene la ruta de la carpeta de Descargas según el sistema operativo.
    
    Returns:
        Path: La ruta de la carpeta de descargas.
    """
    system = platform.system()

    if system == "Windows":
        return Path(os.environ['USERPROFILE']) / "Downloads"
    elif system == "Darwin":  # macOS
        return Path.home() / "Downloads"
    elif system == "Linux":
        return Path.home() / "Downloads"
    else:
        raise NotImplementedError(f"El sistema operativo {system} no es compatible.")

def main() -> None:
    """
    Main function for Streamlit app. Prompts the user for a YouTube URL, sets up the output path,
    and initiates the video download process.
    """
    st.title("YouTube Video Downloader 🎥")
    
    # Input fields for URL and resolution
    url = st.text_input("Enter the YouTube video URL:")
    resolution = st.selectbox("Select resolution:", ["720p", "1080p", "1440p", "2160p"])
    
    if url:
        # Get YouTube video ID and thumbnail URL
        video_id = get_youtube_video_id(url)
        
        if video_id:
            thumbnail_url = get_thumbnail_url(video_id)
            st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)
        else:
            st.warning("Invalid YouTube URL.")
    
    # Get download folder path
    output_path = get_downloads_folder()
    
    st.write(f"Videos will be saved to: `{output_path}`")

    # Button to trigger download
    if st.button("Download"):
        if url:
            # Ensure the download directory exists
            if not output_path.exists():
                output_path.mkdir(parents=True)
                
            with st.spinner("Downloading video..."):
                try:
                    download_video(url, resolution, str(output_path))
                    st.success(f"Video downloaded successfully in `{output_path}`")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
