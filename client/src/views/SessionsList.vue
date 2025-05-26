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
                    <th>Время сессии</th>
                    <th>Время теста</th>
                    <th>Макс. балл</th>
                    <th>Завершена</th>
                    <!-- <th>Типы вопросов</th> -->
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="session in sessions" :key="session.id">
                    <td>
                        <div class="session-id">{{ session.id }}</div>
                    </td>
                    <td>{{ formatDate(session.date_started) }}</td>
                    <td>{{ formatDuration(session.duration) }}</td>
                    <td>{{ formatDuration(session.test_duration) }}</td>
                    <td>{{ session.max_score }}</td>
                    <td>{{ session.finished ? 'Да' : 'Нет' }}</td>
                    <!-- <td>
                        <ul>
                            <li v-for="(val, type) in session.questions_types" :key="type">
                                {{ readableQuestionType(type) }}
                            </li>
                        </ul>
                    </td> -->
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
                const response = await api.get('/admin/get-sessions', {});
                console.log(response)
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
    border-radius: 10px;
}

th,
td {
    padding: 0.8rem;
    vertical-align: center;
}

.session-id {
    font-weight: bold;
}

tr {
    border-bottom: 1px solid #e0e0e0;
}

th {
    padding: 1rem 0.8rem;
    background-color: #e1eeff;
    text-align: left;
}

thead tr:first-child th:first-child {
    border-radius: 10px 0 0 10px;
}

thead tr:first-child th:last-child {
    border-radius: 0 10px 10px 0;
}

thead tr:first-child,
tr:last-child {
    border: none;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>