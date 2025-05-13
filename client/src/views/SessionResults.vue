<template>
    <div class="session-results">
        <h2>Результаты сессии #{{ sessionId }}</h2>

        <div v-if="loading">Загрузка результатов...</div>
        <div v-else-if="results.length === 0">Нет результатов для этой сессии</div>

        <table v-else>
            <thead>
                <tr>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>ID студента</th>
                    <th>Правильных ответов</th>
                    <th>Всего вопросов</th>
                    <th>Процент</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="res in results" :key="res.student_id">
                    <td>{{ res.first_name }}</td>
                    <td>{{ res.last_name }}</td>
                    <td>{{ res.student_id }}</td>
                    <td>{{ res.correct_answers }}</td>
                    <td>{{ res.total_questions }}</td>
                    <td>{{ percent(res.correct_answers, res.total_questions) }}%</td>
                </tr>
            </tbody>
        </table>

        <button @click="$emit('back')">Назад к списку</button>

        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios'
import Cookies from 'js-cookie'

export default {
    name: 'SessionResults',
    props: ['sessionId'],
    data() {
        return {
            results: [],
            loading: true,
            error: '',
        }
    },
    mounted() {
        this.fetchResults()
    },
    methods: {
        async fetchResults() {
            try {
                const token = Cookies.get('token')
                const response = await axios.get(
                    `http://localhost:8000/admin/get-results/${this.sessionId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                this.results = response.data
            } catch (err) {
                this.error = 'Ошибка загрузки результатов.'
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        percent(correct, total) {
            if (total === 0) return 0
            return Math.round((correct / total) * 100)
        },
    },
}
</script>

<style scoped>
.session-results {
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
}

th {
    background-color: #f0f0f0;
}

button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
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