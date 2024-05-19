FROM nikolaik/python-nodejs:python3.12-nodejs20

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app

# where the code lives
WORKDIR $PYTHONPATH

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl

# install dependencies
RUN pip install --upgrade pip
RUN pip install setuptools

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

# install python dependencies
COPY pyproject.toml poetry.lock ./
# export poetry to requirements.txt, only main dependencies
RUN poetry export -f requirements.txt --without-hashes --only main -o requirements.txt
# install python dependencies
RUN pip install -r requirements.txt
# remove requirements.txt
RUN rm requirements.txt

# copy entrypoint.sh
COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# install app
COPY . .

# install node dependencies and build app
RUN npm install --force
RUN npm run build

# run entrypoint.sh
ENTRYPOINT ["/entrypoint"]
