<script setup>
import { ref, onMounted } from 'vue'

const doctorName = ref('Иванов')
const today = ref(new Date())
const appointments = ref([
  { time: '09:00', patient: 'Сергей Сергеев', type: 'Первичный приём' },
  { time: '10:30', patient: 'Мария Иванова', type: 'Повторный приём' },
  { time: '12:00', patient: 'Анна Антонова', type: 'Онлайн-консультация' }
])
</script>

<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="container">
        <h1>Панель врача — {{ doctorName }}</h1>
        <p class="date">Сегодня, {{ today.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) }}</p>
        <router-link to="/" class="btn btn-back">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px">
            <path d="M19 12H5M5 12l6 6M5 12l6-6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Вернуться на главную
        </router-link>
      </div>
    </header>

    <div class="container">
      <div class="dashboard-content">
        <div class="card">
          <h2>Сегодняшние приёмы</h2>
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

        <div class="stats-grid">
          <div class="stat-card">
            <h3>Всего пациентов</h3>
            <div class="stat-value">1,245</div>
            <div class="stat-trend">↑ 12% за месяц</div>
          </div>
          <div class="stat-card">
            <h3>Сегодня приёмов</h3>
            <div class="stat-value">{{ appointments.length }}</div>
            <div class="stat-trend">План: 8</div>
          </div>
          <div class="stat-card">
            <h3>Критические случаи</h3>
            <div class="stat-value">3</div>
            <div class="stat-trend">Требуют внимания</div>
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
}

.btn-back:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}

.dashboard-content {
  padding: 40px 0;
}

.card {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.card h2 {
  font-size: 1.8rem;
  margin: 0 0 20px 0;
  color: white;
}

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
}

.appointment-item:hover {
  transform: translateX(5px);
  background: rgba(255,255,255,0.12);
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
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
}

@media (max-width: 768px) {
  .dashboard-header h1 {
    font-size: 2rem;
  }
  
  .card {
    padding: 20px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>