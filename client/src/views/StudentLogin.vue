<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100 flex-center bg-gradient-blue">
        <form @submit.prevent="handleLogin" class="bg-white p-8 rounded shadow-md w-full max-w-md">
            <h2 class="text-2xl font-semibold mb-6 text-center">Вход студента</h2>
            <div class="mb-4">
                <label class="block mb-1">ID сессии</label>
                <input v-model="sessionId" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Имя</label>
                <input v-model="firstName" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Фамилия</label>
                <input v-model="lastName" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Отчество</label>
                <input v-model="patronymic" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <div class="mb-4">
                <label class="block mb-1">Группа</label>
                <input v-model="group" type="text" class="w-full border px-3 py-2 rounded" required />
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Войти</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const sessionId = ref('')
const firstName = ref('')
const lastName = ref('')
const patronymic = ref('')
const group = ref('')

async function handleLogin() {
    error.value = ''
    try {
        const response = await api.post('/student/login', {
            name: [firstName.value, lastName.value, patronymic.value].join(' '),
            group: group,
            session_id: sessionId
        })

        console.log(response, response.data);
        router.push('/test') 
    } catch (err) {
        error.value = 'Ошибка входа: ' + (err.response?.data?.message || 'проверьте корректность введенных данных')
    }
}
</script>