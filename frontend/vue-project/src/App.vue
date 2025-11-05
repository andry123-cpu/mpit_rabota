<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import express from "express";
import bodyParser from "body-parser";

const app = express();
app.use(bodyParser.json());

app.post("/api/requests", (req, res) => {
  const { age, symptoms, location, chronicDiseases } = req.body;

  // лог анализа
  let priority = "низкий";
  let format = "телемедицина";

  const severeSymptoms = ["боль в груди", "потеря сознания", "затруднённое дыхание"];
  const homeVisitNeeded = ["пожилой", "ограниченная подвижность"];

  // приоритет
  if (severeSymptoms.some(s => symptoms.toLowerCase().includes(s))) {
    priority = "высокий";
    format = "выезд врача";
  } else if (age > 65 || chronicDiseases?.length > 0) {
    priority = "средний";
    format = "очный приём";
  }

  res.json({
    priority,
    recommendedFormat: format,
    message: `Обращение проанализировано: ${format}, приоритет — ${priority}.`
  });
});

app.listen(3000, () => console.log("✅ Сервер запущен на http://localhost:3000"));

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
    
    </div>
  </header>

  <main>
    <TheWelcome />
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
