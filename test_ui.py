import gradio as gr
import requests

API_URL = "http://localhost:8000"  # Adjust if your FastAPI runs elsewhere

# ------------------------- Management Functions -------------------------

# --- Channels ---
def create_channel(display_name, username, password):
    data = {"display_name": display_name, "username": username, "password": password}
    res = requests.post(f"{API_URL}/management/channels/", json=data)
    return res.json()

def list_channels():
    res = requests.get(f"{API_URL}/management/channels/")
    return res.json()

def subscribe(channel_id, subscriber_id, subscription_type):
    data = {
        "subscriber_id": subscriber_id,
        "channel_id": channel_id,
        "subscription_type": subscription_type
    }
    res = requests.post(f"{API_URL}/management/channels/{channel_id}/subscribe", json=data)
    return res.json()

# --- Videos ---
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
    res = requests.post(f"{API_URL}/management/videos/", files=files, data=data)
    return res.json()

def list_videos(channel_id):
    res = requests.get(f"{API_URL}/management/videos/channel/{channel_id}")
    return res.json()

# --- Playlists ---
def create_playlist(channel_id, playlist_name):
    data = {"channel_id": channel_id, "playlist_name": playlist_name}
    res = requests.post(f"{API_URL}/management/playlists/", json=data)
    return res.json()

def list_playlists(channel_id):
    res = requests.get(f"{API_URL}/management/playlists/channel/{channel_id}")
    return res.json()

def add_video_to_playlist(playlist_id, video_id):
    data = {"playlist_id": playlist_id, "video_id": video_id}
    res = requests.post(f"{API_URL}/management/playlists/{playlist_id}/videos", json=data)
    return res.json()

def list_videos_in_playlist(playlist_id):
    res = requests.get(f"{API_URL}/management/playlists/{playlist_id}/videos")
    return res.json()

# --- Comments ---
def add_comment(video_id, channel_id, content, parent_comment_id=None):
    data = {
        "video_id": video_id,
        "channel_id": channel_id,
        "content": content,
        "parent_comment_id": parent_comment_id
    }
    res = requests.post(f"{API_URL}/management/comments/", json=data)
    return res.json()

def list_comments(video_id):
    res = requests.get(f"{API_URL}/management/comments/video/{video_id}")
    return res.json()

# --- History ---
def add_history(channel_id, video_id):
    data = {"channel_id": channel_id, "video_id": video_id}
    res = requests.post(f"{API_URL}/management/history/", json=data)
    return res.json()

def list_history(channel_id):
    res = requests.get(f"{API_URL}/management/history/channel/{channel_id}")
    return res.json()

def search_videos(query):
    if not query:
        return {"error": "Empty search query"}
    try:
        res = requests.get(f"{API_URL}/management/search/videos", params={"q": query})
        return res.json()
    except Exception as e:
        return {"error": str(e)}
# ------------------------- Gradio UI -------------------------
with gr.Blocks() as app:
    gr.Markdown("## Video Platform Management UI")


    


    # --- Channels ---
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

        gr.Markdown("### Subscribe to Channel")
        channel_id_sub = gr.Number(label="Channel ID")
        subscriber_id = gr.Number(label="Subscriber ID")
        sub_type = gr.Dropdown(["all notif", "no notif"], label="Subscription Type")
        sub_btn = gr.Button("Subscribe")
        sub_out = gr.JSON()
        sub_btn.click(subscribe, [channel_id_sub, subscriber_id, sub_type], sub_out)

    # --- Videos ---
    with gr.Tab("Videos"):
        gr.Markdown("### Upload Video")
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

        gr.Markdown("### List Videos")
        list_vid_channel_id = gr.Number(label="Channel ID")
        list_vid_btn = gr.Button("List Videos")
        list_vid_out = gr.JSON()
        list_vid_btn.click(list_videos, [list_vid_channel_id], list_vid_out)

    # --- Playlists ---
    with gr.Tab("Playlists"):
        p_channel_id = gr.Number(label="Channel ID")
        p_name = gr.Textbox(label="Playlist Name")
        p_create_btn = gr.Button("Create Playlist")
        p_create_out = gr.JSON()
        p_create_btn.click(create_playlist, [p_channel_id, p_name], p_create_out)

        p_list_btn = gr.Button("List Playlists")
        p_list_out_channel_id = gr.Number(label="Channel ID")
        p_list_out = gr.JSON()
        p_list_btn.click(list_playlists, [p_list_out_channel_id], p_list_out)

        pv_playlist_id = gr.Number(label="Playlist ID")
        pv_video_id = gr.Number(label="Video ID")
        pv_add_btn = gr.Button("Add Video to Playlist")
        pv_add_out = gr.JSON()
        pv_add_btn.click(add_video_to_playlist, [pv_playlist_id, pv_video_id], pv_add_out)

        pv_list_playlist_id = gr.Number(label="Playlist ID")
        pv_list_btn = gr.Button("List Videos in Playlist")
        pv_list_out = gr.JSON()
        pv_list_btn.click(list_videos_in_playlist, [pv_list_playlist_id], pv_list_out)

    # --- Comments ---
    with gr.Tab("Comments"):
        c_video_id = gr.Number(label="Video ID")
        c_channel_id = gr.Number(label="Channel ID")
        c_content = gr.Textbox(label="Comment Content")
        c_add_btn = gr.Button("Add Comment")
        c_add_out = gr.JSON()
        c_add_btn.click(add_comment, [c_video_id, c_channel_id, c_content], c_add_out)

        c_list_video_id = gr.Number(label="Video ID")
        c_list_btn = gr.Button("List Comments")
        c_list_out = gr.JSON()
        c_list_btn.click(list_comments, [c_list_video_id], c_list_out)

    # --- History ---
    with gr.Tab("History"):
        h_channel_id = gr.Number(label="Channel ID")
        h_video_id = gr.Number(label="Video ID")
        h_add_btn = gr.Button("Add History")
        h_add_out = gr.JSON()
        h_add_btn.click(add_history, [h_channel_id, h_video_id], h_add_out)

        h_list_channel_id = gr.Number(label="Channel ID")
        h_list_btn = gr.Button("List History")
        h_list_out = gr.JSON()
        h_list_btn.click(list_history, [h_list_channel_id], h_list_out)

    with gr.Tab("Search Videos"):
        gr.Markdown("### Search Videos")
        search_query = gr.Textbox(label="Search Query")
        search_btn = gr.Button("Search")
        search_out = gr.JSON()
        search_btn.click(search_videos, search_query, search_out)


app.launch()
