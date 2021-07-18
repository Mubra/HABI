FROM python:3.7
ENV PYTHONUNBUFFERED 1 \
    LC_ALL en_US.UTF-8 \
    LANG en_US.UTF-8
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pip install pipenv && \
    pipenv install --dev