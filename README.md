### Телеграмм боты
Примеры телеграмм-ботов с использованием трех видов нейронных сетей:
- диалоговые нейросетки `OpenAI`,
- нейросетки, создающие изображения по текстовому описанию `OpenAI`,
- моделей детекции изображения на примере `NVIDIA SSD Model`


### Саммаризатор из аудио в саммари
Исходник summary_bot.py

### Чат-бот с рисованием
Исходник draw_bot.py

### Детекция изображений и видео
Исходник detected_bot.ipynb, detected_videobot.ipynb (Google Colab) на аппаратном ускорителе T4 GPU

### Инструменты:

- `SpeechRecognition` позволяет распознавать речь в текст
- OpenAI `gpt-3.5-turbo` - диалоговая нейросетка, основа для ChatGPT, создает саммари по поданному в нее тексту, аналогично можно доработать вообще любой запрос
- OpenAI `dall-e-3` - нейросеть, разработанная `OpenAI` для создания изображений по текстовому описанию
- Модель [SSD model NVIDIA](https://github.com/NVIDIA/DeepLearningExamples) - модель детекции изображений
- [Replit](replit.com) - хостинг скриптов на питоне. Рекомендательно далее можно разместить бота на таком сервисе и телеграмм-бот будет работать круглосуточно
- [uptimerobot](uptimerobot.com) - сервис пинга ботов, сайтов и прочих веб-приложений

### Использованные токены:

- token_ai токен от API OpenAI
- token_1 токен телеграмм-бота @DetectionPetsBot
- token_2 токен телеграмм-бота @v2tsummarybot
- token_3 токен телеграмм-бота @JuditBot


### Источники:

- [Как хостить телеграм-бота](https://habr.com/ru/articles/709314/?code=1877bacda11c5f5a9295bd01289a5815&state=oRnb3YvAKhybrE5bNnUN0mDK&hl=ru)


### FAQ
`python -m venv myenv`
Windows: `myenv\Scripts\activate`
Unix: `source myenv/bin/activate`
Устанавливаем необходимые библиотеки:
`pip install -r requirements.txt`
`pip freeze > requirements.txt`

https://replit.com/@mkudryashova12/AIBot
https://dashboard.uptimerobot.com/monitors/796929787
