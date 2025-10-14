<template>
  <main class="min-h-screen bg-base-200">
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

    <!-- Loading State -->
    <div v-if="selectedChemicalStore.loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center space-y-4">
        <span class="loading loading-spinner loading-lg text-primary"></span>
        <p class="text-base-content/70">Loading chemical data...</p>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="container mx-auto px-4 py-8 lg:py-12">
      <div class="flex gap-8">
        <!-- Content Column -->
        <div class="grid grid-cols-1 space-y-8">
          <!-- Header Section -->
          <div class="card bg-base-100 shadow-xl" data-aos="fade-up">
            <div class="card-body">
              <div class="space-y-4">
                <div class="badge badge-primary badge-lg">
                  {{ selectedChemicalStore.selectedChemical.api_id }}
                </div>

                <h1 class="text-2xl md:text-4xl font-bold">
                  {{ selectedChemicalStore.selectedChemical.identifier.iupac_name }}
                </h1>

                <div class="flex flex-wrap gap-4 text-sm text-base-content/70">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    <span>Created on</span>
                    <time :datetime="selectedChemicalStore.selectedChemical.created_at" class="font-semibold">
                      {{ new Date(selectedChemicalStore.selectedChemical.created_at).toLocaleDateString('sv-SE') }}
                    </time>
                  </div>

                  <div class="divider divider-horizontal"></div>

                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
                    </svg>
                    <span>First published</span>
                    <time :datetime="selectedChemicalStore.getFirstPublicationDate().toISOString()"
                      class="font-semibold">
                      {{ selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', {
                        month: 'short',
                        year: 'numeric'
                      }) }}
                    </time>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2D and 3D Structures -->
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
            <!-- 2D Depiction -->
            <section data-aos="fade-up" class="card bg-base-100 shadow-xl" id="2d_depiction">
              <div class="card-body">
                <h2 class="card-title text-2xl mb-4">2D Depiction</h2>

                <div class="flex flex-wrap gap-2 mb-4">
                  <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-primary btn-sm gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                      </svg>
                      <span>Structure Search</span>
                    </div>
                    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-10 w-48 p-2 shadow-lg">
                      <li><a @click="similaritySearch">Similarity</a></li>
                      <li><a @click="substructureSearch">Substructure</a></li>
                    </ul>
                  </div>

                  <NuxtLink :to="selectedChemicalStore.selectedChemical.chem_depiction_image" target="_blank"
                    class="btn btn-outline btn-primary btn-sm gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="w-4 h-4">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                    </svg>
                    <span>Get Image</span>
                  </NuxtLink>
                </div>

                <figure class="bg-base-200 rounded-lg p-4">
                  <img :src="selectedChemicalStore.selectedChemical.chem_depiction_image" alt="Molecular Structure"
                    class="w-full h-auto rounded-lg" loading="lazy" />
                </figure>
              </div>
            </section>

            <!-- 3D Conformation -->
            <section data-aos="fade-up" class="card bg-base-100 shadow-xl" id="3d_conformations"
              v-if="selectedChemicalStore.selectedChemical?.conformation?.[confsPagination.state.page - 1]">
              <div class="card-body">
                <h2 class="card-title text-2xl mb-4">3D Conformation</h2>

                <div class="flex flex-wrap gap-2 mb-4">
                  <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-primary btn-sm gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                      </svg>
                      <span>Structure Search</span>
                    </div>
                    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-10 w-48 p-2 shadow-lg">
                      <li><a @click="similaritySearch">Similarity</a></li>
                      <li><a @click="substructureSearch">Substructure</a></li>
                    </ul>
                  </div>

                  <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-outline btn-primary btn-sm gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                      </svg>
                      <span>Download</span>
                    </div>
                    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-10 w-52 p-2 shadow-lg">
                      <li>
                        <a :href="selectedChemicalStore.selectedChemical.conformation[confsPagination.state.page - 1].conf_file"
                          :download="getFileName(selectedChemicalStore.selectedChemical.conformation[confsPagination.state.page - 1].conf_file)"
                          target="_blank" rel="noopener noreferrer">
                          Current Conformation
                        </a>
                      </li>
                      <li>
                        <a :href="getAllConformationsDownloadLink()"
                          :download="`${selectedChemicalStore.selectedChemical.api_id}_confs.zip`" target="_blank"
                          rel="noopener noreferrer">
                          All Conformations (ZIP)
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>

                <div class="bg-base-200 rounded-lg overflow-hidden">
                  <ngl-viewer :key="nglViewerKey"
                    :file="selectedChemicalStore.selectedChemical.conformation[confsPagination.state.page - 1].conf_file"
                    class="h-64 md:h-80" />
                </div>

                <div class="flex justify-center mt-4">
                  <pagination :pagination="confsPagination" />
                </div>
              </div>
            </section>
          </div>

          <!-- Data Tables -->
          <PropertyTable v-for="section in dataSections" :key="section.id" :id="section.id" :title="section.title"
            :headers="section.headers" :rows="section.rows" data-aos="fade-up" />

          <!-- References -->
          <section data-aos="fade-up" class="card bg-base-100 shadow-xl" id="reference">
            <div class="card-body">
              <h2 class="card-title text-2xl mb-4">References</h2>
              <div class="space-y-3">
                <a v-for="citation in selectedChemicalStore.selectedChemical.literature" :key="citation.api_id"
                  :href="doiRedirectionSiteHost + citation.doi" target="_blank" rel="noopener noreferrer"
                  class="block p-4 rounded-lg border border-base-300 hover:border-primary hover:shadow-lg transition-all">
                  <p class="text-primary font-semibold text-sm mb-1">
                    {{ citation.doi }}
                  </p>
                  <p class="font-bold text-lg mb-1" v-html="citation.title"></p>
                  <p class="text-base-content/70 text-sm" v-html="citation.publication_name"></p>
                  <time :datetime="selectedChemicalStore.getFirstPublicationDate().toISOString()"
                    class="text-base-content/60 text-sm">
                    {{ selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', {
                      month: 'short',
                      year: 'numeric'
                    }) }}
                  </time>
                </a>
              </div>
            </div>
          </section>
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
              <div class="p-4 max-h-[calc(100vh-12rem)] overflow-y-auto custom-scrollbar">
                <scrollspy :sections="sectionsRef" scrollspy-list="menu menu-sm space-y-1"
                  scrollspy-item="text-sm hover:bg-base-200 rounded-lg transition-all duration-200 hover:translate-x-1" />
              </div>

              <!-- Footer stats -->
              <div class="bg-base-200 px-6 py-3 text-xs text-base-content/60 border-t border-base-300">
                {{ sectionsRef.length }} feature categories
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </main>
</template>

<script setup>
import utils from "~/utils/util"
import { onMounted, ref, computed, watch } from 'vue'
import { useSelectedChemicalStore } from '~/stores/selectedChemicalStore'
import { useRoute, useRouter } from 'vue-router'
import { useFilterStore } from '~/stores/filterStore'
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore'
import { useSortStore } from '~/stores/sortingStore'
import { usePagination } from '~/composables/usePagination'

import NglViewer from '~/components/NglViewer.vue'
import Pagination from '~/components/Pagination.vue'
import PropertyTable from "~/components/PropertyTable.vue"
import Scrollspy from "~/components/Scrollspy.vue"

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()

const nglViewerKey = ref(1)
const isTableOfContentsOpened = ref(false)
const doiRedirectionSiteHost = "https://www.doi.org/"

// Stores
const selectedChemicalStore = useSelectedChemicalStore()
const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()
const sortStore = useSortStore()

// Composables
const confsPagination = usePagination()

// Computed Data Sections
const dataSections = computed(() => {
  const chem = selectedChemicalStore.selectedChemical
  if (!chem) return []

  return [
    {
      id: 'names_and_identifiers',
      title: 'Names and Identifiers',
      headers: ['Identifier', 'Name', 'Reference'],
      rows: [
        ['LabSOA ID', chem.api_id, '—'],
        ['IUPAC Name', chem.identifier.iupac_name, `<a href="${doiRedirectionSiteHost}${chem.literature[0].doi}" target="_blank" class="link link-primary">${chem.literature[0].doi}</a>`],
        ['Molecular Formula', utils.replaceStringNumberBySubscript(chem.identifier.chem_formula), 'Computed by RDKit'],
        ['Canonical SMILES', chem.identifier.smiles, 'Computed by <a href="https://pubs.acs.org/doi/10.1021/ci100384d" target="_blank" class="link link-primary">OPSIN</a> (2.8.0v)'],
        ['InChI', chem.identifier.inchi, 'Computed by RDKit'],
        ['InChI Key', chem.identifier.inchi_key, 'Computed by RDKit']
      ]
    },
    {
      id: 'physical_property',
      title: 'Physical Property',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Molecular Weight', `${chem.physical_property.molecular_weight.toFixed(2)} g/mol`, 'Computed by RDKit'],
        ...(chem.physical_property.mp_lower_bound && chem.physical_property.mp_upper_bound ?
          [['Melting Point', `${chem.physical_property.mp_lower_bound.toFixed(1)} - ${chem.physical_property.mp_upper_bound.toFixed(1)} ℃`, `<a href="${doiRedirectionSiteHost}${chem.literature[0].doi}" target="_blank" class="link link-primary">${chem.literature[0].doi}</a>`]] : []),
        ...(chem.physical_property.mp_lower_bound && !chem.physical_property.mp_upper_bound ?
          [['Melting Point', `≥ ${chem.physical_property.mp_lower_bound.toFixed(1)} ℃`, `<a href="${doiRedirectionSiteHost}${chem.literature[0].doi}" target="_blank" class="link link-primary">${chem.literature[0].doi}</a>`]] : []),
        ...(chem.physical_property.state_of_matter ?
          [['State of Matter', chem.physical_property.state_of_matter, `<a href="${doiRedirectionSiteHost}${chem.literature[0].doi}" target="_blank" class="link link-primary">${chem.literature[0].doi}</a>`]] : []),
        ...(chem.physical_property.color ?
          [['Color', `${chem.physical_property.color} <div style="background-color: ${chem.physical_property.color_hexadecimal}; width: 1rem; height: 1rem; display: inline-block; border-radius: 0.25rem; margin-left: 0.5rem; vertical-align: middle;"></div>`, `<a href="${doiRedirectionSiteHost}${chem.literature[0].doi}" target="_blank" class="link link-primary">${chem.literature[0].doi}</a>`]] : []),
        ['H-Bond Acceptor Count', chem.physical_property.count_h_bond_acceptor, 'Computed by RDKit'],
        ['H-Bond Donor Count', chem.physical_property.count_h_bond_donor, 'Computed by RDKit'],
        ['Rotatable Bond Count', chem.physical_property.count_rotatable_bond, 'Computed by RDKit'],
        ['Atomic Volume', `${chem.physical_property.volume.toFixed(2)} Å³`, 'Computed by RDKit'],
        ['Atom Count', chem.physical_property.count_atom, 'Computed by RDKit'],
        ['Heavy Atom Count', chem.physical_property.count_heavy_atom, 'Computed by RDKit'],
        ['Aromatic Heavy Atom Count', chem.physical_property.count_aromatic_heavy_atom, 'Computed by RDKit'],
        ['Ring Count', chem.physical_property.count_ring, 'Computed by RDKit'],
        ['Carbon Count', chem.physical_property.count_carbon, 'Computed by RDKit'],
        ['Heteroatom Count', chem.physical_property.count_heteroatom, 'Computed by RDKit']
      ]
    },
    {
      id: 'partition_coefficient',
      title: 'Partition Coefficient (LogPow)',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Wildman-Crippen LogP', chem.partition_coefficient.wildman_crippen_logp.toFixed(2), '<a href="https://pubs.acs.org/doi/10.1021/ci990307l" target="_blank" class="link link-primary">10.1021/ci990307l</a>'],
        ['XLogP v2', chem.partition_coefficient.xlogp.toFixed(2), '<a href="https://link.springer.com/article/10.1023/A:1008763405023" target="_blank" class="link link-primary">10.1023/A:1008763405023</a>'],
        ['JPLogP', chem.partition_coefficient.jplogp.toFixed(2), '<a href="https://link.springer.com/article/10.1186/s13321-018-0316-5" target="_blank" class="link link-primary">10.1186/s13321-018-0316-5</a>'],
        ['Mouriguchi LogP', chem.partition_coefficient.mouriguchi_logp.toFixed(2), '<a href="https://doi.org/10.1248/cpb.40.127" target="_blank" class="link link-primary">10.1248/cpb.40.127</a>']
      ]
    },
    {
      id: 'solubility',
      title: 'Solubility (LogS)',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['ESOL LogS', chem.solubility.esol_logs.toFixed(2), '<a href="https://pubs.acs.org/doi/10.1021/ci034243x" target="_blank" class="link link-primary">10.1021/ci034243x</a>'],
        ['Filter-It LogS', chem.solubility.filter_it_logs.toFixed(2), "Computed by Silicos-It's Filter-It"]
      ]
    },
    {
      id: 'physicochemical_property',
      title: 'Physicochemical Property',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Fraction of SP3 Hybridised Carbon Atoms', chem.physicochemical_property.fraction_csp3.toFixed(2), 'Computed by RDKit'],
        ['Molar Refractivity', `${chem.physicochemical_property.molar_refractivity.toFixed(2)} cm³/mol`, 'Computed by RDKit'],
        ['Topological Polar Surface Area', `${chem.physicochemical_property.tpsa.toFixed(2)} Å²`, 'Computed by RDKit']
      ]
    },
    {
      id: 'qsar_score',
      title: 'QSAR Score',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Quantitative Estimate of Druglikeness (QED)', chem.qsar_score.qed_score.toFixed(2), 'Computed by RDKit'],
        ['Synthetic Accessibility Score', chem.qsar_score.synthetic_accessibility_score.toFixed(2), 'Computed by RDKit'],
        ['Natural Product Score', chem.qsar_score.natural_product_score.toFixed(2), 'Computed by RDKit']
      ]
    },
    {
      id: 'drug_like_rule',
      title: 'Drug-like Rule',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Lipinski Violation Count', chem.druglike_rule.count_lipinski_violation, '<a href="https://doi.org/10.1016/S0169-409X(00)00129-0" target="_blank" class="link link-primary">10.1016/S0169-409X(00)00129-0</a>'],
        ['Ghose Violation Count', chem.druglike_rule.count_ghose_violation, '<a href="https://pubs.acs.org/doi/10.1021/cc9800071" target="_blank" class="link link-primary">10.1021/cc9800071</a>'],
        ['Veber Violation Count', chem.druglike_rule.count_veber_violation, '<a href="https://pubs.acs.org/doi/10.1021/jm020017n" target="_blank" class="link link-primary">10.1021/jm020017n</a>'],
        ['Egan Violation Count', chem.druglike_rule.count_egan_violation, '<a href="https://pubs.acs.org/doi/10.1021/jm000292e" target="_blank" class="link link-primary">10.1021/jm000292e</a>'],
        ['Muegge Violation Count', chem.druglike_rule.count_muegge_violation, '<a href="https://pubs.acs.org/doi/10.1021/jm015507e" target="_blank" class="link link-primary">10.1021/jm015507e</a>']
      ]
    },
    {
      id: 'pharmacokinetics',
      title: 'Pharmacokinetics',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['Gastrointestinal Absorption', chem.pharmacokinetics.gastrointestinal_absorption, 'Computed by <a href="https://chemistry-europe.onlinelibrary.wiley.com/doi/full/10.1002/cmdc.201600182" target="_blank" class="link link-primary">BOILED-Egg</a>'],
        ['Blood-Brain Barrier Permeation', chem.pharmacokinetics.blood_brain_barrier_permeation, 'Computed by <a href="https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.858126/full" target="_blank" class="link link-primary">DeePred-BBB</a>']
      ]
    },
    {
      id: 'p450_inhibition',
      title: 'P450 Inhibition',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['CYP1A2 Inhibitor', chem.p450_inhibition.cyp1a2_inhibitor, 'Computed by <a href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" target="_blank" class="link link-primary">DEEPCYP</a>'],
        ['CYP2C9 Inhibitor', chem.p450_inhibition.cyp2c9_inhibitor, 'Computed by <a href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" target="_blank" class="link link-primary">DEEPCYP</a>'],
        ['CYP2C19 Inhibitor', chem.p450_inhibition.cyp2c19_inhibitor, 'Computed by <a href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" target="_blank" class="link link-primary">DEEPCYP</a>'],
        ['CYP2D6 Inhibitor', chem.p450_inhibition.cyp2d6_inhibitor, 'Computed by <a href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" target="_blank" class="link link-primary">DEEPCYP</a>'],
        ['CYP3A4 Inhibitor', chem.p450_inhibition.cyp3a4_inhibitor, 'Computed by <a href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" target="_blank" class="link link-primary">DEEPCYP</a>']
      ]
    },
    {
      id: 'pains_alert',
      title: 'PAINS Alert',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['PAINS Alert Count', chem.undesirable_substructure_alert.count_pains_alert, 'Computed by RDKit']
      ]
    },
    {
      id: 'brenk_alert',
      title: 'BRENK Alert',
      headers: ['Property Name', 'Property Value', 'Reference'],
      rows: [
        ['BRENK Alert Count', chem.undesirable_substructure_alert.count_brenk_alert, 'Computed by RDKit']
      ]
    }
  ]
})

// Table of Contents
const sectionsRef = ref([
  { id: "2d_depiction", label: "2D Depiction" },
  { id: "3d_conformations", label: "3D Conformation" },
  { id: 'names_and_identifiers', label: 'Names and Identifiers' },
  { id: "physical_property", label: "Physical Property" },
  { id: "partition_coefficient", label: "Partition Coefficient" },
  { id: "solubility", label: "Solubility" },
  { id: "physicochemical_property", label: "Physicochemical Property" },
  { id: 'qsar_score', label: "QSAR Score" },
  { id: 'drug_like_rule', label: "Drug-like Rule" },
  { id: 'pharmacokinetics', label: "Pharmacokinetics" },
  { id: 'p450_inhibition', label: 'P450 Inhibition' },
  { id: 'pains_alert', label: 'PAINS Alert' },
  { id: 'brenk_alert', label: 'BRENK Alert' },
  { id: 'reference', label: 'References' }
])

// Functions
const getAllConformationsDownloadLink = () => {
  return `${config.public.downloadChemicalConformationsEndpoint}${selectedChemicalStore.selectedChemical.api_id}/`
}

const fetchSelectedChemicalDetail = async () => {
  selectedChemicalStore.$reset()
  await selectedChemicalStore.fetchSelectedChemical(route.params.labsoadbId)
}

const getFileName = (url) => {
  return url.substring(url.lastIndexOf('/') + 1)
}

const similaritySearch = () => {
  const similarity_threshold = 0.85

  confsPagination.setPage(1)
  filterStore.$reset()
  fetchChemicalStore.$reset()
  sortStore.$reset()

  filterStore.setExactFilter('similarity_threshold', similarity_threshold)
  filterStore.setExactFilter('query', selectedChemicalStore.selectedChemical.identifier.smiles)
  filterStore.setExactFilter('representation_type', 'smiles')
  filterStore.setExactFilter('search_type', 'similarity')

  fetchChemicalStore.setMode('summary')
  fetchChemicalStore.setType('search')
  fetchChemicalStore.fetchChemicals()

  router.push('/chemicals/search')
}

const substructureSearch = () => {
  confsPagination.setPage(1)
  filterStore.$reset()
  fetchChemicalStore.$reset()
  sortStore.$reset()

  filterStore.setExactFilter('query', selectedChemicalStore.selectedChemical.identifier.smiles)
  filterStore.setExactFilter('representation_type', 'smiles')
  filterStore.setExactFilter('search_type', 'substructure')

  fetchChemicalStore.setMode('summary')
  fetchChemicalStore.setType('search')
  fetchChemicalStore.fetchChemicals()

  router.push('/chemicals/search')
}

// Lifecycle
onMounted(async () => {
  await fetchSelectedChemicalDetail()

  const totalConformations = selectedChemicalStore.selectedChemical?.conformation?.length || 0
  confsPagination.setTotalItems(totalConformations)
  confsPagination.setPageSize(1)
  confsPagination.setPage(1)
})

// Watchers
watch(() => confsPagination.state.page, () => {
  nglViewerKey.value *= -1
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