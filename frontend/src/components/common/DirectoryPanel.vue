<template>
  <div class="card overflow-hidden">
    <div class="flex items-center justify-between p-5 border-b border-slate-100">
      <h3 class="font-semibold text-slate-800">{{ title }}</h3>
      <button @click="$emit('add')" class="btn-sm btn-primary">+ Добавить</button>
    </div>
    <div v-if="loading" class="p-6 space-y-2">
      <div v-for="i in 4" :key="i" class="skeleton h-12 rounded-lg"></div>
    </div>
    <div v-else-if="items.length === 0" class="p-8 text-center text-slate-400 text-sm">Список пуст</div>
    <div v-else class="divide-y divide-slate-100">
      <div v-for="item in items" :key="item.id"
        class="flex items-center gap-4 px-5 py-3 hover:bg-slate-50 transition-colors">
        <span class="flex-1 text-sm font-medium text-slate-800">{{ item.name }}</span>
        <span v-if="item.workshop_name" class="text-xs text-slate-400">{{ item.workshop_name }}</span>
        <span class="text-xs text-slate-400">{{ item.machines_count !== undefined ? item.machines_count + ' станков' : '' }}</span>
        <div class="flex items-center gap-1">
          <button @click="$emit('edit', item)" class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps({ title: String, items: { type: Array, default: () => [] }, loading: Boolean })
defineEmits(['add', 'edit', 'delete'])
</script>
