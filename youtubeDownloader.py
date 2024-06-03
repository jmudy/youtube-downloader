from pytube import YouTube
import os


def download_video(url, output_path):
    try:
        yt = YouTube(url)
        print(f"Downloading video: {yt.title}...")
        yt.streams.get_highest_resolution().download(output_path=output_path)
        print(f"{yt.title} downloaded successfully!")
    except Exception as e:
        print(f"Could not download video: {str(e)}")


def main():
    url = input("Enter the URL of the YouTube video: ")

    # Get the path to the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_directory, "downloads") # "downloads" directory

    print(f"The project directory is: {project_directory}")
    print(f"The files will be saved in: {output_path}")

    download_video(url, output_path)


if __name__ == "__main__":
    main()