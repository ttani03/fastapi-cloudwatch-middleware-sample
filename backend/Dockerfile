#
# BUILD BASE IMAGE (USED IN BOTH OF TEST/PROD)
# ------------------------------------------------------------------------------
FROM python:3.10-slim-bullseye

# install dependent packages
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    # for install
    curl \
    default-libmysqlclient-dev \
    gcc \
    g++ \
    software-properties-common \
    isort \
    flake8 \
    python3-autopep8 \
    && apt install git -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install poetry
WORKDIR /home
ENV HOME /home
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN pip3 install --upgrade pip

# specify working directory and install dependency files
WORKDIR /server
COPY pyproject.toml poetry.lock* /server/
RUN poetry install --only main

# copy base source code and add path into PYTHONPATH
ENV PYTHONPATH $PYTHONPATH:./
COPY ./ /server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "8080"]
