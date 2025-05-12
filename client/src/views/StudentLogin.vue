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
            <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Войти</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const sessionId = ref('')
const firstName = ref('')
const lastName = ref('')

const handleLogin = () => {
    console.log('Студент залогинен:', { sessionId: sessionId.value, firstName: firstName.value, lastName: lastName.value })
    // Здесь будет логика входа и переход на страницу теста
}
</script>