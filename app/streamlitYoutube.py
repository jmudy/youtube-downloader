import streamlit as st
from pytubefix.cli import on_progress
from pytubefix import YouTube
import os
import re
from pathlib import Path
import platform

def get_youtube_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    pattern = r"(?:https?://)?(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w\-_]+)"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None

def get_thumbnail_url(video_id: str) -> str:
    """Returns the URL of the YouTube video thumbnail based on the video ID."""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def download_video(url: str, resolution: str, output_path: str) -> None:
    """Downloads a YouTube video with the specified resolution and saves it to the given output path."""
    yt = YouTube(url, on_progress_callback=on_progress)
    
    try:
        for stream in yt.streams.filter(adaptive=True, only_video=True):
            if stream.resolution == resolution:
                stream.download(output_path=output_path)
                return
        st.error(f"No video stream found with resolution {resolution}.")
    except Exception as e:
        st.error(f"Could not download video: {str(e)}")

def get_downloads_folder() -> Path:
    """Obtiene la ruta de la carpeta de Descargas según el sistema operativo."""
    system = platform.system()

    if system == "Windows":
        return Path(os.environ['USERPROFILE']) / "Downloads"
    elif system == "Darwin":  # macOS
        return Path.home() / "Downloads"
    elif system == "Linux":
        return Path.home() / "Downloads"
    else:
        raise NotImplementedError(f"El sistema operativo {system} no es compatible.")

def resolution_to_value(resolution: str) -> int:
    """Converts a resolution string to a numeric value for sorting."""
    if resolution.endswith('p'):
        return int(resolution[:-1])
    return 0

def main() -> None:
    """Main function for Streamlit app."""
    st.title("YouTube Video Downloader 🎥")
    
    url = st.text_input("Enter the YouTube video URL:")
    
    resolution_options = []
    if url:
        video_id = get_youtube_video_id(url)
        
        if video_id:
            yt = YouTube(url)
            # Use a set to avoid duplicates
            unique_resolutions = set()
            for stream in yt.streams.filter(adaptive=True, only_video=True):
                if stream.mime_type == 'video/mp4':
                    unique_resolutions.add(stream.resolution)
            
            # Convert the set to a sorted list by resolution value
            resolution_options = sorted(unique_resolutions, key=resolution_to_value, reverse=True)
            
            if resolution_options:
                thumbnail_url = get_thumbnail_url(video_id)
                st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)
            else:
                st.warning("No adaptative MP4 streams available for this video.")
        else:
            st.warning("Invalid YouTube URL.")
    
    # Dropdown for resolution selection
    resolution = st.selectbox("Select resolution:", resolution_options)
    
    # Display download button only if a resolution is selected
    if resolution:
        st.write(f"Selected resolution: {resolution}")
        output_path = get_downloads_folder()
        st.write(f"Videos will be saved to: `{output_path}`")

        if st.button("Download"):
            if url:
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
