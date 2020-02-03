FROM python:3.8.1-slim as builder

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean
COPY requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install --no-cache-dir --user -r requirements.txt
COPY . /app

# Here is the production image
FROM python:3.8.1-slim as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
WORKDIR app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
