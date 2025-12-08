import ffmpeg
import hashlib
import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()




BASE_DIR = "uploads"
os.makedirs(BASE_DIR, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges"],
)


def random_hash_name(original_name: str) -> str:
    """Generate a random hash based on time + filename."""
    h = hashlib.sha256()
    h.update(f"{time.time()}_{original_name}".encode())
    return h.hexdigest()[:32]  # 32 chars


@app.get("/")
def read_root():
    return {"Hello": "World"}


# =============================================
#               UPLOAD (PUT)
# =============================================
@app.put("/videos")
async def upload_video(file: UploadFile = File(...)):

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")

    # ---- Step 1: Make folder ----
    folder_name = random_hash_name(file.filename)
    folder_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # ---- Step 2: Save raw uploaded file ----
    raw_name = random_hash_name(file.filename) + ".bin"
    raw_path = os.path.join(folder_path, raw_name)

    with open(raw_path, "wb") as f:
        f.write(await file.read())

    # ---- Step 3: Thumbnail ----
    thumb_path = os.path.join(folder_path, "thumbnail.jpg")
    ffmpeg.input(raw_path, ss=0).output(thumb_path, vframes=1).run(overwrite_output=True)

    # ---- Step 4: Multi-resolution settings ----
    renditions = [
        ("1080p", "1920x1080", "5000k", "6000k"),
        ("720p",  "1280x720",  "3000k", "4000k"),
        ("480p",  "854x480",   "1500k", "2000k"),
        ("360p",  "640x360",   "800k",  "1200k"),
        ("240p",  "426x240",   "400k",  "600k"),
    ]

    # ---- Step 5: Create HLS playlists for each resolution ----
    master_playlist_path = os.path.join(folder_path, "master.m3u8")

    with open(master_playlist_path, "w") as master:
        master.write("#EXTM3U\n")

        for name, resolution, bitrate, maxrate in renditions:
            playlist = f"{name}.m3u8"
            playlist_path = os.path.join(folder_path, playlist)
            segment_pattern = os.path.join(folder_path, f"{name}_%03d.ts")

            (
                ffmpeg
                .input(raw_path)
                .output(
                    playlist_path,
                    format="hls",
                    hls_time=4,
                    hls_playlist_type="vod",
                    hls_segment_filename=segment_pattern,
                    vf=f"scale={resolution}",
                    acodec="aac",
                    vcodec="libx264",
                    video_bitrate=bitrate,
                    maxrate=maxrate,
                    bufsize="2000k"
                )
                .run(overwrite_output=True)
            )

            # Add to master playlist
            master.write(
                f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate.replace('k','000')},RESOLUTION={resolution}\n"
                f"{playlist}\n"
            )

    return {
        "message": "Video uploaded and processed (multi-resolution HLS)",
        "id": folder_name,
        "manifest_url": f"/videos/{folder_name}/manifest",
        "thumbnail_url": f"/videos/{folder_name}/thumbnail",
        "remove_url": f"/videos/{folder_name}"
    }


# =============================================
#               GET 1 VIDEO INFO
# =============================================
@app.get("/videos/{video_id}")
def get_video_info(video_id: str):
    folder_path = os.path.join(BASE_DIR, video_id)

    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Video not found")

    files = os.listdir(folder_path)

    return {
        "id": video_id,
        "manifest": "/videos/{}/manifest".format(video_id),
        "files": files
    }


# =============================================
#           GET MANIFEST (HLS .m3u8)
# =============================================
@app.get("/videos/{video_id}/master.m3u8")
def get_manifest(video_id: str):
    path = os.path.join(BASE_DIR, video_id, "master.m3u8")
    with open(path) as f:
        data = f.read()
    return Response(data, media_type="application/vnd.apple.mpegurl")




@app.get("/videos/{video_id}/{segment_name}")
def get_segment(video_id: str, segment_name: str):
    file_path = os.path.join(BASE_DIR, video_id, segment_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Segment not found")

    # Return the file exactly as bytes (correct for .m3u8 and .ts)
    return FileResponse(file_path)


@app.get("/thumbnails/{folder}")
def get_thumbnail(folder: str):
    path = os.path.join(BASE_DIR, folder, "thumbnail.jpg")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(path, media_type="image/jpeg")



# =============================================
#               DELETE VIDEO
# =============================================
@app.delete("/videos/{video_id}")
def delete_video(video_id: str):
    folder_path = os.path.join(BASE_DIR, video_id)

    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Video not found")

    shutil.rmtree(folder_path)

    return {
        "message": "Video deleted successfully",
        "id": video_id
    }
