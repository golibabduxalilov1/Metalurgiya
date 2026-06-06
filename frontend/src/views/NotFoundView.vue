<template>
  <div class="min-h-screen flex items-center justify-center" style="background: #0F172A;">
    <div class="text-center">
      <div class="text-8xl font-black text-slate-700 mb-4">404</div>
      <h1 class="text-2xl font-bold text-white mb-2">Страница не найдена</h1>
      <p class="text-slate-400 mb-8">Запрашиваемая страница не существует</p>
      <RouterLink to="/" class="btn-md btn-primary">На главную</RouterLink>
    </div>
  </div>
</template>
<script setup>
import { RouterLink } from 'vue-router'
</script>
