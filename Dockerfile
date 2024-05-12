FROM python:latest
WORKDIR /trppChess
COPY . .

RUN apt-get update && apt-get install -y libxrender-dev libx11-6 libxext-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && rm -rf /var/lib/apt/lists/*

RUN pip install pygame
ENV PYTHONPATH "${PYTHONPATH}:/"
#CMD ["python", "abc.py"]
CMD ["python", "main.py"]