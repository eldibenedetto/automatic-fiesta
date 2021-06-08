FROM python:3.9.2
RUN mkdir /project
WORKDIR /project
# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
ENV PATH="${PATH}:/root/.local/bin"
# Clone Repository
# RUN git clone https://github.com/eldibenedetto/automatic-fiesta.git
COPY . /project/
RUN poetry install
RUN poetry run python3 manage.py migrate
EXPOSE 8000