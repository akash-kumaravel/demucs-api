FROM runpod/pytorch:3.10-2.0.1-120-devel

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg wget

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "handler.py"]
