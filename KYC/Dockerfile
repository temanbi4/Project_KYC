# мспользование образа python3
FROM python:3

# заданем рабочую директорию
WORKDIR /workdir_KYC

# копируем файл с зависимостями пректа в рабочую директорию
COPY ./requirements.txt .

# запускаем установку зависимостей
RUN pip install -r requirements.txt

# копируем все файлы из текущей директории в рабочую директорию
COPY . .