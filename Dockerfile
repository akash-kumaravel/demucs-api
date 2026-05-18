FROM runpod/pytorch:3.10-2.0.1-120-devel

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "handler.py"]