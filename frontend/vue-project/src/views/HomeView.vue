<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const isHighContrast = ref(false)
const fontSizeScale = ref(1.0) 


const sendToDatabase = async (data) => {
  try {
    const response = await fetch('https://your-api-endpoint.com/api/triage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      body: JSON.stringify(data)
    })
    
    if (!response.ok) {
      throw new Error('Ошибка сервера: ' + response.status)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Ошибка при отправке данных:', error)
    throw error
  }
}



// Загружаем настройки из localStorage
onMounted(() => {
  const savedContrast = localStorage.getItem('highContrastMode')
  const savedFontSize = localStorage.getItem('fontSizeScale')
  
  if (savedContrast) {
    isHighContrast.value = JSON.parse(savedContrast)
  }
  
  if (savedFontSize) {
    fontSizeScale.value = parseFloat(savedFontSize)
  }
  

  applyAccessibilitySettings()
})


const applyAccessibilitySettings = () => {
  document.body.style.fontSize = `${16 * fontSizeScale.value}px`
  
  if (isHighContrast.value) {
    document.body.classList.add('high-contrast')
  } else {
    document.body.classList.remove('high-contrast')
  }
}


watch(isHighContrast, (newValue) => {
  localStorage.setItem('highContrastMode', JSON.stringify(newValue))
  applyAccessibilitySettings()
})

watch(fontSizeScale, (newValue) => {
  localStorage.setItem('fontSizeScale', newValue.toString())
  applyAccessibilitySettings()
})


const toggleHighContrast = () => {
  isHighContrast.value = !isHighContrast.value
}

// Увеличение/уменьшение шрифта
const increaseFontSize = () => {
  fontSizeScale.value = Math.min(fontSizeScale.value + 0.2, 2.0)
}

const decreaseFontSize = () => {
  fontSizeScale.value = Math.max(fontSizeScale.value - 0.2, 0.8)
}

// Сброс настроек
const resetAccessibility = () => {
  isHighContrast.value = false
  fontSizeScale.value = 1.0
}

// hot keys
onMounted(() => {
  document.addEventListener('keydown', (e) => {

    // шрифт +
    if (e.ctrlKey && e.key === '+') {
      e.preventDefault()
      increaseFontSize()
    }
    
    // шрифт - 
    if (e.ctrlKey && e.key === '-') {
      e.preventDefault()
      decreaseFontSize()
    }
    
    // сброс
    if (e.ctrlKey && e.key === '0') {
      e.preventDefault()
      resetAccessibility()
    }
    
    // контраст
    if (e.ctrlKey && e.key.toLowerCase() === 'c') {
      e.preventDefault()
      toggleHighContrast()
    }
  })
})


const patientData = ref({
  age: null,
  symptoms: '',
  location: '',
  hasChronicDiseases: false
})

const analysisResult = ref(null)
const isSubmitting = ref(false)
const apiError = ref(null)

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

const normalizeSymptoms = (input) => {
  if (!input) return []
  return input.toLowerCase().split(',').map(s => s.trim())
}

const analyzeUrgency = () => {
  const age = patientData.value.age
  const symptoms = normalizeSymptoms(patientData.value.symptoms)
  const hasChronic = patientData.value.hasChronicDiseases

  let urgency = 'низкая'
  let format = 'телемедицина'

  const hasCriticalSymptom = symptoms.some(s => 
    CRITICAL_SYMPTOMS.some(cs => s.includes(cs))
  )
  
  const isHighRiskElderly = (age >= 70) || (hasChronic && age >= 60)

  if (hasCriticalSymptom || isHighRiskElderly) {
    urgency = 'критическая'
    format = 'выезд врача'
  } else {
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

  if (age >= 75 && urgency !== 'критическая') {
    format = 'выезд врача (по возрасту)'
  }

  return { urgency, format }
}

const submitTriageForm = async () => {
  if (!patientData.value.age || !patientData.value.symptoms || !patientData.value.location) {
    alert('Пожалуйста, заполните все обязательные поля')
    return
  }

  isSubmitting.value = true
  apiError.value = null

  try {
    const result = analyzeUrgency()
    analysisResult.value = result
    
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

// Функционал страницы
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

  document.querySelectorAll('.action').forEach(btn => {
    btn.addEventListener('click', () => {
      if (dlg) dlg.showModal()
    })
  })
})

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

const bookAppointment = () => {
  const dlg = document.getElementById('bookModal')
  if (dlg) dlg.showModal()
}

const closeModal = () => {
  const dlg = document.getElementById('bookModal')
  if (dlg) dlg.close('cancel')
}

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
    console.log('Готово к отправке записи:', {
      ...bookingData.value,
      triageResult: analysisResult.value
    })
    
    alert('Спасибо! Мы свяжемся с вами в ближайшее время.')
    
    const dlg = document.getElementById('bookModal')
    if (dlg) dlg.close('ok')
    
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

        <!-- ПЕРЕКЛЮЧАТЕЛЬ ТЕМЫ -->
        <div class="theme-toggle-container" aria-label="Настройки доступности">
          <div class="theme-toggle" :class="{ 'high-contrast-active': isHighContrast }">
            <button 
              class="theme-btn" 
              @click="decreaseFontSize"
              aria-label="Уменьшить размер шрифта"
              title="Уменьшить шрифт (Ctrl + -)"
            >
              A-
            </button>
            <button 
              class="theme-btn theme-btn-main" 
              @click="toggleHighContrast"
              :aria-pressed="isHighContrast"
              aria-label="Включить/выключить режим для слабовидящих"
              title="Режим для слабовидящих (Ctrl + C)"
            >
              <span class="theme-indicator">{{ isHighContrast ? '♿' : '♿' }}</span>
              <span class="theme-label">{{ isHighContrast ? 'Стандартная' : 'Для слабовидящих' }}</span>
            </button>
            <button 
              class="theme-btn" 
              @click="increaseFontSize"
              aria-label="Увеличить размер шрифта"
              title="Увеличить шрифт (Ctrl + +)"
            >
              A+
            </button>
          </div>
        </div>

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

      <!-- Услуги -->
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
            <button class="action" @click="bookAppointment">Записаться</button>
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
          <router-link to="/dashboard/login" class="admin-link" aria-label="Панель врача для медицинского персонала">
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
        <p class="muted" style="margin-top:0">Заполните данные для первичной оценки срочности.</p>
        <div style="display:grid;gap:10px">
          <input required v-model="bookingData.name" placeholder="Ваше имя" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <input required v-model="bookingData.phone" placeholder="Телефон" pattern="\\+?[0-9\\s\\-()]{6,}" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <select v-model="bookingData.service" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
            <option value="">Выберите специалиста</option>
            <option>Терапевт</option><option>Педиатр</option><option>УЗИ</option>
            <option>Стоматология</option><option>Анализы</option><option>Кардиолог</option>
          </select>

          <!-- НОВЫЕ ПОЛЯ -->
          <input type="number" min="0" max="130" v-model.number="bookingData.age" placeholder="Возраст (полных лет)" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <input v-model="bookingData.location" placeholder="Локация (город, район)" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px">
          <textarea v-model="bookingData.symptoms" placeholder="Симптомы (через запятую: кашель, температура и т.д.)" rows="3" style="padding:12px;border:1px solid var(--gray-200);border-radius:10px;resize:vertical"></textarea>
          <label style="display:flex;align-items:center;gap:8px;font-size:14px">
            <input type="checkbox" v-model="bookingData.hasChronicDiseases" style="width:auto;height:auto">
            Есть хронические заболевания
          </label>
        </div>

        <!-- Отображение результата анализа -->
        <div v-if="analysisResult" :class="`urgency-${analysisResult.urgency.toLowerCase()}`" style="margin-top:12px;padding:10px;border-radius:8px;background:#f8f9fa;color:#000">
          <strong>Уровень срочности:</strong> {{ analysisResult.urgency }}<br>
          <strong>Рекомендуемый формат:</strong> {{ analysisResult.format }}
        </div>

        <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:14px">
          <button class="btn" @click="closeModal" value="cancel">Отмена</button>
          <button class="btn btn-primary" type="submit" :disabled="isSubmitting" value="ok">
            {{ isSubmitting ? 'Отправка...' : 'Отправить' }}
          </button>
        </div>
      </form>
    </dialog>

    <!-- МОБИЛЬНЫЙ ПЕРЕКЛЮЧАТЕЛЬ -->
    <div class="mobile-theme-toggle" aria-label="Мобильное меню доступности">
      <button 
        class="mobile-theme-btn" 
        @click="toggleHighContrast"
        :class="{ 'active': isHighContrast }"
        :aria-pressed="isHighContrast"
        aria-label="Включить/выключить режим для слабовидящих"
      >
        <span class="mobile-theme-icon">{{ isHighContrast ? '♿' : '♿' }}</span>
      </button>
    </div>
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
  
  /* Цвета для режима слабовидящих */
  --hc-bg: #000000;
  --hc-text: #ffffff;
  --hc-accent: #ffcc00;
  --hc-border: #ffffff;
  --hc-card: #1a1a1a;
  --hc-input: #333333;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; font-size: 16px; line-height: 1.5; }
body { 
  margin: 0; 
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; 
  color: var(--gray-800);
  background: linear-gradient(0deg, var(--gray-50), #ffffff);
  transition: background-color 0.3s, color 0.3s;
}

/* Режим слабовидящих */
body.high-contrast {
  background: var(--hc-bg) !important;
  color: var(--hc-text) !important;
  background-image: none !important;
  line-height: 1.7 !important;
}

/* СТИЛИ ПЕРЕКЛЮЧАТЕЛЯ ТЕМЫ */
.theme-toggle-container {
  display: flex;
  align-items: center;
  margin-left: 15px;
}

.theme-toggle {
  display: flex;
  gap: 8px;
  background: var(--white);
  border: 1px solid var(--gray-200);
  border-radius: 20px;
  padding: 4px;
  box-shadow: var(--shadow);
}

.theme-toggle.high-contrast-active {
  background: var(--hc-card);
  border-color: var(--hc-border);
}

.theme-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 15px;
  background: transparent;
  color: var(--gray-800);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.theme-btn:hover {
  background: var(--gray-200);
}

.theme-btn-main {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--burgundy);
  color: var(--white);
  padding: 6px 14px;
}

.theme-btn-main:hover {
  background: var(--burgundy-700);
}

.theme-indicator {
  font-size: 18px;
  line-height: 1;
}

.theme-label {
  font-size: 14px;
  font-weight: 600;
}

/* Стили для режима слабовидящих */
body.high-contrast .theme-btn {
  color: var(--hc-text);
  background: var(--hc-card);
  border-color: var(--hc-border);
}

body.high-contrast .theme-btn:hover {
  background: #2a2a2a;
}

body.high-contrast .theme-btn-main {
  background: var(--hc-accent);
  color: #000000;
}

body.high-contrast .theme-btn-main:hover {
  background: #ffdd55;
  color: #000000;
}

/* МОБИЛЬНЫЙ ПЕРЕКЛЮЧАТЕЛЬ */
.mobile-theme-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  display: none;
}

.mobile-theme-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--burgundy);
  color: white;
  border: none;
  font-size: 24px;
  box-shadow: 0 4px 15px rgba(122, 23, 50, 0.4);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-theme-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(122, 23, 50, 0.6);
}

.mobile-theme-btn.active {
  background: var(--hc-accent);
  color: #000000;
}

/* Улучшенная доступность в режиме слабовидящих */
body.high-contrast header {
  background: var(--hc-card) !important;
  border-bottom: 2px solid var(--hc-border) !important;
  box-shadow: 0 4px 8px rgba(255,255,255,0.1) !important;
}

body.high-contrast .brand h1,
body.high-contrast .about h2,
body.high-contrast .services h3,
body.high-contrast .card h4,
body.high-contrast footer strong {
  color: var(--hc-accent) !important;
  text-shadow: 0 0 2px rgba(255,255,255,0.3) !important;
}

body.high-contrast .btn-primary {
  background: var(--hc-accent) !important;
  color: #000000 !important;
  box-shadow: 0 4px 12px rgba(255,204,0,0.4) !important;
}

body.high-contrast .btn-primary:hover {
  background: #ffdd55 !important;
  box-shadow: 0 6px 16px rgba(255,204,0,0.6) !important;
}

body.high-contrast a:not(.btn),
body.high-contrast .phone {
  color: var(--hc-accent) !important;
  text-decoration: underline !important;
}

body.high-contrast .search,
body.high-contrast .card,
body.high-contrast .about {
  border: 2px solid var(--hc-border) !important;
  background: var(--hc-card) !important;
}

body.high-contrast .kebab-menu {
  background: var(--hc-card) !important;
  border: 2px solid var(--hc-border) !important;
}

body.high-contrast input,
body.high-contrast select,
body.high-contrast button {
  border: 2px solid var(--hc-border) !important;
  background: var(--hc-input) !important;
  color: var(--hc-text) !important;
}

body.high-contrast .price {
  color: var(--hc-accent) !important;
  font-weight: bold !important;
}

body.high-contrast dialog {
  border: 3px solid var(--hc-border) !important;
  background: var(--hc-card) !important;
  color: var(--hc-text) !important;
}

/* Адаптивность для мобильных */
@media (max-width: 768px) {
  .theme-toggle-container {
    display: none;
  }
  
  .mobile-theme-toggle {
    display: block;
  }
  
  body.high-contrast .mobile-theme-btn {
    background: var(--hc-accent) !important;
    color: #000000 !important;
  }
  
  body.high-contrast .mobile-theme-btn.active {
    background: #ffaa00 !important;
    color: #000000 !important;
  }
}

@media (max-width: 480px) {
  .mobile-theme-btn {
    width: 48px;
    height: 48px;
    font-size: 20px;
  }
}

/* Остальные стили без изменений */
header{position:sticky;top:0;z-index:50;background:var(--white);border-bottom:1px solid var(--gray-200);box-shadow:0 2px 10px rgba(0,0,0,.04)}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:inherit}
.brand h1{font-size:1.5rem;line-height:1.1;margin:0}

.main-logo {
  height: 45px;
  width: auto;
  display: block;
  border-radius: 8px; 
  box-shadow: var(--shadow); 
}

.doc-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: var(--shadow);
  background-color: #f8f9fa; 
}

.kebab{border:1px solid var(--gray-200);background:var(--white);border-radius:12px;padding:8px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:8px}
.kebab:hover{background:#fafafa}
.kebab-menu{position:absolute;right:20px;top:64px;background:var(--white);border:1px solid var(--gray-200);border-radius:12px;box-shadow:var(--shadow);padding:6px;width:220px;display:none}
.kebab-menu.open{display:block}
.kebab-menu a{display:flex;gap:10px;align-items:center;padding:10px 12px;border-radius:10px;color:inherit;text-decoration:none}
.kebab-menu a:hover{background:#f3f4f6}

.cta{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.btn{border:0;border-radius:999px;padding:10px 16px;cursor:pointer;font-weight:600;letter-spacing:.2px}
.btn-primary{background:var(--burgundy);color:var(--white);box-shadow:0 6px 18px rgba(122,23,50,.25)}
.btn-primary:hover{background:var(--burgundy-700)}
.phone{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--burgundy);text-decoration:none;white-space:nowrap}

.search-wrap{padding:1.5rem 0 0.5rem}
.search{display:flex;gap:12px;align-items:center;background:var(--white);border:1px solid var(--gray-200);border-radius:999px;padding:8px 12px;box-shadow:var(--shadow)}
.search input{border:0;outline:0;flex:1;font-size:1rem;background:transparent}
.search button{border:0;border-radius:999px;padding:8px 12px;cursor:pointer;background:#f3f4f6}
.search button:hover{background:#ebecef}

.about{margin-top:1.5rem;background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:1.5rem;box-shadow:var(--shadow);display:grid;gap:1rem}
.about h2{margin:0 0 0.5rem 0;font-size:1.6rem}
.about p{font-size:1rem;line-height:1.6;color:var(--gray-800)}
.badges{display:flex;gap:0.6rem;flex-wrap:wrap}
.badge{background:#f3f4f6;border-radius:999px;padding:0.4rem 0.6rem;font-size:0.8rem}

.services{margin:1.5rem 0 3rem}
.services h3{margin:0 0 1rem 0;font-size:1.5rem}
.grid{display:grid;gap:1rem;grid-template-columns:repeat(12,1fr)}
.card{grid-column:span 4;background:#fff;border:1px solid var(--gray-200);border-radius:1rem;padding:1rem;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:0.8rem}
.card.hidden { display: none; }
.card h4{margin:0;font-size:1.1rem;color:var(--burgundy)}
.card p{margin:0;color:var(--gray-500);font-size:0.9rem}
.card .price{margin-top:auto;font-weight:700;font-size:1rem;color:var(--burgundy)}
.card .action{margin-top:0.5rem;align-self:flex-start;background:var(--burgundy);color:#fff;border:0;border-radius:0.6rem;padding:0.6rem 0.8rem;cursor:pointer}
.action:hover{background:var(--burgundy-700)}
.muted{color:var(--gray-500);font-size:0.9rem}

footer{border-top:1px solid var(--gray-200);background:var(--white);color:var(--gray-500);padding:1.5rem 0;font-size:0.9rem}

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

@media (max-width: 960px){
  .grid{grid-template-columns:repeat(6,1fr)}
  .card{grid-column:span 3}
}
@media (max-width: 768px){
  .grid{grid-template-columns:repeat(1,1fr)}
  .card{grid-column:span 1 !important}
  .brand h1{font-size:1.4rem}
  .search-wrap{padding-top:10px}
  .kebab-menu{right:12px}
  .topbar{padding:10px 0; flex-direction: column; gap: 12px;}
  .cta{width:100%; justify-content: center;}
}
@media (max-width: 640px){
  .brand h1{font-size:1.3rem}
  .search button{padding:6px 10px;}
  .btn{padding:8px 14px; font-size:14px;}
}
#bookModal {
  margin: auto;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  position: absolute;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* Для лучшего отображения на мобильных */
@media (max-width: 480px) {
  #bookModal {
    width: 95% !important;
    max-width: 95% !important;
    margin: 10px;
    top: 50%;
    transform: translate(-50%, -50%);
  }
}

/* Фон затемнения для модального окна */
dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}
</style>