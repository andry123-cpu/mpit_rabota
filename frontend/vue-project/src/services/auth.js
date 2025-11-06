// src/services/auth.js

export const login = async (username, password) => {
  try {
    // Здесь будет реальный запрос к API когда он будет готов
    console.log('Попытка входа с данными:', { username, password });

    let response = await fetch('http://26.167.186.152:8000/api/auth/login', {
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'username': username,
            'password': password
        })
    })
    if (response.status == 200) {
        let token = await response.json().token;
        localStorage.setItem('token', token);

        return token
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