FROM python:3.9.1-alpine3.13

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# COPY crontab /etc/cron.d/crontab
# RUN chmod 0644 /etc/cron.d/crontab
# RUN /usr/bin/crontab /etc/cron.d/crontab

# # RUN crontab crontab
# CMD ["crond", "-f"]

CMD ["main.py"]
ENTRYPOINT [ "python" ]