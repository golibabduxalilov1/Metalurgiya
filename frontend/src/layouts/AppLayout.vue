<template>
  <div class="app-layout">

    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div v-if="mobileMenuOpen"
        class="fixed inset-0 bg-black/40 backdrop-blur-[2px] z-30 lg:hidden cursor-pointer"
        @click="mobileMenuOpen = false">
      </div>
    </Transition>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 left-0 h-full z-40 flex flex-col bg-white border-r border-slate-100',
        'w-[260px] lg:transition-[width] lg:duration-300',
        sidebarCollapsed ? 'lg:w-[72px]' : 'lg:w-[260px]',
        mobileMenuOpen ? 'translate-x-0 transition-transform duration-300' : '-translate-x-full transition-transform duration-300 lg:translate-x-0 lg:transition-none',
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-4 py-5 border-b border-slate-100">
        <div class="flex-shrink-0 w-9 h-9 rounded-xl overflow-hidden shadow-md shadow-indigo-500/25">
          <img src="@/assets/logo.jpg" alt="Logo" class="w-full h-full object-cover" />
        </div>
        <Transition name="fade">
          <div v-if="sidebarShowContent" class="overflow-hidden">
            <div class="text-slate-800 font-bold text-sm leading-tight">Lazana</div>
            <div class="text-slate-400 text-xs mt-0.5">{{ t('nav.equipment_registry') }}</div>
          </div>
        </Transition>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        <!-- Main -->
        <div v-if="sidebarShowContent" class="px-3 mb-1.5">
          <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">{{ t('nav.main') }}</span>
        </div>
        <NavItem v-for="item in mainNavItems" :key="item.name"
          :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />

        <!-- Management -->
        <template v-if="auth.isAdmin || auth.isMaster">
          <div v-if="sidebarShowContent" class="px-3 mt-5 mb-1.5">
            <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">{{ t('nav.management') }}</span>
          </div>
          <div v-if="!sidebarShowContent" class="border-t border-slate-100 my-2 mx-1"></div>
          <NavItem v-for="item in managementNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />
        </template>

        <!-- Admin only -->
        <template v-if="auth.isAdmin">
          <div v-if="sidebarShowContent" class="px-3 mt-5 mb-1.5">
            <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">{{ t('nav.administration') }}</span>
          </div>
          <div v-if="!sidebarShowContent" class="border-t border-slate-100 my-2 mx-1"></div>
          <NavItem v-for="item in adminNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />
        </template>
      </nav>

      <!-- User section -->
      <div class="border-t border-slate-100 p-3 space-y-1">
        <RouterLink to="/profile"
          class="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors group cursor-pointer">
          <div class="relative flex-shrink-0">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
              <span class="text-white text-xs font-bold select-none">{{ userInitials }}</span>
            </div>
            <span class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-white"></span>
          </div>
          <Transition name="fade">
            <div v-if="sidebarShowContent" class="overflow-hidden flex-1 min-w-0">
              <div class="text-slate-800 text-sm font-semibold truncate group-hover:text-indigo-600 transition-colors">{{ auth.userFullName }}</div>
              <div class="text-slate-400 text-xs truncate">{{ auth.userRole }}</div>
            </div>
          </Transition>
        </RouterLink>
        <button v-if="sidebarShowContent"
          @click="auth.logout"
          class="w-full flex items-center gap-2 px-2 py-1.5 text-slate-400 hover:text-rose-500
                 hover:bg-rose-50 rounded-lg text-sm transition-colors cursor-pointer">
          <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          {{ t('nav.logout') }}
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 min-w-0 flex flex-col min-h-screen transition-all duration-300 ml-0"
      :class="sidebarCollapsed ? 'lg:ml-[72px]' : 'lg:ml-[260px]'">

      <!-- Top bar -->
      <header class="fixed top-0 left-0 right-0 z-30 h-16 bg-white/95 backdrop-blur-sm border-b border-slate-100
        flex items-center px-4 lg:px-6 gap-3 shadow-[0_1px_8px_rgba(15,23,42,0.06)] transition-all duration-300"
        :class="sidebarCollapsed ? 'lg:left-[72px]' : 'lg:left-[260px]'">

        <!-- Toggle sidebar / hamburger -->
        <button @click="toggleMenu"
          class="lg:hidden p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors cursor-pointer flex-shrink-0">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Breadcrumb (hidden on mobile) -->
        <div class="hidden sm:flex items-center gap-1.5 text-sm min-w-0">
          <span class="text-slate-400 flex-shrink-0">{{ t('nav.home') }}</span>
          <svg class="w-3.5 h-3.5 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
          <span class="text-slate-700 font-medium truncate">{{ currentPageTitle }}</span>
        </div>

        <div class="flex-1"></div>

        <!-- Role badge (hidden on mobile) -->
        <div class="hidden sm:block" :class="roleBadgeClass">{{ auth.userRole }}</div>

        <!-- Language toggle button -->
        <button @click="langStore.toggle()"
          class="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-slate-200
                 bg-slate-50 hover:bg-indigo-50 hover:border-indigo-200
                 text-xs font-bold text-slate-600 hover:text-indigo-700
                 transition-all duration-200 cursor-pointer flex-shrink-0 select-none">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
          </svg>
          {{ langStore.lang === 'ru' ? 'UZ' : 'RU' }}
        </button>

        <!-- Notifications -->
        <button class="relative p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors cursor-pointer flex-shrink-0">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>

        <!-- User avatar -->
        <RouterLink to="/profile"
          class="flex items-center gap-2 sm:gap-2.5 sm:pl-2 sm:pr-3 py-1.5 sm:rounded-xl hover:bg-slate-100 transition-colors cursor-pointer">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold select-none">{{ userInitials }}</span>
          </div>
          <span class="text-sm font-medium text-slate-700 hidden md:block">{{ auth.userFullName }}</span>
        </RouterLink>
      </header>

      <!-- Page content -->
      <main class="flex-1 pt-16">
        <div class="p-3 sm:p-4 md:p-6">
          <RouterView v-slot="{ Component, route }">
            <Transition name="fade" mode="out-in">
              <component :is="Component" :key="route.path" />
            </Transition>
          </RouterView>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useLangStore } from '@/store/lang'
import { useI18n } from '@/i18n'
import NavItem from '@/components/common/NavItem.vue'

const auth = useAuthStore()
const langStore = useLangStore()
const { t } = useI18n()
const route = useRoute()
const sidebarCollapsed = ref(false)
const mobileMenuOpen = ref(false)

const sidebarShowContent = computed(() => !sidebarCollapsed.value || mobileMenuOpen.value)

function toggleMenu() {
  if (window.innerWidth < 1024) {
    mobileMenuOpen.value = !mobileMenuOpen.value
  } else {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}

watch(() => route.path, () => {
  mobileMenuOpen.value = false
})

const userInitials = computed(() => {
  const name = auth.userFullName
  if (!name) return '?'
  const parts = name.split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
  return name[0].toUpperCase()
})

const routeTitleMap = {
  Dashboard: 'nav.home',
  Machines: 'nav.machines',
  MachineCreate: 'nav.machine_add',
  MachineDetail: 'nav.machine_card',
  MachineEdit: 'nav.machine_edit',
  Employees: 'nav.employees',
  Directories: 'nav.directories',
  Users: 'nav.users',
  Audit: 'nav.audit',
  Profile: 'nav.profile',
}

const currentPageTitle = computed(() => {
  const key = routeTitleMap[route.name]
  return key ? t(key) : (route.meta?.title || '')
})

const roleBadgeClass = computed(() => {
  const role = auth.user?.role
  if (role === 'admin') return 'role-admin'
  if (role === 'master') return 'role-master'
  return 'role-operator'
})

const mainNavItems = computed(() => [
  { name: 'Dashboard', label: t('nav.home'), icon: 'home', to: '/dashboard' },
  { name: 'Machines', label: t('nav.machines'), icon: 'cog', to: '/machines' },
])

const managementNavItems = computed(() => {
  const items = []
  if (auth.isAdmin || auth.isMaster) {
    items.push({ name: 'Employees', label: t('nav.employees'), icon: 'users', to: '/employees' })
  }
  return items
})

const adminNavItems = computed(() => [
  { name: 'Directories', label: t('nav.directories'), icon: 'book', to: '/directories' },
  { name: 'Users', label: t('nav.users'), icon: 'user-group', to: '/users' },
  { name: 'Audit', label: t('nav.audit'), icon: 'document', to: '/audit' },
])
</script>
