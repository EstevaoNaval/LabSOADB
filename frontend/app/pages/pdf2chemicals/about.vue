<template>
    <main>

        <Head>
            <Title>About | PDF2Chemicals</Title>
            <Meta name="description" :content="pdf2chemicals_about_content" />
        </Head>

        <!-- Hero Section -->
        <section class="relative py-20 lg:py-28 bg-gradient-to-br from-base-200 to-base-300 overflow-hidden">
            <!-- Decorative background elements -->
            <div class="absolute inset-0 opacity-5">
                <div class="absolute top-20 left-10 w-72 h-72 bg-primary rounded-full blur-3xl"></div>
                <div class="absolute bottom-20 right-10 w-96 h-96 bg-secondary rounded-full blur-3xl"></div>
            </div>

            <div class="relative container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
                <div data-aos="fade-up" class="max-w-4xl mx-auto text-center space-y-6">
                    <div class="inline-block px-4 py-2 bg-primary/10 rounded-full mb-4">
                        <span class="text-primary font-semibold text-sm">Free & Open Access</span>
                    </div>

                    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-base-content leading-tight">
                        About <span class="text-primary">PDF2Chemicals</span>
                    </h1>

                    <p class="text-lg sm:text-xl lg:text-2xl text-base-content/80 leading-relaxed max-w-3xl mx-auto">
                        A <strong class="text-base-content">free</strong>, <strong
                            class="text-base-content">easy-to-use</strong>, and
                        <strong class="text-base-content">versatile</strong> tool that <strong
                            class="text-base-content">extracts</strong>,
                        <strong class="text-base-content">cleans</strong>, and <strong
                            class="text-base-content">structures</strong> chemical
                        experimental data from scientific literature PDFs
                    </p>

                    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
                        <button @click="openPDF2ChemicalsSubmitModal" class="btn btn-primary btn-lg gap-2 group">
                            <span>Get Started for Free</span>
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 7l5 5m0 0l-5 5m5-5H6" />
                            </svg>
                        </button>
                        <NuxtLink to='/pdf2chemicals/features' class="btn btn-outline btn-lg gap-2">
                            <span>Explore Features</span>
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Grid -->
        <section class="py-16 lg:py-24 bg-base-100">
            <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
                <div data-aos="fade-up" class="text-center mb-12 lg:mb-16">
                    <h2 class="text-3xl lg:text-4xl font-bold text-base-content mb-4">
                        Powerful Features at Your Fingertips
                    </h2>
                    <p class="text-lg text-base-content/70 max-w-2xl mx-auto">
                        Transform your chemical research workflow with our comprehensive suite of tools
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
                    <!-- Feature Card 1 -->
                    <div data-aos="fade-up" data-aos-delay="0"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Multi-Source Extraction</h3>
                            <p class="text-base-content/70">
                                Seamlessly gather chemical data from papers, PhD theses, MSc dissertations, and more
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 2 -->
                    <div data-aos="fade-up" data-aos-delay="100"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Format Conversion</h3>
                            <p class="text-base-content/70">
                                Convert IUPAC names to SMILES, InChI, chemical formulas, and other standard formats
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 3 -->
                    <div data-aos="fade-up" data-aos-delay="200"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Experimental Data</h3>
                            <p class="text-base-content/70">
                                Extract melting points, states of matter, colors, and other experimental properties
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 4 -->
                    <div data-aos="fade-up" data-aos-delay="0"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 7h6m0 0v6m0-6l-6 6" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Property Calculation</h3>
                            <p class="text-base-content/70">
                                Calculate molecular weight, TPSA, H-bond donors/acceptors, rotatable bonds, and more
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 5 -->
                    <div data-aos="fade-up" data-aos-delay="100"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">3D Structure Generation</h3>
                            <p class="text-base-content/70">
                                Generate molecular conformations in SDF, PDB, MOL2, PNG, and other formats
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 6 -->
                    <div data-aos="fade-up" data-aos-delay="200"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Pharmacokinetic Predictions</h3>
                            <p class="text-base-content/70">
                                Predict blood-brain barrier and gastrointestinal tract permeability
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 7 -->
                    <div data-aos="fade-up" data-aos-delay="0"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">P450 Cytochrome Analysis</h3>
                            <p class="text-base-content/70">
                                Predict inhibition of P450 cytochrome enzymes for drug metabolism insights
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 8 -->
                    <div data-aos="fade-up" data-aos-delay="100"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Lipinski's Rule Validation</h3>
                            <p class="text-base-content/70">
                                Automatically check drug-likeness using Lipinski's rule of five criteria
                            </p>
                        </div>
                    </div>

                    <!-- Feature Card 9 -->
                    <div data-aos="fade-up" data-aos-delay="200"
                        class="card bg-base-200 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                        <div class="card-body">
                            <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <h3 class="card-title text-xl mb-2">Toxicity Predictions</h3>
                            <p class="text-base-content/70">
                                Assess cardiotoxicity, hepatotoxicity, and Ames mutagenicity potential
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="py-16 lg:py-20 bg-gradient-to-br from-primary to-secondary">
            <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
                <div data-aos="fade-up" class="text-center space-y-6">
                    <h2 class="text-3xl lg:text-4xl font-bold text-primary-content">
                        Ready to Transform Your Research?
                    </h2>
                    <p class="text-lg lg:text-xl text-primary-content/90 max-w-2xl mx-auto">
                        Start extracting and analyzing chemical data from your PDFs today—completely free
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
                        <button @click="openPDF2ChemicalsSubmitModal" class="btn btn-neutral btn-lg gap-2 group">
                            <span>Submit Your PDFs</span>
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 7l5 5m0 0l-5 5m5-5H6" />
                            </svg>
                        </button>
                        <NuxtLink to='/pdf2chemicals/features'
                            class="btn btn-outline btn-lg text-primary-content border-primary-content hover:bg-primary-content hover:text-primary">
                            View All Features
                        </NuxtLink>
                    </div>
                </div>
            </div>
        </section>
        <modal ref="pdf2ChemicalsSubmitRef">
            <PDF2ChemicalsSubmitComponent></PDF2ChemicalsSubmitComponent>
        </modal>
    </main>
</template>

<script setup>
import { useThemeStore } from '~/stores/theme';

const PDF2ChemicalsSubmitComponent = defineAsyncComponent({
    loader: () => import('~/components/PDF2ChemicalsSubmitComponent.vue')
})

const pdf2chemicals_about_content = ref("PDF2Chemicals is a free, easy to use and versatile tool that extracts, cleans and structure chemicals experimental data from scientific literature PDFs.")

const themeStore = useThemeStore()

var pdf2ChemicalsSubmitRef = ref(null)

const openPDF2ChemicalsSubmitModal = () => {
    if (pdf2ChemicalsSubmitRef.value) {
        pdf2ChemicalsSubmitRef.value.toggleComponentModal()
    }
}

onBeforeMount(() => {
    themeStore.initializeTheme()
})
</script>

<style scoped>
/* Custom gradient animations can be added here if needed */
</style>