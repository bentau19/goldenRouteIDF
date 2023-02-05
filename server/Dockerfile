#FROM python:3.8.5
#
#WORKDIR /server
#COPY . .
#
#RUN pip install -r requirements.txt
#
#ENTRYPOINT ["python"]
#CMD py server.py


FROM python:3.8.5
WORKDIR /server
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["server.py"]

