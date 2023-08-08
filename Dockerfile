FROM python:3.8 AS builder

# Set the working directory inside the container
WORKDIR /

# Copy the Python script and requirements file into the container
COPY . ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the compiled executable
CMD ["python", "tiniyvissv2.py"]
