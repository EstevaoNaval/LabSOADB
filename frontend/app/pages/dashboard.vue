<template>
  <main class="min-h-screen bg-base-200">
    <!-- Hero Section with Stats -->
    <section class="relative bg-gradient-to-br from-primary/10 via-base-100 to-secondary/10">
      <div class="container mx-auto px-4 py-12">
        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-3">
            Welcome Back, <b>{{ userStore.user.first_name }}</b>!
          </h1>
          <p class="text-base-content/70 text-lg">
            Here's an overview of your chemical analysis tasks
          </p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
          <!-- Successful Tasks -->
          <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 border border-success/20">
            <div class="card-body items-center text-center p-6">
              <div class="w-16 h-16 rounded-full bg-success/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                  stroke="currentColor" class="w-8 h-8 text-success">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                </svg>
              </div>
              <h3 class="text-sm font-medium text-base-content/70 mb-1">Successful Tasks</h3>
              <p class="text-3xl font-bold text-success">{{ totalSuccessfulTasks }}</p>
            </div>
          </div>

          <!-- Pending Tasks -->
          <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 border border-warning/20">
            <div class="card-body items-center text-center p-6">
              <div class="w-16 h-16 rounded-full bg-warning/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                  stroke="currentColor" class="w-8 h-8 text-warning">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                </svg>
              </div>
              <h3 class="text-sm font-medium text-base-content/70 mb-1">Pending Tasks</h3>
              <p class="text-3xl font-bold text-warning">{{ totalPendingTasks }}</p>
            </div>
          </div>

          <!-- Failed Tasks -->
          <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 border border-error/20">
            <div class="card-body items-center text-center p-6">
              <div class="w-16 h-16 rounded-full bg-error/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                  stroke="currentColor" class="w-8 h-8 text-error">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </div>
              <h3 class="text-sm font-medium text-base-content/70 mb-1">Failed Tasks</h3>
              <p class="text-3xl font-bold text-error">{{ totalFailedTasks }}</p>
            </div>
          </div>

          <!-- User Chemicals -->
          <div class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 border border-info/20">
            <div class="card-body items-center text-center p-6">
              <div class="w-16 h-16 rounded-full bg-info/10 flex items-center justify-center mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor"
                  class="w-8 h-8 text-info">
                  <path
                    d="M256 0 34.297 128v255.999l221.702 128 221.702-128V128zm0 473.828L67.355 364.914V147.085L256 38.171l188.644 108.914v217.829h.001z" />
                  <path
                    d="M256 108.044c-81.583 0-147.956 66.372-147.956 147.956S174.416 403.957 256 403.957 403.958 337.585 403.958 256 337.583 108.044 256 108.044m0 262.854c-63.356 0-114.898-51.544-114.898-114.899S192.644 141.101 256 141.101s114.899 51.543 114.899 114.898S319.357 370.898 256 370.898" />
                </svg>
              </div>
              <h3 class="text-sm font-medium text-base-content/70 mb-1">User Chemicals</h3>
              <p class="text-3xl font-bold text-info">{{ userChemicalsStore.totalChemicals }}</p>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card bg-base-100 shadow-lg">
          <div class="card-body p-4 md:p-6">
            <h2 class="card-title text-xl mb-4">Quick Actions</h2>
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <!-- Draw Structure -->
              <button @click="openKetcherModal()" type="button"
                class="group btn btn-ghost bg-base-100/50 hover:bg-base-100 border border-base-300 hover:border-primary/50 hidden md:flex md:flex-col items-center justify-center gap-3 p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
                aria-label="Draw Chemical Structure">
                <div
                  class="w-10 h-10 md:w-12 md:h-12 flex items-center justify-center text-primary group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-full h-full">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>

                </div>
                <span class="font-semibold text-sm md:text-base lg:text-lg text-center">Draw Structure</span>
              </button>

              <NuxtLink to="/chemicals/search/advanced"
                class="group btn btn-ghost bg-base-100/50 hover:bg-base-100 border border-base-300 hover:border-primary/50 flex flex-col items-center justify-center gap-3 p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
                aria-label="Advanced Search">
                <div
                  class="w-10 h-10 md:w-12 md:h-12 flex items-center justify-center text-primary group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-full h-full">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
                  </svg>
                </div>
                <span class="font-semibold text-sm md:text-base lg:text-lg text-center">Advanced Search</span>
              </NuxtLink>

              <button type="button"
                class="group btn btn-ghost bg-base-100/50 hover:bg-base-100 border border-base-300 hover:border-primary/50 flex flex-col items-center justify-center gap-3 p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
                @click="handleSearchAllChemicals" aria-label="Browse All Data">
                <div
                  class="w-10 h-10 md:w-12 md:h-12 flex items-center justify-center text-primary group-hover:scale-110 transition-transform duration-300">

                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-full h-full">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                  </svg>
                </div>
                <span class="font-semibold text-sm md:text-base lg:text-lg text-center">Browse Data</span>
              </button>

              <button type="button"
                class="group btn btn-ghost bg-base-100/50 hover:bg-base-100 border border-base-300 hover:border-primary/50 flex flex-col items-center justify-center gap-3 p-4 md:p-6 h-auto transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
                @click="openPDF2ChemicalsSubmitModal" aria-label="Submit PDF for Chemical Extraction">
                <div
                  class="w-10 h-10 md:w-12 md:h-12 flex items-center justify-center text-primary group-hover:scale-110 transition-transform duration-300">

                  <svg fill="currentColor" viewBox="0 0 191.119 147.034" xml:space="preserve"
                    xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
                    <path
                      d="M66.227 56.696 52.859 43.328a1.98 1.98 0 0 0-1.403-.581H1.985A1.984 1.984 0 0 0 0 44.731v80.218a1.984 1.984 0 0 0 1.985 1.984h62.838a1.984 1.984 0 0 0 1.985-1.984v-66.85c0-.526-.21-1.03-.581-1.403M53.44 49.522l6.593 6.593H53.44ZM3.969 46.716h45.503v2.715H3.969Zm58.87 76.248H3.97V53.4h45.503v4.7a1.984 1.984 0 0 0 1.984 1.984H62.84z" />
                    <path
                      d="M44.678 81.653c-.957-.006-1.899.04-2.83.094q-.513.036-1.02.082a25 25 0 0 1-1.01-1.112c-2.069-2.45-3.74-5.227-5.1-8.113.36-1.395.65-2.85.825-4.362.319-2.759.428-5.903-.606-8.533-.357-.908-1.308-2.013-2.406-1.462-1.263.633-1.618 2.426-1.72 3.697a12.3 12.3 0 0 0 .147 3.067c.176 1.017.459 1.983.767 2.947a44 44 0 0 0 .949 2.631 46 46 0 0 1-.696 2.012c-.57 1.493-1.185 2.911-1.777 4.275l-.917 1.987a67 67 0 0 1-3.126 6.09c-2.689.949-5.102 2.048-7.106 3.34-1.075.695-2.024 1.45-2.815 2.277-.747.78-1.505 1.794-1.572 2.917-.037.633.214 1.248.733 1.623.713.533 1.659.498 2.487.324 2.712-.568 4.794-2.9 6.568-4.864a54 54 0 0 0 4.066-5.15l.01-.015a62 62 0 0 1 8.09-1.906 56 56 0 0 1 4.046-.522c.97.907 2.016 1.734 3.159 2.424.89.548 1.836 1.01 2.827 1.355 1.001.327 2.009.594 3.05.763a9 9 0 0 0 1.611.089c1.226-.046 2.984-.516 3.1-2.003a2.1 2.1 0 0 0-.26-1.204c-.963-1.718-4.294-2.258-5.822-2.5-1.205-.192-2.434-.25-3.652-.248m-19.86 5.476a45 45 0 0 1-1.648 2.392c-1.278 1.738-2.736 3.802-4.848 4.574-.401.146-.93.297-1.486.265-.496-.03-.985-.248-.962-.811.01-.295.155-.671.376-1.04.242-.405.542-.777.867-1.118.695-.731 1.575-1.44 2.587-2.095 1.551-1.007 3.404-1.913 5.469-2.722q-.178.284-.355.555m7.203-22.294a10 10 0 0 1-.086-2.778 6.6 6.6 0 0 1 .275-1.31c.113-.353.358-1.211.748-1.322.643-.182.84 1.199.913 1.59.414 2.22.05 4.69-.448 6.87q-.12.52-.257 1.027a32 32 0 0 1-.436-1.275c-.291-.933-.558-1.876-.71-2.802m4.415 17.537a63 63 0 0 0-6.874 1.51c.26-.073 1.449-2.325 1.714-2.793 1.25-2.2 2.27-4.509 3.005-6.93 1.297 2.563 2.87 5.016 4.803 7.2q.267.297.543.587-1.626.175-3.191.426m16.336 3.094c-.088.477-1.108.75-1.584.826-1.407.22-2.895.044-4.24-.408a13.6 13.6 0 0 1-2.662-1.24 16 16 0 0 1-2.364-1.766c.907-.055 1.826-.09 2.748-.073.923.01 1.853.056 2.772.176 1.723.192 3.653.783 5.009 1.9.267.221.352.416.321.585m-19.5 19.032h-4.393v12.694h4.107q3.17 0 4.92-1.72 1.748-1.718 1.749-4.896 0-2.952-1.663-4.515t-4.72-1.563m2.093 8.974q-.73.907-2.292.907h-.764v-7.111h.998q1.407 0 2.097.842.69.843.69 2.588 0 1.866-.729 2.774m-9.716-7.923q-1.207-1.05-3.612-1.051h-4.393v12.694h3.43v-4.211h.963q2.31 0 3.565-1.16 1.254-1.158 1.254-3.286 0-1.936-1.207-2.986m-2.722 4.202q-.456.434-1.229.434h-.625v-2.917h.886q1.424 0 1.424 1.285 0 .764-.456 1.198m26.505-2.5v-2.753h-7.502v12.694h3.377v-4.767h3.804v-2.752h-3.804v-2.423zm141.107-30.454L177.17 63.43a1.98 1.98 0 0 0-1.403-.581h-49.47a1.984 1.984 0 0 0-1.985 1.984v80.218a1.984 1.984 0 0 0 1.984 1.984h62.839a1.984 1.984 0 0 0 1.984-1.984V78.2c0-.526-.209-1.03-.581-1.403m-12.787-7.174 6.593 6.593h-6.593Zm-49.47-2.806h45.502v2.715H128.28Zm58.87 76.249h-58.87V73.5h45.502v4.7a1.984 1.984 0 0 0 1.984 1.984h11.384z" />
                    <path
                      d="M147.599 106.71q-.08.07-.153.145l.051.013q.053-.077.102-.159m-8.62 6.903a2 2 0 0 0 .12.785 15 15 0 0 1-.063-.74q-.028-.023-.058-.045m33.44 11.752.176.061c.01-.019.05-.056.03-.057-.08-.004-.137-.002-.207-.004" />
                    <path
                      d="M181.353 117.858c-.372-1.574-1.263-2.89-2.508-3.704-2.032-1.33-4.519-.98-6.205.662l-8.798-5.755a6.804 7.71 0 0 0 .231-1.993c0-3.57-2.146-6.58-5.052-7.468V88.089c2.099-.833 3.609-3.099 3.609-5.758 0-3.363-2.416-6.1-5.384-6.1s-5.384 2.737-5.384 6.1c0 2.66 1.51 4.925 3.609 5.758v11.51c-2.906.889-5.052 3.9-5.052 7.47 0 .688.081 1.356.23 1.992l-8.797 5.755c-1.686-1.642-4.173-1.991-6.205-.662-1.245.815-2.136 2.13-2.508 3.704s-.181 3.218.538 4.629 1.88 2.42 3.268 2.842a5.422 6.143 0 0 0 1.403.21 4.9 4.9 0 0 0 2.683-.82c1.245-.814 2.136-2.13 2.508-3.703a6.9 6.9 0 0 0 .09-2.718l8.799-5.755a6.825 7.733 0 0 0 3.043 1.994v11.51c-2.099.834-3.609 3.1-3.609 5.758 0 3.363 2.415 6.1 5.384 6.1s5.384-2.737 5.384-6.1c0-2.66-1.51-4.925-3.61-5.758v-11.51a6.83 7.738 0 0 0 3.044-1.995l8.798 5.756c-.15.89-.122 1.815.091 2.717.372 1.574 1.263 2.89 2.508 3.704.83.543 1.75.82 2.683.82.468 0 .939-.07 1.403-.21 1.388-.423 2.55-1.432 3.268-2.843a6.77 6.77 0 0 0 .538-4.628m-42.097 3.378a1.822 2.065 0 0 1-1.392.207 1.822 2.065 0 0 1-1.113-.968 1.822 2.065 0 0 1-.183-1.576 1.821 2.063 0 0 1 .854-1.262 1.823 2.066 0 0 1 .914-.278c.634 0 1.251.373 1.59 1.039.506.992.205 2.265-.67 2.838m16.156-38.905c0-1.145.823-2.077 1.834-2.077s1.834.932 1.834 2.077-.823 2.078-1.834 2.078-1.834-.932-1.834-2.078m3.668 49.474c0 1.145-.823 2.078-1.834 2.078s-1.834-.933-1.834-2.078.823-2.078 1.834-2.078 1.834.932 1.834 2.078m-1.834-21.024c-1.807 0-3.277-1.665-3.277-3.713s1.47-3.713 3.277-3.713 3.277 1.666 3.277 3.713-1.47 3.713-3.277 3.713m20.495 9.694a1.822 2.065 0 0 1-1.113.968 1.821 2.063 0 0 1-1.392-.207c-.875-.573-1.177-1.846-.67-2.838.338-.666.956-1.039 1.59-1.039.311 0 .626.09.914.278a1.822 2.065 0 0 1 .854 1.262 1.822 2.065 0 0 1-.183 1.576m-75.745-13.974c-.03.008-.06.013-.088.024a.9.9 0 0 0-.316.179q.157-.013.313-.036a.6.6 0 0 0 .09-.167m2.149.657q-.106.129-.22.251c.067.06.143.112.22.162zm-.638-7.383a.8.8 0 0 0-.327.133l.196.027c.095-.03.323.002.285-.09-.022-.053-.078-.076-.154-.07m.222-4.592q.212.058.416.137v-.133q-.207.003-.416-.004M78.3 107.539l-.031.04a2 2 0 0 0 .193-.011zm21.723 21.26q-.134.505-.31 1.386-.177.881-.236 1.47-.05-.815-.57-2.889l-1.672-6.223h-3.728l4.005 12.277h3.905l4.022-12.277h-3.711z" />
                    <path
                      d="m121.753 76.732-13.368-13.369a1.98 1.98 0 0 0-1.403-.58H57.51a1.984 1.984 0 0 0-1.985 1.984v80.217a1.984 1.984 0 0 0 1.985 1.984h62.839a1.984 1.984 0 0 0 1.984-1.984v-66.85c0-.526-.21-1.03-.581-1.402m-12.787-7.175 6.593 6.593h-6.593Zm-49.47-2.806h45.501v2.715H59.495Zm0 76.249V73.435h45.501v4.7a1.984 1.984 0 0 0 1.985 1.984h11.383v62.88z" />
                    <path
                      d="M79.214 125.087q.782 0 1.462.218a11 11 0 0 1 1.36.537l1.016-2.611q-1.813-.865-3.804-.865-1.822 0-3.17.777-1.348.776-2.066 2.22t-.718 3.351q0 3.049 1.482 4.66 1.483 1.613 4.262 1.613 1.94 0 3.477-.68v-2.805a16 16 0 0 1-1.537.546 5.5 5.5 0 0 1-1.579.227q-2.696 0-2.695-3.544 0-1.705.663-2.675.664-.97 1.847-.97m10.9 2.41q-1.654-.755-2.028-1.04-.373-.286-.373-.647 0-.336.294-.563.293-.226.94-.226 1.251 0 2.972.79l1.017-2.562q-1.982-.882-3.888-.882-2.159 0-3.393.949-1.234.95-1.234 2.645 0 .907.29 1.57t.89 1.176 1.801 1.058q1.327.596 1.633.79.307.192.446.381t.138.441q0 .403-.344.66-.345.256-1.084.256-.856 0-1.88-.273a10 10 0 0 1-1.974-.76v2.956q.899.428 1.73.6t2.057.172q1.47 0 2.561-.491t1.671-1.377.58-2.028q0-1.243-.617-2.062t-2.205-1.532m-.454-49.805-14.09 8.66v17.319l14.09 8.66 14.091-8.66V86.35Zm0 32.056-11.988-7.368V87.643l11.989-7.369 11.99 7.369v14.737z" />
                    <path
                      d="M89.66 85.002c-5.184 0-9.402 4.49-9.402 10.01s4.218 10.009 9.403 10.009 9.403-4.49 9.403-10.01-4.218-10.01-9.403-10.01m0 17.783c-4.027 0-7.302-3.487-7.302-7.773s3.275-7.773 7.302-7.773 7.302 3.487 7.302 7.773-3.275 7.773-7.302 7.773" />
                    <path
                      d="M477.694 262.331C450.839 157.565 355.775 80.137 242.645 80.137 108.637 80.137 0 188.766 0 322.782l117.984-8.92c-2.226-51.185 37.105-113.516 57.879-123.169-28.193-3.702-60.104-2.114-60.104-2.114 21.476-8.346 45.081-12.968 69.863-12.968 90.637 0 165.581 61.775 177.733 142.025l-57.637 25.177 166.21 89.048 40.072-187z"
                      transform="matrix(.19767 .01855 -.0253 .15386 37.9 -16.556)" />
                    <path style="stroke-width:.475411" d="M127.434 68.685v-2.803h48.696v5.606h-48.696z"
                      transform="translate(-.538 -.707)" />
                    <path style="stroke-width:.36591" d="M65.313 68.854v-1.657h40.717v3.314H65.313Z"
                      transform="translate(-.538 -.707)" />
                    <path style="stroke-width:.713591" d="M58.382 68.98v-3.038h6.705v6.076h-6.705Z"
                      transform="translate(-.538 -.707)" />
                    <path style="stroke-width:.497812" d="M2.675 48.758v-3.002H52.22v6.002H2.675Z"
                      transform="translate(-.538 -.707)" />
                  </svg>
                </div>
                <span class="font-semibold text-sm md:text-base lg:text-lg text-center">PDF2Chemicals</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content Sections -->
    <div class="container mx-auto px-4 py-12 space-y-12">
      <!-- User Tasks Section -->
      <section class="space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl md:text-3xl font-bold">User Tasks</h2>
          <div class="badge badge-lg badge-neutral">
            {{ userTaskPagination.state.totalItems }} total
          </div>
        </div>

        <!-- Pagination Top -->
        <PaginationControls v-if="userTaskPagination.state.totalItems > 0 && userTaskPagination.getTotalPages() > 1"
          :pagination="userTaskPagination" />

        <!-- Table -->
        <div class="card bg-base-100 shadow-xl overflow-x-auto">
          <user-tasks-table />
        </div>

        <!-- Pagination Bottom -->
        <PaginationControls v-if="userTaskPagination.state.totalItems > 0 && userTaskPagination.getTotalPages() > 1"
          :pagination="userTaskPagination" />
      </section>

      <!-- User Chemicals Section -->
      <section class="space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl md:text-3xl font-bold">User Chemicals</h2>
          <div class="badge badge-lg badge-neutral">
            {{ userChemicalsPagination.state.totalItems }} total
          </div>
        </div>

        <!-- Pagination Top -->
        <PaginationControls
          v-if="userChemicalsPagination.state.totalItems > 0 && userChemicalsPagination.getTotalPages() > 1"
          :pagination="userChemicalsPagination" />

        <!-- Table -->
        <div class="card bg-base-100 shadow-xl overflow-x-auto">
          <user-chemicals-table />
        </div>

        <!-- Pagination Bottom -->
        <PaginationControls
          v-if="userChemicalsPagination.state.totalItems > 0 && userChemicalsPagination.getTotalPages() > 1"
          :pagination="userChemicalsPagination" />
      </section>
    </div>

    <!-- Modals -->
    <modal ref="ketcherModalRef">
      <ketcher-component />
    </modal>
    <modal ref="pdf2ChemicalsSubmitRef">
      <PDF2ChemicalsSubmitComponent />
    </modal>
  </main>
</template>

<script setup>
import Modal from '~/components/Modal.vue'
import UserTasksTable from '~/components/UserTasksTable.vue'
import UserChemicalsTable from '~/components/UserChemicalsTable.vue'
import PaginationControls from '~/components/PaginationControls.vue'

import { useRouter } from 'nuxt/app'
import { defineAsyncComponent, watch } from 'vue'
import { useUserChemicalsStore } from '~/stores/userChemicals'
import { useUserTasksStore } from '~/stores/userTasks'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { usePagination } from '~/composables/usePagination'
import { useFilterStore } from '~/stores/filterStore'
import { useHistogramRangeSliderStore } from '~/stores/histogramRangeSliderStore'
import { useSortStore } from '~/stores/sortingStore'
import { useUserStore } from '~/stores/user'

const KetcherComponent = defineAsyncComponent({
  loader: () => import('~/components/KetcherComponent.vue')
})

const PDF2ChemicalsSubmitComponent = defineAsyncComponent({
  loader: () => import('~/components/PDF2ChemicalsSubmitComponent.vue')
})


const router = useRouter()

// Stores
const userChemicalsStore = useUserChemicalsStore()
const userTasksStore = useUserTasksStore()
const fetchChemicalStore = useFetchChemicalStore()
const filterStore = useFilterStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()
const sortStore = useSortStore()
const userStore = useUserStore()

// Composables
const userTaskPagination = usePagination()
const userChemicalsPagination = usePagination()

// Data
const totalSuccessfulTasks = ref(0)
const totalPendingTasks = ref(0)
const totalFailedTasks = ref(0)
const isLoading = ref(true)

// Refs
const ketcherModalRef = ref(null)
const pdf2ChemicalsSubmitRef = ref(null)

// Functions
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

const handleSearchAllChemicals = () => {
  histogramRangeSliderStore.$reset()
  filterStore.$reset()
  fetchChemicalStore.$reset()
  sortStore.$reset()

  fetchChemicalStore.setType('all')
  fetchChemicalStore.setMode('summary')
  fetchChemicalStore.fetchChemicals()

  router.push('/chemicals/search')
}

async function fetchUserTasks(page) {
  userTaskPagination.setPage(page)
  await userTasksStore.fetchTasksPerUser({ page })
  userTaskPagination.setTotalItems(userTasksStore.totalTasks)
}

async function fetchUserChemicals(page) {
  userChemicalsPagination.setPage(page)
  await userChemicalsStore.fetchChemicalsPerUser({ page })
  userChemicalsPagination.setTotalItems(userChemicalsStore.totalChemicals)
}

async function loadDashboardData() {
  isLoading.value = true
  try {
    // Fetch stats
    totalSuccessfulTasks.value = await userTasksStore.getTotalSuccessfulTasks()
    totalPendingTasks.value = await userTasksStore.getTotalPendingTasks()
    totalFailedTasks.value = await userTasksStore.getTotalFailedTasks()

    // Fetch initial data
    await Promise.all([
      fetchUserTasks(1),
      fetchUserChemicals(1)
    ])
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

// Watches
watch(() => userTaskPagination.state.page, (newPage) => {
  fetchUserTasks(newPage)
})

watch(() => userChemicalsPagination.state.page, (newPage) => {
  fetchUserChemicals(newPage)
})

// Lifecycle
onBeforeMount(() => {
  loadDashboardData()
})

definePageMeta({
  middleware: 'auth'
})
</script>