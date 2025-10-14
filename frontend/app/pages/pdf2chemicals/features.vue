<template>
  <main class="min-h-screen bg-gradient-to-br from-base-200 via-base-100 to-base-200">

    <Head>
      <Title>Features | PDF2Chemicals</Title>
    </Head>

    <!-- Mobile Table of Contents with improved accessibility -->
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
        <div class="text-center max-w-4xl mx-auto">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
              stroke="currentColor" class="w-5 h-5 text-primary">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 16a9.065 9.065 0 0 1-6.23-.693L5 15.3m14.8 0 .438 1.75a1.5 1.5 0 0 1-1.5 1.875H5.262a1.5 1.5 0 0 1-1.5-1.875l.438-1.75" />
            </svg>
            <span class="text-sm font-semibold text-primary">Comprehensive Feature Set</span>
          </div>

          <h1
            class="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent leading-tight">
            PDF2Chemicals Features
          </h1>

          <p class="text-lg md:text-xl text-base-content/70 max-w-2xl mx-auto">
            Explore our powerful suite of chemical data extraction and analysis tools
          </p>
        </div>
      </section>

      <div class="flex gap-8 lg:gap-12 relative">
        <!-- Main Content Column -->
        <div class="flex-1 min-w-0">
          <div class="space-y-6">
            <property-table data-aos="fade-up" v-for="(section, index) in dataSections" :key="section.id"
              :id="section.id" :title="section.title" :headers="section.headers" :rows="section.rows"
              :data-aos-delay="index * 50" />
          </div>
        </div>

        <!-- Desktop Table of Contents - Enhanced -->
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
              <div class="p-4 max-h-[calc(100vh-12rem)] overflow-y-auto custom-scrollbar">
                <scrollspy :sections="sectionsRef" scrollspy-list="menu menu-sm space-y-1"
                  scrollspy-item="text-sm hover:bg-base-200 rounded-lg transition-all duration-200 hover:translate-x-1" />
              </div>

              <!-- Footer stats -->
              <div class="bg-base-200 px-6 py-3 text-xs text-base-content/60 border-t border-base-300">
                {{ sectionsRef.length }} feature categories
              </div>
            </div>

            <!-- Quick Stats Card -->
            <div class="card bg-gradient-to-br from-primary/5 to-secondary/5 shadow-lg border border-base-300 mt-6">
              <div class="card-body p-6">
                <h4 class="font-semibold text-sm text-base-content/70 mb-3">Quick Overview</h4>
                <div class="space-y-3">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                        stroke="currentColor" class="w-5 h-5 text-primary">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
                      </svg>
                    </div>
                    <div>
                      <div class="text-2xl font-bold">{{ totalProperties }}</div>
                      <div class="text-xs text-base-content/60">Total Properties</div>
                    </div>
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
import PropertyTable from '~/components/PropertyTable.vue';
import { useThemeStore } from '~/stores/theme';

const themeStore = useThemeStore()
const currTheme = computed(() => themeStore.currentTheme)

const isTableOfContentsOpened = ref(false)

const dataSections = computed(() => {
  return [
    {
      id: 'identifier',
      title: 'Identifier',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['IUPAC Name', 'iupac', 'String'],
        ['Chemical Formula', 'formula', 'String'],
        ['PDF2Chemicals Chemical Id', 'id', 'String'],
        ['Chemical Reference Index', 'reference_index', 'String'],
        ['InChi', 'inchi', 'String'],
        ['InChI Key', 'inchi_key', 'String'],
        ['SMILES', 'smiles', 'String']
      ]
    },
    {
      id: 'physical-property',
      title: 'Physical Property',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Atomic Volume', 'volume', 'Float'],
        ['Atom Count', 'num_atom', 'Integer'],
        ['Heavy Atom Count', 'num_heavy_atom', 'Integer'],
        ['Aromatic Heavy Atom Count', 'num_arom_heavy_atom', 'Integer'],
        ['Rotatable Bond Count', 'num_rotatable_bond', 'Integer'],
        ['H-Bond Acceptor Count', 'num_h_bond_accept', 'Integer'],
        ['H-Bond Donor Count', 'num_h_bond_donor', 'Integer'],
        ['Ring Count', 'num_ring', 'Integer'],
        ['Carbon Count', 'num_carbon', 'Integer'],
        ['Heteroatom Count', 'num_heteroatom', 'Integer']
      ]
    },
    {
      id: 'physicochemical-property',
      title: 'Physicochemical Property',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Molecular Weight (MW)', 'mass_weight', 'Float'],
        ['Fraction of SP3 Hybridised Carbon Atoms', 'fraction_csp3', 'Float between 0 and 1'],
        ['Molar Refractivity (MR)', 'molar_refractivity', 'Float'],
        ['Topological Polar Surface Area (TPSA)', 'tpsa', 'Float']
      ]
    },
    {
      id: 'experimental-melting-point',
      title: 'Experimental Melting Point',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Melting Point Lower Bound', 'melting_point_lower_bound', 'Float'],
        ['Melting Point Upper Bound', 'melting_point_upper_bound', 'Float']
      ]
    },
    {
      id: 'experimental-state-of-matter',
      title: 'Experimental State of Matter',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['State of Matter', 'state_of_matter', 'String'],
        ['Color', 'color', 'String'],
        ['Color Hexadecimal', 'color_hex_value', 'String']
      ]
    },
    {
      id: 'log-pow',
      title: 'Partition Coefficient (LogPow)',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Wildman-Crippen LogP', 'wlogp', 'Float'],
        ['XLogP v2', 'xlogp2', 'Float'],
        ['JPLogP', 'jplogp', 'Float'],
        ['Mouriguchi LogP', 'mlogp', 'Float'],
        ['Consensus LogP', 'consensus_logp', 'Float']
      ]
    },
    {
      id: 'log-s',
      title: 'Solubility (LogS)',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['ESOL LogS', 'esol_logs', 'Float'],
        ['Filter-It LogS', 'filter_it_logs', 'Float']
      ]
    },
    {
      id: 'qsar-score',
      title: 'QSAR Score',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Quantitative Estimate of Druglikeness (QED)', 'qed_score', 'Float between 0 and 1'],
        ['Synthetic Accessibility', 'synthetic_accessibility_score', 'Float between 1 and 10'],
        ['Natural Product', 'natural_product_score', 'Float between -5 and 5']
      ]
    },
    {
      id: 'drug-like-rule',
      title: 'Drug-like Rule',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Lipinski Violation Count', 'num_lipinski_violation', 'Integer'],
        ['Ghose Violation Count', 'num_ghose_violation', 'Integer'],
        ['Veber Violation Count', 'num_veber_violation', 'Integer'],
        ['Egan Violation Count', 'num_egan_violation', 'Integer'],
        ['Muegge Violation Count', 'num_muegge_violation', 'Integer']
      ]
    },
    {
      id: 'pharmacokinetics',
      title: 'Pharmacokinetics',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Gastrointestinal Absorption', 'gi_absorption', 'Integer 0 (false) or 1 (true)'],
        ['Blood-Brain Barrier Permeation', 'bbb_permeant', 'Integer 0 (false) or 1 (true)'],
        ['Skin Permeation (LogKp)', 'logkp', 'Float']
      ]
    },
    {
      id: 'p450-inhibition',
      title: 'P450 Inhibition',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['CYP1A2 Inhibitor', 'cyp1a2_inhibitor', 'Integer 0 (false) or 1 (true)'],
        ['CYP2C9 Inhibitor', 'cyp2c9_inhibitor', 'Integer 0 (false) or 1 (true)'],
        ['CYP2C19 Inhibitor', 'cyp2c19_inhibitor', 'Integer 0 (false) or 1 (true)'],
        ['CYP2D6 Inhibitor', 'cyp2d6_inhibitor', 'Integer 0 (false) or 1 (true)'],
        ['CYP3A4 Inhibitor', 'cyp3a4_inhibitor', 'Integer 0 (false) or 1 (true)']
      ]
    },
    {
      id: 'pains-violation',
      title: 'PAINS Violation',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['PAINS Violation Count', 'num_pains_violation', 'Integer']
      ]
    },
    {
      id: 'brenk-violation',
      title: 'BRENK Violation',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['BRENK Violation Count', 'num_brenk_violation', 'Integer']
      ]
    },
    {
      id: 'toxicity',
      title: 'Toxicity',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Cardiotoxicity Prediction', 'cardiotoxicity_prediction', 'Integer 0 (false) or 1 (true)'],
        ['Hepatotoxicity Prediction', 'hepatotoxicity_prediction', 'Integer 0 (false) or 1 (true)'],
        ['Ames Mutagenesis Prediction', 'ames_mutagenesis_prediction', 'Integer 0 (false) or 1 (true)']
      ]
    },
    {
      id: 'literature',
      title: 'Literature',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Document Id', 'document_id', 'String'],
        ['DOI', 'doi', 'String']
      ]
    },
    {
      id: 'molecular-conformation',
      title: 'Molecular Conformation',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Generation of a Given Number of Molecule Conformations', '—', '—']
      ]
    },
    {
      id: 'directory-path',
      title: 'Chemical Directory Path',
      headers: ['Property', 'CSV Representation', 'Data Type'],
      rows: [
        ['Directory path where all PDB, MOL2, SDF, etc, files generated for each chemical are located', 'compound_path', 'String']
      ]
    }
  ]
})

// Calculate total properties
const totalProperties = computed(() => {
  return dataSections.value.reduce((total, section) => total + section.rows.length, 0)
})

// Table of Contents
const sectionsRef = ref([
  { id: "identifier", label: "Identifier" },
  { id: "physical-property", label: "Physical Property" },
  { id: 'physicochemical-property', label: 'Physicochemical Property' },
  { id: "experimental-melting-point", label: "Experimental Melting Point" },
  { id: "experimental-state-of-matter", label: "Experimental State of Matter" },
  { id: "log-pow", label: "Partition Coefficient (LogPow)" },
  { id: "log-s", label: "Solubility (LogS)" },
  { id: 'qsar-score', label: "QSAR Score" },
  { id: 'drug-like-rule', label: "Drug-like Rule" },
  { id: 'pharmacokinetics', label: "Pharmacokinetics" },
  { id: 'p450-inhibition', label: 'P450 Inhibition' },
  { id: 'pains-violation', label: 'PAINS Violation' },
  { id: 'brenk-violation', label: 'BRENK Violation' },
  { id: 'toxicity', label: 'Toxicity' },
  { id: 'literature', label: 'Literature' },
  { id: 'molecular-conformation', label: 'Molecular Conformation' },
  { id: 'directory-path', label: 'Chemical Directory Path' },
])

watch(currTheme, (newTheme) => {
  if (import.meta.client) {
    document.documentElement.setAttribute('data-theme', newTheme)
  }
})

</script>

<style scoped>
/* Custom scrollbar for sidebar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: hsl(var(--bc) / 0.2);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--bc) / 0.3);
}

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
</style>