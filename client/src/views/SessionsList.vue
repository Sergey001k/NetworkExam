<template>
    <div class="sessions-list">
        <h2>Список всех сессий</h2>

        <div v-if="loading">Загрузка...</div>
        <div v-else-if="sessions.length === 0">Сессии не найдены.</div>

        <table v-else>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Дата начала</th>
                    <th>Продолжительность</th>
                    <th>Макс. балл</th>
                    <th>Завершена</th>
                    <th>Типы вопросов</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="session in sessions" :key="session.id">
                    <td>{{ session.id }}</td>
                    <td>{{ formatDate(session.date_started) }}</td>
                    <td>{{ formatDuration(session.duration) }}</td>
                    <td>{{ session.max_score }}</td>
                    <td>{{ session.finished ? 'Да' : 'Нет' }}</td>
                    <td>
                        <ul>
                            <li v-for="(val, type) in session.questions_types" :key="type" v-if="val > 0">
                                {{ readableQuestionType(type) }}
                            </li>
                        </ul>
                    </td>
                    <td>
                        <button @click="$emit('viewResults', session.id)">Результаты</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'
import api from '../api.js'

export default {
    name: 'SessionsList',
    data() {
        return {
            sessions: [],
            loading: true,
            error: '',
        }
    },
    mounted() {
        this.fetchSessions()
    },
    methods: {
        async fetchSessions() {
            try {
                const response = await api.get('/admin/get-sessions', {
                });
                console.log(response);
                this.sessions = response.data
            } catch (err) {
                this.error = 'Не удалось загрузить список сессий.'
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        formatDate(dateStr) {
            const date = new Date(dateStr)
            return date.toLocaleString()
        },
        formatDuration(seconds) {
            const days = Math.floor(seconds / 86400)
            return `${days} дн.`
        },
        readableQuestionType(key) {
            const map = {
                network_address: 'Адрес сети',
                broadcast_address: 'Широковещ. адрес',
                first_last_address: 'Первый/последний адрес',
                same_network: 'Проверка сети',
                mask_count: 'Маска по кол-ву сетей',
                mask_range: 'Маска по диапазону',
                host_addr: 'Узел?',
            }
            return map[key] || key
        },
    },
}
</script>

<style scoped>
.sessions-list {
    padding: 1rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

th,
td {
    padding: 0.7rem;
    border-bottom: 1px solid #ccc;
    vertical-align: top;
}

th {
    background-color: #f0f0f0;
    text-align: left;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

button {
    padding: 0.4rem 0.8rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>