# FROM python:3.9-alpine3.13
FROM python:3.10-alpine3.13
# use alpine version of python, lightweight image of python
# apline package manager is called 'apk'

LABEL maintainer="ikehunter.com"
# indicates who maintains this docker image, can just put personal domain

ENV PYTHONUNBUFFERED 1
# dont want to buffer output in console, see logs immediately

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000
# copy requirements, app root, set workdir to app dir, expose port 8000 to local machine

ARG DEV=false
# default dev config is set to false, or prod mode
# build-base postgresql-dev musl-dev

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev gcc python3-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        -D \
        -H \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
# creates a new image layer with multiple commands
# 1. create virtual env
# 2. install and upgrade pip inside virtual env
# 3. apk install postgres client package to be able to work with postgres
# 4. apk install the following packages (build-base, postgresql-dev musl-dev) into a virtual dependency called .tmp-build-deps to delete later.
    # These packages are just needed to install postgres on django, and not needed to run it, so delete them after install
# 4. install list of requirements in virtual env
    # 3b. install dev requirements if in dev mode
# 5. remove tmp directory to keep it lightweight and clean
# 6. use apk to delete temp dependency for postgres packages
# 7. adds new user that is not root user (convention not to use root)
    # 7a. disable password so login is automatic
    # 7b. no need to make new home directory for user, keep lightweight
    # 7c. name the user, can name it anything

ENV PATH="/scripts:/py/bin:$PATH"
# updates env variable with PATH

USER django-user
# specifies user to switch to, switches from root user to new django-user

CMD ["run.sh"]