import gradio as gr
import requests

API_URL = "http://localhost:8000"  # Adjust if your FastAPI runs elsewhere

# ------------------------- Management Functions -------------------------
def upload_video_management(channel_id, title, description, category, privacy, file):
    if file is None:
        return {"error": "No file selected"}

    files = {"file": (file.name, open(file.name, "rb"), "video/mp4")}
    data = {
        "channel_id": channel_id,
        "title": title,
        "description": description,
        "category": category,
        "privacy": privacy
    }

    try:
        res = requests.post(f"{API_URL}/management/videos/", files=files, data=data)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def list_channels():
    res = requests.get(f"{API_URL}/management/channels/")
    return res.json()

def create_channel(display_name, username, password):
    data = {"display_name": display_name, "username": username, "password": password}
    res = requests.post(f"{API_URL}/management/channels/", json=data)
    return res.json()

# ------------------------- Gradio UI -------------------------
with gr.Blocks() as app:
    gr.Markdown("## Video Platform Management UI")

    # ---------------- Channels ----------------
    with gr.Tab("Channels"):
        gr.Markdown("### Create Channel")
        display_name = gr.Textbox(label="Display Name")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password")
        create_channel_btn = gr.Button("Create Channel")
        channel_out = gr.JSON()
        create_channel_btn.click(create_channel, [display_name, username, password], channel_out)

        gr.Markdown("### List Channels")
        list_channels_btn = gr.Button("List Channels")
        list_channels_out = gr.JSON()
        list_channels_btn.click(list_channels, [], list_channels_out)

    # ---------------- Video Upload ----------------
    with gr.Tab("Upload Video"):
        gr.Markdown("### Upload Video with Metadata")
        v_channel_id = gr.Number(label="Channel ID")
        v_title = gr.Textbox(label="Title")
        v_desc = gr.Textbox(label="Description")
        v_cat = gr.Textbox(label="Category")
        v_privacy = gr.Dropdown(["public", "private", "limited"], label="Privacy")
        video_file = gr.File(label="Select Video", file_types=[".mp4", ".mov", ".avi"])
        upload_btn = gr.Button("Upload Video")
        upload_output = gr.JSON()
        upload_btn.click(upload_video_management,
                         [v_channel_id, v_title, v_desc, v_cat, v_privacy, video_file],
                         upload_output)

app.launch()
