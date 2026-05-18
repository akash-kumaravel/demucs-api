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
                "message": "audio_url missing"
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

        # Output folder
        output_path = f"separated/htdemucs/{os.path.splitext(filename)[0]}"

        # Check output exists
        if not os.path.exists(output_path):
            return {
                "message": "Demucs failed",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        files = os.listdir(output_path)

        return {
            "message": "Demucs completed successfully",
            "output_path": output_path,
            "files": files,
            "stdout": result.stdout
        }

    except Exception as e:
        return {
            "message": "Exception occurred",
            "details": str(e)
        }

runpod.serverless.start({"handler": handler})
