<template>
    <div class="flex-center bg-gradient-blue" style="padding: 2rem">
        <div class="test-page">
            <div class="timer">
                Время: {{ formattedTime }}
            </div>

            <div class="question-container">
                <h3>{{ generateQuestionText(questions[currentQuestion]) }}</h3>
                <p>{{ questions[currentQuestion].questionText }}</p>

                <div v-if="questions[currentQuestion].type === 'ip'">
                    <input v-model="answers[currentQuestion]" type="text" inputmode="numeric" placeholder="0.0.0.0"
                        @input="filterIpInput"
                        :class="{ 'invalid': answers[currentQuestion] && !isValidIp(answers[currentQuestion]) }" />
                    <small class="hint">Введите IP-адрес или маску</small>
                    <!-- <span v-if="!isValidIp(answers[currentQuestion]) && answers[currentQuestion] !== ''"
                        class="error-message">
                        Введите корректный IP-адрес, маску или диапазон!
                    </span> -->
                </div>

                <div class="controls">
                    <button @click="previousQuestion" :disabled="currentQuestion === 0">Назад</button>
                    <button @click="nextQuestion"
                        :disabled="!isValidIp(answers[currentQuestion]) || currentQuestion === questions.length - 1">
                        {{ currentQuestion === questions.length - 1 ? 'Завершить тест' : 'Далее' }}
                    </button>
                </div>
            </div>

            <!-- Блок с завершением теста -->
            <div v-if="currentQuestion === questions.length - 1" class="end-test">
                <h3>Тест завершен!</h3>
                <button @click="submitTest">Завершить тест</button>
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
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Генерация случайного IP-адреса
function generateRandomIp() {
    const octets = Array.from({ length: 4 }, () => Math.floor(Math.random() * 256));
    return octets.join('.');
}

// Генерация вопросов с IP-адресами и масками
const questions = ref([
    { type: 'ip', template: 'Определите адрес сети <адрес/маска>', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Укажите сеть, к которой принадлежит данный IP-адрес' },
    { type: 'ip', template: 'Определите широковещательный адрес <адрес/маска>', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Выведите широковещательный адрес для этой сети' },
    { type: 'ip', template: 'Определите первый и последний адреса в сети <адрес сети/маска>', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Найдите первый и последний адрес в данной сети' },
    { type: 'ip', template: 'Определите, находятся ли адреса <адрес сети/маска>, <адрес сети/маска> в одной сети', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Проверьте, принадлежат ли два указанных адреса одной сети' },
    { type: 'ip', template: 'Найдите такую маску подсети, чтобы кол-во сетей было не меньше n, а кол-во хостов было максимально возможным.', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Найдите маску подсети для заданных условий' },
    { type: 'ip', template: 'Найдите маску подсети для диапазона ip адресов <адрес> - <адрес>', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Найдите маску подсети для указанного диапазона адресов' },
    { type: 'ip', template: 'Определите может ли адрес <адрес сети/маска> быть адресом узла.', ip: generateRandomIp(), mask: '255.255.255.0', questionText: 'Проверьте, является ли данный адрес допустимым для узла' }
]);

const currentQuestion = ref(0);
const answers = ref([]);
const timeLeft = ref(600); // 10 минут (600 секунд)

// Генерация текста вопроса с подстановкой IP и маски
function generateQuestionText(question) {
    return question.template.replace('<адрес>', question.ip).replace('<маска>', question.mask);
}

// Таймер
let timer;
onMounted(() => {
    timer = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--;
        }
    }, 1000);
});

onUnmounted(() => {
    clearInterval(timer);
});

// Форматирование времени
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secondsRemaining = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secondsRemaining).padStart(2, '0')}`;
}

const formattedTime = computed(() => formatTime(timeLeft.value));

// Переход к следующему вопросу
function nextQuestion() {
    if (currentQuestion.value < questions.value.length - 1) {
        currentQuestion.value++;
    }
}

// Переход к предыдущему вопросу
function previousQuestion() {
    if (currentQuestion.value > 0) {
        currentQuestion.value--;
    }
}

// Валидация IP-адреса или маски
function isValidIp(ip) {
    const regex = /^(\d{1,3}\.){3}\d{1,3}$/;
    return regex.test(ip) && ip.split('.').every(octet => {
        const n = parseInt(octet, 10);
        return n >= 0 && n <= 255;
    });
}

function filterIpInput(event) {
    const rawValue = event.target.value;
    const filtered = rawValue.replace(/[^0-9.]/g, '');
    answers.value[currentQuestion] = filtered;
}

// Завершение теста
function submitTest() {
    console.log('Ответы на тест:', answers.value);
    // Тут можно отправить результаты на сервер
}
</script>

<style scoped>
.test-page {
    /* width: 95vw;
    margin: 2rem auto; */
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

.error-message {
    color: red;
    font-size: 0.875rem;
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
</style>