import runpod

def handler(job):
    return {"message": "hello"}

runpod.serverless.start({"handler": handler})
