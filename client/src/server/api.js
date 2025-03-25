import axios from 'axios';
import router from '@/router';


const API_BASE_URL = 'http://127.0.0.1:8000';



const axiosInstance = axios.create({
  baseURL: API_BASE_URL
});


axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export const fetchData = async (endpoint) => {
  try {
    const response = await axiosInstance.get(`/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
    throw error;
  }
};

export const postData = async (endpoint, data) => {
  try {
    const response = await axiosInstance.post(`/${endpoint}`, data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
    throw error;
  }
};

axiosInstance.interceptors.response.use(
  response => response,
  error =>{
    if (error.response.status == 401){
      localStorage.removeItem('authToken');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);
