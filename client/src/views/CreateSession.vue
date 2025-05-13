<template>
    <div class="create-session">
        <h2>Создание новой сессии</h2>
        <form @submit.prevent="submitSession">
            <div class="session-params">
                <div class="form-group">
                    <label>Длительность сессии:</label>
                    <input v-model="duration" placeholder="Пример: P3D" required />
                </div>

                <div class="form-group">
                    <label>Длительность теста:</label>
                    <input v-model="test_duration" placeholder="Пример: P3D" required />
                </div>
            </div>

            <h3>Количество вопросов по темам</h3>
            <div class="questions-grid">
                <div v-for="(label, key) in questionTypes" :key="key" class="question-field">
                    <label>{{ label }}:</label>
                    <input type="number" min="0" v-model.number="questions[key]" />
                </div>
            </div>

            <hr />

            <button type="submit" class="submit-button">Создать сессию</button>
        </form>

        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>

<script>
import api from '../api.js'

export default {
    name: 'CreateSession',
    data() {
        return {
            duration: '',
            test_duration: '',
            questions: {
                network_address: 0,
                broadcast_address: 0,
                first_last_address: 0,
                same_network: 0,
                mask_count: 0,
                mask_range: 0,
                host_addr: 0,
            },
            questionTypes: {
                network_address: 'Адрес сети',
                broadcast_address: 'Широковещательный адрес',
                first_last_address: 'Первый и последний адрес',
                same_network: 'Одинаковая ли сеть',
                mask_count: 'Маска по количеству сетей',
                mask_range: 'Маска для диапазона адресов',
                host_addr: 'Является ли адрес адресом узла',
            },
            successMessage: '',
            errorMessage: '',
        }
    },
    methods: {
        async submitSession() {
            try {
                const response = await api.post('/admin/create-session', {
                    duration: this.duration,
                    test_duration: this.test_duration,
                    questions: this.questions,
                });
                console.log(response);
                this.successMessage = 'Сессия успешно создана!'
                this.errorMessage = ''
            } catch {
                this.errorMessage = 'Ошибка при создании сессии'
                this.successMessage = ''
            }
        },
    },
}
</script>

<style scoped>
.create-session {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

form {
    padding: 0;
    box-shadow: none;
    max-width: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.session-params {
    display: flex;
    gap: 30px;
}

.form-group input {
    padding: 0.5rem;
    width: 100%;
    box-sizing: border-box;
    margin-top: 0.3rem;
}

.questions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

.question-field label {
    display: block;
    margin-bottom: 0.3rem;
}

.question-field input {
    width: 100%;
    padding: 0.4rem;
}

.submit-button {
    margin: auto;
    max-width: 300px;
}

.success-message {
    color: green;
    text-align: center;
}

.error-message {
    color: red;
    text-align: center;
}

hr {
    width: 100%;
    height: 1px;
    background-color: #e0e0e0;
    border: none;
}
</style>