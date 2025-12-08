import gradio as gr
import requests

API_URL = "http://localhost:8000/videos"   # URL backend FastAPI của bạn

def upload_to_backend(video_file):
    if video_file is None:
        return "No file uploaded"

    with open(video_file, "rb") as f:
        files = {
            "file": (video_file, f, "video/mp4")
        }
        response = requests.put(API_URL, files=files)

    try:
        return response.json()
    except:
        return f"Server error: {response.text}"


ui = gr.Interface(
    fn=upload_to_backend,
    inputs=gr.Video(label="Upload Video to Test Backend"),
    outputs="json",
    title="Backend Video Upload Tester",
    description=(
        "Upload a real video file. "
        "This will send it directly to your FastAPI /videos endpoint "
        "and return the backend response."
    )
)

ui.launch()
