import runpod
import requests
import uuid
import subprocess
import os

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

    # Run Demucs
    command = [
        "python",
        "-m",
        "demucs",
        "--device",
        "cpu",
        filename
    ]

    subprocess.run(command)

    # Output folder
    output_folder = "separated/htdemucs"

    return {
        "message": "Demucs completed successfully",
        "output_folder": output_folder
    }

runpod.serverless.start({"handler": handler})
