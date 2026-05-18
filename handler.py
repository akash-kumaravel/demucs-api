import runpod
import requests
import uuid
import os
import subprocess

def handler(job):

    job_input = job["input"]

    audio_url = job_input.get("audio_url")

    if not audio_url:
        return {"error": "audio_url missing"}

    filename = f"{uuid.uuid4()}.mp3"

    # Download audio
    response = requests.get(audio_url)

    with open(filename, "wb") as f:
        f.write(response.content)

    # Run Demucs in CPU mode
    command = [
        "python",
        "-m",
        "demucs",
        "--device",
        "cpu",
        filename
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "error": result.stderr
        }

    return {
        "message": "Demucs completed successfully"
    }

runpod.serverless.start({"handler": handler})
