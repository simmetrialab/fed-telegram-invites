FROM python:3.9.1-alpine3.13

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["main.py"]
ENTRYPOINT ["python3"]
