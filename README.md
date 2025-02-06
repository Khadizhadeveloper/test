# Витрина товаров на GraphQL

Этот проект представляет собой GraphQL API для управления витриной товаров. С помощью API можно:
- Просматривать список товаров.
- Получать информацию о конкретном товаре по ID.
- Добавлять новые товары в каталог.

## 🚀 Функционал

### Query
1. `getProducts(minPrice: Float, maxPrice: Float): [Product]`
   - Возвращает список товаров. Можно использовать фильтры по минимальной и максимальной цене.
   - **Пример:**
     ```graphql
     query {
       getProducts(minPrice: 50, maxPrice: 200) {
         id
         name
         description
         price
         createdAt
       }
     }
     ```

2. `getProduct(id: ID!): Product`
   - Возвращает товар по его ID.
   - **Пример:**
     ```graphql
     query {
       getProduct(id: 1) {
         id
         name
         description
         price
         createdAt
       }
     }
     ```

### Mutation
1. `createProduct(name: String!, description: String!, price: Float!): ID`
   - Добавляет новый товар и возвращает его ID.
   - **Пример:**
     ```graphql
     mutation {
       createProduct(name: "Телефон", description: "Смартфон с отличной камерой", price: 500) 
     }
     ```

## 🛠️ Технологии
- **Python 3.10**
- **Strawberry GraphQL** — для создания GraphQL-схемы.
- **SQLAlchemy** — для работы с базой данных SQLite.
- **FastAPI** — для запуска веб-приложения.
- **Uvicorn** — ASGI-сервер для обработки запросов.

## 📦 Установка и запуск

### 1. Клонируйте репозиторий:
```bash
git clone git@github.com:Khadizhadeveloper/test.git
cd test
