FROM python:3.10-alpine3.21


WORKDIR /app


COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY ./ /app/


EXPOSE 8000


CMD ["python3", "main.py"]