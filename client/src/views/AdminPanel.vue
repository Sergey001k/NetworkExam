<template>
    <div class="flex-center bg-gradient-blue" style="padding: 2rem">
        <div class="admin-panel">
            <div class="tabs">
                <button v-for="tab in tabs" :key="tab" :class="['tab-button', { active: currentTab === tab }]"
                    @click="currentTab = tab">
                    {{ tabTitles[tab] }}
                </button>
            </div>

            <div class="tab-content">
                <div v-if="currentTab === 'constructor'">
                    <h3>🛠️ Конструктор тестов</h3>

                    <div class="form-group">
                        <label for="testTitle">Название теста:</label>
                        <input id="testTitle" v-model="testTitle" type="text" placeholder="Название теста" />
                    </div>

                    <div class="question-list">
                        <div class="question-item" v-for="(q, index) in questions" :key="index">
                            <div class="question">
                                <h4>Вопрос {{ index + 1 }}</h4>
                                <div class="remove-btn" @click="removeQuestion(index)">
                                    <font-awesome-icon :icon="['fas', 'xmark']" />
                                </div>
                            </div>

                            <input v-model="q.text" placeholder="Текст вопроса" />

                            <select v-model="q.type">
                                <option value="single">Один вариант</option>
                                <option value="multiple">Несколько вариантов</option>
                                <option value="text">Ответ текстом</option>
                            </select>

                            <div v-if="q.type !== 'text'" class="answers">
                                <div v-for="(opt, oIndex) in q.options" :key="oIndex" class="answer-option">
                                    <input v-model="opt.text" placeholder="Вариант ответа" type="text" />
                                    <label class="answer-option-input">
                                        <input v-if="q.type === 'single'" type="radio" :name="'correct-' + index"
                                            v-model="q.correctIndex" :value="oIndex" />
                                        <input v-else-if="q.type === 'multiple'" type="checkbox"
                                            v-model="q.correctIndexes" :value="oIndex" />
                                        Правильный
                                    </label>
                                    <div class="remove-btn" @click="removeOption(index, oIndex)">
                                        <font-awesome-icon :icon="['fas', 'xmark']" />
                                    </div>
                                </div>
                                <button class="add-item" @click="addOption(index)">Добавить вариант</button>
                            </div>

                            <hr />
                        </div>
                    </div>

                    <button class="add-item" @click="addQuestion"><font-awesome-icon :icon="['fas', 'plus']" /></button>
                </div>

                <div v-else-if="currentTab === 'results'">
                    <h3>📊 Результаты тестов</h3>
                    <p>Здесь будет список студентов с результатами. Пока что заглушка.</p>
                </div>

                <div v-else-if="currentTab === 'session'">
                    <h3>📡 Текущая сессия</h3>
                    <p>Здесь будет отображаться информация о текущей сессии. Пока заглушка.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faXmark, faPlus } from "@fortawesome/free-solid-svg-icons";

library.add(faXmark);
library.add(faPlus)

const tabs = ['constructor', 'results', 'session']
const tabTitles = {
    constructor: 'Конструктор',
    results: 'Результаты',
    session: 'Сессия'
}
const currentTab = ref('constructor')

const testTitle = ref('')
const questions = ref([])

function addQuestion() {
    questions.value.push({
        text: '',
        type: 'single',
        options: [],
        correctIndex: 0,
        correctIndexes: [],
    })
}

function removeQuestion(index) {
    questions.value.splice(index, 1)
}

function addOption(qIndex) {
    questions.value[qIndex].options.push({ text: '' })
}

function removeOption(qIndex, oIndex) {
    questions.value[qIndex].options.splice(oIndex, 1)
}
</script>

<style scoped>
.admin-panel {
    background: #fff;
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 800px;
}

.tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.tab-button {
    flex: 1;
    padding: 0.75rem;
    border: none;
    background-color: #e3e8f0;
    border-radius: 0.5rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
    outline: none;
    color: black;
}

.tab-button.active {
    background-color: #4a90e2;
    color: white;
}

.add-item:hover,
.tab-button:hover {
    background-color: #d0d7e2;
}

.form-group,
.question-item {
    margin-bottom: 1rem;
}

input,
select {
    display: block;
    width: 100%;
    padding: 0.75rem;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
    border-radius: 0.5rem;
    font-size: 1rem !important;
    border: 1px solid #ccc;
    outline: none;
}

.answer-option-input {
    width: 50%;
}

select {
    background-color: #e3e8f0;
    border: none;
}

label {
    display: flex;
    align-items: center;
    gap: 10px;
}

.answer-option {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.remove-btn {
    color: #8f939b;
    font-size: 1.2rem;
    transition: color 0.3s ease;
}

.remove-btn:hover {
    color: #787b81;
    cursor: pointer;
}

button {
    margin-top: 0.5rem;
}

.add-item {
    background-color: #e3e8f0;
    color: #5b5d61;
}

.question {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>