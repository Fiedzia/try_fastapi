FROM ubuntu:24.04
WORKDIR /app
COPY weblogs/* /app/
RUN apt-get update
RUN apt-get install -y curl python3
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN /root/.cargo/bin/uv sync
RuN python3 populate.py
EXPOSE 8000
CMD /root/.cargo/bin/uv run fastapi dev --host 0.0.0.0 weblogs.py 
