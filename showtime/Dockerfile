FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
EXPOSE 3002
CMD ["python","-u","showtime.py","docker"]
