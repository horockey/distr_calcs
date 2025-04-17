FROM ubuntu:22.04
COPY . .
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python3", "-m", "flask", "--app", "./src/app.py", "run", "--host", "0.0.0.0", "--port", "5000"]