<template>
    <div class="flex-center bg-gradient-blue" style="padding: 2rem">
        <div class="test-page">
            <div v-if="!isFinished">
                <div class="timer">Время: {{ formattedTime }}</div>

                <div v-if="questions.length" class="question-container">
                    <h3>{{ getQuestionTitle(questions[currentQuestion]) }}</h3>
                    <p>{{ questions[currentQuestion].question.question }}</p>

                    <div v-if="questions[currentQuestion].type.includes('address')">
                        <input v-model="answers[currentQuestion]" type="text" inputmode="numeric" placeholder="0.0.0.0"
                            @input="filterIpInput"
                            :class="{ 'invalid': answers[currentQuestion] && !isValidIp(answers[currentQuestion]) }" />
                        <small class="hint">Введите IP-адрес или маску</small>
                    </div>

                    <div class="controls">
                        <button @click="previousQuestion" :disabled="currentQuestion === 0">Назад</button>
                        <button @click="nextQuestion"
                            :disabled="!isValidIp(answers[currentQuestion]) || currentQuestion === questions.length - 1">
                            {{ currentQuestion === questions.length - 1 ? 'Завершить тест' : 'Далее' }}
                        </button>
                    </div>
                </div>

                <div class="question-navigation">
                    <h4>Перейти к вопросу:</h4>
                    <div class="question-buttons">
                        <button v-for="(question, index) in questions" :key="index"
                            :class="{ 'question-button': true, 'active': currentQuestion === index, 'answered': answers[index] }"
                            @click="currentQuestion = index">
                            {{ index + 1 }}
                        </button>
                    </div>
                </div>

                <div v-if="currentQuestion === questions.length - 1" class="end-test">
                    <button @click="finishTest">Завершить тест</button>
                </div>
            </div>

            <div v-if="isFinished" class="end-screen">
                <lottie-player src="https://assets2.lottiefiles.com/packages/lf20_DMgKk1.json" background="transparent"
                    speed="1" style="width: 200px; height: 200px; margin: 0 auto" loop autoplay>
                </lottie-player>

                <h2>Тест завершён!</h2>
                <p>Вы ответили на <strong>{{ answeredCount }}</strong> из <strong>{{ totalQuestions }}</strong>
                    вопросов.</p>

                <div class="end-motivation">
                    <p>{{ motivationalMessage(answeredCount, totalQuestions).emoji }} {{
                        motivationalMessage(answeredCount, totalQuestions).text }}</p>
                    <blockquote>{{ motivationalMessage(answeredCount, totalQuestions).quote }}</blockquote>
                </div>

                <button v-if="!submitSuccess" class="submit-button" @click="submitTest">Отправить результаты</button>
            </div>

            <div v-if="error" class="error-message">{{ error }}</div>
            <div v-if="submitSuccess && !error" class="success-message">Результаты успешно отправлены!</div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import api from '@/api';

const questions = ref([]);
const answers = ref([]);
const sessionId = ref(null);
const currentQuestion = ref(0);
const timeLeft = ref(600); // 10 минут
const error = ref('');
const submitSuccess = ref(false);
const isFinished = ref(false);
const finalMessage = ref('');

function getQuestionTitle(q) {
    const map = {
        network_address: 'Укажите адрес сети',
        broadcast_address: 'Определите широковещательный адрес',
        first_last_address: 'Укажите первый и последний адрес в сети',
        same_network: 'Определите, принадлежат ли адреса одной сети',
        mask_count: 'Укажите маску по кол-ву сетей',
        mask_range: 'Найдите маску подсети для диапазона',
        host_addr: 'Может ли это быть адресом узла?'
    };
    return map[q.type] || 'Вопрос';
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secondsRemaining = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secondsRemaining).padStart(2, '0')}`;
}

const formattedTime = computed(() => formatTime(timeLeft.value));
const totalQuestions = computed(() => questions.value.length);
const answeredCount = computed(() => answers.value.filter(a => a && a.trim() !== '').length);

onMounted(async () => {
    error.value = '';
    try {
        const response = await api.get('/student/get-questions');
        console.log(response)
        questions.value = response.data;
        sessionId.value = response.data[0]?.session_id || null;
        answers.value = questions.value.map(q => q.student_answer || '');
    } catch {
        error.value = 'Ошибка получения вопросов';
    }

    timer = setInterval(() => {
        if (timeLeft.value > 0) timeLeft.value--;
    }, 1000);
});

onUnmounted(() => clearInterval(timer));

function nextQuestion() {
    if (currentQuestion.value < questions.value.length - 1) {
        currentQuestion.value++;
    }
}

function previousQuestion() {
    if (currentQuestion.value > 0) {
        currentQuestion.value--;
    }
}

function isValidIp(ip) {
    const regex = /^\d{1,3}(\.\d{1,3}){3}$/;
    return regex.test(ip) && ip.split('.').every(o => {
        const n = parseInt(o, 10);
        return n >= 0 && n <= 255;
    });
}

function filterIpInput(event) {
    const rawValue = event.target.value;
    const filtered = rawValue.replace(/[^0-9.]/g, '');
    answers.value[currentQuestion.value] = filtered;
}

function finishTest() {
    isFinished.value = true;
}

async function submitTest() {
    try {
        const payload = questions.value.map((q, i) => ({
            question_id: q.id,
            answer: answers.value[i]
        }));
        const response = await api.patch('/student/send-answer', payload);
        finalMessage.value = response.data.message || 'Тест завершён!';
        isFinished.value = true;
        submitSuccess.value = true;
    } catch {
        error.value = 'Ошибка при отправке теста';
    }
}

function percentageAnswered(answeredCount, totalQuestions) {
    return totalQuestions > 0
        ? Math.round((answeredCount / totalQuestions) * 100)
        : 0;
}

function motivationalMessage(answeredCount, totalQuestions) {
    const p = percentageAnswered(answeredCount, totalQuestions);
    if (p < 30) return { emoji: '😓', text: 'Старайся больше!', quote: 'Каждая ошибка — это шаг к успеху.' };
    if (p < 50) return { emoji: '🙂', text: 'Неплохо, но можно лучше!', quote: 'Дорогу осилит идущий.' };
    if (p < 75) return { emoji: '👍', text: 'Хороший результат!', quote: 'Настойчивость побеждает талант.' };
    return { emoji: '🚀', text: 'Молодец, супер!', quote: 'Успех — результат подготовки и упорства.' };
}

let timer;
</script>

<style scoped>
.test-page {
    background: #fff;
    padding: 2rem;
    border-radius: 1rem;
    width: 100%;
    max-width: 1000px;
    margin: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.timer {
    font-size: 1.25rem;
    text-align: center;
    margin-bottom: 1.5rem;
    color: #5b5e61;
}

h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

input[type="text"] {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ccc;
}

.invalid {
    border-color: red;
}

.controls {
    margin-top: 1rem;
    display: flex;
    gap: 10px;
}

button {
    background: #4a90e2;
    color: white;
    cursor: pointer;
    font-size: 1rem;
}

button:hover {
    background: #357ab7;
}

button:disabled {
    background-color: #e3e8f0;
    color: #8e9297;
    cursor: not-allowed;
}

.question-navigation {
    margin-top: 2rem;
}

.question-buttons {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.question-button.answered {
    background-color: #4a90e2;
    color: white;
}

.question-button:not(.answered) {
    background-color: #e3e8f0;
    color: black;
}

.question-button:not(.answered):hover {
    background-color: #d0d7e2;
}

.question-button.active {
    background-color: #357ab7;
    color: white;
}

.question-button:hover {
    background-color: #357ab7;
}

.end-test {
    margin-top: 2rem;
    text-align: center;
}

.question-container p {
    font-size: 1rem;
    margin-bottom: 1rem;
}

.end-screen {
    text-align: center;
    padding: 2rem;
    background: #f0f9ff;
    border-radius: 12px;
    animation: fadeIn 0.8s ease-in;
}

.end-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.end-motivation {
    margin-top: 1.5rem;
    font-style: italic;
    color: #555;
}

.submit-button {
    margin-top: 2rem;
    padding: 0.8rem 2rem;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>