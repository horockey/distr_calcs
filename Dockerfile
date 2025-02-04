FROM python:3.11-alpine
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "./src/app.py", "run", "--host", "0.0.0.0", "--port", "5000"]