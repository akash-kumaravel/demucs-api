import runpod
import requests
import uuid
import subprocess
import os

def handler(job):

    try:

        job_input = job["input"]

        audio_url = job_input.get("audio_url")

        if not audio_url:
            return {
                "error": "audio_url missing"
            }

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

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        # If failed
        if result.returncode != 0:
            return {
                "error": result.stderr,
                "stdout": result.stdout
            }

        # Output folder
        output_path = f"separated/htdemucs/{os.path.splitext(filename)[0]}"

        # Verify output exists
        if not os.path.exists(output_path):
            return {
                "error": "Output folder not found"
            }

        files = os.listdir(output_path)

        return {
            "message": "Demucs completed successfully",
            "output_path": output_path,
            "files": files
        }

    except Exception as e:
        return {
            "error": str(e)
        }

runpod.serverless.start({"handler": handler})
