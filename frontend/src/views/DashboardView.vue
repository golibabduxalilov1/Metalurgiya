<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold text-slate-900">{{ t('dashboard.title') }}</h1>
        <p class="text-xs text-slate-400 mt-0.5">{{ currentDate }}</p>
      </div>

      <!-- Period picker -->
      <div class="flex flex-wrap items-center gap-2">
        <!-- Presets -->
        <div class="flex gap-1">
          <button
            v-for="p in presets" :key="p.key"
            @click="applyPreset(p)"
            :class="['period-preset', activePreset === p.key ? 'period-preset--active' : '']"
          >{{ t(`dashboard.${p.key}`) }}</button>
        </div>
        <!-- Date inputs -->
        <div class="period-range-box">
          <svg class="w-3.5 h-3.5 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <input type="date" v-model="periodFrom" @change="onPeriodChange" class="period-date-input" />
          <span class="text-slate-300 text-xs">—</span>
          <input type="date" v-model="periodTo" @change="onPeriodChange" class="period-date-input" />
        </div>
      </div>

      <!-- Health / time badge -->
      <div :class="['health-badge', `health-${fleetHealth.level}`]">
        <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" :class="{
          'bg-emerald-500': fleetHealth.level === 'good',
          'bg-amber-500':   fleetHealth.level === 'warning',
          'bg-rose-500':    fleetHealth.level === 'critical',
        }"></span>
        <template v-if="periodStats">
          {{ periodStats.working_hours }} {{ t('dashboard.period_hours') }}
        </template>
        <template v-else>
          {{ fleetHealth.label }}
        </template>
      </div>
    </div>

    <!-- KPI skeleton -->
    <div v-if="loading" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="skeleton h-36 rounded-2xl"></div>
    </div>

    <!-- KPI Cards -->
    <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-4">

      <div class="kpi-card kpi-indigo" @click="$router.push('/machines')">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="kpi-value">{{ stats.total }}</div>
            <div class="kpi-label">{{ t('dashboard.total') }}</div>
          </div>
          <div class="kpi-icon bg-indigo-50">
            <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
            </svg>
          </div>
        </div>
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-xs text-slate-400">{{ t('dashboard.efficiency') }}</span>
          <span class="text-xs font-bold text-indigo-600">{{ efficiency }}%</span>
        </div>
        <div class="progress-track"><div class="progress-fill bg-indigo-500" :style="{ width: efficiency + '%' }"></div></div>
      </div>

      <div class="kpi-card kpi-emerald" @click="goToStatus('working')">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="kpi-value text-emerald-600">{{ stats.working }}</div>
            <div class="kpi-label">{{ t('dashboard.working') }}</div>
          </div>
          <div class="kpi-icon bg-emerald-50">
            <svg class="w-6 h-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-xs text-slate-400">{{ t('dashboard.of_fleet') }}</span>
          <span class="text-xs font-bold text-emerald-600">{{ pct(stats.working) }}%</span>
        </div>
        <div class="progress-track"><div class="progress-fill bg-emerald-500" :style="{ width: pct(stats.working) + '%' }"></div></div>
      </div>

      <div class="kpi-card kpi-rose" @click="goToStatus('repair')">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="kpi-value text-rose-500">{{ stats.repair }}</div>
            <div class="kpi-label">{{ t('dashboard.repair') }}</div>
          </div>
          <div class="kpi-icon bg-rose-50">
            <svg class="w-6 h-6 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
        </div>
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-xs text-slate-400">{{ t('dashboard.of_fleet') }}</span>
          <span class="text-xs font-bold text-rose-500">{{ pct(stats.repair) }}%</span>
        </div>
        <div class="progress-track"><div class="progress-fill bg-rose-500" :style="{ width: pct(stats.repair) + '%' }"></div></div>
      </div>

      <div class="kpi-card kpi-amber" @click="goToStatus('idle')">
        <div class="flex items-start justify-between mb-4">
          <div>
            <div class="kpi-value text-amber-500">{{ stats.idle }}</div>
            <div class="kpi-label">{{ t('dashboard.idle') }}</div>
          </div>
          <div class="kpi-icon bg-amber-50">
            <svg class="w-6 h-6 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="flex justify-between items-center mb-1.5">
          <span class="text-xs text-slate-400">{{ t('dashboard.of_fleet') }}</span>
          <span class="text-xs font-bold text-amber-500">{{ pct(stats.idle) }}%</span>
        </div>
        <div class="progress-track"><div class="progress-fill bg-amber-500" :style="{ width: pct(stats.idle) + '%' }"></div></div>
      </div>
    </div>

    <!-- Period Stats -->
    <div class="card p-5">
      <div class="chart-header mb-4">
        <div>
          <h3 class="chart-title">{{ t('dashboard.period_title') }}</h3>
          <p class="text-[11px] text-slate-400 mt-0.5">{{ t('dashboard.period_all_machines') }}</p>
        </div>
        <div v-if="loadingPeriod" class="text-xs text-slate-400 flex items-center gap-1.5">
          <span class="w-3 h-3 border-2 border-indigo-300 border-t-indigo-600 rounded-full animate-spin"></span>
          Yuklanmoqda...
        </div>
      </div>

      <div v-if="loadingPeriod && !periodStats" class="skeleton rounded-xl" style="height:200px"></div>

      <template v-else-if="periodStats">
        <!-- Three time cards -->
        <div class="grid grid-cols-3 gap-3 mb-4">
          <div class="period-stat-card period-stat-green">
            <div class="period-stat-value text-emerald-700">
              {{ periodStats.working_hours }}
              <span class="period-stat-unit">{{ t('dashboard.period_hours') }}</span>
            </div>
            <div class="period-stat-label text-emerald-500">{{ t('dashboard.period_working') }}</div>
          </div>
          <div class="period-stat-card period-stat-red">
            <div class="period-stat-value text-rose-600">
              {{ periodStats.repair_hours }}
              <span class="period-stat-unit">{{ t('dashboard.period_hours') }}</span>
            </div>
            <div class="period-stat-label text-rose-400">{{ t('dashboard.period_repair') }}</div>
          </div>
          <div class="period-stat-card period-stat-amber">
            <div class="period-stat-value text-amber-600">
              {{ periodStats.idle_hours }}
              <span class="period-stat-unit">{{ t('dashboard.period_hours') }}</span>
            </div>
            <div class="period-stat-label text-amber-500">{{ t('dashboard.period_idle') }}</div>
          </div>
        </div>


        <!-- Daily stacked bar chart -->
        <div style="height:200px">
          <Bar :data="periodChartData" :options="periodChartOptions" />
        </div>
      </template>

      <div v-else class="no-data">{{ t('common.no_data') }}</div>
    </div>

    <!-- Row 2: Donut + Line -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">

      <!-- Status Doughnut -->
      <div class="card p-5">
        <div class="chart-header">
          <h3 class="chart-title">{{ t('dashboard.statuses') }}</h3>
        </div>
        <div v-if="loading" class="skeleton h-64 rounded-xl mt-4"></div>
        <template v-else-if="statusDistribution.length > 0">
          <div class="relative mt-3" style="height:210px">
            <Doughnut :data="doughnutData" :options="doughnutOptions" />
            <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <div class="text-3xl font-bold text-slate-900 tabular-nums">{{ efficiency }}%</div>
              <div class="text-xs text-slate-400 text-center leading-tight mt-1">{{ t('dashboard.efficiency') }}</div>
            </div>
          </div>
          <!-- Legend with mini bars -->
          <div class="mt-4 space-y-2.5">
            <div v-for="item in statusDistribution" :key="item.name" class="group">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="w-2.5 h-2.5 rounded flex-shrink-0"
                    :style="{ backgroundColor: colorHex[item.color] || colorHex.gray }"></span>
                  <span class="text-sm text-slate-600 truncate">{{ item.name }}</span>
                </div>
                <div class="text-sm flex-shrink-0 ml-2">
                  <span class="font-bold text-slate-800">{{ item.count }}</span>
                  <span class="text-slate-400 text-xs font-normal"> / {{ pct(item.count) }}%</span>
                </div>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-1.5">
                <div class="h-1.5 rounded-full transition-all duration-700"
                  :style="{ width: pct(item.count) + '%', backgroundColor: colorHex[item.color] || colorHex.gray }">
                </div>
              </div>
            </div>
          </div>
        </template>
        <div v-else class="no-data mt-4">{{ t('common.no_data') }}</div>
      </div>

      <!-- Activity Line Chart -->
      <div class="card p-5 lg:col-span-2">
        <div class="chart-header mb-3">
          <div>
            <h3 class="chart-title">{{ t('dashboard.activity_trend') }}</h3>
            <p class="text-[11px] text-slate-400 mt-0.5">{{ t('dashboard.activity_trend_hint') }}</p>
          </div>
        </div>

        <!-- Stats summary row -->
        <div v-if="!loadingHistory" class="grid grid-cols-3 gap-3 mb-4">
          <div class="stat-mini bg-indigo-50 rounded-xl p-3">
            <div class="text-xl font-bold text-indigo-700 tabular-nums">{{ activityStats.total }}</div>
            <div class="text-[10px] text-indigo-400 mt-0.5 uppercase tracking-wide font-medium">Jami</div>
          </div>
          <div class="stat-mini bg-slate-50 rounded-xl p-3">
            <div class="text-xl font-bold text-slate-700 tabular-nums">{{ activityStats.max }}</div>
            <div class="text-[10px] text-slate-400 mt-0.5 uppercase tracking-wide font-medium">Maks · {{ activityStats.maxDay }}</div>
          </div>
          <div class="stat-mini bg-slate-50 rounded-xl p-3">
            <div class="text-xl font-bold text-slate-700 tabular-nums">{{ activityStats.avg }}</div>
            <div class="text-[10px] text-slate-400 mt-0.5 uppercase tracking-wide font-medium">O'rtacha / kun</div>
          </div>
        </div>

        <div v-if="loadingHistory" class="skeleton rounded-xl" style="height:220px"></div>
        <div v-else style="height:220px">
          <Line :data="activityTrendData" :options="activityTrendOptions" />
        </div>
      </div>
    </div>

    <!-- Row 3: Workshops bar + Machine Types leaderboard -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">

      <!-- Workshops multi-color horizontal bar -->
      <div class="card p-5" v-if="auth.isAdmin || auth.isMaster">
        <div class="chart-header mb-3">
          <h3 class="chart-title">{{ t('dashboard.workshops') }}</h3>
          <RouterLink to="/directories" class="chart-link">
            {{ t('dashboard.directories_link') }}
            <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>
        <div v-if="loading" class="skeleton rounded-xl" style="height:260px"></div>
        <div v-else-if="workshopStats.length === 0" class="no-data">{{ t('common.no_data') }}</div>
        <div v-else class="chart-box" :style="{ height: chartHeight(workshopStats.length) }">
          <Bar :data="workshopChartData" :options="workshopChartOptions" />
        </div>
      </div>

      <!-- Machine Types leaderboard -->
      <div class="card p-5">
        <div class="chart-header mb-3">
          <h3 class="chart-title">{{ t('dashboard.machine_types') }}</h3>
          <span class="text-[11px] text-slate-400">{{ typeStats.length }} {{ t('dashboard.type_count') }}</span>
        </div>
        <div v-if="loading" class="skeleton rounded-xl" style="height:260px"></div>
        <div v-else-if="typeStats.length === 0" class="no-data">{{ t('common.no_data') }}</div>
        <div v-else class="space-y-3 mt-1">
          <div
            v-for="(tp, i) in typeStats" :key="tp.id"
            class="leaderboard-row"
            @click="router.push(`/machines?machine_type=${tp.id}`)"
          >
            <div
              class="rank-badge"
              :style="{ backgroundColor: typeBarColors[i % typeBarColors.length] + '20',
                        color: typeBarColors[i % typeBarColors.length] }"
            >
              {{ i + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-sm font-medium text-slate-700 truncate pr-2">{{ tp.name }}</span>
                <span class="text-sm font-bold text-slate-800 flex-shrink-0">
                  {{ tp.machines_count }}
                  <span class="text-xs font-normal text-slate-400 ml-1">
                    ({{ stats.total ? Math.round((tp.machines_count / stats.total) * 100) : 0 }}%)
                  </span>
                </span>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all duration-700"
                  :style="{
                    width: typeStats[0].machines_count
                      ? ((tp.machines_count / typeStats[0].machines_count) * 100) + '%'
                      : '0%',
                    backgroundColor: typeBarColors[i % typeBarColors.length],
                  }"
                ></div>
              </div>
            </div>
          </div>
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
import { machinesApi, statusesApi, workshopsApi, machineTypesApi } from '@/api'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import 'dayjs/locale/uz'
import { Doughnut, Bar, Line } from 'vue-chartjs'
import {
  Chart as ChartJS, ArcElement, BarElement, LineElement, PointElement,
  CategoryScale, LinearScale, Tooltip, Legend, Filler,
} from 'chart.js'

ChartJS.register(
  ArcElement, BarElement, LineElement, PointElement,
  CategoryScale, LinearScale, Tooltip, Legend, Filler,
)

const router = useRouter()
const auth = useAuthStore()
const langStore = useLangStore()
const { t } = useI18n()
const loading = ref(true)
const loadingHistory = ref(true)

const stats = ref({ total: 0, working: 0, repair: 0, idle: 0 })
const statusDistribution = ref([])
const workshopStats = ref([])
const typeStats = ref([])
const activityTrend = ref({ labels: [], counts: [] })

// ── Period picker ──
const periodFrom = ref(dayjs().subtract(6, 'day').format('YYYY-MM-DD'))
const periodTo   = ref(dayjs().format('YYYY-MM-DD'))
const activePreset = ref('period_week')
const loadingPeriod = ref(false)
const periodStats = ref(null)

const presets = [
  { key: 'period_today',      from: () => dayjs().format('YYYY-MM-DD'),                      to: () => dayjs().format('YYYY-MM-DD') },
  { key: 'period_week',       from: () => dayjs().subtract(6, 'day').format('YYYY-MM-DD'),   to: () => dayjs().format('YYYY-MM-DD') },
  { key: 'period_month',      from: () => dayjs().subtract(29, 'day').format('YYYY-MM-DD'),  to: () => dayjs().format('YYYY-MM-DD') },
  { key: 'period_this_month', from: () => dayjs().startOf('month').format('YYYY-MM-DD'),     to: () => dayjs().format('YYYY-MM-DD') },
]

function applyPreset(p) {
  activePreset.value = p.key
  periodFrom.value = p.from()
  periodTo.value   = p.to()
  loadPeriodStats()
}

function onPeriodChange() {
  activePreset.value = ''
  loadPeriodStats()
}

async function loadPeriodStats() {
  loadingPeriod.value = true
  try {
    const res = await machinesApi.periodStats({ date_from: periodFrom.value, date_to: periodTo.value })
    periodStats.value = res.data
  } catch (e) {
    console.error(e)
    periodStats.value = null
  } finally {
    loadingPeriod.value = false
  }
}

// ── Period chart ──
const periodChartData = computed(() => {
  const daily = periodStats.value?.daily ?? []
  return {
    labels: daily.map(d => d.date),
    datasets: [
      {
        label: t('dashboard.period_working'),
        data: daily.map(d => d.working_hours),
        backgroundColor: '#10b981',
        stack: 'time',
        borderRadius: 3,
        maxBarThickness: 32,
      },
      {
        label: t('dashboard.period_repair'),
        data: daily.map(d => d.repair_hours),
        backgroundColor: '#f43f5e',
        stack: 'time',
        maxBarThickness: 32,
      },
      {
        label: t('dashboard.period_idle'),
        data: daily.map(d => d.idle_hours),
        backgroundColor: '#f59e0b',
        stack: 'time',
        maxBarThickness: 32,
      },
    ],
  }
})

const periodChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  scales: {
    x: {
      grid: { display: false },
      stacked: true,
      ticks: { font: { size: 11 }, maxRotation: 30, minRotation: 30, autoSkip: true, maxTicksLimit: 14 },
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: { font: { size: 11 } },
      grid: { color: '#f1f5f9' },
      title: { display: true, text: 'soat', font: { size: 10 }, color: '#94a3b8' },
    },
  },
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
      labels: { boxWidth: 10, boxHeight: 10, font: { size: 11 }, padding: 12 },
    },
    tooltip: {
      callbacks: {
        label: (ctx) => ` ${ctx.dataset.label}: ${ctx.raw} soat`,
      },
    },
  },
}

// ── Rest of existing code ──
const currentDate = computed(() => {
  const locale = langStore.lang === 'uz' ? 'uz' : 'ru'
  return dayjs().locale(locale).format('DD MMMM YYYY, dddd')
})

const colorHex = {
  green: '#10b981',
  yellow: '#f59e0b',
  red:   '#ef4444',
  gray:  '#94a3b8',
  blue:  '#3b82f6',
}

const typeBarColors = [
  '#6366f1', '#8b5cf6', '#3b82f6', '#0ea5e9',
  '#10b981', '#f59e0b', '#f43f5e', '#64748b',
]

function pct(value) {
  return stats.value.total ? Math.round((value / stats.value.total) * 100) : 0
}

const efficiency = computed(() => pct(stats.value.working))

const fleetHealth = computed(() => {
  const repairShare = pct(stats.value.repair)
  if (!stats.value.total) return { level: 'good', label: t('dashboard.health_good') }
  if (repairShare >= 20)  return { level: 'critical', label: t('dashboard.health_critical') }
  if (repairShare >= 8)   return { level: 'warning', label: t('dashboard.health_warning') }
  return { level: 'good', label: t('dashboard.health_good') }
})

// --- Doughnut ---
const doughnutData = computed(() => ({
  labels: statusDistribution.value.map(i => i.name),
  datasets: [{
    data: statusDistribution.value.map(i => i.count),
    backgroundColor: statusDistribution.value.map(i => colorHex[i.color] || colorHex.gray),
    borderWidth: 3,
    borderColor: '#ffffff',
    hoverOffset: 10,
  }],
}))

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '68%',
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => ` ${ctx.label}: ${ctx.raw} (${Math.round((ctx.raw / (stats.value.total || 1)) * 100)}%)`,
      },
    },
  },
}

// --- Activity stats ---
const activityStats = computed(() => {
  const counts = activityTrend.value.counts
  const labels = activityTrend.value.labels
  if (!counts.length) return { total: 0, max: 0, maxDay: '—', avg: '0' }
  const total = counts.reduce((a, b) => a + b, 0)
  const max   = Math.max(...counts)
  const maxIdx = counts.indexOf(max)
  return {
    total,
    max,
    maxDay: labels[maxIdx] || '—',
    avg: (total / counts.length).toFixed(1),
  }
})

// --- Activity line chart with avg reference line ---
const activityTrendData = computed(() => {
  const avg = parseFloat(activityStats.value.avg) || 0
  return {
    labels: activityTrend.value.labels,
    datasets: [
      {
        label: t('dashboard.changes_count'),
        data: activityTrend.value.counts,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,0.13)',
        pointBackgroundColor: '#6366f1',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        borderWidth: 3,
        tension: 0.4,
        fill: true,
        order: 1,
      },
      {
        label: 'avg',
        data: activityTrend.value.counts.map(() => avg),
        borderColor: 'rgba(99,102,241,0.4)',
        borderDash: [6, 4],
        borderWidth: 1.5,
        pointRadius: 0,
        pointHoverRadius: 0,
        fill: false,
        order: 2,
      },
    ],
  }
})

const activityTrendOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  scales: {
    x: {
      grid: { display: false },
      ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 7, font: { size: 11 } },
    },
    y: {
      beginAtZero: true,
      ticks: { precision: 0, font: { size: 11 } },
      grid: { color: '#f1f5f9' },
    },
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      filter: (item) => item.datasetIndex === 0,
      callbacks: {
        label: (ctx) => ` ${t('dashboard.changes_count')}: ${ctx.raw}`,
      },
    },
  },
}

// --- Workshops multi-color horizontal bar ---
const workshopBarColors = [
  '#6366f1', '#8b5cf6', '#a855f7', '#7c3aed',
  '#4f46e5', '#3b82f6', '#0ea5e9', '#06b6d4',
]

const workshopChartData = computed(() => ({
  labels: workshopStats.value.map(ws => ws.name),
  datasets: [{
    data: workshopStats.value.map(ws => ws.machines_count || 0),
    backgroundColor: workshopStats.value.map((_, i) => workshopBarColors[i % workshopBarColors.length]),
    borderRadius: 6,
    maxBarThickness: 28,
  }],
}))

const workshopChartOptions = computed(() => ({
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  onClick: (evt, elements) => {
    if (elements.length) {
      const ws = workshopStats.value[elements[0].index]
      if (ws) router.push(`/machines?workshop=${ws.id}`)
    }
  },
  onHover: (evt, elements) => {
    evt.native.target.style.cursor = elements.length ? 'pointer' : 'default'
  },
  scales: {
    x: {
      beginAtZero: true,
      ticks: { precision: 0, font: { size: 12 } },
      grid: { color: '#f1f5f9' },
    },
    y: {
      grid: { display: false },
      ticks: { font: { size: 12 } },
    },
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => ` ${workshopStats.value[ctx.dataIndex]?.name || ''}: ${ctx.raw} ta`,
      },
    },
  },
}))

function chartHeight(itemsCount) {
  return `${Math.max(220, itemsCount * 48)}px`
}

function goToStatus(key) {
  router.push(`/machines?status_color=${key}`)
}

function buildActivityTrend(machines) {
  const days = 14
  const today = dayjs().startOf('day')
  const buckets = new Map()
  for (let i = days - 1; i >= 0; i--) {
    buckets.set(today.subtract(i, 'day').format('YYYY-MM-DD'), 0)
  }
  machines.forEach(m => {
    if (!m.updated_at) return
    const key = dayjs(m.updated_at).format('YYYY-MM-DD')
    if (buckets.has(key)) buckets.set(key, buckets.get(key) + 1)
  })
  return {
    labels: [...buckets.keys()].map(k => dayjs(k).format('DD.MM')),
    counts: [...buckets.values()],
  }
}

async function loadData() {
  try {
    loading.value = true
    const [machinesRes, statusesRes, workshopsRes, typesRes] = await Promise.all([
      machinesApi.list({ page_size: 1 }),
      statusesApi.list(),
      workshopsApi.list(),
      machineTypesApi.list(),
    ])

    const statuses = statusesRes.data.results || statusesRes.data
    workshopStats.value = (workshopsRes.data.results || workshopsRes.data)
      .slice()
      .sort((a, b) => (b.machines_count || 0) - (a.machines_count || 0))
      .slice(0, 8)

    typeStats.value = (typesRes.data.results || typesRes.data)
      .filter(tp => (tp.machines_count || 0) > 0)
      .slice()
      .sort((a, b) => (b.machines_count || 0) - (a.machines_count || 0))
      .slice(0, 8)

    let totalWorking = 0, totalRepair = 0, totalIdle = 0
    statusDistribution.value = statuses.map(s => {
      const count = s.machines_count || 0
      if (s.color === 'green')  totalWorking += count
      if (s.color === 'red')    totalRepair  += count
      if (s.color === 'yellow') totalIdle    += count
      return { name: s.name, count, color: s.color }
    })

    stats.value = {
      total:   machinesRes.data.count || 0,
      working: totalWorking,
      repair:  totalRepair,
      idle:    totalIdle,
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }

  try {
    loadingHistory.value = true
    const res = await machinesApi.list({ page_size: 60, ordering: '-updated_at' })
    activityTrend.value = buildActivityTrend(res.data.results || [])
  } catch (e) {
    console.error(e)
  } finally {
    loadingHistory.value = false
  }
}

onMounted(() => {
  loadData()
  loadPeriodStats()
})
</script>

<style scoped>
/* ── KPI cards ── */
.kpi-card {
  @apply bg-white rounded-2xl border border-slate-200 shadow-sm p-5
         cursor-pointer transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg;
}
.kpi-icon  { @apply w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0; }
.kpi-value { @apply text-4xl font-bold text-slate-900 leading-none tabular-nums; }
.kpi-label { @apply text-sm text-slate-500 mt-1.5; }

.kpi-indigo  { border-left: 4px solid #6366f1; }
.kpi-emerald { border-left: 4px solid #10b981; }
.kpi-rose    { border-left: 4px solid #f43f5e; }
.kpi-amber   { border-left: 4px solid #f59e0b; }

/* ── Progress bar ── */
.progress-track {
  @apply w-full bg-slate-100 rounded-full overflow-hidden;
  height: 5px;
}
.progress-fill {
  height: 5px;
  border-radius: 9999px;
  transition: width 0.7s ease;
  min-width: 2px;
}

/* ── Period picker ── */
.period-range-box {
  @apply flex items-center gap-1.5 bg-white border border-slate-200
         rounded-xl px-3 py-1.5 shadow-sm;
}
.period-date-input {
  @apply text-xs text-slate-700 bg-transparent outline-none border-none
         cursor-pointer;
  font-family: inherit;
  min-width: 0;
}
.period-date-input::-webkit-calendar-picker-indicator {
  opacity: 0.5;
  cursor: pointer;
}
.period-preset {
  @apply text-xs font-medium px-2.5 py-1 rounded-lg border border-slate-200
         bg-white text-slate-600 hover:bg-indigo-50 hover:border-indigo-200
         hover:text-indigo-600 transition-colors duration-150 cursor-pointer;
}
.period-preset--active {
  @apply bg-indigo-50 border-indigo-200 text-indigo-600;
}

/* ── Period stat cards ── */
.period-stat-card {
  @apply rounded-xl p-3 border;
}
.period-stat-green { @apply bg-emerald-50 border-emerald-100; }
.period-stat-red   { @apply bg-rose-50 border-rose-100; }
.period-stat-amber { @apply bg-amber-50 border-amber-100; }

.period-stat-value {
  @apply text-2xl font-bold tabular-nums leading-none;
}
.period-stat-unit  { @apply text-sm font-normal ml-0.5; }
.period-stat-label { @apply text-[10px] uppercase tracking-wide font-medium mt-1; }

/* ── Chart header ── */
.chart-header { @apply flex items-center justify-between; }
.chart-title  { @apply text-sm font-semibold text-slate-700; }
.chart-link   {
  @apply inline-flex items-center gap-1 text-xs font-medium text-indigo-600
         hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100
         border border-indigo-100 px-2.5 py-1 rounded-full
         transition-colors duration-150;
}
.no-data  { @apply text-sm text-slate-400 text-center py-10; }
.chart-box { @apply relative w-full; }

/* ── Activity mini stats ── */
.stat-mini { @apply transition-colors duration-150; }

/* ── Leaderboard ── */
.leaderboard-row {
  @apply flex items-center gap-3 p-2.5 rounded-xl
         cursor-pointer transition-all duration-150
         hover:bg-slate-50 hover:-translate-y-px;
}
.rank-badge {
  @apply w-7 h-7 rounded-lg flex items-center justify-center
         text-xs font-bold flex-shrink-0;
}

/* ── Health badge ── */
.health-badge {
  @apply inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5
         rounded-full border flex-shrink-0;
}
.health-good     { @apply bg-emerald-50 text-emerald-600 border-emerald-100; }
.health-warning  { @apply bg-amber-50   text-amber-600   border-amber-100;  }
.health-critical { @apply bg-rose-50    text-rose-600    border-rose-100;   }

@media (prefers-reduced-motion: reduce) {
  .kpi-card, .progress-fill, .leaderboard-row { transition: none; }
}
</style>
