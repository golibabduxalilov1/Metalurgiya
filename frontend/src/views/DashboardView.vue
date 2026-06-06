<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Главная</h1>
        <p class="page-subtitle">Обзор состояния станочного парка</p>
      </div>
      <div class="text-sm text-slate-400">
        {{ currentDate }}
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div v-for="i in 4" :key="i" class="card p-5 h-24 skeleton"></div>
    </div>

    <!-- Stats cards -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="stat-card card-hover cursor-pointer" @click="$router.push('/machines')">
        <div class="stat-icon bg-primary-100">
          <svg class="w-6 h-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
          </svg>
        </div>
        <div>
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">Всего станков</div>
        </div>
      </div>

      <div class="stat-card card-hover cursor-pointer" @click="goToStatus('working')">
        <div class="stat-icon bg-emerald-100">
          <svg class="w-6 h-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <div class="stat-value text-emerald-600">{{ stats.working }}</div>
          <div class="stat-label">Работают</div>
        </div>
      </div>

      <div class="stat-card card-hover cursor-pointer" @click="goToStatus('repair')">
        <div class="stat-icon bg-red-100">
          <svg class="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
          </svg>
        </div>
        <div>
          <div class="stat-value text-red-500">{{ stats.repair }}</div>
          <div class="stat-label">На ремонте</div>
        </div>
      </div>

      <div class="stat-card card-hover cursor-pointer" @click="goToStatus('idle')">
        <div class="stat-icon bg-amber-100">
          <svg class="w-6 h-6 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <div>
          <div class="stat-value text-amber-500">{{ stats.idle }}</div>
          <div class="stat-label">Простой</div>
        </div>
      </div>
    </div>

    <!-- Status distribution + recent activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- Status distribution -->
      <div class="card p-6">
        <h3 class="font-semibold text-slate-800 mb-4">Статусы станков</h3>
        <div v-if="loading" class="space-y-3">
          <div v-for="i in 4" :key="i" class="skeleton h-10 rounded-lg"></div>
        </div>
        <div v-else class="space-y-3">
          <div v-for="item in statusDistribution" :key="item.name"
            class="flex items-center gap-3 cursor-pointer hover:bg-slate-50 p-2 rounded-lg -mx-2 transition-colors"
            @click="goToStatus(item.colorKey)">
            <div class="w-3 h-3 rounded-full flex-shrink-0" :class="`status-dot-${item.color}`"></div>
            <span class="text-sm text-slate-700 flex-1">{{ item.name }}</span>
            <span class="text-sm font-semibold text-slate-900">{{ item.count }}</span>
            <div class="w-20 bg-slate-100 rounded-full h-1.5 flex-shrink-0">
              <div class="h-1.5 rounded-full transition-all"
                :class="barColorClass(item.color)"
                :style="{ width: `${stats.total ? (item.count / stats.total) * 100 : 0}%` }">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent status changes -->
      <div class="card p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-slate-800">Последние изменения статусов</h3>
          <RouterLink to="/machines" class="text-sm text-primary-600 hover:text-primary-700 font-medium">
            Все →
          </RouterLink>
        </div>
        <div v-if="loadingHistory" class="space-y-3">
          <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-lg"></div>
        </div>
        <div v-else-if="recentChanges.length === 0" class="empty-state py-8">
          <div class="empty-state-title">Нет данных</div>
        </div>
        <div v-else class="divide-y divide-slate-100">
          <div v-for="change in recentChanges" :key="change.id"
            class="py-3 flex items-center gap-3 hover:bg-slate-50 -mx-2 px-2 rounded-lg transition-colors cursor-pointer"
            @click="$router.push(`/machines/${change.machine}`)">
            <div class="flex-shrink-0">
              <span :class="['status-badge', `status-${change.new_status_color}`]">
                <span :class="['status-dot', `status-dot-${change.new_status_color}`]"></span>
                {{ change.new_status_name }}
              </span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-slate-800 truncate">Станок #{{ change.machine }}</div>
              <div class="text-xs text-slate-400">{{ change.changed_by_name }}</div>
            </div>
            <div class="text-xs text-slate-400 flex-shrink-0">{{ formatDate(change.changed_at) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Workshop summary -->
    <div class="card p-6" v-if="auth.isAdmin || auth.isMaster">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-slate-800">Распределение по цехам</h3>
        <RouterLink to="/directories" class="text-sm text-primary-600 hover:text-primary-700 font-medium">
          Справочники →
        </RouterLink>
      </div>
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="i in 4" :key="i" class="skeleton h-16 rounded-xl"></div>
      </div>
      <div v-else-if="workshopStats.length === 0" class="text-slate-400 text-sm text-center py-6">
        Нет данных
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div v-for="ws in workshopStats" :key="ws.id"
          class="bg-slate-50 hover:bg-slate-100 rounded-xl p-4 transition-colors cursor-pointer"
          @click="$router.push(`/machines?workshop=${ws.id}`)">
          <div class="text-xl font-bold text-slate-900">{{ ws.machines_count }}</div>
          <div class="text-sm text-slate-600 truncate" :title="ws.name">{{ ws.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { machinesApi, statusesApi, workshopsApi } from '@/api'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
dayjs.locale('ru')

const router = useRouter()
const auth = useAuthStore()
const loading = ref(true)
const loadingHistory = ref(true)

const stats = ref({ total: 0, working: 0, repair: 0, idle: 0 })
const statusDistribution = ref([])
const recentChanges = ref([])
const workshopStats = ref([])

const currentDate = computed(() => dayjs().format('DD MMMM YYYY, dddd'))

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

    // Load machines summary
    const [machinesRes, statusesRes, workshopsRes] = await Promise.all([
      machinesApi.list({ page_size: 1 }),
      statusesApi.list(),
      workshopsApi.list(),
    ])

    const statuses = statusesRes.data.results || statusesRes.data
    workshopStats.value = (workshopsRes.data.results || workshopsRes.data).slice(0, 8)

    // Build status distribution
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

  // Load recent history
  try {
    loadingHistory.value = true
    // We'll use machine list and get recent status from them
    const res = await machinesApi.list({ page_size: 10, ordering: '-updated_at' })
    // For demonstration, show machines with their status
    const machines = res.data.results || []
    recentChanges.value = machines.slice(0, 6).map(m => ({
      id: m.id,
      machine: m.id,
      new_status_name: m.current_status_name || 'Не задан',
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
