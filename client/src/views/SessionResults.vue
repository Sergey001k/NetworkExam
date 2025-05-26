<template>
    <div class="session-results">
        <h2>Результаты сессии #{{ sessionId }}</h2>

        <div v-if="loading">Загрузка результатов...</div>
        <div v-else-if="results.length === 0">Нет результатов для этой сессии</div>

        <table v-else>
            <thead>
                <tr>
                    <th>Группа</th>
                    <th>ФИО студента</th>
                    <th>Правильные ответы</th>
                    <th>Всего вопросов</th>
                    <th>Процент</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="res in results" :key="res.student_id">
                    <td>{{ res.group }}</td>
                    <td>{{ res.student_name }}</td>
                    <td>{{ res.score }}</td>
                    <td>{{ 10 }}</td>
                    <td>{{ percent(res.score, 10) }}%</td>
                </tr>
            </tbody>
        </table>

        <div class="buttons">
            <button @click="$emit('back')">Назад к списку</button>
            <button @click="exportResults()">Экспортировать результаты</button>
        </div>

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
                this.results = response.data
            } catch (err) {
                this.error = 'Ошибка загрузки результатов.'
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        async exportResults() {
            try {
                const response = await api.get(`/admin/export-results/${this.sessionId}`, {
                    responseType: 'blob'
                });

                // Формируем имя файла в нужном формате
                const now = new Date();
                const pad = (num) => String(num).padStart(2, '0');
                const formattedDate = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}.${pad(now.getMinutes())}`;
                const fileName = `Results-${formattedDate}.xlsx`;

                // Скачиваем файл
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', fileName);
                document.body.appendChild(link);
                link.click();

                // Очистка
                link.remove();
                window.URL.revokeObjectURL(url);
            } catch (err) {
                this.error = 'Ошибка экспортирования результатов';
                console.error(err);
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
    border-radius: 10px;
}

th,
td {
    padding: 0.8rem;
    vertical-align: center;
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

button {
    margin-top: 1rem;
    max-width: 300px;
}

.buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>