#
FROM python:3.9.13

#
WORKDIR /docker_image

#
COPY ./requirements.txt /docker_image/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /docker_image/requirements.txt

#
COPY ./app /docker_image/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2410"]
