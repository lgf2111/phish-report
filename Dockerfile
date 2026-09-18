# Runs the app in Docker so it works the same on everyone's laptop.
FROM python:3.12-slim

WORKDIR /app

# install the requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the code in
COPY . .

# run the app by default. pass your key like:
#   docker run --rm -it -e GROQ_API_KEY=xxx phishreport
# to run the tests instead:  docker run --rm phishreport pytest
CMD ["python", "app/main.py"]
