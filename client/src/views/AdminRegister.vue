<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100 flex-center bg-gradient-blue">
        <form @submit.prevent="handleLogin" class="bg-white p-8 rounded shadow-md w-full max-w-md">
            <h2 class="text-2xl font-semibold mb-6 text-center">Регистрация администратора</h2>
            <div class="mb-4">
                <label class="block mb-1">Фамилия</label>
                <input v-model="lastName" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Имя</label>
                <input v-model="firstName" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Отчество</label>
                <input v-model="patronymic" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Почта</label>
                <input v-model="email" type="email" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Пароль</label>
                <input v-model="password" type="password" class="w-full border px-3 py-2 rounded" required />
            </div>
            <button type="submit" class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">Зарегистрироваться</button>
            <div class="account">
                Есть аккаунт? <router-link to="/admin/login">Войти</router-link>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const firstName = ref('')
const lastName = ref('')
const patronymic = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function handleLogin() {
    error.value = ''
    try {
        const response = await api.post('/admin/register', {
            name: [lastName.value, firstName.value, patronymic.value].join(' '),
            email: email.value,
            password: password.value,
        })

        console.log(response, response.data);
        router.push('/admin/login') 
    } catch (err) {
        error.value = 'Ошибка входа: ' + (err.response?.data?.message || 'проверьте логин и пароль')
    }
}
</script>