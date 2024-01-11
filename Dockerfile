FROM python:3.12-bookworm
ARG TOKEN_BOT
# Run as a non-privileged user to allow watch property
RUN adduser --shell /bin/bash -u 1001 app
USER app
# Copy source files into application directory
COPY --chown=app:app . ./app/
WORKDIR /app
RUN python -m pip install -r requirements.txt
CMD [ "python", "./server.py" ]