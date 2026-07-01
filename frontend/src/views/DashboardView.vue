<template>
  <div class="animate-fade-in space-y-6">

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold text-slate-900">Панель управления</h1>
        <p class="text-xs text-slate-400 mt-0.5">{{ currentDate }}</p>
      </div>

      <!-- ── Time filter ── -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="flex bg-slate-100 rounded-xl p-1 gap-1">
          <button v-for="p in presets" :key="p.key"
            @click="setPreset(p.key)"
            class="px-3 py-1.5 text-xs font-medium rounded-lg transition-all"
            :class="preset === p.key
              ? 'bg-white text-indigo-700 shadow-sm font-semibold'
              : 'text-slate-500 hover:text-slate-700'">
            {{ p.label }}
          </button>
        </div>
        <Transition name="fade-slide">
          <div v-if="preset === 'custom'" class="flex items-center gap-2">
            <input type="date" v-model="customFrom"
              class="text-xs border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-white" />
            <span class="text-slate-400 text-xs">—</span>
            <input type="date" v-model="customTo"
              class="text-xs border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-300 bg-white" />
          </div>
        </Transition>
      </div>
    </div>

    <!-- ══════════════════════════════════════════
         1. UMUMIY XARAJATLAR
    ══════════════════════════════════════════ -->
    <div class="space-y-4">
      <h2 class="section-title px-1">Общие расходы</h2>
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">

        <!-- Donut chart -->
        <div class="card p-5">
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wide mb-3">Состав</div>
          <div v-if="loading" class="skeleton h-44 rounded-xl"></div>
          <div v-else>
            <div class="flex justify-center mb-3">
              <div style="position:relative; height:150px; width:150px">
                <Doughnut :data="totalDonutData" :options="donutOptions" />
              </div>
            </div>
            <div class="space-y-2">
              <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-slate-50">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-indigo-500"></div>
                  <span class="text-slate-600">Расходы ТО</span>
                </div>
                <span class="font-bold text-indigo-700">
                  ${{ fmtNum(d.total_expenses?.to_amount) }}
                  <span class="text-slate-400 font-normal">({{ d.total_expenses?.to_pct }}%)</span>
                </span>
              </div>
              <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-slate-50">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                  <span class="text-slate-600">Расходы склада</span>
                </div>
                <span class="font-bold text-emerald-700">
                  ${{ fmtNum(d.total_expenses?.warehouse_amount) }}
                  <span class="text-slate-400 font-normal">({{ d.total_expenses?.warehouse_pct }}%)</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Total + comparison -->
        <div class="card p-5 xl:col-span-2 flex flex-col justify-between">
          <div>
            <div class="text-xs font-medium text-slate-500 uppercase tracking-wide">Итого расходов</div>
            <div v-if="loading" class="skeleton h-10 w-40 rounded-lg mt-2"></div>
            <div v-else class="mt-2">
              <div class="text-4xl font-bold text-slate-900 tabular-nums">${{ fmtNum(d.total_expenses?.total) }}</div>
            </div>
          </div>
          <div v-if="!loading && d.total_expenses">
            <div class="mt-4 pt-4 border-t border-slate-100">
              <div class="text-xs text-slate-500 mb-2">Сравнение с предыдущим периодом</div>
              <div class="flex items-center gap-3">
                <div class="flex-1 bg-slate-50 rounded-xl p-3">
                  <div class="text-xs text-slate-500">Предыдущий период</div>
                  <div class="text-lg font-bold text-slate-700 tabular-nums mt-0.5">
                    ${{ fmtNum(d.total_expenses.prev_total) }}
                  </div>
                </div>
                <div class="flex-shrink-0">
                  <div class="flex flex-col items-center">
                    <div class="text-2xl"
                      :class="(d.total_expenses.change_pct ?? 0) >= 0 ? 'text-rose-500' : 'text-emerald-500'">
                      {{ (d.total_expenses.change_pct ?? 0) >= 0 ? '↑' : '↓' }}
                    </div>
                    <div v-if="d.total_expenses.change_pct != null"
                      class="text-sm font-bold tabular-nums"
                      :class="d.total_expenses.change_pct >= 0 ? 'text-rose-600' : 'text-emerald-600'">
                      {{ d.total_expenses.change_pct >= 0 ? '+' : '' }}{{ d.total_expenses.change_pct }}%
                    </div>
                    <div v-else class="text-xs text-slate-400">—</div>
                  </div>
                </div>
                <div class="flex-1 rounded-xl p-3"
                  :class="(d.total_expenses.change_amount ?? 0) >= 0 ? 'bg-rose-50' : 'bg-emerald-50'">
                  <div class="text-xs text-slate-500">Разница</div>
                  <div class="text-lg font-bold tabular-nums mt-0.5"
                    :class="(d.total_expenses.change_amount ?? 0) >= 0 ? 'text-rose-700' : 'text-emerald-700'">
                    {{ (d.total_expenses.change_amount ?? 0) >= 0 ? '+' : '' }}${{ fmtNum(Math.abs(d.total_expenses.change_amount ?? 0)) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════
         2. STANOKLAR HOLATI (HOZIRGI KUN)
    ══════════════════════════════════════════ -->
    <div class="space-y-4">
      <h2 class="section-title px-1">Состояние станков (текущее)</h2>
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-3">

        <!-- Working -->
        <div class="status-card cursor-pointer select-none"
          :class="openGroup === 'working' ? 'ring-2 ring-emerald-400' : ''"
          @click="toggleGroup('working')">
          <div class="flex items-center justify-between">
            <div class="w-9 h-9 rounded-xl bg-emerald-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <svg class="w-4 h-4 text-slate-400 transition-transform"
              :class="openGroup === 'working' ? 'rotate-180' : ''"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div v-if="loading" class="skeleton h-7 w-12 rounded mt-3"></div>
          <div v-else class="text-2xl font-bold text-emerald-700 mt-3 tabular-nums">
            {{ d.machine_status?.working?.count ?? 0 }}
          </div>
          <div class="text-xs font-medium text-emerald-600 mt-0.5">Работает</div>
        </div>

        <!-- In repair -->
        <div class="status-card cursor-pointer select-none"
          :class="openGroup === 'in_repair' ? 'ring-2 ring-blue-400' : ''"
          @click="toggleGroup('in_repair')">
          <div class="flex items-center justify-between">
            <div class="w-9 h-9 rounded-xl bg-blue-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <svg class="w-4 h-4 text-slate-400 transition-transform"
              :class="openGroup === 'in_repair' ? 'rotate-180' : ''"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div v-if="loading" class="skeleton h-7 w-12 rounded mt-3"></div>
          <div v-else class="text-2xl font-bold text-blue-700 mt-3 tabular-nums">
            {{ d.machine_status?.in_repair?.count ?? 0 }}
          </div>
          <div class="text-xs font-medium text-blue-600 mt-0.5">В ремонте</div>
        </div>

        <!-- Stopped -->
        <div class="status-card cursor-pointer select-none"
          :class="openGroup === 'stopped' ? 'ring-2 ring-rose-400' : ''"
          @click="toggleGroup('stopped')">
          <div class="flex items-center justify-between">
            <div class="w-9 h-9 rounded-xl bg-rose-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
              </svg>
            </div>
            <svg class="w-4 h-4 text-slate-400 transition-transform"
              :class="openGroup === 'stopped' ? 'rotate-180' : ''"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div v-if="loading" class="skeleton h-7 w-12 rounded mt-3"></div>
          <div v-else class="text-2xl font-bold text-rose-700 mt-3 tabular-nums">
            {{ d.machine_status?.stopped?.count ?? 0 }}
          </div>
          <div class="text-xs font-medium text-rose-600 mt-0.5">Остановлен</div>
        </div>

        <!-- No schedule -->
        <div class="status-card cursor-pointer select-none"
          :class="openGroup === 'no_schedule' ? 'ring-2 ring-slate-400' : ''"
          @click="toggleGroup('no_schedule')">
          <div class="flex items-center justify-between">
            <div class="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <svg class="w-4 h-4 text-slate-400 transition-transform"
              :class="openGroup === 'no_schedule' ? 'rotate-180' : ''"
              fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div v-if="loading" class="skeleton h-7 w-12 rounded mt-3"></div>
          <div v-else class="text-2xl font-bold text-slate-600 mt-3 tabular-nums">
            {{ d.machine_status?.no_schedule?.count ?? 0 }}
          </div>
          <div class="text-xs font-medium text-slate-500 mt-0.5">Нет графика ТО</div>
        </div>
      </div>

      <!-- Expandable machine list -->
      <Transition name="slide-down">
        <div v-if="openGroup && d.machine_status?.[openGroup]?.machines?.length"
          class="card overflow-hidden">
          <div class="px-5 py-3 border-b border-slate-100 flex items-center justify-between">
            <div class="text-xs font-semibold text-slate-700">
              {{ groupLabel(openGroup) }} — {{ d.machine_status[openGroup].machines.length }} станков
            </div>
            <button @click="openGroup = null" class="text-slate-400 hover:text-slate-600">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="divide-y divide-slate-50 max-h-64 overflow-y-auto">
            <RouterLink v-for="m in d.machine_status[openGroup].machines" :key="m.machine_id"
              :to="`/machines/${m.machine_id}`"
              class="flex items-center gap-3 px-5 py-2.5 hover:bg-slate-50 transition-colors">
              <div class="w-2 h-2 rounded-full flex-shrink-0"
                :class="statusDot(openGroup)"></div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-slate-800 truncate">{{ m.machine_name }}</div>
                <div class="text-[11px] text-slate-400">{{ m.workshop_name }} · {{ m.inventory_number }}</div>
              </div>
              <div class="text-[11px] text-slate-500 flex-shrink-0">{{ m.status_name }}</div>
              <svg class="w-3.5 h-3.5 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ══════════════════════════════════════════
         3. STANOKLAR ISH SOATI
    ══════════════════════════════════════════ -->
    <div class="card overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-100">
        <h2 class="section-title">Рабочие часы станков</h2>
      </div>
      <div class="p-5">
        <!-- Summary totals (all 36 machines) -->
        <div class="grid grid-cols-3 gap-3 mb-5">
          <div class="rounded-xl bg-emerald-50 p-3">
            <div class="text-[11px] font-medium text-emerald-600 uppercase tracking-wide">Рабочие часы</div>
            <div v-if="loading" class="skeleton h-7 w-16 rounded mt-1.5"></div>
            <div v-else class="text-2xl font-bold text-emerald-700 tabular-nums mt-1">
              {{ fmtH(d.machine_hours?.total_work_hours) }}
            </div>
          </div>
          <div class="rounded-xl bg-amber-50 p-3">
            <div class="text-[11px] font-medium text-amber-600 uppercase tracking-wide">Часы ремонта</div>
            <div v-if="loading" class="skeleton h-7 w-16 rounded mt-1.5"></div>
            <div v-else class="text-2xl font-bold text-amber-700 tabular-nums mt-1">
              {{ fmtH(d.machine_hours?.total_repair_hours) }}
            </div>
          </div>
          <div class="rounded-xl bg-slate-100 p-3">
            <div class="text-[11px] font-medium text-slate-500 uppercase tracking-wide">Часы простоя</div>
            <div v-if="loading" class="skeleton h-7 w-16 rounded mt-1.5"></div>
            <div v-else class="text-2xl font-bold text-slate-600 tabular-nums mt-1">
              {{ fmtH(d.machine_hours?.total_idle_hours) }}
            </div>
          </div>
        </div>

        <div v-if="loading" class="skeleton h-52 rounded-xl"></div>
        <div v-else-if="!workshopHours.length"
          class="h-52 flex items-center justify-center text-slate-400 text-sm italic">
          Нет данных за выбранный период
        </div>
        <div v-else style="position:relative; height:220px">
          <Bar :data="hoursChartData" :options="hoursChartOptions" />
        </div>
        <div v-if="!loading && workshopHours.length" class="text-[11px] text-slate-400 mt-2 text-center">
          Нажмите на столбец цеха для детального просмотра
        </div>

        <!-- Drill-down: machines within selected workshop -->
        <Transition name="slide-down">
          <div v-if="selectedWorkshop" class="mt-4 rounded-xl border border-slate-100 overflow-hidden">
            <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between bg-slate-50">
              <div class="text-xs font-semibold text-slate-700">
                {{ selectedWorkshop.workshop_name }} — {{ selectedWorkshop.machines.length }} станков
              </div>
              <button @click="selectedWorkshopIndex = null" class="text-slate-400 hover:text-slate-600">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            <div class="max-h-72 overflow-y-auto">
              <table class="w-full text-xs">
                <thead class="sticky top-0 bg-white">
                  <tr class="text-slate-400 border-b border-slate-100">
                    <th class="text-left font-medium px-4 py-2">Станок</th>
                    <th class="text-right font-medium px-4 py-2">Работа</th>
                    <th class="text-right font-medium px-4 py-2">Ремонт</th>
                    <th class="text-right font-medium px-4 py-2">Простой</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="m in selectedWorkshop.machines" :key="m.machine_id">
                    <td class="px-4 py-2">
                      <div class="font-medium text-slate-800">{{ m.machine_name }}</div>
                      <div class="text-[11px] text-slate-400">{{ m.inventory_number }}</div>
                    </td>
                    <td class="text-right px-4 py-2 text-emerald-700 font-medium tabular-nums">{{ fmtH(m.work_hours) }}</td>
                    <td class="text-right px-4 py-2 text-amber-700 font-medium tabular-nums">{{ fmtH(m.repair_hours) }}</td>
                    <td class="text-right px-4 py-2 text-slate-500 font-medium tabular-nums">{{ fmtH(m.idle_hours) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- ══════════════════════════════════════════
         4. SKLAD XARAJATLARI
    ══════════════════════════════════════════ -->
    <div class="space-y-4">
      <h2 class="section-title px-1">Расходы склада</h2>
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">

        <!-- Total warehouse card -->
        <div class="card p-5 flex flex-col justify-between">
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wide">Итого расходов склада</div>
          <div v-if="loading" class="skeleton h-8 w-32 rounded-lg mt-2"></div>
          <div v-else class="mt-2">
            <div class="text-3xl font-bold text-emerald-700 tabular-nums">${{ fmtNum(d.warehouse_expenses?.total) }}</div>
            <div class="text-xs text-slate-400 mt-1">Расход склада</div>
          </div>
        </div>

        <!-- Top 5 spare parts -->
        <div class="card overflow-hidden xl:col-span-2">
          <div class="px-5 py-3 border-b border-slate-100">
            <div class="text-xs font-semibold text-slate-700">Наиболее используемые запчасти (Топ 5)</div>
          </div>
          <div v-if="loading" class="p-4 space-y-2">
            <div v-for="i in 5" :key="i" class="skeleton h-10 rounded-lg"></div>
          </div>
          <div v-else-if="!d.warehouse_expenses?.top_parts?.length"
            class="p-5 text-center text-slate-400 text-sm italic">Нет данных</div>
          <div v-else class="divide-y divide-slate-50">
            <div v-for="(part, idx) in d.warehouse_expenses.top_parts" :key="part.id"
              class="flex items-center gap-3 px-5 py-2.5">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                :class="idx === 0 ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'">
                {{ idx + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-slate-800 truncate">{{ part.name }}</div>
                <div class="text-[11px] text-slate-400">
                  Использовано: {{ fmtQty(part.total_qty) }} {{ part.unit }}
                </div>
              </div>
              <div class="text-xs font-bold text-emerald-700 flex-shrink-0">${{ fmtNum(part.total_cost) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════
         5. TO XARAJATLARI
    ══════════════════════════════════════════ -->
    <div class="space-y-4">
      <h2 class="section-title px-1">Расходы ТО</h2>

      <!-- Total TO + monthly line chart -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">

        <!-- Total card -->
        <div class="card p-5 flex flex-col justify-between">
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wide">Итого расходов ТО</div>
          <div v-if="loading" class="skeleton h-8 w-32 rounded-lg mt-2"></div>
          <div v-else class="mt-2">
            <div class="text-3xl font-bold text-indigo-700 tabular-nums">${{ fmtNum(d.to_expenses?.total) }}</div>
            <div class="text-xs text-slate-400 mt-1">За {{ d.period?.days }} дней</div>
          </div>
        </div>

        <!-- Monthly line chart -->
        <div class="card p-5 xl:col-span-2">
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wide mb-3">Расходы ТО по месяцам</div>
          <div v-if="loading" class="skeleton h-28 rounded-xl"></div>
          <div v-else style="position:relative; height:120px">
            <Line :data="toLineChartData" :options="lineChartOptions" />
          </div>
        </div>
      </div>

      <!-- By workshop + by machine -->
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">

        <!-- By workshop -->
        <div class="card overflow-hidden">
          <div class="px-5 py-3 border-b border-slate-100">
            <div class="text-xs font-semibold text-slate-700">По цехам</div>
          </div>
          <div v-if="loading" class="p-4 space-y-2">
            <div v-for="i in 3" :key="i" class="skeleton h-10 rounded-lg"></div>
          </div>
          <div v-else-if="!d.to_expenses?.by_workshop?.length"
            class="p-5 text-center text-slate-400 text-sm italic">Нет данных</div>
          <div v-else class="divide-y divide-slate-50">
            <div v-for="ws in d.to_expenses.by_workshop" :key="ws.workshop_id"
              class="flex items-center gap-3 px-5 py-3">
              <div class="flex-1 min-w-0">
                <div class="text-sm font-semibold text-slate-800 truncate">{{ ws.workshop_name }}</div>
                <div class="text-xs text-slate-400">{{ ws.machines_count }} станков</div>
                <div class="mt-1.5 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-indigo-500 rounded-full"
                    :style="`width:${workshopMaxCost ? ws.cost / workshopMaxCost * 100 : 0}%`"></div>
                </div>
              </div>
              <div class="text-sm font-bold text-indigo-700 flex-shrink-0">${{ fmtNum(ws.cost) }}</div>
            </div>
          </div>
        </div>

        <!-- By machine -->
        <div class="card overflow-hidden">
          <div class="px-5 py-3 border-b border-slate-100">
            <div class="text-xs font-semibold text-slate-700">По станкам (Топ 10)</div>
          </div>
          <div v-if="loading" class="p-4 space-y-2">
            <div v-for="i in 5" :key="i" class="skeleton h-12 rounded-lg"></div>
          </div>
          <div v-else-if="!d.to_expenses?.by_machine?.length"
            class="p-5 text-center text-slate-400 text-sm italic">Нет данных</div>
          <div v-else class="divide-y divide-slate-50">
            <RouterLink v-for="(m, idx) in d.to_expenses.by_machine" :key="m.machine_id"
              :to="`/machines/${m.machine_id}`"
              class="flex items-center gap-3 px-5 py-2.5 hover:bg-slate-50 transition-colors">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                :class="idx === 0 ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-500'">
                {{ idx + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold text-slate-800 truncate">{{ m.machine_name }}</div>
                <div class="text-[11px] text-slate-400 truncate">{{ m.workshop_name }} · {{ m.inventory_number }}</div>
                <div class="mt-1 h-1 bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-indigo-400 rounded-full" :style="`width:${m.percentage}%`"></div>
                </div>
              </div>
              <div class="text-xs font-bold text-indigo-700 flex-shrink-0">${{ fmtNum(m.cost) }}</div>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { Bar, Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale, LinearScale,
  BarElement, LineElement, PointElement,
  ArcElement, Tooltip, Legend, Filler,
} from 'chart.js'
import { dashboardApi } from '@/api'
import dayjs from 'dayjs'

ChartJS.register(
  CategoryScale, LinearScale,
  BarElement, LineElement, PointElement,
  ArcElement, Tooltip, Legend, Filler,
)

// ── State ──
const loading = ref(true)
const d = ref({})
const preset = ref('1m')
const customFrom = ref('')
const customTo = ref('')
const openGroup = ref(null)
const selectedWorkshopIndex = ref(null)

const presets = [
  { key: '1m', label: '1 месяц' },
  { key: '3m', label: '3 месяца' },
  { key: '6m', label: '6 месяцев' },
  { key: 'custom', label: 'Вручную' },
]

const currentDate = computed(() => dayjs().format('DD.MM.YYYY, dddd'))

function setPreset(key) {
  preset.value = key
  openGroup.value = null
  selectedWorkshopIndex.value = null
  if (key !== 'custom') loadData()
}

const dateRange = computed(() => {
  const today = dayjs().format('YYYY-MM-DD')
  if (preset.value === '1m') return { date_from: dayjs().subtract(1, 'month').format('YYYY-MM-DD'), date_to: today }
  if (preset.value === '3m') return { date_from: dayjs().subtract(3, 'month').format('YYYY-MM-DD'), date_to: today }
  if (preset.value === '6m') return { date_from: dayjs().subtract(6, 'month').format('YYYY-MM-DD'), date_to: today }
  return { date_from: customFrom.value, date_to: customTo.value }
})

watch([customFrom, customTo], () => {
  if (preset.value === 'custom' && customFrom.value && customTo.value) loadData()
})

// ── Formatters ──
function fmtNum(v) {
  if (v == null) return '0'
  const n = Number(v)
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M'
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'k'
  return n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}
function fmtH(v) { return `${Number(v ?? 0).toFixed(0)} ч` }
function fmtQty(v) { return Number(v ?? 0).toLocaleString('en-US', { maximumFractionDigits: 2 }) }

// ── Machine hours stacked bar (grouped by workshop) ──
const workshopHours = computed(() => d.value.machine_hours?.by_workshop || [])
const selectedWorkshop = computed(() => (
  selectedWorkshopIndex.value != null ? workshopHours.value[selectedWorkshopIndex.value] : null
))

function onHoursChartClick(evt, elements) {
  if (!elements.length) return
  const idx = elements[0].index
  selectedWorkshopIndex.value = selectedWorkshopIndex.value === idx ? null : idx
}

const hoursChartData = computed(() => {
  const items = workshopHours.value
  return {
    labels: items.map(w => w.workshop_name),
    datasets: [
      {
        label: 'Рабочее время',
        data: items.map(w => w.work_hours),
        backgroundColor: '#10b981',
        borderRadius: { topLeft: 0, topRight: 0 },
        stack: 'hours',
      },
      {
        label: 'Время ремонта',
        data: items.map(w => w.repair_hours),
        backgroundColor: '#f59e0b',
        stack: 'hours',
      },
      {
        label: 'Простой',
        data: items.map(w => w.idle_hours),
        backgroundColor: '#cbd5e1',
        borderRadius: { topLeft: 4, topRight: 4 },
        stack: 'hours',
      },
    ],
  }
}
)
const hoursChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  onClick: (evt, elements) => onHoursChartClick(evt, elements),
  onHover: (evt, elements) => {
    evt.native.target.style.cursor = elements.length ? 'pointer' : 'default'
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: ctx => ` ${ctx.dataset.label}: ${ctx.raw} ч`,
      },
    },
  },
  scales: {
    x: { stacked: true, grid: { display: false }, ticks: { font: { size: 10 }, maxRotation: 45 } },
    y: { stacked: true, grid: { color: '#f1f5f9' }, ticks: { font: { size: 10 }, callback: v => `${v}ч` } },
  },
}

// ── TO monthly line chart ──
const toLineChartData = computed(() => {
  const chart = d.value.to_expenses?.monthly_chart || []
  return {
    labels: chart.map(m => m.month_label),
    datasets: [{
      label: 'Расходы ТО ($)',
      data: chart.map(m => m.cost),
      borderColor: '#6366f1',
      backgroundColor: 'rgba(99,102,241,0.08)',
      borderWidth: 2,
      pointRadius: 4,
      pointBackgroundColor: '#6366f1',
      fill: true,
      tension: 0.3,
    }],
  }
})
const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: ctx => ` $${ctx.raw}` } },
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 10 } } },
    y: { grid: { color: '#f1f5f9' }, ticks: { font: { size: 10 }, callback: v => `$${v}` } },
  },
}

// ── Total donut ──
const totalDonutData = computed(() => ({
  labels: ['Расходы ТО', 'Расходы склада'],
  datasets: [{
    data: [
      d.value.total_expenses?.to_amount ?? 0,
      d.value.total_expenses?.warehouse_amount ?? 0,
    ],
    backgroundColor: ['#6366f1', '#10b981'],
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
    tooltip: { callbacks: { label: ctx => ` ${ctx.label}: $${ctx.raw}` } },
  },
}

// ── Workshop expense bar width ──
const workshopMaxCost = computed(() => {
  const list = d.value.to_expenses?.by_workshop || []
  return Math.max(...list.map(w => w.cost), 1)
})

// ── Status group ──
function toggleGroup(key) {
  openGroup.value = openGroup.value === key ? null : key
}
function groupLabel(key) {
  return { working: 'Работает', in_repair: 'В ремонте', stopped: 'Остановлен', no_schedule: 'Нет графика ТО' }[key] || key
}
function statusDot(key) {
  return {
    working: 'bg-emerald-500',
    in_repair: 'bg-blue-500',
    stopped: 'bg-rose-500',
    no_schedule: 'bg-slate-400',
  }[key] || 'bg-slate-400'
}

// ── Data loading ──
async function loadData() {
  const { date_from, date_to } = dateRange.value
  if (!date_from || !date_to) return
  loading.value = true
  try {
    const res = await dashboardApi.get({ date_from, date_to })
    d.value = res.data
  } finally {
    loading.value = false
  }
}

loadData()
</script>

<style scoped>
.card { @apply bg-white rounded-2xl border border-slate-200 shadow-sm; }

.status-card {
  @apply bg-white rounded-2xl border border-slate-200 shadow-sm p-4 transition-all hover:shadow-md;
}

.section-title { @apply text-sm font-semibold text-slate-800; }

.fade-slide-enter-active,
.fade-slide-leave-active { transition: all .2s ease; }
.fade-slide-enter-from,
.fade-slide-leave-to { opacity: 0; transform: translateY(-6px); }

.slide-down-enter-active,
.slide-down-leave-active { transition: all .25s ease; }
.slide-down-enter-from,
.slide-down-leave-to { opacity: 0; transform: translateY(-8px); }

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px) } to { opacity: 1; transform: none } }
.animate-fade-in { animation: fadeIn .25s ease; }
</style>
