# 1. Start with an official Python blueprint
FROM python:3.11-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copy just the requirements file first (for faster building)
COPY requirements.txt .

# 4. Install the Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Flask app code into the container
COPY . .

# 6. Document that the container will listen on port 5000
EXPOSE 5000

# 7. The command to run your app when the container starts
CMD ["python", "app.py"]