<template>
  <main class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200">

    <Head>
      <Title>About | LabSOADB</Title>
    </Head>

    <!-- Mobile Table of Contents -->
    <div class="lg:hidden sticky top-0 z-50 backdrop-blur-md bg-base-100/80 border-b border-base-300">
      <div class="collapse collapse-arrow" :class="isTableOfContentsOpened ? 'collapse-open' : 'collapse-close'">
        <input type="checkbox" class="min-h-0" v-model="isTableOfContentsOpened"
          aria-label="Toggle table of contents" />
        <div class="collapse-title text-base font-semibold flex items-center gap-3 py-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
            class="w-5 h-5 text-primary">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
          </svg>
          <span>Jump to Section</span>
        </div>
        <div class="collapse-content">
          <scrollspy @click="isTableOfContentsOpened = false" :sections="sectionsRef"
            scrollspy-list="menu space-y-1 pb-2"
            scrollspy-item="text-sm hover:bg-base-200 rounded-lg transition-all duration-200" />
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8 lg:py-16 max-w-7xl">
      <!-- Hero Header Section -->
      <section class="mb-12 lg:mb-16" data-aos="fade-down">
        <div class="max-w-4xl">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
              stroke="currentColor" class="w-5 h-5 text-primary">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
            </svg>
            <span class="text-sm font-semibold text-primary">Our Story & Mission</span>
          </div>

          <h1
            class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent leading-tight">
            About LabSOADB
          </h1>

          <p class="text-lg md:text-xl text-base-content/70 leading-relaxed">
            Democratizing access to chemical data through automated extraction and open science
          </p>
        </div>
      </section>

      <div class="flex gap-8 lg:gap-12 relative">
        <!-- Main Content Column -->
        <div class="flex-1 min-w-0">
          <div class="space-y-8">
            <!-- Introduction Section -->
            <section data-aos="fade-up" id="introduction" class="card bg-base-100 shadow-xl border border-base-300">
              <div class="card-body p-6 lg:p-10">
                <div class="flex items-start gap-4 mb-6">
                  <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-6 h-6 text-primary">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                    </svg>
                  </div>
                  <div>
                    <h2 class="text-2xl md:text-4xl font-bold mb-2">Introduction</h2>
                    <div class="h-1 w-20 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
                  </div>
                </div>

                <div class="prose prose-lg max-w-none space-y-6 text-base-content/80">
                  <p class="leading-relaxed">
                    LabSOADB is an <span class="font-semibold text-primary">open database</span> of chemicals gathered
                    solely from <span class="font-semibold text-primary">automated chemical extraction</span> from
                    literature.
                    Using <span class="font-semibold text-secondary">data mining techniques</span>, enhanced with <span
                      class="font-semibold text-secondary">NLP</span>, <span
                      class="font-semibold text-secondary">Machine Learning</span> and <span
                      class="font-semibold text-secondary">Deep Learning</span>, all chemicals that compose LabSOADB
                    were extracted
                    from manuscripts, MSc dissertations, theses, and more in an automated way.
                  </p>

                  <div class="card bg-gradient-to-br from-primary/5 to-secondary/5 border border-primary/20">
                    <div class="card-body p-6">
                      <p class="leading-relaxed">
                        LabSOADB exists with the purpose of leading a <span
                          class="font-semibold text-base-content">family of databases composed by chemical data,
                          automatically mined from several unstructured data sources</span>.
                        Using <NuxtLink to="/pdf2chemicals/about"
                          class="link link-primary font-semibold hover:link-secondary transition-colors duration-200">
                          PDF2Chemicals
                        </NuxtLink> as
                        this mining tool, LabSOADB becomes a
                        proof of concept (PoC) demonstrating that <span class="font-semibold text-base-content">it is
                          possible to populate chemical databases requiring minimal human interference</span>.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- UFF-LabSOA Project Section -->
            <section data-aos="fade-up" id="uff-labsoa-project"
              class="card bg-base-100 shadow-xl border border-base-300">
              <div class="card-body p-6 lg:p-10">
                <div class="flex items-start gap-4 mb-6">
                  <div class="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-6 h-6 text-secondary">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 16a9.065 9.065 0 0 1-6.23-.693L5 15.3m14.8 0 .438 1.75a1.5 1.5 0 0 1-1.5 1.875H5.262a1.5 1.5 0 0 1-1.5-1.875l.438-1.75" />
                    </svg>
                  </div>
                  <div>
                    <h2 class="text-2xl md:text-4xl font-bold mb-2">The UFF-LabSOA Project</h2>
                    <div class="h-1 w-20 bg-gradient-to-r from-secondary to-accent rounded-full"></div>
                  </div>
                </div>

                <div class="prose prose-lg max-w-none space-y-6 text-base-content/80">
                  <p class="leading-relaxed">
                    One of the core problems faced by cheminformatics nowadays is the limited amount of structured
                    experimental data. Cheminformatics primarily works with the use of <span class="italic">in
                      silico</span> data processing in order to
                    generate chemical attributes that, previously, could only be generated through laboratory
                    experiments.
                  </p>

                  <p class="leading-relaxed">
                    With the advent of the information age, accompanied by machine and deep learning techniques,
                    the priority of more structured data went from an optional status to an extremely urgent need,
                    considering that machine and deep learning models, to generate good results, need a large amount of
                    structured data.
                  </p>

                  <div class="divider my-8"></div>

                  <div class="space-y-6">
                    <div class="flex gap-4">
                      <div class="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                        <span class="text-primary font-bold">1</span>
                      </div>
                      <div>
                        <h3 class="text-xl font-semibold mb-2">Step One: PDF2Chemicals</h3>
                        <p class="leading-relaxed">
                          With the purpose of solving this problem, the project UFF-LabSOA was born, dividing itself
                          into two steps.
                          The first step was creating a tool called <NuxtLink to="/pdf2chemicals/about"
                            class="link link-primary font-semibold hover:link-secondary transition-colors duration-200">
                            PDF2Chemicals
                          </NuxtLink>,
                          to extract experimental data scattered through manuscripts, theses, books, etc. As an initial
                          test, we used <NuxtLink to="/pdf2chemicals/about"
                            class="link link-primary font-semibold hover:link-secondary transition-colors duration-200">
                            PDF2Chemicals
                          </NuxtLink> to
                          extract the organic compounds synthesized by the Brazilian <a
                            href="https://en.wikipedia.org/wiki/Fluminense_Federal_University"
                            class="link link-primary font-semibold hover:link-secondary transition-colors duration-200"
                            target="_blank" rel="noopener noreferrer">Federal
                            Fluminense University's</a>
                          <a class="link link-primary font-semibold hover:link-secondary transition-colors duration-200"
                            href="https://international.uff.br/project/laboratory-of-applied-organic-synthesis/"
                            target="_blank" rel="noopener noreferrer">Organic
                            Synthesis Lab (UFF-LabSOA)</a>, hence the name of the project.
                        </p>
                      </div>
                    </div>

                    <div class="flex gap-4">
                      <div
                        class="w-8 h-8 rounded-lg bg-secondary/10 flex items-center justify-center flex-shrink-0 mt-1">
                        <span class="text-secondary font-bold">2</span>
                      </div>
                      <div>
                        <h3 class="text-xl font-semibold mb-2">Step Two: Building the Database</h3>
                        <p class="leading-relaxed">
                          The next step was to create a database called <NuxtLink to="/home"
                            class="link link-secondary font-semibold hover:link-primary transition-colors duration-200">
                            LabSOADB
                          </NuxtLink>, populated with the extracted data,
                          to <span class="font-semibold text-base-content">democratize access to this data for the
                            scientific community</span>. Also, to <span class="font-semibold text-base-content">ease the
                            search and download of <NuxtLink to="/home"
                              class="link link-secondary font-semibold hover:link-primary transition-colors duration-200">
                              LabSOADB
                            </NuxtLink> data</span>,
                          this website was created, <span class="font-semibold text-base-content">allowing any
                            non-technical user to access the gathered experimental data
                            inserted in our database</span>.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="card bg-gradient-to-br from-accent/5 to-primary/5 border border-accent/20 mt-8">
                    <div class="card-body p-6">
                      <div class="flex items-start gap-3">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                          stroke="currentColor" class="w-6 h-6 text-accent flex-shrink-0 mt-1">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
                        </svg>
                        <p class="text-sm leading-relaxed">
                          <span class="font-semibold">Our Mission:</span> To make chemical research data freely
                          accessible and easily searchable, accelerating scientific discovery through open science and
                          automated data extraction.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>

        <!-- Desktop Table of Contents -->
        <aside class="hidden lg:block w-72 flex-shrink-0">
          <div class="sticky top-6">
            <div class="card bg-base-100 shadow-xl border border-base-300 overflow-hidden">
              <!-- Header with gradient -->
              <div class="bg-gradient-to-br from-primary/10 to-secondary/10 px-6 py-4 border-b border-base-300">
                <h3 class="font-bold text-lg flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                    stroke="currentColor" class="w-5 h-5 text-primary">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
                  </svg>
                  Contents
                </h3>
              </div>

              <!-- Scrollspy content -->
              <div class="p-4">
                <scrollspy :sections="sectionsRef" scrollspy-list="menu menu-sm space-y-1"
                  scrollspy-item="text-sm hover:bg-base-200 rounded-lg transition-all duration-200 hover:translate-x-1" />
              </div>
            </div>

            <!-- Quick Info Card -->
            <div class="card bg-gradient-to-br from-primary/5 to-secondary/5 shadow-lg border border-base-300 mt-6">
              <div class="card-body p-6">
                <h4 class="font-semibold text-sm text-base-content/70 mb-4 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                    stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                  </svg>
                  Key Highlights
                </h4>
                <div class="space-y-3 text-sm">
                  <div class="flex items-start gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-4 h-4 text-primary flex-shrink-0 mt-0.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Open access database</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-4 h-4 text-primary flex-shrink-0 mt-0.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Automated extraction</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-4 h-4 text-primary flex-shrink-0 mt-0.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>AI-powered processing</span>
                  </div>
                  <div class="flex items-start gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                      stroke="currentColor" class="w-4 h-4 text-primary flex-shrink-0 mt-0.5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                    </svg>
                    <span>Minimal human intervention</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </main>
</template>

<script setup>
import Scrollspy from '~/components/Scrollspy.vue';

const isTableOfContentsOpened = ref(false)

const sectionsRef = ref([
  {
    id: 'introduction',
    label: 'Introduction',
  },
  {
    id: 'uff-labsoa-project',
    label: 'The UFF-LabSOA Project'
  }
])
</script>

<style scoped>
/* Smooth gradient background animation */
@keyframes gradient-shift {

  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

main {
  background-size: 200% 200%;
  animation: gradient-shift 15s ease infinite;
}

/* Custom prose styling for better readability */
.prose p {
  line-height: 1.8;
}

.prose a {
  text-decoration: none;
  transition: all 0.2s ease;
}

.prose a:hover {
  transform: translateX(2px);
}
</style>