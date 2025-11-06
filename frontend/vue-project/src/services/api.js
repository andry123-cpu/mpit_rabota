// src/services/auth.js

export const login = async (username, password) => {
  try {
    // Здесь будет реальный запрос к API когда он будет готов
    console.log('Попытка входа с данными:', { username, password });
    
    // Временная заглушка для демонстрации
    if (username === 'doctor' && password === 'password') {
      // Генерируем временный токен
      const fakeToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' + 
                       'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRvY3RvciBJdmFub3YiLCJpYXQiOjE1MTYyMzkwMjJ9.' +
                       'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';
      
      localStorage.setItem('token', fakeToken);
      localStorage.setItem('user', JSON.stringify({
        username: username,
        name: 'Доктор Иванов',
        role: 'doctor'
      }));
      
      return {
        access: fakeToken,
        user: {
          username: username,
          name: 'Доктор Иванов',
          role: 'doctor'
        }
      };
    } else {
      throw new Error('Неверное имя пользователя или пароль');
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