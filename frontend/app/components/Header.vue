<template>
  <header role="banner">
    <div class="bg-base-200 shadow-md font-semibold">
      <ul class="menu menu-horizontal text-base hidden md:flex w-full px-4">
        <li>
          <NuxtLink to="/about" class="flex hover:text-primary transition-colors duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
            </svg>
            <p>About</p>
          </NuxtLink>
        </li>
        <li>
          <div class="dropdown dropdown-hover">
            <div tabindex="0" role="button" class="flex hover:text-primary transition-colors duration-200">
              PDF2Chemicals
            </div>
            <ul tabindex="0" class="dropdown-content menu p-2 rounded-box bg-base-200 shadow-md w-52">
              <li>
                <NuxtLink class="flex hover:text-primary transition-colors duration-200" to="/pdf2chemicals/about">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                  </svg>
                  <p>About</p>
                </NuxtLink>
              </li>
              <li>
                <NuxtLink
                  class="flex hover:bg-gradient-to-r hover:from-primary hover:via-secondary hover:to-accent transition-colors duration-200"
                  to="/pdf2chemicals/features">

                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                  </svg>

                  <p>Features</p>
                </NuxtLink>
              </li>
              <li>
                <a class="flex hover:text-primary transition-colors duration-200" @click="openPDF2ChemicalsSubmitModal">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="h-6 w-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                  </svg>
                  <p>Submit</p>
                </a>
              </li>
            </ul>
          </div>
        </li>
        <li>
          <a href="" class="flex hover:text-primary transition-colors duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
            </svg>

            Download
          </a>
        </li>
        <li>
          <a class="flex hover:text-primary transition-colors duration-200" :href="config.public.docsAPIEndpoint"
            rel="noopener noreferrer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
            </svg>

            API
          </a>
        </li>
        <div class="flex ml-auto items-center gap-4">
          <li>
            <label class="btn btn-circle btn-ghost swap swap-rotate hover:text-primary transition-colors duration-200">
              <input ref="themeController" type="checkbox" class="theme-controller" v-model="themeStore.darkMode"
                @click="themeStore.toggleDarkMode()" />
              <!-- Moon SVG icon class="swap-on fill-current h-6 w-6" -->
              <svg class="swap-on fill-current size-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
              </svg>
              <!-- Sun SVG icon class="swap-off fill-current h-6 w-6" -->
              <svg class="swap-off fill-current size-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path
                  d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
              </svg>
            </label>
          </li>
          <li class="hover:text-primary transition-colors duration-200">
            <div class="indicator">
              <span class="indicator-item badge badge-xs badge-primary"></span>
              <!-- Notification SVG icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 
                        8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 
                        1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 
                        24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
              </svg>
            </div>
          </li>
          <li>
            <div v-if="authStore.isAuthenticated && userStore.user" class="dropdown dropdown-bottom dropdown-end">
              <div tabindex="0" role="button" aria-label="User menu">
                <div class="avatar avatar-placeholder">
                  <div
                    :class="themeStore.isDarkMode ? 'w-8 rounded-full bg-neutral text-white' : 'w-8 rounded-full bg-slate-600 text-white'">
                    <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                  </div>
                </div>
              </div>
              <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-48 p-2 shadow-md">
                <li>
                  <NuxtLink to="/user/profile" class="flex hover:text-primary transition-colors duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                            9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                            3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    <p>{{ getUserName() }}</p>
                  </NuxtLink>
                </li>
                <li>
                  <NuxtLink to="/dashboard" class="flex hover:text-primary transition-colors duration-200">
                    <!-- Dashboard SVG icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                            0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                            1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                    </svg>
                    <p>Dashboard</p>
                  </NuxtLink>
                </li>
                <div class="divider my-1"></div>
                <li>
                  <a class="flex hover:text-primary transition-colors duration-200" @click="handleLogout">
                    <!-- Logout SVG icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                    </svg>
                    <p>Log out</p>
                  </a>
                </li>
              </ul>
            </div>
            <a v-else href="/auth/login" class="flex hover:text-primary transition-colors duration-200">
              <!-- Login SVG icon -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
              </svg>
              <p>Log In</p>
            </a>
          </li>
        </div>
      </ul>
      <ul class="flex menu menu-horizontal text-base md:hidden w-full px-4">
        <li class="ml-auto">
          <label class="btn btn-ghost swap swap-rotate hover:text-primary transition-colors duration-200">
            <input ref="themeController" type="checkbox" class="theme-controller" v-model="themeStore.darkMode"
              @click="themeStore.toggleDarkMode()" />
            <!-- Moon SVG icon -->
            <svg class="swap-on fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path
                d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" />
            </svg>
            <!-- Sun SVG icon -->
            <svg class="swap-off fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path
                d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" />
            </svg>
          </label>
        </li>
        <li>
          <div v-if="authStore.isAuthenticated && userStore.user" class="dropdown dropdown-bottom dropdown-end">
            <div tabindex="0" role="button" aria-label="User menu">
              <div class="avatar avatar-placeholder">
                <div
                  :class="themeStore.isDarkMode ? 'w-8 rounded-full bg-neutral text-white' : 'w-8 rounded-full bg-slate-600 text-white'">
                  <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                </div>
              </div>
            </div>
            <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow-md">
              <li>
                <NuxtLink to="/user/profile" class="flex hover:text-primary transition-colors duration-200">
                  <!-- User avatar SVG icon -->
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                            9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                            3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <p>{{ getUserName() }}</p>
                </NuxtLink>
              </li>
              <li>
                <NuxtLink to="/dashboard" class="flex hover:text-primary transition-colors duration-200">
                  <!-- Dashboard SVG icon -->
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                            0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                            1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                  </svg>
                  <p>Dashboard</p>
                </NuxtLink>
              </li>
              <div class="divider my-1"></div>
              <li>
                <a class="flex hover:text-primary transition-colors duration-200" @click="handleLogout">
                  <!-- Logout SVG icon -->
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                  </svg>
                  <p>Log out</p>
                </a>
              </li>
            </ul>
          </div>
          <a v-else href="/auth/login" class="flex hover:text-primary transition-colors duration-200">
            <!-- User avatar SVG icon -->
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                    9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                    3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
            Log In
          </a>
        </li>
      </ul>
    </div>
    <div class="navbar bg-base-100 shadow-md px-4">
      <div class="navbar-start">
        <div class="drawer md:hidden">
          <input id="my-drawer" type="checkbox" class="drawer-toggle" />
          <div class="drawer-content">
            <label for="my-drawer" class="btn btn-ghost drawer-button" aria-label="Open menu">
              <!-- Hamburger SVG icon -->
            </label>
          </div>
          <div class="drawer-side z-[2]">
            <label for="my-drawer" aria-label="Close sidebar" class="drawer-overlay"></label>
            <ul class="menu p-4 w-64 min-h-full bg-base-100 text-base font-semibold">
              <li>
                <NuxtLink to="/about" class="flex hover:text-primary transition-colors duration-200">
                  <!-- About SVG icon -->
                  About
                </NuxtLink>
              </li>
              <li>
                <div class="dropdown">
                  <div tabindex="0" role="button">PDF2Chemicals</div>
                  <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                    <li>
                      <NuxtLink to="/pdf2chemicals/about" class="hover:text-primary transition-colors duration-200">
                        <!-- About SVG icon -->
                        About
                      </NuxtLink>
                    </li>
                    <li>
                      <NuxtLink to="/pdf2chemicals/features" class="hover:text-primary transition-colors duration-200">
                        <!-- Features SVG icon -->
                        Features
                      </NuxtLink>
                    </li>
                    <li>
                      <a @click="openPDF2ChemicalsSubmitModal"
                        class="hover:text-primary transition-colors duration-200">
                        <!-- Submit SVG icon -->
                        Submit
                      </a>
                    </li>
                  </ul>
                </div>
              </li>
              <li>
                <NuxtLink class="flex hover:text-primary transition-colors duration-200" to="/">
                  <!-- Download SVG icon -->
                  Download
                </NuxtLink>
              </li>
              <li>
                <NuxtLink class="flex hover:text-primary transition-colors duration-200"
                  :to="config.public.docsAPIEndpoint">
                  <!-- API SVG icon -->
                  Web API
                </NuxtLink>
              </li>
            </ul>
          </div>
        </div>
        <NuxtLink to="/home" class="btn btn-ghost text-2xl text-primary hidden md:flex">
          <img v-if="themeStore.isDarkMode" src="~/assets/labsodb_logo_dark.webp" class="my-auto w-52 lg:w-64"
            alt="Logo" />
          <img v-else src="~/assets/labsodb_logo_light.webp" class="my-auto w-52 lg:w-64" alt="Logo" />
        </NuxtLink>
      </div>
      <div class="navbar-center">
        <NuxtLink to="/home" class="btn btn-ghost text-lg text-primary md:hidden">
          <img v-if="themeStore.isDarkMode" src="~/assets/labsodb_logo_dark.webp" class="my-auto w-52 lg:w-64"
            alt="Logo" />
          <img v-else src="~/assets/labsodb_logo_light.webp" class="my-auto w-52 lg:w-64" alt="Logo" />
        </NuxtLink>
      </div>
      <div class="navbar-end">
        <div class="hidden md:flex flex-col gap-1">
          <header-quick-search-field></header-quick-search-field>
          <div class="flex text-sm font-semibold gap-4">
            <a class="link link-secondary lg:link-primary hover:text-secondary transition-colors duration-200"
              @click="openKetcherModal()">Draw Structure</a>
            <NuxtLink to="/chemicals/advanced"
              class="link link-secondary lg:link-primary hover:text-secondary transition-colors duration-200">
              Advanced Search</NuxtLink>
          </div>
        </div>
        <div class="md:hidden">
          <button ref="searchBarToggleButton" class="btn btn-ghost transition-colors duration-200"
            @click="toggleSearchBar" aria-label="Toggle search">
            <!-- Search SVG icon -->
          </button>
        </div>
      </div>
    </div>
    <div class="bg-base-200 shadow-md md:hidden">
      <transition name="collapse" @enter="$enter" @after-enter="$afterEnter" @leave="$leave" @after-leave="$afterLeave">
        <div v-show="isSearchBarVisible" class="collapsible px-4 py-2">
          <div class="flex flex-col gap-1 m-auto">
            <header-quick-search-field></header-quick-search-field>
            <div class="flex text-sm font-semibold gap-4">
              <NuxtLink to="/chemicals/advanced"
                class="link link-secondary hover:text-secondary transition-colors duration-200">Advanced
                Search</NuxtLink>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <modal ref="ketcherModalRef">
      <ketcher-component></ketcher-component>
    </modal>
    <modal ref="pdf2ChemicalsSubmitRef">
      <PDF2ChemicalsSubmitComponent></PDF2ChemicalsSubmitComponent>
    </modal>
  </header>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue';
import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'
import { useUserStore } from '~/stores/user'
import { useNuxtApp } from 'nuxt/app';
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

const { $enter, $afterEnter, $leave, $afterLeave } = useNuxtApp()

const router = useRouter()

const themeStore = useThemeStore();
const authStore = useAuthStore()
const userStore = useUserStore()

var searchBarToggleButton = ref(null)

var ketcherModalRef = ref(null)
var pdf2ChemicalsSubmitRef = ref(null)

var isSearchBarVisible = ref(false)
var menuSummary = ref(null)
var menuDetailsSwapCheckbox = ref(null)

const getUserFirstAndLastFirstLetters = () => {
  let first_name_first_letter = userStore.user.first_name.charAt(0)
  let last_name_first_letter = userStore.user.last_name.charAt(0)

  return first_name_first_letter + last_name_first_letter
}

const getUserName = () => {
  return `${userStore.user.first_name} ${userStore.user.last_name}`
}

const openKetcherModal = () => {
  if (ketcherModalRef.value) {
    ketcherModalRef.value.toggleComponentModal()
  }
}

const openPDF2ChemicalsSubmitModal = () => {
  if (pdf2ChemicalsSubmitRef.value) {
    pdf2ChemicalsSubmitRef.value.toggleComponentModal()
  }
}

const handleLogout = async () => {
  await authStore.logout()

  userStore.clearUserProfile()

  router.replace({
    path: '/home'
  })
}

const toggleDetailsSwapCheckbox = () => {
  menuDetailsSwapCheckbox.value.checked = !menuDetailsSwapCheckbox.value.checked
}

const toggleSearchBar = () => {
  isSearchBarVisible.value = !isSearchBarVisible.value
  searchBarToggleButton.value.classList.toggle('text-primary')
}
</script>