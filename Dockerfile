# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7.4

# Install pip requirements

RUN apt-get update && apt-get --assume-yes install libomp-dev 
COPY requirements.txt .
RUN python -m pip install  --no-cache-dir  -r requirements.txt
RUN python -m nltk.downloader punkt

# port where the Django app runs  
EXPOSE 5000  

COPY . .
WORKDIR "/webapp"

CMD ["python", "start_api.py", "-t", "True"]
