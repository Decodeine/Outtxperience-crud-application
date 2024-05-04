# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install necessary utilities and libraries
# Install necessary utilities and libraries
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat
# Add these lines before pip install
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]