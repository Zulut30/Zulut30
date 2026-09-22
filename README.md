<h1 align="center">Zulut30</h1>

<p align="center"><strong>Backend · Data · Automation</strong></p>

<p align="center">
  Разрабатываю сервисы и веб-интерфейсы — от данных и API до деплоя.<br>
  Развиваю проекты Manacost Labs и инструменты для сообщества Hearthstone.
</p>

<p align="center">
  <a href="https://github.com/Manacost-Labs">Manacost Labs</a> &nbsp;·&nbsp;
  <a href="https://hs-manacost.ru">Сайт</a> &nbsp;·&nbsp;
  <a href="https://vk.com/manacost">Сообщество</a>
</p>

Всегда готов изучать новое. Активно развиваюсь в инженерном направлении: углубляю знания в архитектуре систем, надёжности и эксплуатации сервисов.

### Практические результаты

**Миллионы матчей Hearthstone в неделю.** Спроектировал систему парсинга и анализа, которая обрабатывает отдельные записи матчей и агрегированную статистику, сортирует данные и формирует аналитические выборки.

[Разбор проекта: архитектура, проверка данных и работающий API →](https://github.com/Zulut30/Zulut30/blob/main/case-studies/hearthstone-data-platform.md)

**AntiSpamBee — за один вечер.** Создал Telegram-бота модерации с TypeSafe Jev и OCR. В моей проверке примерно на 156 спам-ботах обнаружены все — 100% этой выборки.

[Разбор проекта: Jev, анализ рекламы и надёжная обработка событий →](https://github.com/Zulut30/Zulut30/blob/main/case-studies/antispambee.md)

**На 76,86% меньше текстового вывода в контексте ИИ.** ObservationPack сохраняет полные ответы инструментов локально, а модели передаёт краткий обзор с возможностью запросить оригинал. Результат зафиксирован 18 сентября 2026 года на 705 тестовых и рабочих вызовах; измерялся объём вывода, передаваемого модели.

[Устройство ObservationPack и результаты измерения →](https://github.com/Manacost-Labs/Server/blob/main/integrations/codex/subscription-savings/README.md#фактическое-измерение)

### Экспертиза

- **Базы данных.** Проектирую структуру хранения, пишу и оптимизирую запросы, настраиваю миграции, синхронизацию и кеширование.
- **API и парсеры.** Разрабатываю REST и GraphQL API, интегрирую внешние сервисы. Собираю, очищаю и нормализую данные из разных источников.
- **Автоматизация.** Превращаю повторяющиеся задачи в воспроизводимые процессы: фоновые задания, очереди, расписания и контроль ошибок.
- **Telegram.** Создаю ботов и инструменты для каналов: сбор и подготовка контента, автопубликация, модерация и управление доступом.
- **Фронтенд и SEO.** Разрабатываю веб-интерфейсы и занимаюсь поисковой оптимизацией сайтов.
- **Деплой и инфраструктура.** Разворачиваю сервисы, подключаю домены, настраиваю DNS и Nginx.

### Инженерия ИИ-инструментов

Разрабатываю среду работы ИИ-агентов: маршрутизацию задач и моделей, управление контекстом, контроль границ изменений и автоматические проверки качества. Настраиваю **Codex и Claude Code**, инструкции, skills и права доступа под конкретную задачу.

Организую работу исполнителей и ревьюеров с учётом риска. Использую Scope Guard для обнаружения конфликтующих изменений и единую команду проверки локально и в CI. Отделяю экспериментальную среду от продакшена; для рискованных операций предусматриваю ограничения, обязательное ревью и план отката.

### Стек

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-24292f?style=flat-square&amp;logo=python&amp;logoColor=FFD43B">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-24292f?style=flat-square&amp;logo=typescript&amp;logoColor=60A5FA">
  <img alt="React" src="https://img.shields.io/badge/React-24292f?style=flat-square&amp;logo=react&amp;logoColor=61DAFB">
  <img alt="PHP" src="https://img.shields.io/badge/PHP-24292f?style=flat-square&amp;logo=php&amp;logoColor=B4B8F0">
  <img alt="C# / .NET" src="https://img.shields.io/badge/C%23%20%2F%20.NET-24292f?style=flat-square&amp;logo=dotnet&amp;logoColor=C4B5FD">
  <img alt="Go" src="https://img.shields.io/badge/Go-24292f?style=flat-square&amp;logo=go&amp;logoColor=67D7E5">
  <br>
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-24292f?style=flat-square&amp;logo=postgresql&amp;logoColor=93C5FD">
  <img alt="Redis" src="https://img.shields.io/badge/Redis-24292f?style=flat-square&amp;logo=redis&amp;logoColor=FF8585">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-24292f?style=flat-square&amp;logo=docker&amp;logoColor=60A5FA">
  <img alt="Nginx" src="https://img.shields.io/badge/Nginx-24292f?style=flat-square&amp;logo=nginx&amp;logoColor=86EFAC">
  <img alt="Telegram Bot API" src="https://img.shields.io/badge/Telegram%20Bot%20API-24292f?style=flat-square&amp;logo=telegram&amp;logoColor=7DD3FC">
  <img alt="WordPress" src="https://img.shields.io/badge/WordPress-24292f?style=flat-square&amp;logo=wordpress&amp;logoColor=CBD5E1">
</p>

### Избранные проекты

| Проект | Задача и технологии |
| :--- | :--- |
| **[Koloda API](https://github.com/Manacost-Labs/api.kolodahearthstone.com)** | Платформа игровых данных: парсеры, нормализация, PostgreSQL, REST и GraphQL. |
| **[AntiSpamBee](https://github.com/Manacost-Labs/AntiSpamBee)** | Модерация рекламы в Telegram: TypeSafe Jev, OCR и анализ профилей. Go, PostgreSQL, NATS JetStream. |
| **[Server — AI Engineering Toolkit](https://github.com/Manacost-Labs/Server)** | Инструменты для ИИ-агентов: выбор моделей, управление контекстом, Scope Guard и проверки качества. Python, Bash, GitHub Actions. |
| **[DeckView](https://github.com/Manacost-Labs/Deckview-TG)** | Telegram-бот и HTTP API для визуализации колод. Python, очереди Redis/RQ и кеширование. |
| **[HeartPulse](https://github.com/Manacost-Labs/HeartPulse)** | Веб-платформа аналитики Hearthstone: статистика, тир-листы и библиотека карт. TypeScript, React. |
| **[ManacostTeam](https://github.com/Manacost-Labs/ManacostTeam)** | Инструменты и AI-skills для исследований, редактуры, переводов и проверки контента. |
| **[DevOps Skill Platform](https://github.com/Manacost-Labs/devops-skill)** | Настройка ИИ-агентов для работы с инфраструктурой: ограничения действий, проверки и откат. |
| **[IceCrow](https://github.com/Manacost-Labs/IceCrow)** | Windows-приложение для Hearthstone: парсинг логов, состояние матча и история игр. C# / .NET. В разработке. |

<p><sub>Больше проектов — в <a href="https://github.com/Manacost-Labs">Manacost Labs</a> и <a href="https://github.com/Zulut30?tab=repositories">личных репозиториях</a>.</sub></p>
