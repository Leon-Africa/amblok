# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9092 available to the world outside this container
EXPOSE 9092

# Run the Kafka producer script
CMD ["python", "kafka_producer_alchemy.py"]