FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

COPY src/squirro /app/squirro/

EXPOSE 8000
CMD ["uvicorn", "squirro.app:app", "--host", "0.0.0.0", "--port", "80"]
