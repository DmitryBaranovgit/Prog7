# Task Management System (Spring Boot)

## 📝 Описание
Restful веб-приложение **Task Management System** для управления задачами. Реализованы операции **CRUID** (Создание, чтение, обновление, удаление) через REST API с использованием **Spring Boot**, **Spring Data JPA**, **H2 Database** и **Spring Security**.

## 🚀 Функционал
- Добавление новой задачи
- Просмотр списка задач
- Редактирование задачи
- Удаление задачи
- Защита эндпоинтов с помощью **HTTP Basic Authentification**

## 🛠️ Технологии
- Java 25 + Spring Boot 3.5.6
- Spring Web
- Spring Data JPA
- H2 Database (in-memory)
- Spring Security (Basic Authentication)
- Maven (Сборка проекта)
- Postman (тестирование API)

## 📊 Тестирование приложения
1. Запуск приложения
`mvn spring-boot:run`
2. Доступ к H2 Console
- URL: `http://localhost:8080/h2-console/`
- JDBC URL : `jdbc:h2:mem:taskdb`
- Username: sa
- Password: password
3. Доступ в Postman
- Username: admin
- Password: admin123

## 🖼️ Демонстрация работы
[Отчет со скриншотами](springboot_practice_report.pdf)

## ✅️ Выводы
В ходе практической работы успешно:
- Настроена среда разработки
- Реализовано полнофункциональное REST API
- Интерирована база данных H2 с Spring Data JPA
- Настроена безопасность с помощью Spring Security
- Протестированы CRUID операции
- Документирован процесс разработки

Приложение готово к использованию и демонстрирует основные принципы разработки на Spring Boot
