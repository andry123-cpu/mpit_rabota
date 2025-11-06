export const login = async (username, password) => {
  try {
    console.log('Попытка входа с данными:', { username, password });

    let response = await fetch('http://26.167.186.152:8000/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    
    if (response.status === 200) {
        const data = await response.json(); 
        const token = data.token; 
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