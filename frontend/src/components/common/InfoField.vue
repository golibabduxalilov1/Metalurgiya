<template>
  <div>
    <dt class="text-xs text-slate-500 font-medium mb-0.5">{{ label }}</dt>
    <dd :class="['text-sm text-slate-900', mono ? 'font-mono' : '']">
      {{ value || '—' }}
    </dd>
  </div>
</template>
<script setup>
defineProps({ label: String, value: [String, Number], mono: Boolean })
</script>
