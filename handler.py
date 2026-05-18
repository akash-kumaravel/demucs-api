import runpod

def handler(job):
    return {
        "message": "RunPod serverless working"
    }

runpod.serverless.start({"handler": handler})