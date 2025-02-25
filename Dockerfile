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

# Explain what entrypoint does

# ENTRYPOINT is used to specify the command that will run when the container starts
# You can't override the ENTRYPOINT command when running the container
# Unless you do so by specifying the --entrypoint flag when running the container
# docker run --entrypoint <command> <image_name> <arg1> <arg2> <arg3> ... <argN>
# You shouldn't do this unless you know what you're doing
ENTRYPOINT [ "uv", "run", "manager.py" ]

# CMD is used to specify the default arguments that will be passed to the ENTRYPOINT
# You can override the CMD arguments when running the container with 
# docker run <image_name> <arg1> <arg2> <arg3> ... <argN>
CMD ["--help"]

# In order to run the script with arguments use the following command
# docker run --rm --network db_network <image_name> <arg1> <arg2> <arg3> ... <argN>

# You can check connections to different databases by doing
# docker run -it --rm --network db_network <image_name> verify

