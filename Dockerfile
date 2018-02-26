# grab the latest version of Python
FROM python:latest
# create a temporary folder to hold installation
COPY . /app
WORKDIR /app
# install dependencies
RUN pip install -r require.txt
# expose port 8080
EXPOSE 8080
# run the app
CMD [ "python", "v6/api.py" ]