FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements/requirements-dev-macos.txt
RUN sed -i 's/\r$//' start.sh
EXPOSE 8000
# ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["/bin/sh", "start.sh"]