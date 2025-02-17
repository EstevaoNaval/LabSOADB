<template>
  <div class="flex flex-col gap-4 min-h-screen">
    <section :class="themeStore.isDarkMode? 'dashboard-buttons-background-dark bg-scroll bg-cover bg-center' : 'dashboard-buttons-background-light bg-scroll bg-cover bg-center'">
      <div :class="themeStore.isDarkMode ? 'bg-opacity-80 h-full flex flex-col justify-center bg-base-300 py-8 gap-4' : 'bg-opacity-0 h-full flex flex-col justify-center bg-base-300 py-8 gap-4'">
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 w-[95%] mx-auto">
          <div 
            role="button" 
            :class="themeStore.isDarkMode ? 
            'stats shadow bg-base-300 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl' : 
            'stats shadow bg-green-500 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl'"
          >
            <div class="stat m-auto">
              <div :class="themeStore.isDarkMode ? 'stat-figure text-success' : 'stat-figure text-white'">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke-width="1.5" 
                  stroke="currentColor" 
                  class="inline-block stroke-current size-16 m-auto"
                >
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    d="m4.5 12.75 6 6 9-13.5" 
                  />
                </svg>
              </div>
              <div :class="themeStore.isDarkMode ? 'stat-title' : 'stat-title text-white'">Concluded Tasks</div>
              <div :class="themeStore.isDarkMode ? 'stat-value text-success' : 'stat-value text-white'">89,400</div>
            </div>
          </div>
          <div 
            role="button" 
            :class="themeStore.isDarkMode ? 
            'stats shadow bg-base-300 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl' : 
            'stats shadow bg-amber-500 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl'"
          >
            <div class="stat m-auto">
              <div :class="themeStore.isDarkMode ? 'stat-figure text-warning' : 'stat-figure text-white'">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  fill="none" 
                  viewBox="0 0 24 24" 
                  stroke-width="1.5" 
                  stroke="currentColor" 
                  class="inline-block stroke-current size-16 m-auto"
                >
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 
                    3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 
                    3.182m0-4.991v4.99" 
                  />
                </svg>
              </div>
              <div :class="themeStore.isDarkMode ? 'stat-title' : 'stat-title text-white'">Tasks in Progress</div>
              <div :class="themeStore.isDarkMode ? 'stat-value text-warning' : 'stat-value text-white'">89,400</div>
            </div>
          </div>
          
          <div 
            role="button" 
            :class="themeStore.isDarkMode ? 
            'stats shadow bg-base-300 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl' : 
            'stats shadow bg-rose-500 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl'"
          >
            <div class="stat m-auto">
                <div :class="themeStore.isDarkMode ? 'stat-figure text-error' : 'stat-figure text-white'">
                    <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        fill="none" 
                        viewBox="0 0 24 24" 
                        stroke-width="1.5" 
                        stroke="currentColor" 
                        class="inline-block stroke-current size-16 m-auto"
                    >
                        <path 
                            stroke-linecap="round" 
                            stroke-linejoin="round" 
                            d="M6 18 18 6M6 6l12 12" 
                        />
                    </svg>
                  
                </div>
                <div :class="themeStore.isDarkMode ? 'stat-title' : 'stat-title text-white'">Failed Tasks</div>
                <div :class="themeStore.isDarkMode ? 'stat-value text-error' : 'stat-value text-white'">89,400</div>
            </div>
          </div>
          <div 
            role="button" 
            :class="themeStore.isDarkMode ? 
            'stats shadow bg-base-300 cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl' : 
            'stats shadow bg-primary cursor-pointer transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-xl'"
          >
            <div class="stat m-auto">
                <div :class="themeStore.isDarkMode ? 'stat-figure text-info' : 'stat-figure text-white'">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-file-earmark-pdf inline-block m-auto size-14" viewBox="0 0 16 16">
                        <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2M9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5z"/>
                        <path d="M4.603 14.087a.8.8 0 0 1-.438-.42c-.195-.388-.13-.776.08-1.102.198-.307.526-.568.897-.787a7.7 7.7 0 0 1 1.482-.645 20 20 0 0 0 1.062-2.227 7.3 7.3 0 0 1-.43-1.295c-.086-.4-.119-.796-.046-1.136.075-.354.274-.672.65-.823.192-.077.4-.12.602-.077a.7.7 0 0 1 .477.365c.088.164.12.356.127.538.007.188-.012.396-.047.614-.084.51-.27 1.134-.52 1.794a11 11 0 0 0 .98 1.686 5.8 5.8 0 0 1 1.334.05c.364.066.734.195.96.465.12.144.193.32.2.518.007.192-.047.382-.138.563a1.04 1.04 0 0 1-.354.416.86.86 0 0 1-.51.138c-.331-.014-.654-.196-.933-.417a5.7 5.7 0 0 1-.911-.95 11.7 11.7 0 0 0-1.997.406 11.3 11.3 0 0 1-1.02 1.51c-.292.35-.609.656-.927.787a.8.8 0 0 1-.58.029m1.379-1.901q-.25.115-.459.238c-.328.194-.541.383-.647.547-.094.145-.096.25-.04.361q.016.032.026.044l.035-.012c.137-.056.355-.235.635-.572a8 8 0 0 0 .45-.606m1.64-1.33a13 13 0 0 1 1.01-.193 12 12 0 0 1-.51-.858 21 21 0 0 1-.5 1.05zm2.446.45q.226.245.435.41c.24.19.407.253.498.256a.1.1 0 0 0 .07-.015.3.3 0 0 0 .094-.125.44.44 0 0 0 .059-.2.1.1 0 0 0-.026-.063c-.052-.062-.2-.152-.518-.209a4 4 0 0 0-.612-.053zM8.078 7.8a7 7 0 0 0 .2-.828q.046-.282.038-.465a.6.6 0 0 0-.032-.198.5.5 0 0 0-.145.04c-.087.035-.158.106-.196.283-.04.192-.03.469.046.822q.036.167.09.346z"/>
                    </svg>
                </div>
                <div :class="themeStore.isDarkMode ? 'stat-title' : 'stat-title text-white'">Uploaded PDFs</div>
                <div :class="themeStore.isDarkMode ? 'stat-value text-info' : 'stat-value text-white'">89,400</div>
            </div>
          </div>
        </div>

        <div class="m-auto grid grid-cols-2 lg:grid-cols-4">
          <button @click="openKetcherModal()" type="button" class="hidden md:flex flex-col duration-200 btn-ghost m-auto rounded-box font-semibold text-primary text-xl md:text-2xl p-3 md:p-8">
            <svg fill="currentColor" class="size-20 md:size-36 mx-auto" viewBox="0 0 500 670" xmlns="http://www.w3.org/2000/svg">
              <path d="m461.449 423-.57-48.735c11.658-5.872 19.875-18.05 20.072-32.235.13-9.759-3.441-18.987-10.05-25.988-6.6-6.996-15.445-10.915-25.355-11.04-10.611 0-20.1 5.003-26.607 12.737l-38.723-22.96c1.468-5.992 1.59-12.275-.018-18.408-1.74-6.634-5.245-12.43-9.985-17.02.187.038.327.116.514.145-2.757-2.83-5.918-5.27-9.47-7.078l-.56-48.74c11.658-5.877 19.875-18.05 20.062-32.24.141-9.754-3.43-18.987-10.04-25.988-6.6-6.99-15.454-10.91-25.355-11.04-10.611 0-20.1 5.009-26.607 12.737l-38.732-22.935c1.458-5.993 1.59-12.276-.018-18.409-2.469-9.426-8.35-17.3-16.552-22.154a35.387 36.5 0 0 0-17.614-4.86c-12.659 0-24.443 7.02-30.74 18.326-3.122 5.598-4.473 11.702-4.539 17.734l-40.33 23.591c-5.881-4.372-12.935-6.85-20.68-6.952-10.607 0-22.382 6.34-26.585 12.738-2.902 4.031-11.793 11.77-8.96 31.214 2.832 19.44 16.855 24.45 24.363 27.044l.706 44.998c-.201.068-.37.179-.57.237l1.566.299a35.6 35.6 0 0 0-20.563 16.735c-3.108 5.588-4.47 11.692-4.534 17.733l-41.682 24.372c-5.745-3.92-12.532-6.195-19.6-6.195a35.467 36.582 0 0 0-18.226 5.217c-16.727 10.393-22.144 32.891-12.103 50.132 4.431 7.608 11.434 13.132 19.436 15.843l.724 45.822A35.84 35.84 0 0 0 25.49 433.52c-4.72 8.466-5.955 18.312-3.486 27.743 2.473 9.43 8.349 17.3 16.552 22.159a35.516 36.632 0 0 0 17.627 4.85c7.727 0 15.084-2.642 21.11-7.242l40.452 23.972c-.187 3.8.051 7.636 1.038 11.417 2.468 9.43 8.348 17.3 16.552 22.16 5.37 3.172 11.457 4.859 17.632 4.859 12.658 0 24.433-7.03 30.73-18.33 4.01-7.203 5.235-15.226 4.249-22.903l38.719-22.428c6.15 5.65 14.116 9.267 22.965 9.373h.523c7.536 0 14.515-2.535 20.278-6.75l43.089 25.535c-.196 3.817.047 7.637 1.028 11.436 2.478 9.43 8.357 17.29 16.557 22.14a35.443 36.558 0 0 0 17.632 4.861c12.66 0 24.429-7.02 30.73-18.323 4.02-7.212 5.235-15.235 4.254-22.91l38.704-22.42c6.367 5.863 14.38 9.267 22.98 9.364h.533c19.249 0 35.114-16.162 35.357-36.026.199-14.438-7.898-26.964-19.846-33.057m-15.715-98.242c4.348.058 8.415 1.851 11.453 5.072a16.229 16.739 0 0 1 4.61 11.938c-.131 9.141-7.415 16.567-16.259 16.567v9.276h-.01l-.205-9.276c-8.966-.135-16.164-7.772-16.071-17.02.131-9.132 7.433-16.557 16.482-16.557m-85.609-30.49c-4.31 7.708-14.658 10.66-22.231 6.19-7.788-4.613-10.47-14.893-6.002-22.92 2.888-5.193 8.312-8.423 14.135-8.423 2.823 0 5.61.77 8.087 2.232 3.778 2.242 6.48 5.853 7.61 10.183 1.122 4.334.562 8.856-1.599 12.737m-14.574-140.09c4.347.062 8.415 1.86 11.453 5.076 3.019 3.22 4.655 7.454 4.6 11.938-.122 9.136-7.405 16.562-16.25 16.562h-.215c-8.965-.13-16.163-7.763-16.07-17.015.121-9.132 7.413-16.562 16.482-16.562M231.7 106.961c2.888-5.202 8.306-8.423 14.14-8.423 2.823 0 5.61.771 8.078 2.232 3.782 2.242 6.483 5.853 7.61 10.178a17.1 17.1 0 0 1-1.59 12.738c-4.305 7.714-14.654 10.665-22.227 6.19-7.783-4.608-10.484-14.887-6.011-22.915m-98.408 60.827c.127-9.127 7.414-16.551 16.478-16.551h.01c4.347.057 8.414 1.856 11.447 5.077 3.03 3.206 4.666 7.453 4.61 11.937-.127 9.133-7.414 16.557-16.259 16.557h-.21c-8.98-.125-16.187-7.767-16.076-17.02m32.18 81.7-.566-48.73c11.667-5.878 19.885-18.052 20.077-32.25a37.6 37.6 0 0 0-2.693-14.427l33.553-19.618c2.996 5.005 7.049 9.407 12.322 12.54a35.467 36.582 0 0 0 17.637 4.855c9.372 0 18.244-3.87 24.789-10.476l39.929 23.668c-.272 1.79-.57 3.568-.598 5.424-.224 18.958 13.742 34.617 31.664 36.614l.683 42.496.104.029c-11.228 1.215-21.4 7.873-27.085 18.08-3.121 5.603-4.468 11.702-4.534 17.734l-40.33 23.59c-5.877-4.372-12.935-6.85-20.68-6.952-10.607 0-20.082 5.01-26.585 12.738l-38.714-22.954c1.463-5.998 1.59-12.276-.018-18.418-2.098-7.955-6.712-14.672-13-19.541l.815.158c-2.1-1.745-4.321-3.317-6.77-4.56m100.557 89.34c-.127 9.132-7.41 16.557-16.259 16.557v9.286h-.01l-.2-9.286c-8.98-.125-16.178-7.753-16.071-17.019.122-9.122 7.409-16.557 16.473-16.557h.01c4.347.068 8.419 1.862 11.452 5.082 3.025 3.21 4.66 7.453 4.605 11.938M136.12 274.597c2.888-5.192 8.306-8.433 14.136-8.433 2.819 0 5.604.772 8.072 2.242a16.205 16.714 0 0 1 7.62 10.178c1.131 4.325.575 8.848-1.598 12.739-4.306 7.713-14.655 10.674-22.228 6.19-7.783-4.599-10.475-14.878-6.002-22.916m-96.327 71.251c-4.627-7.926-2.127-18.273 5.549-23.036a16.309 16.821 0 0 1 8.357-2.392c5.782 0 11.013 3.047 13.977 8.138a16.149 16.656 0 0 1 1.851 12.71c-1.056 4.34-3.687 8.023-7.399 10.328-7.527 4.676-17.875 1.957-22.335-5.748m30.53 114.268c-4.301 7.705-14.669 10.675-22.214 6.19-3.772-2.226-6.46-5.852-7.6-10.173a16.22 16.73 0 0 1 1.607-12.757 16.357 16.87 0 0 1 14.13-8.418c2.815 0 5.61.772 8.083 2.237 7.765 4.609 10.452 14.907 5.993 22.92m96.775 55.168c-4.3 7.714-14.617 10.665-22.217 6.18-3.772-2.246-6.474-5.842-7.606-10.173a17.1 17.1 0 0 1 1.6-12.738c2.893-5.197 8.31-8.428 14.139-8.428 2.824 0 5.633.762 8.082 2.218 7.774 4.638 10.471 14.917 6.002 22.94m47.61-63.122c-.051 3.838.64 7.464 1.664 10.955l-35.965 20.83c-2.664-3.396-5.89-6.414-9.774-8.738-5.37-3.153-11.453-4.83-17.618-4.83-11.584 0-22.382 5.93-28.958 15.591L89 465.188c6.394-16.595.308-35.976-15.136-45.119-3.473-2.063-7.282-3.424-11.191-4.185l-.687-43.199c3.502-.877 6.89-2.227 10.013-4.166 8.11-5.024 13.822-12.998 16.122-22.467 1.953-8.081 1.042-16.355-2.24-23.818l34.395-20.115c2.986 5.005 7.035 9.407 12.312 12.54a35.467 36.582 0 0 0 17.632 4.855c9.372 0 18.25-3.87 24.798-10.476l39.94 23.678c-.282 1.783-.576 3.547-.604 5.39-.2 16.258 10.042 30.047 24.22 34.965l.71 44.993c-14.039 4.725-24.374 18.127-24.575 34.096m35.456 17.26v9.875l-.257-9.874c-8.971-.117-16.17-7.753-16.053-17.01.112-9.122 7.409-16.548 16.482-16.548 8.98.126 16.179 7.754 16.067 17.01-.126 9.122-7.4 16.548-16.24 16.548m112.711 48.812c-4.29 7.695-14.602 10.684-22.222 6.162a16.092 16.598 0 0 1-7.601-10.154c-1.141-4.33-.58-8.853 1.599-12.728 2.898-5.198 8.311-8.438 14.135-8.438 2.823 0 5.62.772 8.078 2.228 7.788 4.609 10.48 14.908 6.011 22.93m47.605-63.122c-.047 3.78.608 7.434 1.646 10.944l-35.956 20.819c-2.664-3.393-5.881-6.402-9.78-8.717a35.507 36.624 0 0 0-17.613-4.84c-11.583 0-22.372 5.94-28.944 15.583l-37.152-22.005a35.147 36.252 0 0 0 2.86-13.79c.178-14.464-7.927-26.98-19.876-33.055l-.566-48.735c11.673-5.872 19.881-18.05 20.077-32.246.066-5.034-.897-9.913-2.692-14.426l33.553-19.623c3 5.004 7.05 9.41 12.322 12.546a35.548 36.665 0 0 0 17.632 4.85c9.377 0 18.25-3.867 24.793-10.477l39.93 23.668c-.272 1.784-.571 3.568-.6 5.43-.223 18.957 13.744 34.616 31.666 36.603l.496 41.763c-17.595 1.939-31.571 17.117-31.796 35.708m35.47 17.241v9.874l-.262-9.874c-4.347-.057-8.414-1.851-11.453-5.072-3.02-3.201-4.655-7.445-4.599-11.928.112-9.132 7.404-16.557 16.491-16.557 8.976.134 16.174 7.762 16.053 17.03-.122 9.122-7.404 16.527-16.23 16.527"/><path d="M2.25 12.938v2.812h2.812l8.294-8.294-2.812-2.812zM15.53 5.28a.747.747 0 0 0 0-1.057L13.777 2.47a.747.747 0 0 0-1.057 0l-1.373 1.373 2.812 2.812z" transform="matrix(24.77711 5.69828 -5.28006 22.9586 275.41 312.585)" style="transform-origin:9px 9px"/>
            </svg>
            <p>Draw Structure</p>
          </button>

          <button type="button" class="flex flex-col duration-200 btn-ghost m-auto rounded-box font-semibold text-primary text-xl md:text-2xl p-3 md:p-8">
            <NuxtLink to="/chemicals/advanced">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-20 md:size-36 mx-auto">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
              </svg>
              <p>Advanced Search</p>
            </NuxtLink>
          </button>
        
          <button type="button" class="flex flex-col duration-200 btn-ghost m-auto rounded-box font-semibold text-primary text-xl md:text-2xl p-3 md:p-8" @click="handleSearchAllChemicals">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-20 md:size-36 mx-auto">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
            </svg>
          
            <p>Browse Data</p>
          </button>

          <button type="button" class="flex flex-col duration-200 btn-ghost m-auto rounded-box font-semibold text-primary text-xl md:text-2xl p-3 md:p-8" @click="openPDF2ChemicalsSubmitModal">
            <svg fill="currentColor" viewBox="0 0 191.119 147.034" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" class="size-20 md:size-36 mx-auto">
              <path d="M66.227 56.696 52.859 43.328a1.98 1.98 0 0 0-1.403-.581H1.985A1.984 1.984 0 0 0 0 44.731v80.218a1.984 1.984 0 0 0 1.985 1.984h62.838a1.984 1.984 0 0 0 1.985-1.984v-66.85c0-.526-.21-1.03-.581-1.403M53.44 49.522l6.593 6.593H53.44ZM3.969 46.716h45.503v2.715H3.969Zm58.87 76.248H3.97V53.4h45.503v4.7a1.984 1.984 0 0 0 1.984 1.984H62.84z"/><path d="M44.678 81.653c-.957-.006-1.899.04-2.83.094q-.513.036-1.02.082a25 25 0 0 1-1.01-1.112c-2.069-2.45-3.74-5.227-5.1-8.113.36-1.395.65-2.85.825-4.362.319-2.759.428-5.903-.606-8.533-.357-.908-1.308-2.013-2.406-1.462-1.263.633-1.618 2.426-1.72 3.697a12.3 12.3 0 0 0 .147 3.067c.176 1.017.459 1.983.767 2.947a44 44 0 0 0 .949 2.631 46 46 0 0 1-.696 2.012c-.57 1.493-1.185 2.911-1.777 4.275l-.917 1.987a67 67 0 0 1-3.126 6.09c-2.689.949-5.102 2.048-7.106 3.34-1.075.695-2.024 1.45-2.815 2.277-.747.78-1.505 1.794-1.572 2.917-.037.633.214 1.248.733 1.623.713.533 1.659.498 2.487.324 2.712-.568 4.794-2.9 6.568-4.864a54 54 0 0 0 4.066-5.15l.01-.015a62 62 0 0 1 8.09-1.906 56 56 0 0 1 4.046-.522c.97.907 2.016 1.734 3.159 2.424.89.548 1.836 1.01 2.827 1.355 1.001.327 2.009.594 3.05.763a9 9 0 0 0 1.611.089c1.226-.046 2.984-.516 3.1-2.003a2.1 2.1 0 0 0-.26-1.204c-.963-1.718-4.294-2.258-5.822-2.5-1.205-.192-2.434-.25-3.652-.248m-19.86 5.476a45 45 0 0 1-1.648 2.392c-1.278 1.738-2.736 3.802-4.848 4.574-.401.146-.93.297-1.486.265-.496-.03-.985-.248-.962-.811.01-.295.155-.671.376-1.04.242-.405.542-.777.867-1.118.695-.731 1.575-1.44 2.587-2.095 1.551-1.007 3.404-1.913 5.469-2.722q-.178.284-.355.555m7.203-22.294a10 10 0 0 1-.086-2.778 6.6 6.6 0 0 1 .275-1.31c.113-.353.358-1.211.748-1.322.643-.182.84 1.199.913 1.59.414 2.22.05 4.69-.448 6.87q-.12.52-.257 1.027a32 32 0 0 1-.436-1.275c-.291-.933-.558-1.876-.71-2.802m4.415 17.537a63 63 0 0 0-6.874 1.51c.26-.073 1.449-2.325 1.714-2.793 1.25-2.2 2.27-4.509 3.005-6.93 1.297 2.563 2.87 5.016 4.803 7.2q.267.297.543.587-1.626.175-3.191.426m16.336 3.094c-.088.477-1.108.75-1.584.826-1.407.22-2.895.044-4.24-.408a13.6 13.6 0 0 1-2.662-1.24 16 16 0 0 1-2.364-1.766c.907-.055 1.826-.09 2.748-.073.923.01 1.853.056 2.772.176 1.723.192 3.653.783 5.009 1.9.267.221.352.416.321.585m-19.5 19.032h-4.393v12.694h4.107q3.17 0 4.92-1.72 1.748-1.718 1.749-4.896 0-2.952-1.663-4.515t-4.72-1.563m2.093 8.974q-.73.907-2.292.907h-.764v-7.111h.998q1.407 0 2.097.842.69.843.69 2.588 0 1.866-.729 2.774m-9.716-7.923q-1.207-1.05-3.612-1.051h-4.393v12.694h3.43v-4.211h.963q2.31 0 3.565-1.16 1.254-1.158 1.254-3.286 0-1.936-1.207-2.986m-2.722 4.202q-.456.434-1.229.434h-.625v-2.917h.886q1.424 0 1.424 1.285 0 .764-.456 1.198m26.505-2.5v-2.753h-7.502v12.694h3.377v-4.767h3.804v-2.752h-3.804v-2.423zm141.107-30.454L177.17 63.43a1.98 1.98 0 0 0-1.403-.581h-49.47a1.984 1.984 0 0 0-1.985 1.984v80.218a1.984 1.984 0 0 0 1.984 1.984h62.839a1.984 1.984 0 0 0 1.984-1.984V78.2c0-.526-.209-1.03-.581-1.403m-12.787-7.174 6.593 6.593h-6.593Zm-49.47-2.806h45.502v2.715H128.28Zm58.87 76.249h-58.87V73.5h45.502v4.7a1.984 1.984 0 0 0 1.984 1.984h11.384z"/><path d="M147.599 106.71q-.08.07-.153.145l.051.013q.053-.077.102-.159m-8.62 6.903a2 2 0 0 0 .12.785 15 15 0 0 1-.063-.74q-.028-.023-.058-.045m33.44 11.752.176.061c.01-.019.05-.056.03-.057-.08-.004-.137-.002-.207-.004"/><path d="M181.353 117.858c-.372-1.574-1.263-2.89-2.508-3.704-2.032-1.33-4.519-.98-6.205.662l-8.798-5.755a6.804 7.71 0 0 0 .231-1.993c0-3.57-2.146-6.58-5.052-7.468V88.089c2.099-.833 3.609-3.099 3.609-5.758 0-3.363-2.416-6.1-5.384-6.1s-5.384 2.737-5.384 6.1c0 2.66 1.51 4.925 3.609 5.758v11.51c-2.906.889-5.052 3.9-5.052 7.47 0 .688.081 1.356.23 1.992l-8.797 5.755c-1.686-1.642-4.173-1.991-6.205-.662-1.245.815-2.136 2.13-2.508 3.704s-.181 3.218.538 4.629 1.88 2.42 3.268 2.842a5.422 6.143 0 0 0 1.403.21 4.9 4.9 0 0 0 2.683-.82c1.245-.814 2.136-2.13 2.508-3.703a6.9 6.9 0 0 0 .09-2.718l8.799-5.755a6.825 7.733 0 0 0 3.043 1.994v11.51c-2.099.834-3.609 3.1-3.609 5.758 0 3.363 2.415 6.1 5.384 6.1s5.384-2.737 5.384-6.1c0-2.66-1.51-4.925-3.61-5.758v-11.51a6.83 7.738 0 0 0 3.044-1.995l8.798 5.756c-.15.89-.122 1.815.091 2.717.372 1.574 1.263 2.89 2.508 3.704.83.543 1.75.82 2.683.82.468 0 .939-.07 1.403-.21 1.388-.423 2.55-1.432 3.268-2.843a6.77 6.77 0 0 0 .538-4.628m-42.097 3.378a1.822 2.065 0 0 1-1.392.207 1.822 2.065 0 0 1-1.113-.968 1.822 2.065 0 0 1-.183-1.576 1.821 2.063 0 0 1 .854-1.262 1.823 2.066 0 0 1 .914-.278c.634 0 1.251.373 1.59 1.039.506.992.205 2.265-.67 2.838m16.156-38.905c0-1.145.823-2.077 1.834-2.077s1.834.932 1.834 2.077-.823 2.078-1.834 2.078-1.834-.932-1.834-2.078m3.668 49.474c0 1.145-.823 2.078-1.834 2.078s-1.834-.933-1.834-2.078.823-2.078 1.834-2.078 1.834.932 1.834 2.078m-1.834-21.024c-1.807 0-3.277-1.665-3.277-3.713s1.47-3.713 3.277-3.713 3.277 1.666 3.277 3.713-1.47 3.713-3.277 3.713m20.495 9.694a1.822 2.065 0 0 1-1.113.968 1.821 2.063 0 0 1-1.392-.207c-.875-.573-1.177-1.846-.67-2.838.338-.666.956-1.039 1.59-1.039.311 0 .626.09.914.278a1.822 2.065 0 0 1 .854 1.262 1.822 2.065 0 0 1-.183 1.576m-75.745-13.974c-.03.008-.06.013-.088.024a.9.9 0 0 0-.316.179q.157-.013.313-.036a.6.6 0 0 0 .09-.167m2.149.657q-.106.129-.22.251c.067.06.143.112.22.162zm-.638-7.383a.8.8 0 0 0-.327.133l.196.027c.095-.03.323.002.285-.09-.022-.053-.078-.076-.154-.07m.222-4.592q.212.058.416.137v-.133q-.207.003-.416-.004M78.3 107.539l-.031.04a2 2 0 0 0 .193-.011zm21.723 21.26q-.134.505-.31 1.386-.177.881-.236 1.47-.05-.815-.57-2.889l-1.672-6.223h-3.728l4.005 12.277h3.905l4.022-12.277h-3.711z"/><path d="m121.753 76.732-13.368-13.369a1.98 1.98 0 0 0-1.403-.58H57.51a1.984 1.984 0 0 0-1.985 1.984v80.217a1.984 1.984 0 0 0 1.985 1.984h62.839a1.984 1.984 0 0 0 1.984-1.984v-66.85c0-.526-.21-1.03-.581-1.402m-12.787-7.175 6.593 6.593h-6.593Zm-49.47-2.806h45.501v2.715H59.495Zm0 76.249V73.435h45.501v4.7a1.984 1.984 0 0 0 1.985 1.984h11.383v62.88z"/><path d="M79.214 125.087q.782 0 1.462.218a11 11 0 0 1 1.36.537l1.016-2.611q-1.813-.865-3.804-.865-1.822 0-3.17.777-1.348.776-2.066 2.22t-.718 3.351q0 3.049 1.482 4.66 1.483 1.613 4.262 1.613 1.94 0 3.477-.68v-2.805a16 16 0 0 1-1.537.546 5.5 5.5 0 0 1-1.579.227q-2.696 0-2.695-3.544 0-1.705.663-2.675.664-.97 1.847-.97m10.9 2.41q-1.654-.755-2.028-1.04-.373-.286-.373-.647 0-.336.294-.563.293-.226.94-.226 1.251 0 2.972.79l1.017-2.562q-1.982-.882-3.888-.882-2.159 0-3.393.949-1.234.95-1.234 2.645 0 .907.29 1.57t.89 1.176 1.801 1.058q1.327.596 1.633.79.307.192.446.381t.138.441q0 .403-.344.66-.345.256-1.084.256-.856 0-1.88-.273a10 10 0 0 1-1.974-.76v2.956q.899.428 1.73.6t2.057.172q1.47 0 2.561-.491t1.671-1.377.58-2.028q0-1.243-.617-2.062t-2.205-1.532m-.454-49.805-14.09 8.66v17.319l14.09 8.66 14.091-8.66V86.35Zm0 32.056-11.988-7.368V87.643l11.989-7.369 11.99 7.369v14.737z"/><path d="M89.66 85.002c-5.184 0-9.402 4.49-9.402 10.01s4.218 10.009 9.403 10.009 9.403-4.49 9.403-10.01-4.218-10.01-9.403-10.01m0 17.783c-4.027 0-7.302-3.487-7.302-7.773s3.275-7.773 7.302-7.773 7.302 3.487 7.302 7.773-3.275 7.773-7.302 7.773"/><path d="M477.694 262.331C450.839 157.565 355.775 80.137 242.645 80.137 108.637 80.137 0 188.766 0 322.782l117.984-8.92c-2.226-51.185 37.105-113.516 57.879-123.169-28.193-3.702-60.104-2.114-60.104-2.114 21.476-8.346 45.081-12.968 69.863-12.968 90.637 0 165.581 61.775 177.733 142.025l-57.637 25.177 166.21 89.048 40.072-187z"  transform="matrix(.19767 .01855 -.0253 .15386 37.9 -16.556)"/><path style="stroke-width:.475411" d="M127.434 68.685v-2.803h48.696v5.606h-48.696z" transform="translate(-.538 -.707)"/><path style="stroke-width:.36591" d="M65.313 68.854v-1.657h40.717v3.314H65.313Z" transform="translate(-.538 -.707)"/><path style="stroke-width:.713591" d="M58.382 68.98v-3.038h6.705v6.076h-6.705Z" transform="translate(-.538 -.707)"/><path style="stroke-width:.497812" d="M2.675 48.758v-3.002H52.22v6.002H2.675Z" transform="translate(-.538 -.707)"/>
            </svg>
            <p>PDF2Chemicals</p>
          </button>
        </div>
      </div>
    </section>
    
    <div class="gap-y-8 w-[95%] grid grid-cols-1 container mx-auto">

      <div class="space-y-4">
        <p class="text-2xl font-semibold">Recent Tasks</p>
        <!-- Recent Tasks Table -->
        <div class="overflow-x-auto rounded-box shadow-lg">
          <table class="ml-auto table table-auto table-zebra table-pin-rows">
            <!-- head -->
            <thead class="text-sm md:text-lg">
              <tr>
                <th>ID</th>
                <th>Description</th>
                <th>Created At</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody class="text-sm md:text-lg font-normal">
              <tr class="hover">
                <td>T121</td>
                <td>Extracting chemicals from 'paper.pdf'</td>
                <td>2024-11-12, 02:15 PM</td>
                <td :class="themeStore.isDarkMode ? 'text-warning' : 'text-amber-500'">In Progress</td>
                <td>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                  </svg>
                
                </td>
              </tr>
              <tr class="hover">
                <td>T218</td>
                <td>Uploading chemicals to LabSOADB</td>
                <td>2026-10-10, 01:12 AM</td>
                <td :class="themeStore.isDarkMode ? 'text-success' : 'text-green-500'">Concluded</td>
                <td>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                  </svg>
                
                </td>
              </tr>
              <tr class="hover">
                <td>T223</td>
                <td>Extracting chemicals from 'academic15.pdf'</td>
                <td>2023-01-10, 09:27 PM</td>
                <td :class="themeStore.isDarkMode ? 'text-error' : 'text-rose-500'">Failed</td>
                <td>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                  </svg>
                
                </td>
              </tr>
            </tbody>
          </table>
          
        </div>
      </div>
      <div class="space-y-4">
        <p class="text-2xl font-semibold">Recent Uploaded Chemicals</p>
        <!-- Recent Uploaded Chemicals Table -->
        <div class="overflow-x-auto rounded-box shadow-lg">
          <table class="ml-auto table table-auto table-zebra table-pin-rows">
            <!-- head -->
            <thead class="text-sm md:text-lg">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Formula</th>
                <th>Reference</th>
                <th>Created At</th>
                <th></th>
              </tr>
            </thead>
            <tbody class="text-sm md:text-lg font-normal">
              <tr class="hover">
                <td>LSOA54875455</td>
                <td>
                  <div class="md:max-w-xs max-w-full whitespace-normal break-words lg:tooltip lg:tooltip-up" :data-tip="iupac">
                    <span>Methyl benzyl((4-chlorophenyl)...</span>
                  </div>
                  
                </td>
                <td>C26H22N4O6</td>
                <td class="md:max-w-xs max-w-full whitespace-normal break-words">
                  <a 
                    href="https://www.doi.org/10.2174/1568026618666181002110116" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="link-lg link-sm"
                  >
                  10.2174/1568026618666181002110116
                  </a>
                  
                </td>
                <td>2024-05-01, 15:07 PM</td>
                <td>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8 mx-auto">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                  </svg>
                </td>
              </tr>
            </tbody>
          </table>
          
        </div>
      </div>
    </div>
  </div>
  <modal ref="ketcherModalRef">
    <ketcher-component></ketcher-component>
  </modal>
  <modal ref="pdf2ChemicalsSubmitRef">
    <PDF2ChemicalsSubmitComponent></PDF2ChemicalsSubmitComponent>
  </modal>
</template>

<script setup>
import Modal from '~/components/Modal.vue';
import { useThemeStore } from '~/stores/theme';
import { defineAsyncComponent } from 'vue';

const KetcherComponent = defineAsyncComponent({
  loader: () => import('~/components/KetcherComponent.vue')
});

const PDF2ChemicalsSubmitComponent = defineAsyncComponent({
  loader: () => import('~/components/PDF2ChemicalsSubmitComponent.vue')
})

const themeStore = useThemeStore()

const iupac = "Methyl benzyl((4-chlorophenyl)(3-((methoxycarbonyl)oxy)-1,4-dioxo-1,4-dihydronaph thalen-2-yl)methyl)carbamate"
const smiles = 'C(C1=CC=CC=C1)N(C(OC)=O)C(C=1C(C2=CC=CC=C2C(C1OC(=O)OC)=O)=O)C1=CC=C(C=C1)Cl'

var ketcherModalRef =  ref(null)

const openKetcherModal = () => {
  if(ketcherModalRef.value) {
    ketcherModalRef.value.toggleComponentModal();
  }
}

var pdf2ChemicalsSubmitRef = ref(null)

const openPDF2ChemicalsSubmitModal = () => {
  if(pdf2ChemicalsSubmitRef.value) {
    pdf2ChemicalsSubmitRef.value.toggleComponentModal()
  }
}

definePageMeta({
  middleware: 'auth'
});
</script>

<style scoped>
.dashboard-buttons-background-dark {
  background-image: url('~/assets/dashboard_buttons_background_dark.webp');
}

.dashboard-buttons-background-light {
  background-image: url('~/assets/dashboard_buttons_background_light.webp');
}

.link-sm {
  @apply link link-secondary;
}

.link-lg {
  @apply lg:link-primary duration-200 lg:hover:text-secondary;
}
</style>