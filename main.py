import ffmpeg
import hashlib
import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = "uploads"
os.makedirs(BASE_DIR, exist_ok=True)


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

    # ---- Step 3: Segment into HLS ----
    m3u8_path = os.path.join(folder_path, "master.m3u8")
    segment_pattern = os.path.join(folder_path, "seg_%03d.ts")

    try:
        (
            ffmpeg
            .input(raw_path)
            .output(
                m3u8_path,
                format="hls",
                hls_time=4,
                hls_playlist_type="vod",
                hls_segment_filename=segment_pattern,
                vcodec="libx264",
                acodec="aac"
            )
            .run(overwrite_output=True)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ffmpeg error: {str(e)}")

    return {
        "message": "Video uploaded and segmented",
        "id": folder_name,
        "manifest_url": f"/videos/{folder_name}/manifest",
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
@app.get("/videos/{video_id}/manifest")
def get_manifest(video_id: str):
    m3u8_path = os.path.join(BASE_DIR, video_id, "master.m3u8")

    if not os.path.exists(m3u8_path):
        raise HTTPException(status_code=404, detail="Manifest not found")

    with open(m3u8_path, "r") as f:
        return f.read()

@app.get("/videos/{video_id}/{segment_name}")
def get_segment(video_id: str, segment_name: str):
    file_path = os.path.join(BASE_DIR, video_id, segment_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Segment not found")

    # Return the file exactly as bytes (correct for .m3u8 and .ts)
    return FileResponse(file_path)



# =============================================
#      LIST ALL VIDEOS (Folders in uploads)
# =============================================
@app.get("/videos")
def list_videos():
    videos = os.listdir(BASE_DIR)
    return {
        "count": len(videos),
        "videos": videos
    }


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
