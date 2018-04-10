# grab the latest version of Python
FROM python:latest
# create a temporary folder to hold installation
COPY . /brightcoin
WORKDIR /brightcoin
# install dependencies
RUN pip install -r requirements.txt
# run the app
CMD [ "python", "latest/api.py" ]