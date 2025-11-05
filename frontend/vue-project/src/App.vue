<script setup>

// server.js
import express from "express";
import bodyParser from "body-parser";
import cors from "cors";

const app = express();
const PORT = 3000;

// Мидлвары
app.use(cors());
app.use(bodyParser.json());

// Вспомогательная функция анализа обращения
function analyzeRequest({ age, symptoms = "", location = "", chronicDiseases = [] }) {
  const normalizedSymptoms = symptoms.toLowerCase();

  // Ключевые слова для быстрой проверки
  const severeSymptoms = ["боль в груди", "потеря сознания", "затруднённое дыхание", "высокая температура", "сильная боль", "Острая боль", "лихорадка", "Боль при мочеиспускании", "Кровавая рвота" ];
  const moderateSymptoms = ["кашель", "повышенная температура", "усталость", "боль в горле", "боль в животе", "Мышечная слабость", "Боль в спине", "Отеки", "Рвота"];

  let priority = "низкий";
  let format = "телемедицина";
  let score = 0;

  // --- Алгоритм анализа ---

  // Симптомы
  if (severeSymptoms.some(s => normalizedSymptoms.includes(s))) score += 3;
  else if (moderateSymptoms.some(s => normalizedSymptoms.includes(s))) score += 1;

  // Возраст
  if (age > 65) score += 2;
  else if (age < 5) score += 2;

  // Хронические заболевания
  if (chronicDiseases.length > 0) score += 1;

  // --- Определяем приоритет и формат ---
  if (score >= 4) {
    priority = "высокий";
    format = "выезд врача";
  } else if (score >= 2) {
    priority = "средний";
    format = "очный приём";
  }

  return { priority, recommendedFormat: format, score };
}

// Главный маршрут
app.post("/api/requests", (req, res) => {
  try {
    const { age, symptoms, location, chronicDiseases } = req.body;

    if (!age || !symptoms) {
      return res.status(400).json({ error: "Необходимо указать возраст и симптомы" });
    }

    const result = analyzeRequest({ age, symptoms, location, chronicDiseases });

    res.json({
      success: true,
      message: "Обращение проанализировано",
      data: result,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Ошибка сервера" });
  }
});

// Тестовый маршрут
app.get("/", (req, res) => {
  res.send("Сервер медицинской платформы работает ✅");
});

// Запуск сервера
app.listen(PORT, () => {
  console.log(`✅ Сервер запущен на http://localhost:${PORT}`);
});

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
      <title>OptiMed </title>
    <div class="wrapper">
    
    </div>
  </header>

  <main>
   
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
