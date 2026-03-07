FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN playwright install --with-deps chromium
COPY . .
CMD ["pytest", "-v", "-n", "2", "--alluredir=allure-results", "--clean-alluredir"]
