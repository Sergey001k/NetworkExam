import axios from 'axios'
import Cookies from 'js-cookie'

const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
})

// Добавляем токен в заголовки запросов
api.interceptors.request.use(config => {
    const token = Cookies.get('access-token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export default api
