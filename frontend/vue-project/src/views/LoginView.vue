<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/auth'

const username = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)
const router = useRouter()

const handleLogin = async () => {
  console.log('производится аунтификация');
  if (!username.value || !password.value) {
    error.value = 'Пожалуйста, заполните все поля';
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    await login(username.value, password.value);
    router.push('/dashboard');
  } catch (err) {
    error.value = err.message || 'Ошибка при входе';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
<h2> Вход в систему </h2>
<p> Клиника «Оптимед» - панель управления </p>

<form @submit.prevent="handleLogin">
  <label for="username">Имя пользователя</label>
  <input type="text" v-model="username">

  <label for="password">Пароль</label>
  <input type="text" v-model="password">

  <button type="submit">
    Войти
  </button>
</form>

</template>