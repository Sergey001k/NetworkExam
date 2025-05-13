<template>
    <div class="admin min-h-screen flex items-center justify-center bg-gray-100 flex-center bg-gradient-blue">
        <div class="admin-container">
            <h1 class="title">Панель администратора</h1>
            <div class="tabs">
                <button v-for="(tab, index) in tabs" :key="index" :class="{ active: activeTab === tab.name }"
                    @click="activeTab = tab.name">
                    {{ tab.label }}
                </button>
            </div>
        </div>

        <div class="tab-content">
            <CreateSession v-if="activeTab === 'create'" />
            <SessionsList v-if="activeTab === 'sessions'" @viewResults="openResults" />
            <SessionResults v-if="activeTab === 'results'" :sessionId="selectedSessionId"
                @back="activeTab = 'sessions'" />
        </div>
    </div>
</template>

<script>
import CreateSession from './CreateSession.vue'
import SessionsList from './SessionsList.vue'
import SessionResults from './SessionResults.vue'

export default {
    name: 'AdminPanel',
    components: { CreateSession, SessionsList, SessionResults },
    data() {
        return {
            activeTab: 'create',
            selectedSessionId: null,
            tabs: [
                { name: 'create', label: 'Создание сессии' },
                { name: 'sessions', label: 'Все сессии' },
                { name: 'results', label: 'Результаты' }
            ]
        }
    },
    methods: {
        openResults(sessionId) {
            this.selectedSessionId = sessionId
            this.activeTab = 'results'
        }
    }
}
</script>

<style scoped>
.admin {
    align-items: start;
    flex-direction: column;
    justify-content: start;
}

.admin-container,
.tab-content {
    width: 95vw;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.title {
    text-align: center;
    margin-bottom: 2rem;
}

.tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.tabs button {
    background: #e1eeff;
    color: black;
}

button:hover {
  background-color: #b7d9ff;
}

.tabs button.active {
    background: #4a90e2;
    color: #fff;
}

.tab-content {
    margin-top: 0;
}
</style>