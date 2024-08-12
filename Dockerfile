# Use an official Python runtime as a parent image
FROM --platform=linux/amd64  python:3.9.12-slim

# Set the working directory in the container
WORKDIR /app

# Explicitly copy the necessary files to save space
COPY requirements.txt /app/
COPY ./my_qa_model /app/my_qa_model
COPY all_chunks.pkl /app/
COPY embeddings.npy /app/
COPY legal_cases.index /app/
COPY inference.py /app/

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Install CPU-only version of PyTorch
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 8080

# # Run the Flask application
# CMD ["python", "inference.py"]

# Define environment variable
# ENV API_KEY your_api_key_here

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8080", "inference:app"]
