FROM python:bullseye

RUN useradd --create-home \
    --shell /bin/bash \
    -u 1000 \
    snackquester

WORKDIR /snackquest

COPY api api
COPY cli cli

RUN pip install --no-cache-dir -r api/requirements.txt -r cli/requirements.txt

USER snackquester

EXPOSE 5000/tcp

ENTRYPOINT [ "gunicorn", "-w 2", "-b 0.0.0.0:5000", "api.app:app" ]