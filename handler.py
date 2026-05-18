import runpod

def handler(job):
    job_input = job["input"]

    return {
        "message": "working"
    }

runpod.serverless.start({"handler": handler})
