<template>
    <div class="bg-base-200 shadow-lg font-semibold">
        <ul class="menu menu-horizontal text-lg hidden md:flex">
            <li>
                <NuxtLink to="/about" class="flex hover:text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p>About</p>
                </NuxtLink>
            </li>
            <li>
                <details v-close-details class="dropdown dropdown-hover m-auto flex flex-col closed:text-current group/details">
                    <summary class="flex hover:text-primary duration-200 group-open/details:text-primary" tabindex="0" role="button">
                        PDF2Chemicals
                    </summary>
                    <ul tabindex="0" class="dropdown-content z-[2] menu p-2 rounded-box bg-base-200 mx-auto">
                        <li>
                            <NuxtLink class="flex hover:text-primary" to="/pdf2chemicals/about">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <p>About</p>
                            </NuxtLink>
                        </li>
                        <li>
                            <NuxtLink class="flex hover:text-primary" to="/pdf2chemicals/features">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                                </svg>
                                <p>Features</p>
                            </NuxtLink>
                        </li>
                        <li>
                            <a class="flex hover:text-primary" href="">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                                </svg>
                                <p>Submit</p>
                            </a>
                        </li>
                    </ul>
                </details>
            </li>
            <li>
                <a href="" class="flex hover:text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    Download
                </a>
            </li>
            <li>
                <a class="flex hover:text-primary" :href="docsAPIUrl" rel="noopener noreferrer">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                    </svg>
                    API
                </a>
            </li>
            
            <div class="flex ml-auto">
                <li class="my-auto  hover:text-primary">
                    <label class="btn btn-circle btn-ghost swap swap-rotate">    
                        <!-- this hidden checkbox controls the state -->
                        <input ref="themeController" type="checkbox" class="theme-controller" v-model="themeStore.darkMode" @click="themeStore.toggleDarkMode()" />
                        <!-- moon icon -->
                        <svg class="swap-on fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/>
                        </svg>
                        <!-- sun icon -->
                        <svg class="swap-off fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/>
                        </svg>
                    </label>
                </li>
                <li class="my-auto  hover:text-primary">
                    <div class="indicator">
                        <span class="indicator-item badge badge-primary badge-xs top-3 right-6"></span>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path 
                                stroke-linecap="round"
                                stroke-linejoin="round" 
                                d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 
                                8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 
                                1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 
                                24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" 
                            />
                        </svg>
                    </div>
                </li>

                <li class="my-auto">
                   
                    <div v-if="authStore.isAuthenticated" class="dropdown dropdown-bottom dropdown-end">
                        <div tabindex="0" role="button">
                            <div  class="avatar placeholder">
                                <div :class="themeStore.isDarkMode ? 'w-8 rounded-full bg-neutral text-white' : 'w-8 rounded-full bg-slate-600 text-white'">
                                    <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                                </div>
                            </div>
                        </div>
                        <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-48 shadow m-auto">
                            <li class="hover:text-primary">
                                <NuxtLink to="/user/profile" class="flex">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path 
                                            stroke-linecap="round" 
                                            stroke-linejoin="round" 
                                            d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                                            9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                                            3 0 1 1-6 0 3 3 0 0 1 6 0Z" 
                                        />
                                    </svg>
                                    <p>{{ getUserName() }}</p>
                                </NuxtLink>
                            </li>
                            
                            <li class="hover:text-primary">
                                <NuxtLink to="/dashboard" class="flex">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path 
                                            stroke-linecap="round" 
                                            stroke-linejoin="round" 
                                            d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                                            0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                                            1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" 
                                        />
                                    </svg>
                                    <p>Dashboard</p>
                                </NuxtLink>
                            </li>
                            <div class="divider"></div>
                            <li class="hover:text-primary">
                                <a class="flex" @click="handleLogout">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                        <path 
                                            stroke-linecap="round" 
                                            stroke-linejoin="round" 
                                            d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" 
                                        />
                                    </svg>

                                    <p>Log out</p>
                                </a>
                            </li>
                        </ul>
                    </div>
                    
                    <a v-else href="/auth/login" class="flex hover:text-primary">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <p>Log In</p>
                    </a>
                </li>
            </div>
        </ul>

        <ul class="flex menu menu-horizontal text-lg md:hidden">
            <li class="ml-auto my-auto hover:text-primary">
                <label class="btn btn-ghost swap swap-rotate">
                    <!-- this hidden checkbox controls the state -->
                    <input ref="themeController" type="checkbox" class="theme-controller" v-model="themeStore.darkMode" @click="themeStore.toggleDarkMode()" />
                    <!-- moon icon -->
                    <svg class="swap-on fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z"/>
                    </svg>          
                    <!-- sun icon -->
                    <svg class="swap-off fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z"/>
                    </svg>
                </label>
            </li>
            <li class="my-auto">
                <div v-if="authStore.isAuthenticated" class="dropdown dropdown-bottom dropdown-end">
                    <div tabindex="0" role="button" class="">
                        <div  class="avatar placeholder">
                            <div :class="themeStore.isDarkMode ? 'w-8 rounded-full bg-neutral text-white' : 'w-8 rounded-full bg-slate-600 text-white'">
                                <span>{{ getUserFirstAndLastFirstLetters() }}</span>
                            </div>
                        </div>
                    </div>
                    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 shadow m-auto">
                        <li class="hover:text-primary">
                            <NuxtLink to="/user/profile" class="flex">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path 
                                        stroke-linecap="round" 
                                        stroke-linejoin="round" 
                                        d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 
                                        9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 
                                        3 0 1 1-6 0 3 3 0 0 1 6 0Z" 
                                    />
                                </svg>
                                <p>{{ getUserName() }}</p>
                            </NuxtLink>
                        </li>
                        
                        <li class="hover:text-primary">
                            <NuxtLink to="/dashboard" class="flex">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path 
                                        stroke-linecap="round" 
                                        stroke-linejoin="round" 
                                        d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 
                                        0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 
                                        1.5m-.5-1.5h-9.5m0 0-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" 
                                    />
                                </svg>
                                <p>Dashboard</p>
                            </NuxtLink>
                        </li>
                        <div class="divider"></div>
                        <li class="hover:text-primary">
                            <a class="flex" @click="handleLogout">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                    <path 
                                        stroke-linecap="round" 
                                        stroke-linejoin="round" 
                                        d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" 
                                    />
                                </svg>
                                <p>Log out</p>
                            </a>
                        </li>
                    </ul>
                </div>
                <a v-else href="/auth/login" class="flex hover:text-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                    Log In
                </a>
            </li>
        </ul>
        
    </div>
    <div class="navbar bg-base-100 shadow-xl">
        <div class="navbar-start">
            <div class="drawer md:hidden group/details closed:text-current">
              <input id="my-drawer" type="checkbox" class="drawer-toggle" />
              <div class="drawer-content">
                <!-- Page content here -->
                <label for="my-drawer" class="btn btn-ghost drawer-button">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="swap-off fill-current h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                </label>
              </div>
                <div class="drawer-side z-[2]">
                    <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
                    <ul class="menu menu-md  p-2 shadow min-h-full bg-base-100 w-44 text-lg font-bold">
                        <li>
                            <NuxtLink to='/about' class="flex">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                About
                            </NuxtLink>
                        </li>
                        <li>
                            <details v-close-details class="my-auto">
                                <summary>PDF2Chemicals</summary>
                                <ul class="p-2">
                                    <li>
                                        <NuxtLink to="/pdf2chemicals/about">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                            <p>About</p>
                                        </NuxtLink>
                                    </li>
                                    <li>
                                        <NuxtLink  to="/pdf2chemicals/features">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                              <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                                            </svg>
                                        
                                            <p>Features</p>
                                        </NuxtLink>
                                    </li>
                                    <li>
                                        <a class="flex" href="">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                              <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                                            </svg>
                                            <p>Submit</p>
                                        </a>
                                    </li>
                                </ul>
                            </details>
                        </li>
                        <li>
                            <NuxtLink class="flex" to='/'>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                                </svg>
                                Download
                            </NuxtLink>
                        </li>
                        <li>
                            <a class="flex" :href="docsAPIUrl" rel="noopener noreferrer">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                                </svg>
                                Web API
                            </a>
                        </li>
                    </ul>
                </div>
            </div>

            <!--<details v-close-details class="dropdown md:hidden group/details closed:text-current">
                <summary ref="menuSummary" @click="toggleDetailsSwapCheckbox()" tabindex="0" role="button" class="btn btn-ghost swap swap-rotate duration-200 group-open/details:text-primary">
                    <input type="checkbox" ref="menuDetailsSwapCheckbox" />

                    <svg class="swap-on fill-current h-6 w-6" xmlns="http://www.w3.org/2000/svg" stroke-width="2.5" viewBox="0 0 512 512">
                        <polygon points="400 145.49 366.51 112 256 222.51 145.49 112 112 145.49 222.51 256 112 366.51 145.49 400 256 289.49 366.51 400 400 366.51 289.49 256 400 145.49"/>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="swap-off fill-current h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>    
                </summary>                    

                <ul tabindex="0" class="menu menu-md dropdown-content mt-3 z-[2] p-2 shadow bg-base-100 rounded-box w-44 text-lg font-bold">
                    <li>
                        <NuxtLink to='/about' class="flex">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            About
                        </NuxtLink>
                    </li>
                    <li>
                        <details v-close-details class="my-auto">
                            <summary>PDF2Chemicals</summary>
                            <ul class="p-2">
                                <li>
                                    <NuxtLink to="/pdf2chemicals/about">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <p>About</p>
                                    </NuxtLink>
                                </li>
                                <li>
                                    <NuxtLink  to="/pdf2chemicals/features">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                          <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                                        </svg>

                                        <p>Features</p>
                                    </NuxtLink>
                                </li>
                                <li>
                                    <a class="flex" href="">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                                        </svg>
                                        <p>Submit</p>
                                    </a>
                                </li>
                            </ul>
                        </details>
                    </li>
                    <li>
                        <NuxtLink class="flex" to='/'>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                            Download
                        </NuxtLink>
                    </li>
                    <li>
                        <a class="flex" :href="docsAPIUrl" rel="noopener noreferrer">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
                            </svg>
                            Web API
                        </a>
                    </li>
                </ul>
            </details>-->

            <NuxtLink to="/home" class="btn btn-ghost text-2xl text-primary hidden md:flex">
                <img src="~/assets/labsodb_logo_dark.webp" v-if="themeStore.isDarkMode" class="my-auto w-52 lg:w-64" />
                <img src="~/assets/labsodb_logo_light.webp" v-else class="my-auto w-52 lg:w-64" />
            </NuxtLink>
        </div>
        <div class="navbar-center">
            <NuxtLink to="/home" class="btn btn-ghost text-lg text-primary md:hidden">
                <img src="~/assets/labsodb_logo_dark.webp" v-if="themeStore.isDarkMode" class="my-auto w-36" />
                <img src="~/assets/labsodb_logo_light.webp" v-else class="my-auto w-36" />
            </NuxtLink>
        </div>
        <div class="navbar-end">
            <div class="hidden md:flex">
                <div class="flex flex-col">
                    <div class="join">
                        <input class="input input-bordered join-item text-lg w-72" type="text" placeholder="Search Chemical" required>
                        <div class="indicator">
                          <button type="submit" class="btn btn-primary join-item">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="size-6 m-auto">
                              <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                          </button>
                        </div>
                    </div>
                    <div class="flex text-md font-semibold">
                        <div class="flex gap-2">
                            <a class="link link-secondary lg:link-primary duration-200 lg:hover:text-secondary" @click="openKetcherModal()">Draw Structure</a>
                            <NuxtLink to="/chemicals/advanced" class="link link-secondary lg:link-primary duration-200 lg:hover:text-secondary">Advanced Search</NuxtLink>
                        </div>    
                    </div>
                </div>              
            </div>
            <div class="flex md:hidden">    
                <button type="button" ref="searchBarToggleButton" class="btn btn-ghost duration-200" @click="toggleSearchBar">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" class="h-6 w-6 stroke-current">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                    </svg>
                </button>
            </div>
        </div>
    </div>

    <div class="bg-base-200 shadow-md font-semibold">
        <div class="md:hidden">
            <transition 
            name="collapse"
            @enter="$enter"
            @after-enter="$afterEnter"
            @leave="$leave"
            @after-leave="$afterLeave"
            >   
                <div v-show="isSearchBarVisible" class="collapsible">
                    <ul class="flex w-[90%] menu menu-horizontal mx-auto">
                        <div class="m-auto flex flex-col w-full">
                            <div class="join">
                                <input class="input input-bordered join-item text-md w-full" type="text" placeholder="Search Chemical" required>
                                <div class="indicator">
                                    <button type="submit" class="btn btn-primary join-item">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="h-6 w-6 m-auto">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <div class="flex text-sm font-semibold gap-2">
                                <NuxtLink to="/chemicals/advanced" class="link link-secondary">Advanced Search</NuxtLink>
                            </div>
                        </div>
                    </ul>
                </div>
            </transition>
        </div>
        
    </div>
    <modal ref="ketcherModalRef">
        <ketcher-component></ketcher-component>
    </modal>
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue';
import { useThemeStore } from '~/stores/theme';
import { useAuthStore } from '~/stores/auth'
import { useUserStore } from '~/stores/user'
import { useNuxtApp } from 'nuxt/app';
import { useRouter } from 'nuxt/app';
import Modal from '~/components/Modal.vue';

const KetcherComponent = defineAsyncComponent({
    loader: () => import('~/components/KetcherComponent.vue')
});

const config = useRuntimeConfig()

const { $enter, $afterEnter, $leave, $afterLeave } = useNuxtApp()

const router = useRouter()

const docsAPIUrl = config.public.apiHost + config.public.docsAPIEndpoint

const themeStore = useThemeStore();
const authStore = useAuthStore()
const userStore = useUserStore()

var searchBarToggleButton = ref(null)

var ketcherModalRef =  ref(null)

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
    if(ketcherModalRef.value) {
        ketcherModalRef.value.toggleComponentModal()
    }
}

const handleLogout = async () => {
    await authStore.logout()

    userStore.clearUserProfile()

    router.push({
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