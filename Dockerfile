FROM python:3.8.12-slim-buster
RUN pip install flask pyyaml
COPY ./app.py /app/app.py
CMD ["python","/app/app.py"]