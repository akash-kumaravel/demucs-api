import runpod
import requests
import uuid
import subprocess
import os

def handler(job):

    job_input = job["input"]

    audio_url = job_input.get("audio_url")

    if not audio_url:
        return {
            "error": "audio_url missing"
        }

    filename = f"{uuid.uuid4()}.mp3"

    # Download audio file
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

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Check if Demucs failed
    if result.returncode != 0:
        return {
            "error": "Demucs processing failed"
        }

    # Build output folder path
    output_path = f"separated/htdemucs/{os.path.splitext(filename)[0]}"

    # Check if output exists
    if not os.path.exists(output_path):
        return {
            "error": "Output folder not found"
        }

    # List generated files
    files = os.listdir(output_path)

    return {
        "message": "Demucs completed successfully",
        "output_path": output_path,
        "files": files
    }

runpod.serverless.start({"handler": handler})
