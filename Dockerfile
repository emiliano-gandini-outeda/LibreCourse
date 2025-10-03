FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

COPY package.json ./
RUN if [ -f "package.json" ]; then npm install; fi

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]