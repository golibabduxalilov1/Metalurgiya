<template>
  <div class="py-1">
    <dt class="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1 select-none">{{ label }}</dt>
    <dd :class="[
      'text-sm font-medium text-slate-800 break-words',
      mono ? 'font-mono text-xs bg-slate-100/80 border border-slate-200 px-1.5 py-0.5 rounded-md text-indigo-700 inline-block' : '',
      (!value && value !== 0) ? 'text-slate-400 font-normal italic' : ''
    ]">
      {{ value ?? '—' }}
    </dd>
  </div>
</template>

<script setup>
defineProps({ label: String, value: [String, Number], mono: Boolean })
</script>
