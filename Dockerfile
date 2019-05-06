FROM python:3.6

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
RUN chmod 644 app.py
CMD ["app.py"]