# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=rentcar.py

# Run the command to start the app
CMD ["flask", "run", "--host", "0.0.0.0"]
