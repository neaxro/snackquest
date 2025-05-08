FROM python:slim-bullseye

WORKDIR /snackquest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000/tcp

ENTRYPOINT [ "gunicorn", "-w 2", "-b 0.0.0.0", "--log-level=info", "web.app:app" ]
