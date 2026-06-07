<template>
  <div class="card overflow-hidden">
    <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
      <h3 class="text-sm font-semibold text-slate-700">{{ title }}</h3>
      <button @click="$emit('add')" class="btn-sm btn-primary">{{ t('directories.add_btn') }}</button>
    </div>
    <div v-if="loading" class="p-4 space-y-2">
      <div v-for="i in 4" :key="i" class="skeleton h-11 rounded-lg"
        :style="{ animationDelay: `${(i-1)*50}ms` }"></div>
    </div>
    <div v-else-if="items.length === 0" class="py-10 flex flex-col items-center gap-2">
      <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
        <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0H4"/>
        </svg>
      </div>
      <p class="text-sm text-slate-400">{{ t('directories.empty_list') }}</p>
    </div>
    <div v-else class="divide-y divide-slate-100">
      <div v-for="item in items" :key="item.id" class="dir-row flex items-center gap-4 px-5 py-3">
        <span class="flex-1 text-sm font-medium text-slate-800">{{ item.name }}</span>
        <span v-if="item.workshop_name"
          class="text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">{{ item.workshop_name }}</span>
        <span v-if="item.machines_count !== undefined"
          class="text-xs font-medium text-slate-500 tabular-nums">{{ item.machines_count }} {{ t('directories.units_suffix') }}</span>
        <button @click="$emit('edit', item)"
          class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from '@/i18n'
defineProps({ title: String, items: { type: Array, default: () => [] }, loading: Boolean })
defineEmits(['add', 'edit', 'delete'])
const { t } = useI18n()
</script>

<style scoped>
.dir-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.dir-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.3);
}
</style>
