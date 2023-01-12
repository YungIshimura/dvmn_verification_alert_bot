FROM python:3.8
WORKDIR /home
COPY requirements.txt /home/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY main.py .
CMD [ "python3", "main.py" ]