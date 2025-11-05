<script setup>
import { ref, computed, onMounted } from 'vue'

// ========================
// ДАННЫЕ ПАЦИЕНТА И АНАЛИЗ
// ========================

const patientData = ref({
  age: null,
  symptoms: '',
  location: '',
  hasChronicDiseases: false
})

const analysisResult = ref(null)
const isSubmitting = ref(false)
const apiError = ref(null)

// Списки симптомов для анализа
const CRITICAL_SYMPTOMS = [
  'грудная боль', 'потеря сознания', 'одышка', 'инфаркт', 'инсульт',
  'сильное кровотечение', 'судороги', 'боль в груди', 'затруднённое дыхание'
]

const HIGH_URGENCY_SYMPTOMS = [
  'температура выше 39', 'высокая температура', 'сильная боль',
  'кровотечение', 'рвота с кровью', 'диарея с кровью', 'лихорадка', 
  'боль при мочеиспускании', 'кровавая рвота', 'острая боль'
]

const MILD_SYMPTOMS = [
  'першение', 'легкая усталость', 'головная боль', 'насморк', 'кашель', 
  'повышенная температура', 'усталость', 'боль в горле', 'боль в животе', 
  'мышечная слабость', 'боль в спине', 'отеки', 'рвота'
]

// Нормализация симптомов для анализа
const normalizeSymptoms = (input) => {
  if (!input) return []
  return input.toLowerCase().split(',').map(s => s.trim())
}

// Определение уровня срочности
const analyzeUrgency = () => {
  const age = patientData.value.age
  const symptoms = normalizeSymptoms(patientData.value.symptoms)
  const hasChronic = patientData.value.hasChronicDiseases

  let urgency = 'низкая'
  let format = 'телемедицина'

  // Критическая срочность
  const hasCriticalSymptom = symptoms.some(s => 
    CRITICAL_SYMPTOMS.some(cs => s.includes(cs))
  )
  
  const isHighRiskElderly = (age >= 70) || (hasChronic && age >= 60)

  if (hasCriticalSymptom || isHighRiskElderly) {
    urgency = 'критическая'
    format = 'выезд врача'
  } else {
    // Высокая срочность
    const hasHighUrgencySymptom = symptoms.some(s => 
      HIGH_URGENCY_SYMPTOMS.some(hs => s.includes(hs))
    )

    if (age >= 60 || hasHighUrgencySymptom) {
      urgency = 'высокая'
      format = 'очный приём'
    } else if (symptoms.some(s => 
      MILD_SYMPTOMS.some(ms => s.includes(ms))
    )) {
      urgency = 'средняя'
      format = 'телемедицина или очно'
    } else {
      urgency = 'средняя'
      format = 'очной приём'
    }
  }

  // Особый случай для пожилых пациентов
  if (age >= 75 && urgency !== 'критическая') {
    format = 'выезд врача (по возрасту)'
  }

  return { urgency, format }
}

// Отправка данных на сервер (заглушка)
const submitTriageForm = async () => {
  if (!patientData.value.age || !patientData.value.symptoms || !patientData.value.location) {
    alert('Пожалуйста, заполните все обязательные поля')
    return
  }

  isSubmitting.value = true
  apiError.value = null

  try {
    // Анализируем локально
    const result = analyzeUrgency()
    analysisResult.value = result
    
    // ЗДЕСЬ БУДЕТ ОТПРАВКА НА БЭКЕНД
    console.log('Готово к отправке на сервер:', {
      ...patientData.value,
      urgency: result.urgency,
      recommendedFormat: result.format
    })
    
    alert('Анализ завершен! Результаты готовы к отправке на сервер.')
    
  } catch (error) {
    console.error('Ошибка при анализе:', error)
    apiError.value = 'Ошибка при анализе данных'
    alert('Ошибка при анализе. Попробуйте позже.')
  } finally {
    isSubmitting.value = false
  }
}

// Очистка формы
const resetForm = () => {
  patientData.value = {
    age: null,
    symptoms: '',
    location: '',
    hasChronicDiseases: false
  }
  analysisResult.value = null
  apiError.value = null
}

// Вычисляемые свойства для отображения
const urgencyClass = computed(() => {
  if (!analysisResult.value) return ''
  const urgency = analysisResult.value.urgency.toLowerCase()
  return `urgency-${urgency}`
})

const recommendationText = computed(() => {
  if (!analysisResult.value) return ''
  
  switch (analysisResult.value.urgency) {
    case 'критическая':
      return 'Немедленно вызовите скорую помощь или обратитесь в приемное отделение больницы.'
    case 'высокая':
      return 'Обратитесь в клинику в течение 24 часов. Если состояние ухудшится - вызовите скорую.'
    case 'средняя':
      return 'Запишитесь на прием в ближайшие 2-3 дня. При ухудшении состояния обратитесь раньше.'
    case 'низкая':
      return 'Можете записаться на прием в удобное время или проконсультироваться по телефону.'
    default:
      return 'Проконсультируйтесь с врачом для уточнения рекомендаций.'
  }
})

// ========================
// ФУНКЦИОНАЛ СТРАНИЦЫ
// ========================

// Мобильное меню
onMounted(() => {
  const kebabBtn = document.getElementById('kebabBtn')
  const kebabMenu = document.getElementById('kebabMenu')
  
  if (kebabBtn && kebabMenu) {
    kebabBtn.addEventListener('click', () => {
      const isOpen = kebabMenu.classList.toggle('open')
      kebabBtn.setAttribute('aria-expanded', String(isOpen))
    })

    document.addEventListener('click', (e) => {
      if (!kebabMenu.contains(e.target) && !kebabBtn.contains(e.target)) {
        kebabMenu.classList.remove('open')
        kebabBtn.setAttribute('aria-expanded', 'false')
      }
    })
  }

  // Модальное окно записи
  const dlg = document.getElementById('bookModal')
  const openBookBtn = document.getElementById('openBook')
  
  if (openBookBtn && dlg) {
    openBookBtn.addEventListener('click', () => dlg.showModal())
    
    dlg.addEventListener('close', () => {
      if (dlg.returnValue === 'ok') {
        alert('Спасибо! Мы свяжемся с вами в ближайшее время.')
      }
    })
  }

  // Кнопки "Записаться" в карточках услуг
  document.querySelectorAll('.action').forEach(btn => {
    btn.addEventListener('click', () => {
      if (dlg) dlg.showModal()
    })
  })
})

// Поиск по услугам
const searchQuery = ref('')
const showNoResults = ref(false)

const services = ref([
  { title: 'Терапевт первичный приём', description: 'Базовая диагностика, план обследований и рекомендации.', price: 'от 1 900 ₽', visible: true },
  { title: 'Педиатр первичный приём', description: 'Наблюдение детей с рождения, индивидуальный подход.', price: 'от 2 100 ₽', visible: true },
  { title: 'УЗИ диагностика брюшной полости', description: 'Аппараты экспертного класса, заключение сразу.', price: 'от 1 500 ₽', visible: true },
  { title: 'Стоматология лечение и гигиена', description: 'Лечение, гигиена, эстетика. Безболезненно и аккуратно.', price: 'от 2 500 ₽', visible: true },
  { title: 'Анализы лаборатория ПЦР биохимия', description: 'Биохимия, гормоны, ПЦР. Результаты — в личном кабинете.', price: 'по прайсу', visible: true },
  { title: 'Кардиолог ЭКГ эхокардиография', description: 'Оценка рисков, подбор терапии, ЭКГ на месте.', price: 'от 2 400 ₽', visible: true }
])

const filteredServices = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    showNoResults.value = false
    return services.value
  }

  const filtered = services.value.map(service => {
    const matches = service.title.toLowerCase().includes(query) || 
                   service.description.toLowerCase().includes(query)
    return { ...service, visible: matches }
  })

  const visibleCount = filtered.filter(s => s.visible).length
  showNoResults.value = visibleCount === 0
  
  return filtered
})

const clearSearch = () => {
  searchQuery.value = ''
  showNoResults.value = false
}

// Запись на приём
const bookAppointment = () => {
  const dlg = document.getElementById('bookModal')
  if (dlg) dlg.showModal()
}

const closeModal = () => {
  const dlg = document.getElementById('bookModal')
  if (dlg) dlg.close('cancel')
}

// ========================
// ДАННЫЕ ДЛЯ МОДАЛЬНОГО ОКНА
// ========================

const bookingData = ref({
  name: '',
  phone: '',
  service: ''
})

const submitBookingForm = async () => {
  if (!bookingData.value.name || !bookingData.value.phone) {
    alert('Пожалуйста, заполните имя и телефон')
    return
  }

  try {
    // ЗДЕСЬ БУДЕТ ОТПРАВКА ЗАПИСИ НА БЭКЕНД
    console.log('Готово к отправке записи:', {
      ...bookingData.value,
      triageResult: analysisResult.value
    })
    
    alert('Спасибо! Мы свяжемся с вами в ближайшее время.')
    
    // Закрываем модальное окно
    const dlg = document.getElementById('bookModal')
    if (dlg) dlg.close('ok')
    
    // Очищаем форму
    bookingData.value = { name: '', phone: '', service: '' }
    
  } catch (error) {
    console.error('Ошибка при создании записи:', error)
    alert('Не удалось создать запись. Попробуйте позже.')
  }
}
</script>

<template>
  <div>
  <header>
    <div class="container topbar" aria-label="Верхняя панель">
      <a class="brand" href="#" aria-label="На главную">
        <img src="@/assets/images/doctor.jpg" alt="Врач" class="doc-img">
        <img src="@/assets/images/Logo.png" alt="Оптимед — логотип" class="main-logo">
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
      <form class="search" role="search" aria-label="Поиск по услугам" @submit.prevent>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input id="searchInput" type="search" v-model="searchQuery" placeholder="Поиск по услугам и специалистам…" autocomplete="off" />
        <button type="button" id="clearSearch" @click="clearSearch" title="Очистить">Очистить</button>
      </form>
    </div>
  </header>

  <div class="container">
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
        <article 
          v-for="(service, index) in filteredServices" 
          :key="index"
          class="card" 
          :data-title="service.title"
          :class="{ hidden: !service.visible }"
        >
          <h4>{{ service.title }}</h4>
          <p>{{ service.description }}</p>
          <div class="price">{{ service.price }}</div>
          <button class="action">Записаться</button>
        </article>
      </div>
      <p class="muted" id="nothingFound" v-show="showNoResults">Ничего не найдено. Попробуйте изменить запрос.</p>
    </section>
  </div>

  <footer id="contacts">
    <div class="container">
      <strong>Клиника «Оптимед»</strong><br>
      г. <b>Астрахань</b>, ул. Примерная, 10 • Ежедневно 8:00–21:00<br>
      <div class="contact-row">
        <span>Тел.: <a class="phone" href="tel:+79991234567">+7 999 123-45-67</a></span>
        <router-link to="/dashboard" class="admin-link" aria-label="Панель врача для медицинского персонала">
          <span class="admin-text">Панель врача</span>
          <span class="admin-icon">👨‍⚕️</span>
        </router-link>
      </div>
      E-mail: info@clinic.example
    </div>
  </footer>

  <!-- Модальное окно записи -->
  <dialog id="bookModal" ref="bookModal" style="border:0;border-radius:16px;padding:0;max-width:520px;width:92%">
    <form method="dialog" style="padding:22px 20px" @submit.prevent="submitBookingForm">
      <h3 style="margin:0 0 8px 0;color:var(--burgundy)">Запись на приём</h3>
      <p class="muted" style="margin-top:0">Оставьте контакты, и администратор свяжется с вами.</p>
      <div style="display:grid;gap:10px">
        <input required v-model="bookingData.name" placeholder="Ваше имя" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
        <input required v-model="bookingData.phone" placeholder="Телефон" pattern="\\+?[0-9\\s\\-()]{6,}" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
        <select v-model="bookingData.service" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <option>Терапевт</option><option>Педиатр</option><option>УЗИ</option>
          <option>Стоматология</option><option>Анализы</option><option>Кардиолог</option>
        </select>
      </div>
      <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:14px">
        <button class="btn" @click="closeModal" value="cancel">Отмена</button>
        <button class="btn btn-primary" type="submit" value="ok">Отправить</button>
      </div>
    </form>
  </dialog>
  </div>
</template>

<style>
    :root {
  --burgundy: #7a1732;
  --burgundy-700: #5f1227;
  --gray-50: #f6f7f8;
  --gray-200: #e5e7eb;
  --gray-500: #6b7280;
  --gray-800: #1f2937;
  --white: #ffffff;
  --radius: 14px;
  --shadow: 0 8px 24px rgba(0, 0, 0, .08);
  --container: 1180px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; font-size: 16px; line-height: 1.5; }
body { 
  margin: 0; 
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; 
  color: var(--gray-800);
  background: linear-gradient(0deg, var(--gray-50), #ffffff);
}
.container { max-width: var(--container); margin: 0 auto; padding: 0 20px; }

    /* АДАПТИВНОСТЬ - УЛУЧШЕНАЯ */
    @media (max-width: 768px) {
      :root { --container: 100%; }
      .container { padding: 0 15px; }
      .topbar { 
        flex-direction: column; 
        gap: 12px; 
        text-align: center; 
        padding: 10px 0;
      }
      .brand { 
        flex-direction: column; 
        gap: 8px; 
        width: 100%;
      }
      .brand h1 {
        font-size: 18px;
        margin-top: 5px;
      }
      .cta { 
        width: 100%; 
        justify-content: center; 
        flex-wrap: wrap;
        margin-top: 10px;
      }
      .search-wrap { padding: 12px 0 5px 0; }
      .search { 
        flex-direction: column; 
        padding: 10px; 
        border-radius: 12px;
      }
      .search input {
        width: 100%;
        margin-bottom: 8px;
      }
      .search button {
        align-self: flex-end;
        padding: 8px 16px;
      }
      .about { 
        padding: 20px; 
        margin-top: 12px; 
      }
      .about h2 { font-size: 1.4rem; }
      .services h3 { 
        font-size: 1.3rem; 
        margin-bottom: 8px; 
      }
      .grid {
        grid-template-columns: 1fr;
        gap: 12px;
      }
      .card { 
        padding: 14px; 
        grid-column: span 1 !important;
      }
      .card h4 { font-size: 1rem; }
      .card p { font-size: 0.9rem; }
      .card .price { font-size: 1rem; }
      .card .action {
        padding: 8px 12px;
        font-size: 0.9rem;
      }
      footer { 
        padding: 20px 0; 
        font-size: 14px; 
        text-align: center;
      }
      .contact-row {
        flex-direction: column;
        align-items: center;
        gap: 8px;
      }
      .admin-link {
        justify-content: center;
        width: 100%;
      }
    }
    
    header{position:sticky;top:0;z-index:50;background:var(--white);border-bottom:1px solid var(--gray-200);box-shadow:0 2px 10px rgba(0,0,0,.04)}
    .topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0}
    .brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}
    .brand h1{font-size:18px;line-height:1.1;margin:0}

    /*стиль лого */
    .main-logo {
      height: 50px;
      width: auto;
      display: block;
      border-radius: 8px; 
      box-shadow: var(--shadow); 
    }

    /*доктор */
    .doc-img {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      object-fit: cover;
      box-shadow: var(--shadow);
      background-color: #f8f9fa; 
    }

    .brand h1 {
      font-size: 20px;
      margin: 0;
      align-self: center; 
    }

    .kebab{border:1px solid var(--gray-200);background:var(--white);border-radius:12px;padding:10px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
    .kebab:hover{background:#fafafa}
    .kebab-menu{position:absolute;right:20px;top:68px;background:var(--white);border:1px solid var(--gray-200);border-radius:12px;box-shadow:var(--shadow);padding:6px;width:220px;display:none}
    .kebab-menu.open{display:block}
    .kebab-menu a{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:10px;color:inherit;text-decoration:none}
    .kebab-menu a:hover{background:#f3f4f6}

    /*CTA*/
    .cta{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
    .btn{border:0;border-radius:999px;padding:12px 18px;cursor:pointer;font-weight:600;letter-spacing:.2px}
    .btn-primary{background:var(--burgundy);color:var(--white);box-shadow:0 6px 18px rgba(122,23,50,.25)}
    .btn-primary:hover{background:var(--burgundy-700)}
    

    
    .phone{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--burgundy);text-decoration:none;white-space:nowrap}

    /*Поиск*/
    .search-wrap{padding:22px 0 8px}
    .search{display:flex;gap:12px;align-items:center;background:var(--white);border:1px solid var(--gray-200);border-radius:999px;padding:10px 14px;box-shadow:var(--shadow)}
    .search input{border:0;outline:0;flex:1;font-size:16px;background:transparent}
    .search button{border:0;border-radius:999px;padding:10px 14px;cursor:pointer;background:#f3f4f6}
    .search button:hover{background:#ebecef}

    
    .about{margin-top:22px;background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:28px;box-shadow:var(--shadow);display:grid;gap:10px}
    .about h2{margin:0 0 6px 0;font-size:1.8rem}
    .about p{font-size:1.1rem;line-height:1.6;color:var(--gray-800)}
    .badges{display:flex;gap:10px;flex-wrap:wrap}
    .badge{background:#f3f4f6;border-radius:999px;padding:6px 10px;font-size:13px}

    .services{margin:26px 0 60px}
    .services h3{margin:0 0 14px 0;font-size:1.6rem}
    .grid{display:grid;gap:16px;grid-template-columns:repeat(12,1fr)}
    .card{grid-column:span 4;background:#fff;border:1px solid var(--gray-200);border-radius:16px;padding:16px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:10px}
    .card.hidden { display: none; }
    .card h4{margin:0;font-size:1.2rem;color:var(--burgundy)}
    .card p{margin:0;color:var(--gray-500);font-size:0.95rem}
    .card .price{margin-top:auto;font-weight:700;font-size:1.1rem;color:var(--burgundy)}
    .card .action{margin-top:8px;align-self:flex-start;background:var(--burgundy);color:#fff;border:0;border-radius:10px;padding:10px 12px;cursor:pointer}
    .action:hover{background:var(--burgundy-700)}
    .muted{color:var(--gray-500)}

    footer{border-top:1px solid var(--gray-200);background:var(--white);color:var(--gray-500);padding:28px 0;font-size:14px}

    @media (max-width:960px){
      .grid{grid-template-columns:repeat(6,1fr)}
      .card{grid-column:span 3}
    }
    @media (max-width:768px){
      .grid{grid-template-columns:repeat(1,1fr)}
      .card{grid-column:span 1 !important}
      .brand h1{font-size:16px}
    }
    @media (max-width:640px){
      .brand h1{display:block;font-size:18px}
      .search-wrap{padding-top:10px}
      .kebab-menu{right:12px}
      .topbar{padding:10px 0}
    }
    
    /* СТИЛИ ДЛЯ КНОПКИ В ФУТЕРЕ */
    .contact-row {
      display: flex;
      align-items: center;
      gap: 15px;
      flex-wrap: wrap;
      margin: 4px 0;
    }

    .admin-link {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: var(--gray-500);
      text-decoration: none;
      font-size: 13px;
      padding: 4px 8px;
      border-radius: 12px;
      background: rgba(122, 23, 50, 0.03);
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }

    .admin-link:hover {
      color: var(--burgundy);
      background: rgba(122, 23, 50, 0.08);
      border-color: rgba(122, 23, 50, 0.2);
      transform: translateY(-1px);
    }

    .admin-icon {
      font-size: 14px;
      line-height: 1;
    }

    @media (max-width: 768px) {
      .contact-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }
      
      .admin-link {
        font-size: 12px;
        padding: 3px 7px;
      }
      
      .admin-text {
        display: inline;
      }
    }

    @media (max-width: 480px) {
      .admin-link {
        font-size: 11px;
        padding: 2px 6px;
      }
      
      .admin-icon {
        font-size: 12px;
      }
      
      .admin-text {
        display: none;
      }
    }
</style>