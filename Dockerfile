# Use the official Python image as the base
FROM python:3.13

# Install curl to fetch the uv installer
RUN apt-get update && apt-get install -y curl

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install the project itself
RUN uv sync

# Define the command to run the application
CMD ["uv", "run", "main.py"]

# In order to run the script with arguments use the following command
# docker run -it <image_name> <arg1> <arg2> <arg3> ... <argN>

