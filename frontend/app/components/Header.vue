<template>
  <header role="banner" class="bg-base-100">
    <!-- Top Utility Bar -->
    <div class="bg-base-200 border-b border-base-300">
      <div class="max-w-7xl mx-auto">
        <!-- Desktop Top Navigation -->
        <nav 
          class="hidden md:flex items-center justify-between px-6 py-2.5" 
          aria-label="Primary navigation"
        >
          <!-- Primary Navigation Links -->
          <ul class="flex items-center gap-1" role="menubar">
            <li role="none">
              <NuxtLink 
                to="/about" 
                class="btn btn-ghost btn-sm gap-2 normal-case font-medium hover:text-primary transition-colors"
                role="menuitem"
                aria-label="About page"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                </svg>
                <span>About</span>
              </NuxtLink>
            </li>
            
            <li role="none">
              <div class="dropdown dropdown-hover dropdown-end">
                <button
                  ref="pdf2ChemicalsDropdownBtn"
                  type="button"
                  class="btn btn-ghost btn-sm gap-2 normal-case font-medium hover:text-primary transition-colors"
                  role="menuitem"
                  aria-label="PDF2Chemicals menu"
                  aria-haspopup="true"
                  :aria-expanded="isPDF2ChemicalsDropdownOpen"
                  @click="togglePDF2ChemicalsDropdown"
                  @keydown.escape="closePDF2ChemicalsDropdown"
                >
                  <span>PDF2Chemicals</span>
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke-width="1.5"
                    stroke="currentColor" 
                    class="w-4 h-4 transition-transform duration-200"
                    :class="{ 'rotate-180': isPDF2ChemicalsDropdownOpen }"
                    aria-hidden="true"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                  </svg>
                </button>
                <ul 
                  v-show="isPDF2ChemicalsDropdownOpen"
                  class="dropdown-content menu p-2 mt-2 rounded-lg bg-base-100 shadow-lg border border-base-300 w-56 z-50"
                  role="menu"
                  aria-orientation="vertical"
                  @keydown.escape="closePDF2ChemicalsDropdown"
                >
                  <li role="none">
                    <NuxtLink 
                      to="/pdf2chemicals/about" 
                      class="gap-3 py-2.5 hover:text-primary transition-colors"
                      role="menuitem"
                      @click="closePDF2ChemicalsDropdown"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                      </svg>
                      <span>About</span>
                    </NuxtLink>
                  </li>
                  <li role="none">
                    <NuxtLink 
                      to="/pdf2chemicals/features"
                      class="gap-3 py-2.5 hover:text-primary transition-colors"
                      role="menuitem"
                      @click="closePDF2ChemicalsDropdown"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                      </svg>
                      <span>Features</span>
                    </NuxtLink>
                  </li>
                  <li role="none">
                    <button 
                      @click="handlePDF2ChemicalsSubmit" 
                      class="gap-3 py-2.5 hover:text-primary transition-colors w-full text-left"
                      role="menuitem"
                      type="button"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                      </svg>
                      <span>Submit</span>
                    </button>
                  </li>
                </ul>
              </div>
            </li>
            
            <li role="none">
              <a 
                href="" 
                class="btn btn-ghost btn-sm gap-2 normal-case font-medium hover:text-primary transition-colors"
                role="menuitem"
                aria-label="Download software"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                <span>Download</span>
              </a>
            </li>
            
            <li role="none">
              <a 
                :href="config.public.docsAPIEndpoint" 
                target="_blank"
                rel="noopener noreferrer"
                class="btn btn-ghost btn-sm gap-2 normal-case font-medium hover:text-primary transition-colors"
                role="menuitem"
                aria-label="API Documentation (opens in new tab)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                </svg>
                <span>API</span>
              </a>
            </li>
          </ul>

          <!-- Utility Actions -->
          <div class="flex items-center gap-2">
            <!-- Theme Toggle -->
            <button
              type="button"
              class="btn btn-ghost btn-sm btn-circle swap swap-rotate hover:text-primary transition-colors duration-200"
              aria-label="Toggle theme"
              @click="themeStore.toggleDarkMode()"
            >
              
              <input ref="themeController" type="checkbox" class="theme-controller" v-model="themeStore.darkMode"
                @click="themeStore.toggleDarkMode()" />
              <!-- Moon SVG icon -->
              <svg class="swap-on fill-current h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
              </svg>
              <!-- Sun SVG icon -->
              <svg class="swap-off fill-current h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
              </svg>
          
            </button>

            <!-- Notifications -->
            <button 
              type="button"
              class="btn btn-ghost btn-sm btn-circle hover:text-primary transition-colors" 
              aria-label="Notifications. You have 1 unread notification"
              @click="handleNotifications"
            >
              <div class="indicator">
                <span class="indicator-item badge badge-xs badge-primary" aria-hidden="true"></span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 
                        8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 
                        1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 
                        24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                </svg>
              </div>
            </button>

            <!-- User Menu -->
            <div v-if="authStore.isAuthenticated && userStore.user" class="dropdown dropdown-end">
              <button
                ref="userMenuBtn"
                type="button"
                tabindex="0"
                class="btn btn-ghost btn-sm btn-circle hover:bg-base-200 transition-colors"
                aria-label="User menu"
                aria-haspopup="true"
              >
                <div class="avatar avatar-placeholder">
                  <div class="w-8 rounded-full text-xs font-semibold" :class="themeStore.isDarkMode ? 'bg-neutral text-neutral-content' : 'bg-slate-600 text-white'">
                    <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                  </div>
                </div>
              </button>
              <ul 
                tabindex="-1"
                class="dropdown-content menu p-2 mt-2 rounded-lg bg-base-100 shadow-lg border border-base-300 w-56 z-50"
                role="menu"
                aria-orientation="vertical"
              >
                <li role="none">
                  <NuxtLink 
                    to="/user/profile" 
                    class="gap-3 py-2.5 hover:text-primary transition-colors" 
                    role="menuitem"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                            9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                            3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <span>{{ getUserName() }}</span>
                  </NuxtLink>
                </li>
                <li role="none">
                  <NuxtLink 
                    to="/dashboard" 
                    class="gap-3 py-2.5 hover:text-primary transition-colors" 
                    role="menuitem"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                            0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                            1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                    </svg>
                    <span>Dashboard</span>
                  </NuxtLink>
                </li>
                <div class="divider my-1"></div>
                <li role="none">
                  <button 
                    @click="handleLogout" 
                    class="gap-3 py-2.5 hover:text-error transition-colors w-full text-left" 
                    role="menuitem"
                    type="button"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                    </svg>
                    <span>Log out</span>
                  </button>
                </li>
              </ul>
            </div>
            <NuxtLink 
              v-else 
              to="/auth/login" 
              class="btn btn-ghost btn-sm gap-2 normal-case font-medium hover:text-primary transition-colors" 
              aria-label="Log in to your account"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="w-5 h-5" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
              </svg>
              <span>Log In</span>
            </NuxtLink>
          </div>
        </nav>

        <!-- Mobile Top Bar -->
        <nav class="flex md:hidden items-center justify-end px-4 py-2.5 gap-2" aria-label="Mobile utility navigation">
          <button
            type="button"
            class="btn btn-ghost btn-sm btn-circle hover:text-primary transition-colors"
            aria-label="Toggle theme"
            @click="themeStore.toggleDarkMode()"
          >
            <svg 
              v-if="!themeStore.isDarkMode"
              class="w-5 h-5" 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
            </svg>
            <svg 
              v-else
              class="w-5 h-5" 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
            </svg>
          </button>

          <div v-if="authStore.isAuthenticated && userStore.user" class="dropdown dropdown-end">
            <button
              type="button"
              tabindex="0"
              class="btn btn-ghost btn-sm btn-circle hover:bg-base-200 transition-colors"
              aria-label="User menu"
              aria-haspopup="true"
              :aria-expanded="isMobileUserMenuOpen"
              @click="toggleMobileUserMenu"
            >
              <div class="avatar avatar-placeholder">
                <div class="w-8 rounded-full text-xs font-semibold" :class="themeStore.isDarkMode ? 'bg-neutral text-neutral-content' : 'bg-slate-600 text-white'">
                  <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                </div>
              </div>
            </button>
            <ul 
              v-show="isMobileUserMenuOpen"
              tabindex="-1"
              class="dropdown-content menu p-2 mt-2 rounded-lg bg-base-100 shadow-lg border border-base-300 w-56 z-50"
              role="menu"
              @keydown.escape="closeMobileUserMenu"
            >
              <li role="none">
                <NuxtLink 
                  to="/user/profile" 
                  class="gap-3 py-3 active:bg-base-200" 
                  role="menuitem"
                  @click="closeMobileUserMenu"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                          9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                          3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <span class="truncate">{{ getUserName() }}</span>
                </NuxtLink>
              </li>
              <li role="none">
                <NuxtLink 
                  to="/dashboard" 
                  class="gap-3 py-3 active:bg-base-200" 
                  role="menuitem"
                  @click="closeMobileUserMenu"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                          0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                          1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                  </svg>
                  <span>Dashboard</span>
                </NuxtLink>
              </li>
              <div class="divider my-1"></div>
              <li role="none">
                <button 
                  @click="handleLogout" 
                  class="gap-3 py-3 w-full text-left active:bg-base-200 hover:text-error transition-colors" 
                  role="menuitem"
                  type="button"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                  </svg>
                  <span>Log out</span>
                </button>
              </li>
            </ul>
          </div>
          <NuxtLink 
            v-else 
            to="/auth/login" 
            class="btn btn-ghost btn-sm btn-circle hover:text-primary transition-colors" 
            aria-label="Log in to your account"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
          </NuxtLink>
        </nav>
      </div>
    </div>

    <!-- Main Navigation Bar with Logo and Search -->
    <div class="bg-base-100 shadow-sm border-b border-base-300">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between px-4 py-3 md:py-4">
          <!-- Left: Mobile Menu + Desktop Logo -->
          <div class="flex items-center gap-3">
            <!-- Mobile Menu Button -->
            <button
              type="button"
              class="btn btn-ghost btn-square md:hidden"
              aria-label="Open navigation menu"
              :aria-expanded="isDrawerOpen"
              @click="toggleDrawer"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2"
                stroke="currentColor" 
                class="w-6 h-6"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
            </button>

            <!-- Desktop Logo -->
            <NuxtLink 
              to="/home" 
              class="hidden md:flex items-center"
              aria-label="LabsoDB home"
            >
              <img 
                v-if="themeStore.isDarkMode" 
                src="~/assets/labsodb_logo_dark.webp" 
                class="h-10 w-auto object-contain"
                alt="LabsoDB" 
                width="200"
                height="40"
                loading="eager"
              />
              <img 
                v-else 
                src="~/assets/labsodb_logo_light.webp" 
                class="h-10 w-auto object-contain"
                alt="LabsoDB" 
                width="200"
                height="40"
                loading="eager"
              />
            </NuxtLink>
          </div>

          <!-- Center: Mobile Logo -->
          <div class="flex md:hidden items-center justify-center">
            <NuxtLink 
              to="/home" 
              class="flex items-center"
              aria-label="LabsoDB home"
            >
              <img 
                v-if="themeStore.isDarkMode" 
                src="~/assets/labsodb_logo_dark.webp" 
                class="h-8 w-auto object-contain max-w-[140px]"
                alt="LabsoDB" 
                width="140"
                height="32"
                loading="eager"
              />
              <img 
                v-else 
                src="~/assets/labsodb_logo_light.webp" 
                class="h-8 w-auto object-contain max-w-[140px]"
                alt="LabsoDB" 
                width="140"
                height="32"
                loading="eager"
              />
            </NuxtLink>
          </div>

          <!-- Right: Search and Actions -->
          <div class="flex items-center gap-2">
            <!-- Desktop Search -->
            <div class="hidden md:flex flex-col gap-2 items-end">
              <header-quick-search-field></header-quick-search-field>
              <div class="flex text-sm font-medium gap-4">
                <button 
                  @click="openKetcherModal" 
                  class="link link-primary hover:link-hover transition-colors no-underline hover:underline"
                  type="button"
                  aria-label="Draw chemical structure"
                >
                  Draw Structure
                </button>
                <NuxtLink 
                  to="/chemicals/advanced"
                  class="link link-primary hover:link-hover transition-colors no-underline hover:underline"
                >
                  Advanced Search
                </NuxtLink>
              </div>
            </div>

            <!-- Mobile Search Toggle -->
            <button 
              ref="searchBarToggleButton" 
              type="button"
              class="btn btn-ghost btn-square md:hidden" 
              :class="{ 'text-primary': isSearchBarVisible }"
              @click="toggleSearchBar"
              aria-label="Toggle search"
              :aria-expanded="isSearchBarVisible"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2"
                stroke="currentColor" 
                class="w-6 h-6"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Search Expandable Section -->
    <Transition
      name="slide-down"
      @enter="onEnter"
      @after-enter="onAfterEnter"
      @leave="onLeave"
      @after-leave="onAfterLeave"
    >
      <div v-show="isSearchBarVisible" class="bg-base-200 md:hidden border-b border-base-300 overflow-hidden">
        <div class="px-4 py-4 space-y-3 max-w-7xl mx-auto">
          <header-quick-search-field></header-quick-search-field>
          <div class="flex flex-wrap text-sm font-medium gap-4 justify-center">
            <button 
              @click="openKetcherModalMobile" 
              type="button"
              class="link link-primary hover:link-hover no-underline hover:underline active:text-primary-focus"
              aria-label="Draw chemical structure"
            >
              Draw Structure
            </button>
            <NuxtLink 
              to="/chemicals/advanced"
              class="link link-primary hover:link-hover no-underline hover:underline active:text-primary-focus"
              @click="isSearchBarVisible = false"
            >
              Advanced Search
            </NuxtLink>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Mobile Navigation Drawer -->
    <Teleport to="body">
      <Transition name="drawer">
        <div v-if="isDrawerOpen" class="fixed inset-0 z-100 md:hidden">
          <!-- Overlay -->
          <div 
            class="fixed inset-0 bg-black/50 backdrop-blur-sm"
            @click="closeDrawer"
            aria-hidden="true"
          ></div>
          
          <!-- Drawer Panel -->
          <nav 
            ref="drawerNav"
            class="fixed top-0 left-0 bottom-0 w-80 max-w-[85vw] bg-base-100 shadow-2xl overflow-y-auto"
            aria-label="Mobile main navigation"
            @click.stop
          >
            <!-- Drawer Header -->
            <div class="sticky top-0 z-10 bg-base-100 border-b border-base-300">
              <div class="flex items-center justify-between p-4">
                <NuxtLink to="/home" @click="closeDrawer" class="flex-shrink-0">
                  <img 
                    v-if="themeStore.isDarkMode" 
                    src="~/assets/labsodb_logo_dark.webp" 
                    class="h-10 w-auto object-contain"
                    alt="LabsoDB" 
                  />
                  <img 
                    v-else 
                    src="~/assets/labsodb_logo_light.webp" 
                    class="h-10 w-auto object-contain"
                    alt="LabsoDB" 
                  />
                </NuxtLink>
                
              </div>
            </div>

            <!-- Navigation Items -->
            <ul class="menu p-4 space-y-1">
              <li>
                <NuxtLink 
                  to="/about" 
                  class="gap-3 py-3 text-base active:bg-base-200 rounded-lg"
                  @click="closeDrawer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                  </svg>
                  <span>About</span>
                </NuxtLink>
              </li>
              
              <li>
                <details class="group">
                  <summary class="py-3 px-4 text-base font-medium cursor-pointer hover:bg-base-200 rounded-lg transition-colors list-none flex items-center justify-between">
                    <span class="flex items-center gap-3">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                      </svg>
                      PDF2Chemicals
                    </span>
                  </summary>
                  <ul class="ml-8 mt-1 space-y-1">
                    <li>
                      <NuxtLink 
                        to="/pdf2chemicals/about" 
                        class="gap-3 py-2.5 text-base active:bg-base-200 rounded-lg"
                        @click="closeDrawer"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                        </svg>
                        <span>About</span>
                      </NuxtLink>
                    </li>
                    <li>
                      <NuxtLink 
                        to="/pdf2chemicals/features" 
                        class="gap-3 py-2.5 text-base active:bg-base-200 rounded-lg"
                        @click="closeDrawer"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                        </svg>
                        <span>Features</span>
                      </NuxtLink>
                    </li>
                    <li>
                      <button 
                        @click="handlePDF2ChemicalsSubmitMobile" 
                        type="button"
                        class="gap-3 py-2.5 text-base w-full text-left active:bg-base-200 rounded-lg"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                        </svg>
                        <span>Submit</span>
                      </button>
                    </li>
                  </ul>
                </details>
              </li>
              
              <li>
                <a 
                  href="" 
                  class="gap-3 py-3 text-base active:bg-base-200 rounded-lg"
                  @click="closeDrawer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                  </svg>
                  <span>Download</span>
                </a>
              </li>
              
              <li>
                <a 
                  :href="config.public.docsAPIEndpoint" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  class="gap-3 py-3 text-base active:bg-base-200 rounded-lg"
                  @click="closeDrawer"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-5 h-5 flex-shrink-0" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                  </svg>
                  <span>API</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </Transition>
    </Teleport>

    <!-- Modals -->
    <modal ref="ketcherModalRef">
      <ketcher-component></ketcher-component>
    </modal>
    <modal ref="pdf2ChemicalsSubmitRef">
      <PDF2ChemicalsSubmitComponent></PDF2ChemicalsSubmitComponent>
    </modal>
  </header>
</template>

<script setup>
import { ref, defineAsyncComponent, onUnmounted, watch, nextTick } from 'vue';
import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'
import { useUserStore } from '~/stores/user'
import { useRouter } from 'nuxt/app';
import Modal from '~/components/Modal.vue';
import HeaderQuickSearchField from '~/components/HeaderQuickSearchField.vue'

const KetcherComponent = defineAsyncComponent({
  loader: () => import('~/components/KetcherComponent.vue')
});

const PDF2ChemicalsSubmitComponent = defineAsyncComponent({
  loader: () => import('~/components/PDF2ChemicalsSubmitComponent.vue')
})

const config = useRuntimeConfig()
const router = useRouter()

const themeStore = useThemeStore();
const authStore = useAuthStore()
const userStore = useUserStore()

// Refs
const searchBarToggleButton = ref(null)
const ketcherModalRef = ref(null)
const pdf2ChemicalsSubmitRef = ref(null)
const drawerNav = ref(null)
const pdf2ChemicalsDropdownBtn = ref(null)
const userMenuBtn = ref(null)

// State
const isSearchBarVisible = ref(false)
const isDrawerOpen = ref(false)
const isPDF2ChemicalsDropdownOpen = ref(false)
const isMobileUserMenuOpen = ref(false)

// User helpers
const getUserFirstAndLastFirstLetters = () => {
  const first_name_first_letter = userStore.user.first_name.charAt(0).toUpperCase()
  const last_name_first_letter = userStore.user.last_name.charAt(0).toUpperCase()
  return first_name_first_letter + last_name_first_letter
}

const getUserName = () => {
  return `${userStore.user.first_name} ${userStore.user.last_name}`
}

// Modal handlers
const openKetcherModal = () => {
  if (ketcherModalRef.value) {
    ketcherModalRef.value.toggleComponentModal()
  }
  closePDF2ChemicalsDropdown()
}

const openKetcherModalMobile = () => {
  openKetcherModal()
  isSearchBarVisible.value = false
}

const openPDF2ChemicalsSubmitModal = () => {
  if (pdf2ChemicalsSubmitRef.value) {
    pdf2ChemicalsSubmitRef.value.toggleComponentModal()
  }
}

const handlePDF2ChemicalsSubmit = () => {
  openPDF2ChemicalsSubmitModal()
  closePDF2ChemicalsDropdown()
}

const handlePDF2ChemicalsSubmitMobile = () => {
  openPDF2ChemicalsSubmitModal()
  closeDrawer()
}

// Dropdown handlers
const togglePDF2ChemicalsDropdown = () => {
  isPDF2ChemicalsDropdownOpen.value = !isPDF2ChemicalsDropdownOpen.value
}

const closePDF2ChemicalsDropdown = () => {
  isPDF2ChemicalsDropdownOpen.value = false
}

const toggleMobileUserMenu = () => {
  isMobileUserMenuOpen.value = !isMobileUserMenuOpen.value
}

const closeMobileUserMenu = () => {
  isMobileUserMenuOpen.value = false
}

// Navigation handlers
const handleLogout = async () => {
  closeMobileUserMenu()
  await authStore.logout()
  userStore.clearUserProfile()
  router.replace({ path: '/home' })
}

const handleNotifications = () => {
  // TODO: Implement notifications
  console.log('Notifications clicked')
}

// Search handlers
const toggleSearchBar = () => {
  isSearchBarVisible.value = !isSearchBarVisible.value
}

// Drawer handlers
const toggleDrawer = () => {
  isDrawerOpen.value = !isDrawerOpen.value
  if (isDrawerOpen.value) {
    // Prevent body scroll when drawer is open
    document.body.style.overflow = 'hidden'
    nextTick(() => {
      const firstFocusable = drawerNav.value?.querySelector('a, button')
      firstFocusable?.focus()
    })
  } else {
    document.body.style.overflow = ''
  }
}

const closeDrawer = () => {
  isDrawerOpen.value = false
  document.body.style.overflow = ''
}

// Transition handlers for mobile search
const onEnter = (el) => {
  el.style.height = '0'
  el.style.opacity = '0'
}

const onAfterEnter = (el) => {
  el.style.height = el.scrollHeight + 'px'
  el.style.opacity = '1'
  el.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
}

const onLeave = (el) => {
  el.style.height = el.scrollHeight + 'px'
  el.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
  nextTick(() => {
    el.style.height = '0'
    el.style.opacity = '0'
  })
}

const onAfterLeave = (el) => {
  el.style.height = ''
  el.style.opacity = ''
  el.style.transition = ''
}

onUnmounted(() => {
  document.body.style.overflow = ''
})

// Close mobile menus on route change
watch(() => router.currentRoute.value, () => {
  closeDrawer()
  isSearchBarVisible.value = false
  closeMobileUserMenu()
})
</script>

<style scoped>
/* Smooth transitions */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-enter-from,
.slide-down-leave-to {
  height: 0;
  opacity: 0;
}

/* Drawer transitions */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drawer-enter-active nav,
.drawer-leave-active nav {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from nav,
.drawer-leave-to nav {
  transform: translateX(-100%);
}


/* Improve touch targets on mobile */
@media (max-width: 768px) {
  .btn-square {
    min-height: 44px;
    min-width: 44px;
  }
  
  .menu li > * {
    min-height: 44px;
  }
}

/* Improve link hover effects */
.link {
  position: relative;
  transition: color 0.2s ease;
}

/* Better active states for mobile */
@media (hover: none) {
  .btn:active {
    transform: scale(0.97);
  }
}

/* Improve focus visibility */
:focus-visible {
  outline: 2px solid hsl(var(--p));
  outline-offset: 2px;
  border-radius: 4px;
}

/* Performance optimization for animations */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Prevent horizontal overflow */
.overflow-hidden {
  overflow: hidden;
}

/* Ensure images don't cause layout shift */
img {
  display: block;
}

/* Better text truncation in dropdowns */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Drawer scrollbar styling */
nav::-webkit-scrollbar {
  width: 8px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background: hsl(var(--b3));
  border-radius: 4px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--bc) / 0.3);
}
</style>
