<template>
    <div class="session-results">
        <h2>Результаты сессии #{{ sessionId }}</h2>

        <div v-if="loading">Загрузка результатов...</div>
        <div v-else-if="results.length === 0">Нет результатов для этой сессии</div>

        <table v-else>
            <thead>
                <tr>
                    <th>ФИО студента</th>
                    <th>Правильные ответы</th>
                    <th>Всего вопросов</th>
                    <th>Процент</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="res in results" :key="res.student_id">
                    <td>{{ res.name }}</td>
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
import api from '@/api';

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
                const response = await api.get(`/admin/get-results/${this.sessionId}`, {});
                console.log(response)
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
    max-width: 300px;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>