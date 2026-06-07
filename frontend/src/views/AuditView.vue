<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-indigo-100 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 12h6M9 16h4"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">{{ t('audit.title') }}</h1>
          <p class="page-subtitle">{{ t('audit.subtitle') }}</p>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="card p-4 mb-5">
      <div class="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center sm:gap-3">
        <!-- Search -->
        <div class="relative w-full sm:flex-1">
          <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-4.35-4.35M17 11A6 6 0 105 11a6 6 0 0012 0z"/>
          </svg>
          <input v-model="filters.search" @input="debouncedLoad" type="text"
            :placeholder="t('audit.search_ph')" class="form-input h-9 pl-8 w-full text-sm" />
        </div>

        <!-- Action filter -->
        <div class="relative w-full sm:w-auto">
          <select v-model="filters.action" @change="loadAudit"
            class="filter-select w-full sm:w-44">
            <option value="">{{ t('audit.all_actions') }}</option>
            <option value="create">{{ t('audit.action_create') }}</option>
            <option value="update">{{ t('audit.action_update') }}</option>
            <option value="delete">{{ t('audit.action_delete') }}</option>
            <option value="status_change">{{ t('audit.action_status') }}</option>
            <option value="login">{{ t('audit.action_login') }}</option>
          </select>
          <svg class="select-chevron" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>

        <!-- Date range -->
        <div class="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          <div class="relative flex-1 sm:flex-none">
            <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <input v-model="filters.date_from" @change="loadAudit" type="date"
              class="form-input h-9 w-full sm:w-40 pl-8 text-sm" />
          </div>
          <span class="text-slate-300 text-lg font-light select-none">—</span>
          <div class="relative flex-1 sm:flex-none">
            <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none"
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <input v-model="filters.date_to" @change="loadAudit" type="date"
              class="form-input h-9 w-full sm:w-40 pl-8 text-sm" />
          </div>
        </div>
      </div>
    </div>

    <!-- Log list -->
    <div class="card overflow-hidden">

      <!-- Skeleton -->
      <div v-if="loading" class="p-4 space-y-2">
        <div v-for="i in 8" :key="i"
          class="skeleton h-[60px] rounded-lg"
          :style="{ animationDelay: `${(i-1)*50}ms` }">
        </div>
      </div>

      <!-- Empty -->
      <div v-else-if="logs.length === 0" class="empty-state py-16">
        <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
        </div>
        <div class="empty-state-title">{{ t('audit.not_found') }}</div>
        <p class="text-sm text-slate-400 mt-1">{{ t('audit.not_found_hint') }}</p>
      </div>

      <!-- Rows -->
      <div v-else class="divide-y divide-slate-100">
        <div v-for="log in logs" :key="log.id" class="log-row px-5 py-3.5">
          <div class="flex items-start gap-3.5">
            <!-- Action icon -->
            <div :class="['w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5', actionColor(log.action)]">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-sm font-semibold text-slate-800">{{ log.user_name }}</span>
                <span :class="['action-badge', actionBadge(log.action)]">{{ log.action_display }}</span>
                <span class="text-sm text-slate-500 truncate">{{ log.object_type }}: <span class="font-medium text-slate-700">{{ log.object_repr }}</span></span>
              </div>
              <div class="flex items-center gap-2 mt-1">
                <svg class="w-3 h-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span class="text-xs text-slate-400 tabular-nums">{{ formatDateTime(log.created_at) }}</span>
                <template v-if="log.ip_address">
                  <span class="text-slate-200">·</span>
                  <span class="text-xs text-slate-400 font-mono">{{ log.ip_address }}</span>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1"
        class="flex flex-wrap items-center justify-between gap-3 px-4 sm:px-5 py-3 border-t border-slate-100 bg-slate-50/60">
        <div class="text-xs text-slate-500 tabular-nums">
          {{ t('audit.total') }}: <span class="font-semibold text-slate-700">{{ pagination.count }}</span>
        </div>
        <div class="flex gap-2">
          <button @click="prevPage" :disabled="!pagination.previous"
            class="pag-btn disabled:opacity-40 disabled:cursor-not-allowed">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            {{ t('audit.prev') }}
          </button>
          <button @click="nextPage" :disabled="!pagination.next"
            class="pag-btn disabled:opacity-40 disabled:cursor-not-allowed">
            {{ t('audit.next') }}
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
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
import { useI18n } from '@/i18n'

const toast = useToast()
const { t } = useI18n()
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
  } catch { toast.error(t('toast.load_error')) }
  finally { loading.value = false }
}

function prevPage() { filters.page--; loadAudit() }
function nextPage() { filters.page++; loadAudit() }

onMounted(loadAudit)
</script>

<style scoped>
.log-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.log-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.3);
}
.action-badge {
  @apply text-xs px-2 py-0.5 rounded-full font-medium;
}
.filter-select {
  @apply form-input h-9 text-sm bg-slate-50 border-slate-200 pl-3 pr-8
         hover:border-slate-300 transition-colors duration-150
         appearance-none cursor-pointer rounded-lg;
}
.select-chevron {
  @apply absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none;
}
.pag-btn {
  @apply inline-flex items-center gap-1 text-xs font-medium px-3 py-1.5
         rounded-lg border border-slate-200 bg-white text-slate-600
         hover:bg-slate-50 hover:border-slate-300 transition-all duration-150 cursor-pointer;
}
</style>
