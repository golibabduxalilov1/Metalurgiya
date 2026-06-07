<template>
  <div class="animate-fade-in space-y-6">

    <!-- Page header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">{{ t('dashboard.title') }}</h1>
        <p class="page-subtitle">{{ t('dashboard.subtitle') }}</p>
      </div>
      <div class="inline-flex items-center gap-2 bg-white border border-slate-200
                  text-slate-600 text-xs font-medium px-3 py-2 rounded-xl shadow-sm flex-shrink-0">
        <svg class="w-3.5 h-3.5 text-indigo-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        {{ currentDate }}
      </div>
    </div>

    <!-- Loading skeletons -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      <div v-for="i in 4" :key="i" class="skeleton h-24 sm:h-28 rounded-xl"></div>
    </div>

    <!-- KPI cards -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">

      <div class="kpi-card kpi-indigo cursor-pointer" @click="$router.push('/machines')">
        <div class="kpi-icon bg-indigo-50">
          <svg class="w-5 h-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
          </svg>
        </div>
        <div>
          <div class="kpi-value">{{ stats.total }}</div>
          <div class="kpi-label">{{ t('dashboard.total') }}</div>
        </div>
      </div>

      <div class="kpi-card kpi-emerald cursor-pointer" @click="goToStatus('working')">
        <div class="kpi-icon bg-emerald-50">
          <svg class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <div class="kpi-value text-emerald-600">{{ stats.working }}</div>
          <div class="kpi-label">{{ t('dashboard.working') }}</div>
        </div>
      </div>

      <div class="kpi-card kpi-rose cursor-pointer" @click="goToStatus('repair')">
        <div class="kpi-icon bg-rose-50">
          <svg class="w-5 h-5 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <div class="kpi-value text-rose-500">{{ stats.repair }}</div>
          <div class="kpi-label">{{ t('dashboard.repair') }}</div>
        </div>
      </div>

      <div class="kpi-card kpi-amber cursor-pointer" @click="goToStatus('idle')">
        <div class="kpi-icon bg-amber-50">
          <svg class="w-5 h-5 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <div class="kpi-value text-amber-500">{{ stats.idle }}</div>
          <div class="kpi-label">{{ t('dashboard.idle') }}</div>
        </div>
      </div>
    </div>

    <!-- Status distribution + recent activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Status distribution -->
      <div class="card p-6">
        <div class="section-header mb-5 pb-4 border-b border-slate-100">
          <div class="section-icon bg-indigo-50">
            <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"/>
            </svg>
          </div>
          <h3 class="section-title">{{ t('dashboard.statuses') }}</h3>
        </div>
        <div v-if="loading" class="space-y-3">
          <div v-for="i in 4" :key="i" class="skeleton h-10 rounded-lg"></div>
        </div>
        <div v-else class="space-y-2">
          <div v-for="item in statusDistribution" :key="item.name"
            class="flex items-center gap-3 cursor-pointer px-2 py-2 rounded-lg -mx-2
                   hover:bg-slate-50 transition-colors duration-150 group"
            @click="goToStatus(item.colorKey)">
            <div class="w-2.5 h-2.5 rounded-full flex-shrink-0"
              :class="`status-dot-${item.color}`"></div>
            <span class="text-sm text-slate-600 flex-1 group-hover:text-slate-800
                         transition-colors duration-150 truncate">{{ item.name }}</span>
            <span class="text-sm font-bold text-slate-900 tabular-nums w-6 text-right">
              {{ item.count }}
            </span>
            <div class="w-20 bg-slate-100 rounded-full h-2 flex-shrink-0 overflow-hidden">
              <div class="h-2 rounded-full transition-all duration-500"
                :class="barColorClass(item.color)"
                :style="{ width: `${stats.total ? (item.count / stats.total) * 100 : 0}%` }">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent status changes -->
      <div class="card p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
          <div class="section-header">
            <div class="section-icon bg-emerald-50">
              <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <h3 class="section-title">{{ t('dashboard.recent_changes') }}</h3>
          </div>
          <RouterLink to="/machines"
            class="inline-flex items-center gap-1 text-xs font-medium text-indigo-600
                   hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100
                   border border-indigo-100 px-2.5 py-1 rounded-full
                   transition-colors duration-150">
            {{ t('dashboard.all') }}
            <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>
        <div v-if="loadingHistory" class="space-y-2.5">
          <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-lg"
            :style="{ animationDelay: `${(i - 1) * 50}ms` }"></div>
        </div>
        <div v-else-if="recentChanges.length === 0"
          class="flex flex-col items-center justify-center py-10 text-center">
          <svg class="w-10 h-10 text-slate-200 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <div class="text-sm text-slate-400">{{ t('common.no_data') }}</div>
        </div>
        <div v-else class="divide-y divide-slate-100/80">
          <div v-for="change in recentChanges" :key="change.id"
            class="py-3 flex items-center gap-3 hover:bg-slate-50/70 -mx-2 px-2
                   rounded-lg transition-colors duration-100 cursor-pointer group"
            @click="$router.push(`/machines/${change.machine}`)">
            <div class="flex-shrink-0">
              <span :class="['status-badge', `status-${change.new_status_color}`]">
                <span :class="['status-dot', `status-dot-${change.new_status_color}`]"></span>
                {{ change.new_status_name }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-semibold text-slate-800 truncate
                          group-hover:text-indigo-600 transition-colors duration-150">
                {{ t('dashboard.machine_prefix') }}{{ change.machine }}
              </div>
              <div class="text-xs text-slate-400 mt-0.5">{{ change.changed_by_name }}</div>
            </div>
            <div class="flex items-center gap-1 text-xs text-slate-400 flex-shrink-0 tabular-nums">
              {{ formatDate(change.changed_at) }}
              <svg class="w-3.5 h-3.5 text-slate-300 opacity-0 group-hover:opacity-100
                          transition-opacity duration-150"
                fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Workshop summary -->
    <div class="card p-6" v-if="auth.isAdmin || auth.isMaster">
      <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
        <div class="section-header">
          <div class="section-icon bg-violet-50">
            <svg class="w-4 h-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
            </svg>
          </div>
          <h3 class="section-title">{{ t('dashboard.workshops') }}</h3>
        </div>
        <RouterLink to="/directories"
          class="inline-flex items-center gap-1 text-xs font-medium text-indigo-600
                 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100
                 border border-indigo-100 px-2.5 py-1 rounded-full
                 transition-colors duration-150">
          {{ t('dashboard.directories_link') }}
          <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
          </svg>
        </RouterLink>
      </div>
      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-xl"></div>
      </div>
      <div v-else-if="workshopStats.length === 0"
        class="text-sm text-slate-400 text-center py-8">{{ t('common.no_data') }}</div>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        <div v-for="ws in workshopStats" :key="ws.id"
          class="workshop-card cursor-pointer group"
          @click="$router.push(`/machines?workshop=${ws.id}`)">
          <div class="text-2xl font-bold text-slate-900 tabular-nums leading-none
                      group-hover:text-indigo-600 transition-colors duration-200">
            {{ ws.machines_count }}
          </div>
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wide mt-2 truncate"
            :title="ws.name">{{ ws.name }}</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useLangStore } from '@/store/lang'
import { useI18n } from '@/i18n'
import { machinesApi, statusesApi, workshopsApi } from '@/api'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import 'dayjs/locale/uz'

const router = useRouter()
const auth = useAuthStore()
const langStore = useLangStore()
const { t } = useI18n()
const loading = ref(true)
const loadingHistory = ref(true)

const stats = ref({ total: 0, working: 0, repair: 0, idle: 0 })
const statusDistribution = ref([])
const recentChanges = ref([])
const workshopStats = ref([])

const currentDate = computed(() => {
  const locale = langStore.lang === 'uz' ? 'uz' : 'ru'
  return dayjs().locale(locale).format('DD MMMM YYYY, dddd')
})

function barColorClass(color) {
  const map = {
    green: 'bg-emerald-500',
    yellow: 'bg-amber-500',
    red: 'bg-red-500',
    gray: 'bg-slate-400',
    blue: 'bg-blue-500',
  }
  return map[color] || 'bg-slate-400'
}

function formatDate(date) {
  return dayjs(date).format('DD.MM HH:mm')
}

function goToStatus(key) {
  router.push(`/machines?status_color=${key}`)
}

async function loadData() {
  try {
    loading.value = true

    const [machinesRes, statusesRes, workshopsRes] = await Promise.all([
      machinesApi.list({ page_size: 1 }),
      statusesApi.list(),
      workshopsApi.list(),
    ])

    const statuses = statusesRes.data.results || statusesRes.data
    workshopStats.value = (workshopsRes.data.results || workshopsRes.data).slice(0, 8)

    const distArr = []
    let totalWorking = 0, totalRepair = 0, totalIdle = 0

    for (const s of statuses) {
      const res = await machinesApi.list({ status: s.id, page_size: 1 })
      const count = res.data.count || 0
      distArr.push({ name: s.name, count, color: s.color, colorKey: s.color })
      if (s.color === 'green') totalWorking += count
      if (s.color === 'red') totalRepair += count
      if (s.color === 'yellow') totalIdle += count
    }

    statusDistribution.value = distArr
    stats.value = {
      total: machinesRes.data.count || 0,
      working: totalWorking,
      repair: totalRepair,
      idle: totalIdle,
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }

  try {
    loadingHistory.value = true
    const res = await machinesApi.list({ page_size: 10, ordering: '-updated_at' })
    const machines = res.data.results || []
    recentChanges.value = machines.slice(0, 6).map(m => ({
      id: m.id,
      machine: m.id,
      new_status_name: m.current_status_name || '—',
      new_status_color: m.current_status_color || 'gray',
      changed_by_name: m.operator_name || '—',
      changed_at: m.updated_at,
    }))
  } catch (e) {
    console.error(e)
  } finally {
    loadingHistory.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
/* ── Section header ── */
.section-header {
  @apply flex items-center gap-3;
}
.section-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0;
}
.section-title {
  @apply text-sm font-semibold text-slate-700;
}

/* ── KPI cards ── */
.kpi-card {
  @apply bg-white rounded-xl border border-slate-200 shadow-sm p-3 sm:p-5
         flex items-center gap-3 sm:gap-4
         transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md;
}
.kpi-icon {
  @apply w-9 h-9 sm:w-11 sm:h-11 rounded-xl flex items-center justify-center flex-shrink-0;
}
.kpi-value {
  @apply text-xl sm:text-2xl font-bold text-slate-900 leading-none tabular-nums;
}
.kpi-label {
  @apply text-xs sm:text-sm text-slate-500 mt-1;
}

/* ── KPI accent left border ── */
.kpi-indigo  { border-left: 3px solid #6366f1; }
.kpi-emerald { border-left: 3px solid #10b981; }
.kpi-rose    { border-left: 3px solid #f43f5e; }
.kpi-amber   { border-left: 3px solid #f59e0b; }

/* ── Workshop card ── */
.workshop-card {
  @apply bg-slate-50 hover:bg-white border border-slate-200 hover:border-indigo-100
         rounded-xl p-3 sm:p-4 shadow-sm hover:shadow-md
         transition-all duration-200 hover:-translate-y-0.5;
}

/* ── Reduced motion ── */
@media (prefers-reduced-motion: reduce) {
  .kpi-card, .workshop-card { transition: none; }
}
</style>
