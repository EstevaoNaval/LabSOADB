<template>
  <main>
    <header>
      <Title>Home | LabSOADB</Title>
    </header>

    <!-- Hero Section -->
    <section class="search_bar_background bg-scroll bg-cover bg-center relative">
      <div class="absolute inset-0 bg-gradient-to-b from-base-300/90 via-base-300/85 to-base-300/90"></div>

      <div class="relative z-10 container mx-auto px-4 py-16 md:py-24 lg:py-32">
        <!-- Hero Text -->
        <div class="max-w-4xl mx-auto text-center mb-12 space-y-6">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-primary leading-tight">
            Explore LabSOADB
          </h1>
          <p class="text-lg md:text-xl lg:text-2xl text-base-content/90 font-medium max-w-3xl mx-auto">
            Discover chemical data mined from literature using cutting-edge machine learning and AI technology
          </p>
        </div>

        <!-- Search Field -->
        <div class="max-w-4xl mx-auto mb-12">
          <search-field :typewriterEffect='true'></search-field>
        </div>

        <!-- Action Buttons Grid -->
        <div class="max-w-5xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
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

          <NuxtLink to="/chemicals/advanced"
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
    </section>

    <!-- Features Section -->
    <section class="py-16 md:py-20 lg:py-24 bg-base-100">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12 md:mb-16 space-y-4">
          <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold text-primary">
            Why LabSOADB?
          </h2>
          <p class="text-base md:text-lg lg:text-xl text-base-content/70 max-w-3xl mx-auto">
            An AI-powered database that extracts chemical data from literature, providing accurate, up-to-date
            information for researchers and chemists.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-6xl mx-auto">
          <div
            class="card bg-base-200 hover:bg-base-300 shadow-lg hover:shadow-xl transition-all duration-300 border border-base-300">
            <div class="card-body p-6 md:p-8 space-y-4">
              <div class="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-8 h-8 text-primary">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                </svg>
              </div>
              <h3 class="text-xl md:text-2xl font-bold text-base-content">
                AI-Driven Data Mining
              </h3>
              <p class="text-base text-base-content/70 leading-relaxed">
                Automatically extracts properties, structures, and references from scientific papers using machine
                learning.
              </p>
            </div>
          </div>

          <div
            class="card bg-base-200 hover:bg-base-300 shadow-lg hover:shadow-xl transition-all duration-300 border border-base-300">
            <div class="card-body p-6 md:p-8 space-y-4">
              <div class="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-8 h-8 text-primary">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75m-16.5-3.75v3.75m16.5 0v3.75C20.25 16.153 16.556 18 12 18s-8.25-1.847-8.25-4.125v-3.75m16.5 0c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125" />
                </svg>
              </div>
              <h3 class="text-xl md:text-2xl font-bold text-base-content">
                Comprehensive Database
              </h3>
              <p class="text-base text-base-content/70 leading-relaxed">
                Access hundreds of chemicals with detailed identifiers, properties, and 3D conformations.
              </p>
            </div>
          </div>

          <div
            class="card bg-base-200 hover:bg-base-300 shadow-lg hover:shadow-xl transition-all duration-300 border border-base-300">
            <div class="card-body p-6 md:p-8 space-y-4">
              <div class="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-8 h-8 text-primary">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0021 18V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v12a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </div>
              <h3 class="text-xl md:text-2xl font-bold text-base-content">
                User-Friendly Tools
              </h3>
              <p class="text-base text-base-content/70 leading-relaxed">
                Draw structures, advanced search, browse data, and extract chemical insights from PDFs seamlessly.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals -->
    <modal ref="ketcherModalRef">
      <ketcher-component></ketcher-component>
    </modal>
    <modal ref="pdf2ChemicalsSubmitRef">
      <PDF2ChemicalsSubmitComponent></PDF2ChemicalsSubmitComponent>
    </modal>
  </main>
</template>

<script setup>
import { defineAsyncComponent, ref } from 'vue';
import { useRouter } from 'vue-router'
import { useFilterStore } from '~/stores/filterStore';
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore';
import { useHistogramRangeSliderStore } from '~/stores/histogramRangeSliderStore';
import { useSortStore } from '~/stores/sortingStore';
import Modal from '~/components/Modal.vue';
import SearchField from '~/components/SearchField.vue';

const KetcherComponent = defineAsyncComponent({
  loader: () => import('~/components/KetcherComponent.vue')
});

const PDF2ChemicalsSubmitComponent = defineAsyncComponent({
  loader: () => import('~/components/PDF2ChemicalsSubmitComponent.vue')
})

const router = useRouter()

const fetchChemicalStore = useFetchChemicalStore()
const histogramRangeSliderStore = useHistogramRangeSliderStore()
const filterStore = useFilterStore()
const sortStore = useSortStore()

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

const ketcherModalRef = ref(null)

const openKetcherModal = () => {
  if (ketcherModalRef.value) {
    ketcherModalRef.value.toggleComponentModal();
  }
}

const pdf2ChemicalsSubmitRef = ref(null)

const openPDF2ChemicalsSubmitModal = () => {
  if (pdf2ChemicalsSubmitRef.value) {
    pdf2ChemicalsSubmitRef.value.toggleComponentModal()
  }
}

definePageMeta({
  layout: 'default'
});
</script>

<style scoped>
.search_bar_background {
  background-image: url('~/assets/search_bar_background.webp');
}
</style>