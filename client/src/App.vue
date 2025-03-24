<script setup>
import { ref } from 'vue';
import { postData } from './server/api';

const name = ref('');
const surname = ref('');
const email = ref('');
const password = ref('');

const handleClick = async () => {
  const resp =  postData('admin',{
    Name: name.value,
    Surname: surname.value,
    Email: email.value,
    Password: password.value
  });
  if (resp['acces-token']){
    console.log(resp);
  };
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
