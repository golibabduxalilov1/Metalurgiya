<template>
  <span :class="['status-badge', colorClass, sizeClass]">
    <span :class="['status-dot', dotClass]"></span>
    {{ status || 'Не задан' }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  status: String,
  color: { type: String, default: 'gray' },
  size: { type: String, default: 'sm' }
})
const colorClass = computed(() => `status-${props.color || 'gray'}`)
const dotClass = computed(() => `status-dot-${props.color || 'gray'}`)
const sizeClass = computed(() => props.size === 'md' ? 'text-sm px-3 py-1.5' : '')
</script>
