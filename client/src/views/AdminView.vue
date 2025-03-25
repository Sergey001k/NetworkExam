<template>
  <div>
    <h1>Админ панель</h1>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { isTokenValid } from '../utils/auth';

const router = useRouter();

onMounted(() => {
  const token = localStorage.getItem('authToken');

  if (!token || !isTokenValid(token)) {
    localStorage.removeItem('authToken');
    router.push('/login');
  }
});
</script>
