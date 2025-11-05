<template>
  <div class="dashboard-shell">
    <div class="topline"></div>
    <div class="wrap">
      <div class="shell">
        <aside class="sidebar">
          <div class="logo">ОПТИМЕД</div>
          <nav class="nav">
            <router-link to="/dashboard" class="nav-link" :class="{ active: currentTab === 'home' }" @click="currentTab = 'home'">Главная</router-link>
            <router-link to="/dashboard/patients" class="nav-link" :class="{ active: currentTab === 'patients' }" @click="currentTab = 'patients'">Пациенты</router-link>
            <router-link to="/dashboard/schedule" class="nav-link" :class="{ active: currentTab === 'schedule' }" @click="currentTab = 'schedule'">Расписание</router-link>
            <router-link to="/dashboard/reports" class="nav-link" :class="{ active: currentTab === 'reports' }" @click="currentTab = 'reports'">Отчётность</router-link>
          </nav>
        </aside>

        <section class="content">
          <div class="toolbar">
            <div>
              <h1 class="title">Добро пожаловать, доктор {{ doctorName }}!</h1>
              <div class="subtitle">{{ formattedTodayDate }}</div>
            </div>
            <button class="menu-btn" aria-label="Меню" @click="toggleMobileMenu">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </button>
          </div>

          <div class="grid">
            <!-- расписание -->
            <div class="card">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
                <h3 style="margin:0">{{ scheduleTitle }}</h3>
                <div class="day-nav">
                  <button class="pill" @click="prevDay" title="Предыдущий день">‹</button>
                  <button class="pill" @click="nextDay" title="Следующий день">›</button>
                </div>
              </div>
              <div class="list">
                <div v-for="(item, index) in scheduleItems" :key="index" class="row">
                  <div class="time">{{ item.time }}</div>
                  <div>
                    <div class="who">{{ item.who }}</div>
                    <div class="desc">{{ item.desc }}</div>
                  </div>
                </div>
                <div v-if="scheduleItems.length === 0" class="no-appointments">
                  Сегодня нет запланированных приёмов
                </div>
              </div>
            </div>

            <!-- календарь -->
            <div class="card calendar">
              <h3>Календарь</h3>
              <div class="cal-head">
                <button class="menu-btn" @click="prevMonth" aria-label="Предыдущий месяц">‹</button>
                <strong>{{ currentMonthName }}</strong>
                <button class="menu-btn" @click="nextMonth" aria-label="Следующий месяц">›</button>
              </div>
              <table class="cal" aria-label="Календарь">
                <thead>
                  <tr>
                    <th v-for="(day, index) in weekdays" :key="index">{{ day }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(week, weekIndex) in calendar" :key="weekIndex">
                    <td 
                      v-for="(day, dayIndex) in week" 
                      :key="dayIndex"
                      :class="{
                        'dim': !day.isCurrentMonth,
                        'today': day.isToday,
                        'selected': day.isSelected
                      }"
                      @click="selectDay(day)"
                    >
                      {{ day.date }}
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="muted">Кликните по дате, чтобы увидеть расписание.</div>
            </div>

            <div class="card" style="grid-column:1 / span 1;">
              <h3>Уведомления</h3>
              <div v-if="notifications.length > 0">
                <div v-for="(notification, index) in notifications" :key="index" class="notification-item">
                  <div class="notification-time">{{ notification.time }}</div>
                  <div class="notification-content">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-details">{{ notification.details }}</div>
                  </div>
                </div>
              </div>
              <p v-else class="muted">У вас нет новых уведомлений</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Реактивные данные
const doctorName = ref('Иванов')
const currentTab = ref('home')
const today = ref(new Date())
const selectedDate = ref(new Date(today.value.getFullYear(), today.value.getMonth(), today.value.getDate()))
const calendarViewDate = ref(new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1))

// Массивы для локализации
const MONTHS = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
const WEEKDAYS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
const FULL_WEEKDAYS = ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

// Уведомления
const notifications = ref([
  {
    time: 'Завтра в 12:00',
    title: 'Приём с пациентом',
    details: 'Анна Антонова'
  },
  {
    time: '25 ноября',
    title: 'Напоминание',
    details: 'Отправить результаты анализов пациенту Петрову'
  }
])

// Вычисляемые свойства
const formattedTodayDate = computed(() => {
  return `Сегодня, ${today.value.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })}`
})

const currentMonthName = computed(() => {
  return MONTHS[calendarViewDate.value.getMonth()]
})

const scheduleTitle = computed(() => {
  const isToday = selectedDate.value.toDateString() === today.value.toDateString()
  if (isToday) return 'Расписание на сегодня'
  
  const weekday = FULL_WEEKDAYS[selectedDate.value.getDay()]
  const dateStr = selectedDate.value.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
  return `Расписание: ${weekday}, ${dateStr}`
})

const calendar = computed(() => {
  const year = calendarViewDate.value.getFullYear()
  const month = calendarViewDate.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const startDay = new Date(firstDay)
  
  // Найти понедельник недели, на которую приходится 1-е число
  const shift = (firstDay.getDay() + 6) % 7 // пн=0
  startDay.setDate(startDay.getDate() - shift)
  
  const weeks = []
  
  for (let week = 0; week < 6; week++) {
    const days = []
    for (let day = 0; day < 7; day++) {
      const currentDate = new Date(startDay.getFullYear(), startDay.getMonth(), startDay.getDate() + (week * 7 + day))
      const isCurrentMonth = currentDate.getMonth() === month
      const isToday = currentDate.toDateString() === today.value.toDateString()
      const isSelected = currentDate.toDateString() === selectedDate.value.toDateString()
      
      days.push({
        date: currentDate.getDate(),
        isCurrentMonth,
        isToday,
        isSelected,
        fullDate: new Date(currentDate)
      })
    }
    weeks.push(days)
  }
  
  return weeks
})

const scheduleItems = computed(() => {
  return getScheduleFor(selectedDate.value)
})

// Методы
const getScheduleFor = (date) => {
  const d = date.getDate()
  const items = []
  const count = (d % 3) + 2 // 2..4 приёма
  
  const names = [
    'Сергей Сергеев', 'Пётр Петров', 'Алексей Алексеев', 
    'Антон Антонов', 'Мария Иванова', 'Ольга Смирнова'
  ]
  
  const descriptions = [
    'Первичный приём',
    'Повторный приём',
    'Онлайн-консультация',
    'Плановый осмотр',
    'Консультация по результатам анализов'
  ]
  
  for (let i = 0; i < count; i++) {
    const hour = 9 + i
    items.push({
      time: `${hour}:00`,
      who: names[(d + i) % names.length],
      desc: descriptions[(d + i) % descriptions.length]
    })
  }
  
  return items
}

const selectDay = (day) => {
  if (day.isCurrentMonth) {
    selectedDate.value = new Date(day.fullDate)
    // Автоматически обновляем вид календаря на месяц выбранной даты
    calendarViewDate.value = new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1)
  }
}

const prevMonth = () => {
  const newDate = new Date(calendarViewDate.value)
  newDate.setMonth(newDate.getMonth() - 1)
  calendarViewDate.value = newDate
}

const nextMonth = () => {
  const newDate = new Date(calendarViewDate.value)
  newDate.setMonth(newDate.getMonth() + 1)
  calendarViewDate.value = newDate
}

const prevDay = () => {
  const newDate = new Date(selectedDate.value)
  newDate.setDate(newDate.getDate() - 1)
  selectedDate.value = newDate
  updateCalendarView()
}

const nextDay = () => {
  const newDate = new Date(selectedDate.value)
  newDate.setDate(newDate.getDate() + 1)
  selectedDate.value = newDate
  updateCalendarView()
}

const updateCalendarView = () => {
  calendarViewDate.value = new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1)
}

const toggleMobileMenu = () => {
  // Здесь можно добавить логику для мобильного меню
  console.log('Мобильное меню toggled')
}

// Инициализация
onMounted(() => {
  // Можно добавить загрузку данных с API здесь
  console.log('Dashboard загружен')
})
</script>

<style scoped>
.topline {
  width: 100%;
  height: 6px;
  background: var(--burgundy);
  box-shadow: 0 4px 16px rgba(122, 23, 50, 0.35) inset;
}

.wrap {
  max-width: var(--container);
  margin: 22px auto;
  padding: 0 18px;
}

.shell {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: var(--shadow);
  display: grid;
  grid-template-columns: 260px 1fr;
  overflow: hidden;
}

.sidebar {
  background: linear-gradient(#fbfbfc, #f0f2f5);
  border-right: 1px solid var(--border);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.logo {
  font-weight: 800;
  letter-spacing: 0.4px;
  font-size: 26px;
  color: var(--burgundy);
}

.nav {
  display: grid;
  gap: 8px;
}

.nav-link {
  display: block;
  text-decoration: none;
  color: #111827;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.nav-link.active {
  background: #eef0f4;
  border-color: #e8ebf0;
  font-weight: 600;
}

.nav-link:hover {
  background: #f4f6f8;
}

.content {
  padding: 28px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.title {
  font-size: 34px;
  font-weight: 700;
  margin: 0;
  color: var(--text);
}

.subtitle {
  color: var(--muted);
  font-size: 16px;
  margin-top: 6px;
}

.menu-btn {
  border: 1px solid var(--border);
  background: #fff;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.menu-btn:hover {
  background: #f8f9fa;
}

.grid {
  display: grid;
  grid-template-columns: 1.4fr 0.9fr;
  gap: 18px;
  margin-top: 22px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 18px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.card h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: var(--text);
}

.list {
  display: grid;
  gap: 14px;
}

.row {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.row:last-child {
  border-bottom: none;
}

.time {
  font-weight: 700;
  min-width: 56px;
  color: var(--burgundy);
}

.who {
  font-weight: 600;
  color: var(--text);
}

.desc {
  color: var(--muted);
  margin-top: 2px;
  font-size: 14px;
}

.no-appointments {
  text-align: center;
  color: var(--muted);
  padding: 20px;
  font-style: italic;
}

.calendar {
  display: grid;
  gap: 12px;
}

.cal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--muted);
  margin-bottom: 12px;
}

.cal {
  width: 100%;
  border-collapse: separate;
  border-spacing: 6px;
  text-align: center;
  color: #111827;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.cal th {
  font-size: 12px;
  color: var(--muted);
  font-weight: 600;
  padding: 8px 0;
  background: #f8f9fa;
}

.cal td {
  padding: 8px 0;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;
  font-weight: 500;
}

.cal td:hover {
  background: #f8f9fa;
  transform: scale(1.05);
}

.cal td.dim {
  color: #c0c6cf;
  opacity: 0.7;
}

.cal td.today {
  background: var(--burgundy);
  color: #fff;
  border-color: var(--burgundy);
  font-weight: bold;
}

.cal td.selected {
  outline: 2px solid var(--burgundy);
  outline-offset: 2px;
  background: #fff5f5;
}

.muted {
  color: var(--muted);
  font-size: 14px;
  margin-top: 8px;
}

.day-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pill {
  border: 1px solid var(--border);
  padding: 6px 10px;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  min-width: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.pill:hover {
  background: #f8f9fa;
  transform: scale(1.1);
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-time {
  min-width: 90px;
  color: var(--burgundy);
  font-weight: 600;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  color: var(--text);
}

.notification-details {
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 960px) {
  .shell {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    display: none;
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
  
  .toolbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .title {
    font-size: 28px;
  }
}

@media (max-width: 640px) {
  .cal {
    font-size: 12px;
  }
  
  .time, .notification-time {
    min-width: 40px;
    font-size: 14px;
  }
  
  .who, .notification-title {
    font-size: 15px;
  }
}
</style>