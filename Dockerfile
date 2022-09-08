FROM python:3.9.12
WORKDIR /app
COPY requirements.txt req.txt
RUN pip3 install -r req.txt
COPY . .
EXPOSE 587/tcp
CMD ["python3", "app.py"]