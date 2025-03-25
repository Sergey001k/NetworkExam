<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { postData } from '../server/api';
import router from '@/router';

const name = ref('');
const surname = ref('');
const email = ref('');
const password = ref('');
const isLoading = ref(false);
const error = ref('');

const handleClick = async () => {
  if (!name.value || !email.value || !password.value) {
    error.value = 'Заполните все обязательные поля';
    return;
  }

  isLoading.value = true;
  error.value = '';
  const token = localStorage.getItem('authToken');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}
  try {
    const resp = await postData('admin/login', {
      name: name.value,
      surname: surname.value,
      email: email.value,
      password: password.value
    });

    if (resp['acces-token']) {
      console.log('Успешная авторизация');

      localStorage.setItem('authToken', resp['acces-token']);
      localStorage.setItem('tokenType', resp['token-type']);

      axios.defaults.headers.common['Authorization'] =
        `${resp['token-type']} ${resp['acces-token']}`;

      const acces_token = resp['acces-token'];
      const token_type = resp['token-type'];


      const createResp = await postData('admin/create', {
        questions: acces_token,
        duration: token_type
      });
      if (createResp != ''){
        router.push('/admin');
      }else{
        router.push('/login');
      }
    }
  } catch (err) {
    error.value = 'Ошибка соединения';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};
</script>


<template>
  <div class="login-container">
    <h2 class="login-title">Войти</h2>
    <div class="input-group">
      <label class="input-label">Имя</label>
      <input type="text" v-model="name" class="input-field" />
    </div>
    <div class="input-group">
      <label class="input-label">Фамилия</label>
      <input type="text" v-model="surname" class="input-field" />
    </div>
    <div class="input-group">
      <label class="input-label">Почта</label>
      <input type="text" v-model="email" class="input-field" />
    </div>
    <div class="input-group">
      <label class="input-label">Пароль</label>
      <input type="password" v-model="password" class="input-field" />
    </div>
    <button @click="handleClick" class="login-button">ВОЙТИ</button>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: white;
  font-family: Arial, sans-serif;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.input-group {
  margin-bottom: 15px;
}

.input-label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #555;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #4a90e2;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  text-transform: uppercase;
}

.login-button:hover {
  background-color: #3a7bc8;
}
</style>
