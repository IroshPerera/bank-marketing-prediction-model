# Use a lightweight Python image
FROM python:3.10-slim
# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy model files into the container
COPY model/ model/

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on (port 80)
EXPOSE 80

# Run the Flask app
ENTRYPOINT ["python3", "app.py"]
