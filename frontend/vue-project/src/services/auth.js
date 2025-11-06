// src/services/auth.js

export const login = async (username, password) => {
  try {
    console.log('Попытка входа с данными:', { username, password });

    let response = await fetch('http://26.167.186.152:8000/api/auth/login', {
        method: 'POST',
        headers: { // ИСПРАВЛЕНО: headers вместо header
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    
    if (response.status === 200) {
        const data = await response.json(); // Сначала получаем JSON
        const token = data.token; // Затем извлекаем токен
        localStorage.setItem('token', token);
        return token;
    } else {
        // Получаем детали ошибки от сервера
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || errorData.message || 'Неверное имя пользователя или пароль';
        throw new Error(errorMessage);
    }
  } catch (error) {
    console.error('Ошибка входа:', error);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};