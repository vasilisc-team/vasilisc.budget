FROM python:3.9

LABEL org.opencontainers.image.source https://github.com/xausssr/vasilisc.budget

# Set language
ENV LANG=en_US.UTF-8

# Create and activate python venv
ENV VIRTUAL_ENV=/budget/env
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Install dependencies
WORKDIR /budget
COPY budget/requirements.txt .
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install wheel \
    && python3 -m pip install --no-cache-dir -r requirements.txt

COPY budget ./budget

EXPOSE 19999
CMD ["python", "./budget/manage.py", "runsslserver", "0.0.0.0:19999", "--insecure", "--certificate", "/budget/certs/certificate.crt", "--key", "/budget/certs/certificate.key"]