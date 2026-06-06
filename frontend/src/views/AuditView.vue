<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">Журнал аудита</h1>
        <p class="page-subtitle">История всех действий пользователей</p>
      </div>
    </div>

    <div class="card p-4 mb-5 flex flex-wrap items-center gap-3">
      <input v-model="filters.search" @input="debouncedLoad" type="text"
        placeholder="Поиск..." class="form-input h-9 flex-1 min-w-[200px]" />
      <select v-model="filters.action" @change="loadAudit" class="form-select h-9 w-44">
        <option value="">Все действия</option>
        <option value="create">Создание</option>
        <option value="update">Изменение</option>
        <option value="delete">Удаление</option>
        <option value="status_change">Смена статуса</option>
        <option value="login">Вход</option>
      </select>
      <input v-model="filters.date_from" @change="loadAudit" type="date" class="form-input h-9 w-40" />
      <span class="text-slate-400 text-sm">—</span>
      <input v-model="filters.date_to" @change="loadAudit" type="date" class="form-input h-9 w-40" />
    </div>

    <div class="card overflow-hidden">
      <div v-if="loading" class="p-6 space-y-2">
        <div v-for="i in 8" :key="i" class="skeleton h-14 rounded-lg"></div>
      </div>
      <div v-else-if="logs.length === 0" class="empty-state">
        <div class="empty-state-title">Записи не найдены</div>
      </div>
      <div v-else class="divide-y divide-slate-100">
        <div v-for="log in logs" :key="log.id" class="px-5 py-3.5 hover:bg-slate-50 transition-colors">
          <div class="flex items-start gap-4">
            <div :class="['w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5', actionColor(log.action)]">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-sm font-semibold text-slate-900">{{ log.user_name }}</span>
                <span :class="['text-xs px-2 py-0.5 rounded-full font-medium', actionBadge(log.action)]">{{ log.action_display }}</span>
                <span class="text-sm text-slate-600">{{ log.object_type }}: {{ log.object_repr }}</span>
              </div>
              <div class="text-xs text-slate-400 mt-0.5">
                {{ formatDateTime(log.created_at) }}
                <span v-if="log.ip_address"> · IP: {{ log.ip_address }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1" class="flex items-center justify-between px-5 py-3 border-t border-slate-200 bg-slate-50/60">
        <div class="text-sm text-slate-500">{{ pagination.count }} записей</div>
        <div class="flex gap-2">
          <button @click="prevPage" :disabled="!pagination.previous" class="btn-sm btn-secondary disabled:opacity-40">← Пред.</button>
          <button @click="nextPage" :disabled="!pagination.next" class="btn-sm btn-secondary disabled:opacity-40">След. →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { auditApi } from '@/api'
import { useDebounceFn } from '@vueuse/core'
import dayjs from 'dayjs'

const toast = useToast()
const logs = ref([])
const loading = ref(true)
const pagination = ref({ count: 0, total_pages: 1, next: null, previous: null })
const filters = reactive({ search: '', action: '', date_from: '', date_to: '', page: 1 })

const debouncedLoad = useDebounceFn(loadAudit, 400)

function formatDateTime(d) { return dayjs(d).format('DD.MM.YYYY HH:mm:ss') }

function actionColor(a) {
  const m = { create: 'bg-emerald-100 text-emerald-600', update: 'bg-blue-100 text-blue-600', delete: 'bg-red-100 text-red-600', status_change: 'bg-amber-100 text-amber-600', login: 'bg-slate-100 text-slate-500' }
  return m[a] || 'bg-slate-100 text-slate-500'
}
function actionBadge(a) {
  const m = { create: 'bg-emerald-100 text-emerald-700', update: 'bg-blue-100 text-blue-700', delete: 'bg-red-100 text-red-700', status_change: 'bg-amber-100 text-amber-700' }
  return m[a] || 'bg-slate-100 text-slate-600'
}

async function loadAudit() {
  loading.value = true
  try {
    const params = { page: filters.page }
    if (filters.search) params.search = filters.search
    if (filters.action) params.action = filters.action
    if (filters.date_from) params.date_from = filters.date_from
    if (filters.date_to) params.date_to = filters.date_to
    const res = await auditApi.list(params)
    logs.value = res.data.results || []
    pagination.value = { count: res.data.count, total_pages: res.data.total_pages, next: res.data.next, previous: res.data.previous }
  } catch { toast.error('Ошибка загрузки') }
  finally { loading.value = false }
}

function prevPage() { filters.page--; loadAudit() }
function nextPage() { filters.page++; loadAudit() }

onMounted(loadAudit)
</script>
