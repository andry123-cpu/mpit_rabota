<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const doctorName = ref('Иванов')
const today = ref(new Date())
const selectedDate = ref(new Date(today.value.getFullYear(), today.value.getMonth(), today.value.getDate()))
const calendarViewDate = ref(new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1))
const isLoading = ref(false)
const error = ref(null)

// Методы навигации
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

const selectDay = (date) => {
  selectedDate.value = new Date(date)
  updateCalendarView()
}

const updateCalendarView = () => {
  calendarViewDate.value = new Date(selectedDate.value.getFullYear(), selectedDate.value.getMonth(), 1)
}

// Демо-данные для расписания
const appointments = ref([
  { time: '09:00', patient: 'Сергей Сергеев', type: 'Первичный приём' },
  { time: '10:30', patient: 'Мария Иванова', type: 'Повторный приём' },
  { time: '12:00', patient: 'Анна Антонова', type: 'Онлайн-консультация' },
  { time: '14:30', patient: 'Пётр Петров', type: 'Плановый осмотр' },
  { time: '16:00', patient: 'Ольга Смирнова', type: 'Консультация по анализам' }
])

// Демо-статистика
const stats = ref([
  { label: 'Всего пациентов', value: '1,245', trend: '+12%' },
  { label: 'Сегодня приемов', value: '5', trend: '+2' },
  { label: 'Критические случаи', value: '1', trend: '-1' },
  { label: 'Телемедицина', value: '2', trend: '+1' }
])

onMounted(() => {
  // Здесь будет загрузка данных с API
  console.log('Дашборд загружен')
})
</script>

<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="container">
        <div class="header-content">
          <h1>Панель врача — {{ doctorName }}</h1>
          <p class="date">{{ today.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
          <router-link to="/" class="btn-back">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px">
              <path d="M19 12H5M5 12l6 6M5 12l6-6" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Вернуться на главную
          </router-link>
        </div>
      </div>
    </header>

    <div class="container">
      <div class="dashboard-content">
        <!-- Статистика -->
        <div class="stats-grid">
          <div v-for="(stat, index) in stats" :key="index" class="stat-card">
            <h3>{{ stat.label }}</h3>
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-trend" :class="{ positive: stat.trend.startsWith('+'), negative: stat.trend.startsWith('-') }">
              {{ stat.trend }}
            </div>
          </div>
        </div>

        <!-- Расписание и календарь -->
        <div class="cards-row">
          <!-- Расписание -->
          <div class="card">
            <div class="card-header">
              <h2>Сегодняшние приёмы</h2>
              <div class="day-nav">
                <button class="pill" @click="prevDay" title="Предыдущий день">‹</button>
                <button class="pill" @click="nextDay" title="Следующий день">›</button>
              </div>
            </div>
            
            <div class="appointments-list">
              <div v-for="(appt, index) in appointments" :key="index" class="appointment-item">
                <div class="appointment-time">{{ appt.time }}</div>
                <div class="appointment-details">
                  <div class="patient-name">{{ appt.patient }}</div>
                  <div class="appointment-type">{{ appt.type }}</div>
                </div>
              </div>
              
              <div v-if="appointments.length === 0" class="no-appointments">
                Сегодня нет запланированных приёмов
              </div>
            </div>
          </div>

          <!-- Календарь и уведомления -->
          <div class="side-column">
            <!-- Календарь -->
            <div class="card calendar-card">
              <h2>Календарь</h2>
              <div class="cal-head">
                <button class="menu-btn" @click="prevMonth" aria-label="Предыдущий месяц">‹</button>
                <strong>{{ calendarViewDate.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' }) }}</strong>
                <button class="menu-btn" @click="nextMonth" aria-label="Следующий месяц">›</button>
              </div>
              <table class="cal" aria-label="Календарь">
                <thead>
                  <tr>
                    <th v-for="(day, index) in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']" :key="index">{{ day }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="week in 6" :key="week">
                    <td 
                      v-for="day in 7" 
                      :key="day"
                      class="calendar-day"
                      :class="{
                        'today': isToday(week, day),
                        'selected': isSelected(week, day),
                        'dim': !isCurrentMonth(week, day)
                      }"
                      @click="selectDay(week, day)"
                    >
                      {{ getDayNumber(week, day) }}
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="muted">Кликните по дате, чтобы увидеть расписание.</div>
            </div>

            <!-- Уведомления -->
            <div class="card notifications-card">
              <h2>Уведомления</h2>
              <div class="notification-item">
                <div class="notification-time">Завтра в 12:00</div>
                <div class="notification-content">
                  <div class="notification-title">Приём с пациентом</div>
                  <div class="notification-details">Анна Антонова</div>
                </div>
              </div>
              <div class="notification-item">
                <div class="notification-time">25 ноября</div>
                <div class="notification-content">
                  <div class="notification-title">Напоминание</div>
                  <div class="notification-details">Отправить результаты анализов пациенту Петрову</div>
                </div>
              </div>
              <div class="notification-item">
                <div class="notification-time">Сегодня</div>
                <div class="notification-content">
                  <div class="notification-title">Критический случай</div>
                  <div class="notification-details">Сергей Сергеев требует немедленного внимания</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.dashboard-header {
  background: rgba(0,0,0,0.2);
  padding: 20px 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin: 0 0 10px 0;
  background: linear-gradient(to right, #fff, #a0aec0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.date {
  color: rgba(255,255,255,0.8);
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.btn-back {
  background: rgba(255,255,255,0.1);
  color: white;
  border: 1px solid rgba(255,255,255,0.2);
  padding: 8px 16px;
  border-radius: 20px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  width: fit-content;
  font-weight: 500;
}

.btn-back:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-content {
  padding: 40px 0;
}

/* Стили для карточек и сетки */
.cards-row {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 30px;
}

.side-column {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.card {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
}

.card h2 {
  font-size: 1.8rem;
  margin: 0 0 20px 0;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* Стили для расписания */
.appointments-list {
  display: grid;
  gap: 15px;
}

.appointment-item {
  display: flex;
  gap: 20px;
  padding: 15px;
  background: rgba(255,255,255,0.08);
  border-radius: 15px;
  transition: transform 0.2s ease;
  border: 1px solid rgba(255,255,255,0.05);
}

.appointment-item:hover {
  transform: translateX(5px);
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.15);
}

.appointment-time {
  min-width: 80px;
  font-weight: bold;
  font-size: 1.2rem;
  color: #ffd700;
}

.patient-name {
  font-weight: 600;
  font-size: 1.1rem;
  color: white;
}

.appointment-type {
  color: rgba(255,255,255,0.8);
  font-size: 0.95rem;
}

.no-appointments {
  text-align: center;
  padding: 30px;
  color: rgba(255,255,255,0.7);
  font-style: italic;
}

/* Стили для статистики */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(255,255,255,0.08);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  border: 1px solid rgba(255,255,255,0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(255,255,255,0.12);
}

.stat-card h3 {
  color: rgba(255,255,255,0.9);
  margin: 0 0 15px 0;
  font-size: 1.2rem;
  font-weight: 500;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  margin: 0 0 5px 0;
}

.stat-trend {
  color: rgba(255,255,255,0.7);
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-trend.positive {
  color: #6ee7b7;
}

.stat-trend.negative {
  color: #fca5a5;
}

/* Стили для календаря */
.calendar-card {
  flex: 1;
}

.cal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255,255,255,0.9);
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.menu-btn {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.menu-btn:hover {
  background: rgba(255,255,255,0.2);
  transform: scale(1.1);
}

.cal {
  width: 100%;
  border-collapse: separate;
  border-spacing: 4px;
  text-align: center;
}

.cal th {
  font-size: 12px;
  color: rgba(255,255,255,0.7);
  font-weight: 600;
  padding: 8px 0;
}

.cal td {
  padding: 8px 0;
  border-radius: 8px;
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.9);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cal td:hover {
  background: rgba(255,255,255,0.15);
  transform: scale(1.05);
}

.cal td.today {
  background: rgba(255, 215, 0, 0.3);
  color: #000;
  font-weight: bold;
}

.cal td.selected {
  background: rgba(102, 126, 234, 0.5);
  color: white;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.3);
}

.cal td.dim {
  color: rgba(255,255,255,0.3);
}

.muted {
  color: rgba(255,255,255,0.6);
  font-size: 0.9rem;
  margin-top: 10px;
  text-align: center;
}

/* Стили для уведомлений */
.notifications-card {
  margin-top: 0;
}

.notification-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  border-left: 3px solid rgba(255,255,255,0.2);
  transition: all 0.2s ease;
}

.notification-item:hover {
  background: rgba(255,255,255,0.12);
  border-left-color: #ffd700;
}

.notification-time {
  min-width: 90px;
  color: #ffd700;
  font-weight: 600;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  font-size: 1rem;
  color: white;
  margin-bottom: 2px;
}

.notification-details {
  color: rgba(255,255,255,0.8);
  font-size: 0.95rem;
  line-height: 1.4;
}

.day-nav {
  display: flex;
  gap: 8px;
}

.pill {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.pill:hover {
  background: rgba(255,255,255,0.2);
  transform: scale(1.1);
}

/* Вспомогательные функции для календаря (в шаблоне) */
</style>