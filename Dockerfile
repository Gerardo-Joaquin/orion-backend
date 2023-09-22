FROM python:3.10

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --user -r requirements.txt

ENV PATH "/root/.local/bin:$PATH"
ENV PYTHONPATH="$PYTHONPATH:/app:/app/app"
ENV PORT 8080
ENV LC_ALL="es_ES.UTF-8"
ENV LC_CTYPE="es_ES.UTF-8"

WORKDIR /app

COPY Makefile /app
COPY app /app/app

CMD make start