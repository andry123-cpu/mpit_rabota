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
 <!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Оптимед — медицинская клиника</title>
  <meta name="description" content="Клиника «Оптимед» в Астрахани: запись на приём, лучшие врачи, популярные услуги." />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

</head>
<body>

  <header>
    <div class="container topbar" aria-label="Верхняя панель">
      
      <a class="brand" href="#" aria-label="На главную">
        <!-- Замените src на свой файл логотипа (из вашего примера «ОПТИМЕД») -->
        <img src="images/optimed-logo.png" alt="Оптимед — логотип" class="logo-img">
        <!-- Иконка врача (PNG из вашего примера); перекрашена в бордовый через CSS -->
        <span class="doc-wrap" aria-hidden="true">
          <img src="images/doctor.png" alt="">
        </span>
        <h1>Клиника «Оптимед»</h1>
      </a>

      <!-- «Записаться» + телефон + троеточие -->
      <div class="cta" role="group" aria-label="Контакты и запись">
        <a class="phone" href="tel:+79991234567" aria-label="Позвонить в клинику">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.06A19.5 19.5 0 0 1 3.14 8.81 19.79 19.79 0 0 1 .09 0 2 2 0 0 1 2.06 0h3a2 2 0 0 1 2 1.72c.13.97.35 1.92.66 2.84a2 2 0 0 1-.45 2.11L6 8a16 16 0 0 0 8 8l1.33-1.27a2 2 0 0 1 2.11-.45c.92.31 1.87.53 2.84.66A2 2 0 0 1 22 16.92Z" fill="currentColor"/>
          </svg>
          +7 999 123-45-67
        </a>
        <button class="btn btn-primary" id="openBook">Записаться</button>

        <button class="kebab" id="kebabBtn" aria-haspopup="menu" aria-expanded="false" aria-label="Дополнительное меню">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>
          </svg>
          Меню
        </button>
      </div>

      <nav class="kebab-menu" id="kebabMenu" aria-label="Меню">
        <a href="#about">О клинике</a>
        <a href="#services">Услуги и цены</a>
        <a href="#contacts">Контакты</a>
        <a href="#faq">Вопрос–ответ</a>
      </nav>
    </div>

    
    <div class="container search-wrap">
      <form class="search" role="search" aria-label="Поиск по услугам" onsubmit="event.preventDefault();">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input id="searchInput" type="search" placeholder="Поиск по услугам и специалистам…" autocomplete="off" />
        <button type="button" id="clearSearch" title="Очистить">Очистить</button>
      </form>
    </div>
  </header>

  <main class="container">
    <!-- Информация -->
    <section id="about" class="about" aria-labelledby="aboutTitle">
      <h2 id="aboutTitle">Современная клиника полного цикла</h2>
      <p>Мы объединяем опытных врачей, цифровые технологии и заботу о каждом пациенте. Диагностика, амбулаторное лечение и дневной стационар — всё в одном месте.</p>
      <div class="badges">
        <span class="badge">12 лет доверия</span>
        <span class="badge">Более 45 врачей</span>
        <span class="badge">Собственная лаборатория</span>
        <span class="badge">Работаем ежедневно 8:00–21:00</span>
      </div>
    </section>

    <!-- Услуги (без изменений содержимого) -->
    <section id="services" class="services" aria-labelledby="servicesTitle">
      <h3 id="servicesTitle">Популярные услуги</h3>
      <div class="grid" id="servicesGrid" aria-live="polite">
        <article class="card" data-title="Терапевт первичный приём">
          <h4>Терапевт — первичный приём</h4>
          <p>Базовая диагностика, план обследований и рекомендации.</p>
          <div class="price">от 1 900 ₽</div><button class="action">Записаться</button>
        </article>
        <article class="card" data-title="Педиатр первичный приём">
          <h4>Педиатр — первичный приём</h4>
          <p>Наблюдение детей с рождения, индивидуальный подход.</p>
          <div class="price">от 2 100 ₽</div><button class="action">Записаться</button>
        </article>
        <article class="card" data-title="УЗИ диагностика брюшной полости">
          <h4>УЗИ диагностика</h4>
          <p>Аппараты экспертного класса, заключение сразу.</p>
          <div class="price">от 1 500 ₽</div><button class="action">Записаться</button>
        </article>
        <article class="card" data-title="Стоматология лечение и гигиена">
          <h4>Стоматология</h4>
          <p>Лечение, гигиена, эстетика. Безболезненно и аккуратно.</p>
          <div class="price">от 2 500 ₽</div><button class="action">Записаться</button>
        </article>
        <article class="card" data-title="Анализы лаборатория ПЦР биохимия">
          <h4>Лабораторные анализы</h4>
          <p>Биохимия, гормоны, ПЦР. Результаты — в личном кабинете.</p>
          <div class="price">по прайсу</div><button class="action">Записаться</button>
        </article>
        <article class="card" data-title="Кардиолог ЭКГ эхокардиография">
          <h4>Кардиолог + ЭКГ</h4>
          <p>Оценка рисков, подбор терапии, ЭКГ на месте.</p>
          <div class="price">от 2 400 ₽</div><button class="action">Записаться</button>
        </article>
      </div>
      <p class="muted" id="nothingFound" style="display:none">Ничего не найдено. Попробуйте изменить запрос.</p>
    </section>
  </main>

  <footer id="contacts">
    <div class="container">
      <strong>Клиника «Оптимед»</strong><br>
      г. <b>Астрахань</b>, ул. Примерная, 10 • Ежедневно 8:00–21:00<br>
      Тел.: <a class="phone" href="tel:+79991234567">+7 999 123-45-67</a> • E-mail: info@clinic.example
    </div>
  </footer>

  <!-- Модальное окно записи -->
  <dialog id="bookModal" style="border:0;border-radius:16px;padding:0;max-width:520px;width:92%">
    <form method="dialog" style="padding:22px 20px">
      <h3 style="margin:0 0 8px 0;color:var(--burgundy)">Запись на приём</h3>
      <p class="muted" style="margin-top:0">Оставьте контакты, и администратор свяжется с вами.</p>
      <div style="display:grid;gap:10px">
        <input required name="name" placeholder="Ваше имя" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
        <input required name="tel" placeholder="Телефон" pattern="\\+?[0-9\\s\\-()]{6,}" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
        <select name="service" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <option>Терапевт</option><option>Педиатр</option><option>УЗИ</option>
          <option>Стоматология</option><option>Анализы</option><option>Кардиолог</option>
        </select>
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:14px">
        <button class="btn" value="cancel">Отмена</button>
        <button class="btn btn-primary" value="ok">Отправить</button>
      </div>
    </form>
  </dialog>

  <script>
    const kebabBtn=document.getElementById('kebabBtn');
    const kebabMenu=document.getElementById('kebabMenu');
    kebabBtn.addEventListener('click',()=>{const open=kebabMenu.classList.toggle('open');kebabBtn.setAttribute('aria-expanded',String(open));});
    document.addEventListener('click',(e)=>{if(!kebabMenu.contains(e.target)&&!kebabBtn.contains(e.target)){kebabMenu.classList.remove('open');kebabBtn.setAttribute('aria-expanded','false');}});

    const dlg=document.getElementById('bookModal');
    document.getElementById('openBook').addEventListener('click',()=>dlg.showModal());
    dlg.addEventListener('close',()=>{if(dlg.returnValue==='ok') alert('Спасибо! Мы свяжемся с вами в ближайшее время.');});

    document.querySelectorAll('.action').forEach(btn=>btn.addEventListener('click',()=>dlg.showModal()));

    const input=document.getElementById('searchInput'); const clearBtn=document.getElementById('clearSearch');
    const grid=document.getElementById('servicesGrid'); const empty=document.getElementById('nothingFound');
    function filter(){
      const q=input.value.trim().toLowerCase(); let visible=0;
      grid.querySelectorAll('.card').forEach(card=>{
        const t=(card.dataset.title||card.textContent).toLowerCase(); const show=!q||t.includes(q);
        card.style.display=show?'':'none'; if(show) visible++;
      });
      empty.style.display=visible?'none':'';
    }
    input.addEventListener('input',filter);
    clearBtn.addEventListener('click',()=>{input.value='';filter();});
  </script>
</body>
</html>

</template>

<style scoped>

    :root{
      --burgundy:#7a1732;
      --burgundy-700:#5f1227;
      --gray-50:#f6f7f8; --gray-200:#e5e7eb; --gray-500:#6b7280; --gray-800:#1f2937;
      --white:#ffffff; --radius:14px; --shadow:0 8px 24px rgba(0,0,0,.08); --container:1180px;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--gray-800);
      background:linear-gradient(0deg,var(--gray-50),#ffffff);}
    .container{max-width:var(--container);margin:0 auto;padding:0 20px}

    
    header{position:sticky;top:0;z-index:50;background:var(--white);border-bottom:1px solid var(--gray-200);box-shadow:0 2px 10px rgba(0,0,0,.04)}
    .topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0}
    .brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}
    .brand h1{font-size:18px;line-height:1.1;margin:0}

    /* логотип + врач */
    .logo-img{height:44px;width:auto;display:block}
    .doc-wrap{width:44px;height:44px;border-radius:50%;overflow:hidden;position:relative;box-shadow:var(--shadow)}
    /* Перекрашиваем зелёный в бордовый: подберите при необходимости значения hue-rotate/saturate */
    .doc-wrap img{width:100%;height:100%;object-fit:cover;filter:hue-rotate(315deg) saturate(130%);}

    .kebab{border:1px solid var(--gray-200);background:var(--white);border-radius:12px;padding:10px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
    .kebab:hover{background:#fafafa}
    .kebab-menu{position:absolute;right:20px;top:68px;background:var(--white);border:1px solid var(--gray-200);border-radius:12px;box-shadow:var(--shadow);padding:6px;width:220px;display:none}
    .kebab-menu.open{display:block}
    .kebab-menu a{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:10px;color:inherit;text-decoration:none}
    .kebab-menu a:hover{background:#f3f4f6}

    /* ====== CTA ====== */
    .cta{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
    .btn{border:0;border-radius:999px;padding:12px 18px;cursor:pointer;font-weight:600;letter-spacing:.2px}
    .btn-primary{background:var(--burgundy);color:var(--white);box-shadow:0 6px 18px rgba(122,23,50,.25)}
    .btn-primary:hover{background:var(--burgundy-700)}
    .phone{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--burgundy);text-decoration:none;white-space:nowrap}

    /* ====== Поиск ====== */
    .search-wrap{padding:22px 0 8px}
    .search{display:flex;gap:12px;align-items:center;background:var(--white);border:1px solid var(--gray-200);border-radius:999px;padding:10px 14px;box-shadow:var(--shadow)}
    .search input{border:0;outline:0;flex:1;font-size:16px;background:transparent}
    .search button{border:0;border-radius:999px;padding:10px 14px;cursor:pointer;background:#f3f4f6}
    .search button:hover{background:#ebecef}

    
    .about{margin-top:22px;background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);display:grid;gap:10px}
    .about h2{margin:0 0 6px 0}
    .badges{display:flex;gap:10px;flex-wrap:wrap}
    .badge{background:#f3f4f6;border-radius:999px;padding:6px 10px;font-size:13px}

    .services{margin:26px 0 60px}
    .services h3{margin:0 0 14px 0}
    .grid{display:grid;gap:16px;grid-template-columns:repeat(12,1fr)}
    .card{grid-column:span 4;background:#fff;border:1px solid var(--gray-200);border-radius:16px;padding:16px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:10px}
    .card h4{margin:0}
    .card p{margin:0;color:var(--gray-500)}
    .card .price{margin-top:auto;font-weight:700}
    .card .action{margin-top:8px;align-self:flex-start;background:var(--burgundy);color:#fff;border:0;border-radius:10px;padding:10px 12px;cursor:pointer}
    .action:hover{background:var(--burgundy-700)}
    .muted{color:var(--gray-500)}

    footer{border-top:1px solid var(--gray-200);background:var(--white);color:var(--gray-500);padding:28px 0;font-size:14px}

    @media (max-width:960px){.card{grid-column:span 6}}
    @media (max-width:640px){.brand h1{display:none}.search-wrap{padding-top:10px}.card{grid-column:span 12}.kebab-menu{right:12px}}
  
</style>
