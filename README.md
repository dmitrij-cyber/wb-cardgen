# WB Card Generator — MVP

Сервис для генерации инфографики/карточек товара (MVP) по ТЗ:
- Загрузка фото
- Автоудаление фона (rembg, с фоллбеком)
- Подбор фона и компоновка с тенями
- Простая автокатегоризация и генерация преимуществ (заглушка + словари)
- Генерация 3 вариантов слайдов 1500×2000 (шаблоны MVP)
- Валидация под пресет Wildberries
- Редактирование текста преимуществ на фронте
- Экспорт PNG/JPEG
- Документация API: `http://localhost:8000/docs`

## Быстрый старт (Docker)

1) Установите Docker и docker-compose.
2) В корне создайте `.env` при необходимости (см. `.env.example`). По умолчанию всё работает на localhost.
3) Запустите:
```bash
docker compose up --build
```
4) Откройте фронтенд: http://localhost:3000

## Локальный запуск без Docker

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Структура
- `backend/` — FastAPI сервис, хранит файлы в `backend/data`.
- `frontend/` — Next.js + Tailwind UI.
- `docker-compose.yml` — оркестрация.
- `.env.example` — пример переменных окружения.

## Примечания
- Для качественного удаления фона установите `rembg` (в requirements уже включен). Если в окружении отсутствуют модели, ремувал попытается работать «из коробки». При ошибке сработает фоллбек (вернёт исходник без альфы).
- Генерация преимуществ сделана как безопасная заглушка (без неэтичных/медицинских утверждений). Подключение LLM провайдера можно добавить в `app/services/textgen.py`.
- Шаблоны лайаута упрощены (3 варианта). Расширяйте в `app/services/cardgen.py`.
