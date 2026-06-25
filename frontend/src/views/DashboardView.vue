<template>
  <div class="animate-fade-in space-y-6">

    <!-- Header -->
    <div>
      <h1 class="text-xl font-bold text-slate-900">Dashboard</h1>
      <p class="text-xs text-slate-400 mt-0.5">{{ currentDate }}</p>
    </div>

    <!-- ── 1. Stats cards ── -->
    <div class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3">
      <template v-if="loading">
        <div v-for="i in 6" :key="i" class="skeleton h-24 rounded-2xl" :style="`animation-delay:${i*60}ms`"></div>
      </template>
      <template v-else>
        <!-- Total machines -->
        <div class="stat-card border-indigo-200 bg-indigo-50">
          <div class="stat-icon bg-indigo-100">
            <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
            </svg>
          </div>
          <div class="stat-val text-indigo-700">{{ d.stats?.total_machines ?? '—' }}</div>
          <div class="stat-lbl text-indigo-400">Jami stanoklar</div>
        </div>
        <!-- In repair -->
        <div class="stat-card border-blue-200 bg-blue-50">
          <div class="stat-icon bg-blue-100">
            <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/>
            </svg>
          </div>
          <div class="stat-val text-blue-700">{{ d.stats?.in_repair ?? '—' }}</div>
          <div class="stat-lbl text-blue-400">Jarayonda</div>
        </div>
        <!-- Overdue -->
        <div class="stat-card border-rose-200 bg-rose-50">
          <div class="stat-icon bg-rose-100">
            <svg class="w-4 h-4 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <div class="stat-val text-rose-700">{{ d.stats?.overdue_to ?? '—' }}</div>
          <div class="stat-lbl text-rose-400">Просрочено</div>
        </div>
        <!-- Near -->
        <div class="stat-card border-yellow-200 bg-yellow-50">
          <div class="stat-icon bg-yellow-100">
            <svg class="w-4 h-4 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="stat-val text-yellow-700">{{ d.stats?.near_to ?? '—' }}</div>
          <div class="stat-lbl text-yellow-500">Muhlati yaqin</div>
        </div>
        <!-- Month expense -->
        <div class="stat-card border-violet-200 bg-violet-50">
          <div class="stat-icon bg-violet-100">
            <svg class="w-4 h-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="stat-val text-violet-700">${{ fmtNum(d.stats?.current_month_expense) }}</div>
          <div class="stat-lbl text-violet-400">Bu oy xarajat</div>
          <div v-if="d.stats?.expense_change != null" class="mt-1 text-[10px] font-semibold"
            :class="d.stats.expense_change >= 0 ? 'text-rose-500' : 'text-emerald-500'">
            {{ d.stats.expense_change >= 0 ? '+' : '' }}{{ d.stats.expense_change }}% o'tgan oyga
          </div>
        </div>
        <!-- Warehouse -->
        <div class="stat-card border-emerald-200 bg-emerald-50">
          <div class="stat-icon bg-emerald-100">
            <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
          </div>
          <div class="stat-val text-emerald-700">${{ fmtNum(d.stats?.total_warehouse_value) }}</div>
          <div class="stat-lbl text-emerald-400">Ombor qiymati</div>
        </div>
      </template>
    </div>

    <!-- ── Main two-column grid ── -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">

      <!-- Left (wide) column -->
      <div class="xl:col-span-2 space-y-6">

        <!-- ── 4. Xarajatlar grafigi ── -->
        <div class="card p-5">
          <h2 class="section-title mb-4">Oxirgi 6 oylik xarajatlar</h2>
          <div v-if="loading" class="skeleton h-44 rounded-xl"></div>
          <div v-else-if="!chartData.datasets[0].data.some(v => v > 0)"
            class="h-44 flex items-center justify-center text-slate-400 text-sm italic">
            Ma'lumot yo'q
          </div>
          <div style="position:relative; height:180px">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <!-- ── 2. Filiallar xarajatlari ── -->
        <div class="card overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100">
            <h2 class="section-title">Filiallar kesimida xarajatlar</h2>
          </div>
          <div v-if="loading" class="p-4 space-y-2">
            <div v-for="i in 4" :key="i" class="skeleton h-10 rounded-lg"></div>
          </div>
          <div v-else-if="!d.workshop_expenses?.length"
            class="p-6 text-center text-slate-400 text-sm italic">Ma'lumot yo'q</div>
          <div v-else class="divide-y divide-slate-50">
            <RouterLink v-for="ws in d.workshop_expenses" :key="ws.workshop_id"
              :to="`/machines?workshop=${ws.workshop_id}`"
              class="flex items-center gap-4 px-5 py-3 hover:bg-slate-50 transition-colors">
              <div class="flex-1 min-w-0">
                <div class="text-sm font-semibold text-slate-800 truncate">{{ ws.workshop_name }}</div>
                <div class="text-xs text-slate-400 mt-0.5">{{ ws.machines_count }} ta stanok</div>
              </div>
              <div class="text-right flex-shrink-0">
                <div class="text-sm font-bold text-violet-700">${{ fmtNum(ws.yearly_cost) }}</div>
                <div class="text-xs text-slate-400">yillik</div>
              </div>
              <div class="text-right flex-shrink-0 w-20">
                <div class="text-xs font-semibold text-slate-600">${{ fmtNum(ws.current_month_cost) }}</div>
                <div class="text-xs text-slate-400">bu oy</div>
              </div>
              <svg class="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>
        </div>

        <!-- ── 3. Top 10 stanoklar ── -->
        <div class="card overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100">
            <h2 class="section-title">Eng ko'p xarajat — Top 10 stanok</h2>
          </div>
          <div v-if="loading" class="p-4 space-y-3">
            <div v-for="i in 5" :key="i" class="skeleton h-12 rounded-lg"></div>
          </div>
          <div v-else-if="!d.top_machines?.length"
            class="p-6 text-center text-slate-400 text-sm italic">Ma'lumot yo'q</div>
          <div v-else class="divide-y divide-slate-50">
            <RouterLink v-for="(m, idx) in d.top_machines" :key="m.machine_id"
              :to="`/machines/${m.machine_id}`"
              class="flex items-center gap-4 px-5 py-3 hover:bg-slate-50 transition-colors">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                :class="idx === 0 ? 'bg-violet-600 text-white' : 'bg-slate-100 text-slate-500'">
                {{ idx + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-sm font-semibold text-slate-800 truncate">{{ m.machine_name }}</div>
                <div class="text-xs text-slate-400 mt-0.5">{{ m.workshop_name }} · {{ m.inventory_number }}</div>
                <div class="mt-1.5 h-1.5 bg-slate-100 rounded-full overflow-hidden w-full">
                  <div class="h-full bg-violet-500 rounded-full transition-all duration-500"
                    :style="`width: ${m.percentage}%`"></div>
                </div>
              </div>
              <div class="text-right flex-shrink-0">
                <div class="text-sm font-bold text-violet-700">${{ fmtNum(m.total_expense) }}</div>
                <div v-if="m.last_to_date" class="text-xs text-slate-400 mt-0.5">{{ fmtDate(m.last_to_date) }}</div>
              </div>
            </RouterLink>
          </div>
        </div>

      </div><!-- /left col -->

      <!-- Right (narrow) column -->
      <div class="space-y-6">

        <!-- ── 5. TO holati donut ── -->
        <div class="card p-5">
          <h2 class="section-title mb-4">TO holati</h2>
          <div v-if="loading" class="skeleton h-44 rounded-xl"></div>
          <div v-else>
            <div class="flex justify-center mb-4">
              <div style="position:relative; height:160px; width:160px">
                <Doughnut :data="donutData" :options="donutOptions" />
              </div>
            </div>
            <div class="space-y-2">
              <RouterLink v-for="seg in donutSegments" :key="seg.key"
                to="/maintenance"
                class="flex items-center justify-between text-xs p-2 rounded-lg hover:bg-slate-50 transition-colors">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full flex-shrink-0" :style="`background:${seg.color}`"></div>
                  <span class="text-slate-600">{{ seg.label }}</span>
                </div>
                <span class="font-bold tabular-nums" :style="`color:${seg.color}`">{{ seg.value }}</span>
              </RouterLink>
            </div>
          </div>
        </div>

        <!-- ── 6. Oxirgi TO lar ── -->
        <div class="card overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 class="section-title">Oxirgi TO lar</h2>
            <RouterLink to="/maintenance" class="text-xs text-indigo-600 hover:underline">Barchasini ko'rish</RouterLink>
          </div>
          <div v-if="loading" class="p-3 space-y-2">
            <div v-for="i in 4" :key="i" class="skeleton h-12 rounded-lg"></div>
          </div>
          <div v-else-if="!d.recent_to?.length"
            class="p-5 text-center text-slate-400 text-sm italic">TO bajarilmagan</div>
          <div v-else class="divide-y divide-slate-50">
            <div v-for="r in d.recent_to" :key="r.machine_name + r.completed_at"
              class="flex items-center gap-3 px-4 py-3">
              <div class="w-8 h-8 rounded-xl bg-emerald-100 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-slate-800 truncate">{{ r.machine_name }}</div>
                <div class="text-[11px] text-slate-400 mt-0.5 truncate">{{ r.completed_by_name }} · {{ fmtDate(r.completed_at) }}</div>
              </div>
              <div v-if="r.total_cost > 0" class="text-xs font-bold text-violet-600 flex-shrink-0">${{ fmtNum(r.total_cost) }}</div>
            </div>
          </div>
        </div>

        <!-- ── 7. Ombor holati ── -->
        <div class="card overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 class="section-title">Kam qolgan mahsulotlar</h2>
            <RouterLink to="/sklad" class="text-xs text-indigo-600 hover:underline">Ko'rish</RouterLink>
          </div>
          <div v-if="loading" class="p-3 space-y-2">
            <div v-for="i in 4" :key="i" class="skeleton h-10 rounded-lg"></div>
          </div>
          <div v-else-if="!d.low_stock?.length"
            class="p-5 text-center text-slate-400 text-sm italic">Ma'lumot yo'q</div>
          <div v-else class="divide-y divide-slate-50">
            <div v-for="sp in d.low_stock" :key="sp.id"
              class="flex items-center gap-3 px-4 py-3">
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-slate-800 truncate">{{ sp.name }}</div>
                <div v-if="sp.machine_names?.length" class="text-[11px] text-slate-400 mt-0.5 truncate">
                  {{ sp.machine_names.join(', ') }}
                </div>
              </div>
              <div class="flex-shrink-0 text-right">
                <span class="text-sm font-bold tabular-nums px-2 py-0.5 rounded-full"
                  :class="sp.quantity <= 3 ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-600'">
                  {{ sp.quantity }} {{ sp.unit_short }}
                </span>
              </div>
            </div>
          </div>
        </div>

      </div><!-- /right col -->
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Bar, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement,
  ArcElement, Tooltip, Legend, Title
} from 'chart.js'
import { dashboardApi } from '@/api'
import dayjs from 'dayjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend, Title)

const loading = ref(true)
const d = ref({})

const currentDate = computed(() => dayjs().format('DD.MM.YYYY, dddd'))

function fmtNum(v) {
  if (v == null) return '0'
  const n = Number(v)
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}
function fmtDate(v) {
  return v ? dayjs(v).format('DD.MM.YYYY') : '—'
}

// ── Bar chart ──
const chartData = computed(() => {
  const months = d.value.monthly_chart || []
  return {
    labels: months.map(m => m.month_label),
    datasets: [{
      label: 'Xarajat ($)',
      data: months.map(m => m.total_cost),
      backgroundColor: 'rgba(139, 92, 246, 0.15)',
      borderColor: 'rgba(139, 92, 246, 0.8)',
      borderWidth: 2,
      borderRadius: 6,
    }],
  }
})
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` $${ctx.raw}` } } },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 11 } } },
    y: { grid: { color: '#f1f5f9' }, ticks: { font: { size: 11 }, callback: v => `$${v}` } },
  },
}

// ── Donut chart ──
const COLORS = {
  no_schedule: '#94a3b8',
  ok: '#10b981',
  near: '#f59e0b',
  overdue: '#f43f5e',
  in_repair: '#3b82f6',
}
const LABELS = {
  no_schedule: 'Grafik yo\'q',
  ok: 'Norma',
  near: 'Muhlati yaqin',
  overdue: 'Просрочено',
  in_repair: 'Jarayonda',
}
const donutSegments = computed(() => {
  const s = d.value.to_status || {}
  return Object.entries(s)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => ({ key: k, label: LABELS[k] || k, value: v, color: COLORS[k] || '#999' }))
})
const donutData = computed(() => ({
  labels: donutSegments.value.map(s => s.label),
  datasets: [{
    data: donutSegments.value.map(s => s.value),
    backgroundColor: donutSegments.value.map(s => s.color),
    borderWidth: 2,
    borderColor: '#fff',
  }],
}))
const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} ta` } },
  },
}

async function loadData() {
  loading.value = true
  try {
    const res = await dashboardApi.get()
    d.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.card { @apply bg-white rounded-2xl border border-slate-200 shadow-sm; }

.stat-card {
  @apply rounded-2xl border p-4 flex flex-col gap-1;
}
.stat-icon {
  @apply w-8 h-8 rounded-xl flex items-center justify-center mb-1;
}
.stat-val  { @apply text-2xl font-bold tabular-nums; }
.stat-lbl  { @apply text-[11px] font-medium uppercase tracking-wide; }

.section-title { @apply text-sm font-semibold text-slate-800; }

@keyframes fadeIn { from { opacity:0; transform:translateY(6px) } to { opacity:1; transform:none } }
.animate-fade-in { animation: fadeIn .25s ease; }
</style>
