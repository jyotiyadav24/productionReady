# Define the base image that you are going to be using
FROM python:3.11

# Open the port for the clients to connect into it
EXPOSE 8000

# Define a directory to work inside of docker
WORKDIR /code/

# Copy the requirements.txt file into the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Copy the contents of the copywritingAgent directory into the container at /code/copywritingAgent
COPY ./copywritingAgent /code/copywritingAgent

# Install the libraries
RUN pip install --no-cache-dir -r /code/requirements.txt

# Tell docker/kubernetes which command should it execute in order to run your agent
CMD ["uvicorn", "copywritingAgent.main:app", "--host", "0.0.0.0", "--port", "8000"]
