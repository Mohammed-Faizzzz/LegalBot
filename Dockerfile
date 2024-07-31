# Use an official Python runtime as a parent image
FROM python:3.9.12-slim

# Set the working directory in the container
# WORKDIR /retrieval_mech

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5001

# Run the Flask application
CMD ["python", "inference.py"]
