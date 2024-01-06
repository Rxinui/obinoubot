FROM python:3.12-bookworm
WORKDIR /app
COPY ./ /app/
RUN python -m pip install -r requirements.txt
CMD [ "python", "./server.py" ]