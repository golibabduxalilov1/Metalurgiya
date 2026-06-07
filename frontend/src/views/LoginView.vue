<template>
  <div class="min-h-screen flex bg-slate-50">

    <!-- Left panel - branding -->
    <div class="hidden lg:flex lg:w-1/2 flex-col justify-between p-12 relative overflow-hidden
                bg-gradient-to-br from-white via-indigo-50/70 to-violet-50">

      <!-- Subtle geometric grid -->
      <div class="absolute inset-0 opacity-[0.055]">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#312e81" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <!-- Decorative blobs -->
      <div class="absolute -top-20 -left-20 w-80 h-80 bg-indigo-200/50 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -right-20 w-96 h-96 bg-violet-200/40 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/3 w-64 h-64 bg-emerald-100/50 rounded-full blur-3xl"></div>

      <!-- Top: logo + headline -->
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-16">
          <div class="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <span class="text-slate-800 text-xl font-bold tracking-tight">{{ t('login.app_name') }}</span>
        </div>

        <h1 class="text-4xl font-bold text-slate-900 leading-tight mb-6">
          {{ t('login.branding_title_line1') }}<br/>
          <span class="text-indigo-600">{{ t('login.branding_title_line2') }}</span>
        </h1>
        <p class="text-slate-500 text-lg leading-relaxed max-w-md">
          {{ t('login.branding_subtitle') }}
        </p>
      </div>

      <!-- Bottom: feature pills -->
      <div class="relative z-10 flex flex-col gap-3">
        <div class="flex items-center gap-3 text-slate-500 text-sm">
          <div class="w-7 h-7 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          {{ t('login.feature1') }}
        </div>
        <div class="flex items-center gap-3 text-slate-500 text-sm">
          <div class="w-7 h-7 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          {{ t('login.feature2') }}
        </div>
        <div class="flex items-center gap-3 text-slate-500 text-sm">
          <div class="w-7 h-7 rounded-lg bg-violet-100 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
          </div>
          {{ t('login.feature3') }}
        </div>
      </div>
    </div>

    <!-- Right panel - login form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 bg-white">
      <div class="w-full max-w-md login-card-enter">

        <!-- Mobile logo -->
        <div class="flex items-center gap-3 mb-8 lg:hidden">
          <div class="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            </svg>
          </div>
          <span class="text-slate-800 text-lg font-bold">{{ t('login.app_name') }}</span>
        </div>

        <!-- Form card -->
        <div class="bg-white border border-slate-100 rounded-2xl p-8 shadow-[0_4px_24px_rgba(15,23,42,0.08)]">

          <!-- Header -->
          <div class="mb-8">
            <div class="flex items-center justify-between mb-4">
              <div class="inline-flex items-center gap-2 bg-indigo-50 border border-indigo-100
                          text-indigo-700 text-xs font-semibold px-3 py-1.5 rounded-full">
                <div class="w-1.5 h-1.5 rounded-full bg-indigo-500"></div>
                Machine Registry
              </div>
              <!-- Language toggle on login page -->
              <button @click="langStore.toggle()"
                class="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-slate-200
                       bg-slate-50 hover:bg-indigo-50 hover:border-indigo-200
                       text-xs font-bold text-slate-600 hover:text-indigo-700
                       transition-all duration-200 cursor-pointer select-none">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
                </svg>
                {{ langStore.lang === 'ru' ? 'UZ' : 'RU' }}
              </button>
            </div>
            <h2 class="text-2xl font-bold text-slate-900 tracking-tight">{{ t('login.title') }}</h2>
            <p class="text-slate-500 text-sm mt-1.5">{{ t('login.subtitle') }}</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-5">

            <!-- Username -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">{{ t('login.username_label') }}</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <input
                  v-model="form.username"
                  type="text"
                  :placeholder="t('login.username_placeholder')"
                  autocomplete="username"
                  class="w-full bg-zinc-50 border border-slate-200 rounded-xl pl-10 pr-4 py-3
                         text-slate-800 placeholder-slate-400 text-sm
                         focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:bg-white
                         hover:border-slate-300 transition-all duration-200"
                />
              </div>
            </div>

            <!-- Password -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">{{ t('login.password_label') }}</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                </div>
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  autocomplete="current-password"
                  class="w-full bg-zinc-50 border border-slate-200 rounded-xl pl-10 pr-10 py-3
                         text-slate-800 placeholder-slate-400 text-sm
                         focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:bg-white
                         hover:border-slate-300 transition-all duration-200"
                />
                <button type="button" @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3.5 flex items-center
                         text-slate-400 hover:text-slate-600 cursor-pointer transition-colors duration-200">
                  <svg v-if="!showPassword" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Error -->
            <Transition name="fade">
              <div v-if="error"
                class="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
                <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                {{ error }}
              </div>
            </Transition>

            <!-- Submit -->
            <button type="submit" :disabled="loading || !form.username || !form.password"
              class="w-full bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800
                     disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer
                     text-white font-semibold py-3 rounded-xl
                     transition-all duration-200
                     flex items-center justify-center gap-2 mt-2
                     shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40
                     hover:-translate-y-px disabled:hover:translate-y-0">
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
              {{ loading ? t('login.entering') : t('login.enter') }}
            </button>

          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useLangStore } from '@/store/lang'
import { useI18n } from '@/i18n'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const langStore = useLangStore()
const { t } = useI18n()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  const result = await auth.login(form)
  loading.value = false
  if (result.success) {
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.login-card-enter {
  animation: cardEnter 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes cardEnter {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
