import runpod
import subprocess
import uuid
import os

def handler(job):

    job_input = job["input"]

    audio_url = job_input.get("audio_url")

    if not audio_url:
        return {"error": "audio_url missing"}

    filename = f"{uuid.uuid4()}.mp3"

    subprocess.run(
        ["wget", audio_url, "-O", filename],
        check=True
    )

    subprocess.run(
        ["demucs", filename],
        check=True
    )

    return {
        "message": "separation completed"
    }

runpod.serverless.start({"handler": handler})
