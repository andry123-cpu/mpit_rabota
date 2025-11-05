import { createApp } from 'vue'
import App from './App.vue'

// Должно монтироваться в элемент с id="app"
const app = createApp(App)
app.mount('#app')