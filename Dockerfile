FROM python:3.11

WORKDIR /app

COPY /src /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN useradd -m appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

CMD [ "python", "main.py" ]
