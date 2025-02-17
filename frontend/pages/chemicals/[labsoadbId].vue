<template>
  <div :class="['collapse collapse-arrow	bg-base-200 mx-auto lg:hidden sticky top-0 z-[1] table-of-contents', isTableOfContentsOpened ? 'collapse-open' : 'collapse-close']" >
    <input type="radio" class="cursor-pointer" name="my-accordion-2" @click="toggleTableOfContents" />
    <div class="collapse-title text-slate-400 text-lg md:text-xl font-medium">Table of Contents</div>
    <div class="collapse-content">
      <div class="bg-base-200 font-semibold lg:hidden overflow-y-auto max-h-screen">
        <div class="flex w-[90%]">
          <div class="flex flex-col w-full">
            <scrollspy
              @click="toggleTableOfContents"
              :sections="sectionsRef"
              scrollspy-list="text-md md:text-lg font-semibold menu text-slate-400" 
              scrollspy-item="py-1 pl-2 hover:text-secondary hover:border-secondary hover:font-bold hover:rounded-sm  hover:border-l-4" 
            />
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div v-if="selectedChemicalStore.loading" class="text-center">
    <span class="loading loading-spinner loading-lg"></span>
  </div>
  
  <div data-aos="fade-up" v-else class="py-4 lg:py-16 w-[90%] mx-auto">
    <div class="flex">
      <div class="w-full flex flex-col rounded-box">
        <div class="space-y-2">
          <div class="flex flex-col w-full md:w-5/6 gap-2">
            <h1 class="text-lg md:text-xl font-semibold text-primary">
              {{ selectedChemicalStore.selectedChemical.api_id }}
            </h1>
            <h1 class="text-xl md:text-3xl font-bold">
              {{ selectedChemicalStore.selectedChemical.identifier.iupac_name }}
            </h1>

            <div class="flex flex-col">
              <h1 class="text-md md:text-lg font-semibold text-slate-400 my-auto">
                <p>Created on
                  <time :datetime="selectedChemicalStore.selectedChemical.created_at">
                    {{ new Date(selectedChemicalStore.selectedChemical.created_at).toLocaleString('sv-SE', { day: 'numeric', month: 'numeric', year: 'numeric' }) }}
                  </time>
                </p>
              </h1>

              <h1 class="text-md md:text-lg font-semibold text-slate-400 my-auto">
                <p>First published in
                  <time :datetime="selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', { day: 'numeric', month: 'numeric', year: 'numeric' })">
                    {{ selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) }}
                  </time>
                </p>
              </h1>
            </div>
          </div>
        </div>
        <div class="py-8">
          <div class="w-full grid grid-cols-1 2xl:grid-cols-2">
            <section data-aos="fade-up" class="space-y-4 w-full lg:w-3/4" id="2d_depiction">
              <h1 class="text-lg md:text-2xl font-bold">2D Depiction</h1>
              <div class="space-y-4">
                <div class="flex space-x-2">
                  <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-ghost md:btn-outline btn-primary btn-sm md:btn-md">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                      </svg>
                      <p class="font-semibold md:text-lg hidden md:flex">Structure Search</p>
                    </div>
                    <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box md:text-lg z-[1] w-52 p-2 shadow">
                      <li @click="similaritySearch"><a>Similarity</a></li>
                      <li @click="substructureSearch"><a>Substructure</a></li>
                    </ul>
                  </div>

                  <NuxtLink :to="selectedChemicalStore.selectedChemical.chem_depiction_image" target="_blank" type="button" class="btn btn-ghost md:btn-outline btn-primary btn-sm md:btn-md my-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                    </svg>
                    <p class="font-semibold md:text-lg hidden md:flex">Get Image</p>
                  </NuxtLink>
                </div>

                <figure class="pb-8">
                  <NuxtImg
                    :src="selectedChemicalStore.selectedChemical.chem_depiction_image"
                    alt="Molecular Structure"
                    class="rounded-box shadow-md duration-200 hover:shadow-xl"
                    format="svg"
                    loading="lazy"
                  />
                </figure>
              </div>
            </section>
            <section 
              data-aos="fade-up" 
              class="space-y-4 w-full lg:w-3/4" 
              id="3d_conformations"
              v-if="selectedChemicalStore.selectedChemical &&
              selectedChemicalStore.selectedChemical.conformation && 
              paginationStore.page > 0 &&
              selectedChemicalStore.selectedChemical.conformation[paginationStore.page - 1]"
            >
              <h1 class="text-lg md:text-2xl font-bold"> 3D Conformation </h1>

              <div class="flex space-x-2">
                <div class="dropdown">
                  <div tabindex="0" role="button" class="btn btn-ghost md:btn-outline btn-primary btn-sm md:btn-md">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                    </svg>
                    <p class="font-semibold md:text-lg hidden md:flex">Structure Search</p>
                  </div>
                  <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box md:text-lg z-[1] w-52 p-2 shadow">
                    <li @click="similaritySearch"><a>Similarity</a></li>
                    <li @click="substructureSearch"><a>Substructure</a></li>
                  </ul>
                </div>

                <div class="dropdown">
                  <div tabindex="0" role="button" class="btn btn-ghost md:btn-outline btn-primary btn-sm md:btn-md">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                    <p class="font-semibold md:text-lg hidden md:flex">Download Coordinates</p>
                  </div>
                  <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box md:text-lg z-[1] w-52 p-2 shadow">
                    <li>
                      <a 
                        :href="selectedChemicalStore.selectedChemical.conformation[paginationStore.page - 1].conf_file" 
                        :download="getFileName(selectedChemicalStore.selectedChemical.conformation[paginationStore.page - 1].conf_file)"
                        target="_blank" 
                        rel="noopener noreferrer" 
                      >
                        Current Conformation
                      </a>
                    </li>
                    <li>
                      <a
                        :href="getAllConformationsDownloadLink()"
                        :download="`${selectedChemicalStore.selectedChemical.api_id}_confs.zip`"
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        All conformations
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              <ngl-viewer
                :key="nglViewerKey" 
                :file="selectedChemicalStore.selectedChemical.conformation[paginationStore.page - 1].conf_file" 
                class="pb-8 rounded-box h-[12rem] md:h-[21rem] shadow-md duration-200 hover:shadow-xl"
              >
              </ngl-viewer>

              <div class="flex justify-center pb-8">
                <pagination></pagination>
              </div>
            </section>
          </div>
          
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="names_and_identifiers">
            <h1 class="text-lg md:text-2xl font-bold">Names and Identifiers</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Indentifier</th>
                    <th>Name</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>LabSOA ID</td>
                    <td>{{ selectedChemicalStore.selectedChemical.api_id }}</td>
                    <td>
                      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-dash-lg size-6 mx-auto" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2 8a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11A.5.5 0 0 1 2 8"/>
                      </svg>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>IUPAC Name</td>
                    <td>{{ selectedChemicalStore.selectedChemical.identifier.iupac_name }}</td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Molecular Formula</td>
                    <td>{{ selectedChemicalStore.selectedChemical.identifier.chem_formula }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Canonical SMILES</td>
                    <td>{{ selectedChemicalStore.selectedChemical.identifier.smiles }}</td>
                    <td>
                      Computed by 
                      <a 
                        class="link-lg link-sm" 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        href="https://pubs.acs.org/doi/10.1021/ci100384d"
                      > OPSIN
                      </a> 
                      (2.8.0v)</td>
                  </tr>
                  <tr class="hover">
                    <td>InChI</td>
                    <td>{{ selectedChemicalStore.selectedChemical.identifier.inchi }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>InChI Key</td>
                    <td>{{ selectedChemicalStore.selectedChemical.identifier.inchi_key }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>

          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="physical_property">
            <h1 class="text-lg md:text-2xl font-bold">Physical Property</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Molecular Weight</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.molecular_weight.toFixed(2) }} g/mol</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover" v-if="selectedChemicalStore.selectedChemical.physical_property.mp_lower_bound && selectedChemicalStore.selectedChemical.physical_property.mp_upper_bound">
                    <td>Melting Point</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.mp_lower_bound.toFixed(1) }} - {{ selectedChemicalStore.selectedChemical.physical_property.mp_upper_bound.toFixed(1) }} ℃</td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover" v-if="selectedChemicalStore.selectedChemical.physical_property.mp_lower_bound && !selectedChemicalStore.selectedChemical.physical_property.mp_upper_bound">
                    <td>Melting Point</td>
                    <td>≥ {{ selectedChemicalStore.selectedChemical.physical_property.mp_lower_bound.toFixed(1) }} ℃</td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover" v-if="!selectedChemicalStore.selectedChemical.physical_property.mp_lower_bound && selectedChemicalStore.selectedChemical.physical_property.mp_upper_bound">
                    <td>Melting Point</td>
                    <td>≤ {{ selectedChemicalStore.selectedChemical.physical_property.mp_upper_bound.toFixed(1) }} ℃</td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover" v-if="selectedChemicalStore.selectedChemical.physical_property.state_of_matter">
                    <td>State of Matter</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.state_of_matter }}</td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover" v-if="selectedChemicalStore.selectedChemical.physical_property.color">
                    <td>Color</td>
                    <td class="flex gap-2">
                      {{ selectedChemicalStore.selectedChemical.physical_property.color }}
                      <div :style="{ backgroundColor: selectedChemicalStore.selectedChemical.physical_property.color_hexadecimal }" class="size-4 mt-2 rounded-sm"></div>
                    </td>
                    <td>
                      <a 
                        :href="`${doiRedirectionSiteHost}${selectedChemicalStore.selectedChemical.literature[0].doi}`" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        {{ selectedChemicalStore.selectedChemical.literature[0].doi }}
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>H-Bond Acceptor Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_h_bond_acceptor }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>H-Bond Donor Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_h_bond_donor }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Rotatable Bond Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_rotatable_bond }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Atomic Volume</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.volume.toFixed(2) }} Å³</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Atom Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_atom }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Heavy Atom Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_heavy_atom }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Aromatic Heavy Atom Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_aromatic_heavy_atom }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Ring Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_ring }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Carbon Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_carbon }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Heteroatom Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physical_property.count_heteroatom }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="partition_coefficient">
            <h1 class="text-lg md:text-2xl font-bold">Partition Coefficient (LogPow)</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Wildman-Crippen LogP</td>
                    <td>{{ selectedChemicalStore.selectedChemical.partition_coefficient.wildman_crippen_logp.toFixed(2) }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/ci990307l" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/ci990307l
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>XLogP v2</td>
                    <td>{{ selectedChemicalStore.selectedChemical.partition_coefficient.xlogp.toFixed(2) }}</td>
                    <td>
                      <a 
                        href="https://link.springer.com/article/10.1023/A:1008763405023" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1023/A:1008763405023
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>JPLogP</td>
                    <td>{{ selectedChemicalStore.selectedChemical.partition_coefficient.jplogp.toFixed(2) }}</td>
                    <td>
                      <a 
                        href="https://link.springer.com/article/10.1186/s13321-018-0316-5" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1186/s13321-018-0316-5
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Mouriguchi LogP</td>
                    <td>{{ selectedChemicalStore.selectedChemical.partition_coefficient.mouriguchi_logp.toFixed(2) }}</td>
                    <td>
                      <a 
                        href="https://doi.org/10.1248/cpb.40.127" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1248/cpb.40.127
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="solubility">
            <h1 class="text-lg md:text-2xl font-bold">Solubility (LogS)</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>ESOL LogS</td>
                    <td>{{ selectedChemicalStore.selectedChemical.solubility.esol_logs.toFixed(2) }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/ci034243x" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/ci034243x
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Filter-It LogS</td>
                    <td>{{ selectedChemicalStore.selectedChemical.solubility.filter_it_logs.toFixed(2) }}</td>
                    <td>
                      Computed by Silicos-It's Filter-It 
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="physicochemical_property">
            <h1 class="text-lg md:text-2xl font-bold">Physicochemical Property</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Fraction of SP3 Hybridised Carbon Atoms</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physicochemical_property.fraction_csp3.toFixed(2) }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Molar Refractivity</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physicochemical_property.molar_refractivity.toFixed(2) }} cm³/mol</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Topological Polar Surface Area</td>
                    <td>{{ selectedChemicalStore.selectedChemical.physicochemical_property.tpsa.toFixed(2) }} Å²</td>
                    <td>Computed by RDKit</td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="qsar_score">
            <h1 class="text-lg md:text-2xl font-bold">QSAR Score</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Quantitative Estimate of Druglikeness (QED)</td>
                    <td>{{ selectedChemicalStore.selectedChemical.qsar_score.qed_score.toFixed(2) }}</td>
                    <td>Computed by RDKit</td>
                  </tr>
                  <tr class="hover">
                    <td>Synthetic Accessibility Score</td>
                    <td>{{ selectedChemicalStore.selectedChemical.qsar_score.synthetic_accessibility_score.toFixed(2) }}</td>
                    <td>
                      Computed by RDKit 
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Natural Product	Score</td>
                    <td>{{ selectedChemicalStore.selectedChemical.qsar_score.natural_product_score.toFixed(2) }}</td>
                    <td>
                      Computed by RDKit 
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="drug_like_rule">
            <h1 class="text-lg md:text-2xl font-bold">Drug-like Rule</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Lipinski Violation Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.druglike_rule.count_lipinski_violation }}</td>
                    <td>
                      <a 
                        href="https://doi.org/10.1016/S0169-409X(00)00129-0" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1016/S0169-409X(00)00129-0
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Ghose Violation Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.druglike_rule.count_ghose_violation }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/cc9800071" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/cc9800071
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Veber Violation Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.druglike_rule.count_veber_violation }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/jm020017n" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/jm020017n
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Egan Violation Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.druglike_rule.count_egan_violation }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/jm000292e" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/jm000292e
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Muegge Violation Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.druglike_rule.count_muegge_violation }}</td>
                    <td>
                      <a 
                        href="https://pubs.acs.org/doi/10.1021/jm015507e" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        10.1021/jm015507e
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="pharmacokinetics">
            <h1 class="text-lg md:text-2xl font-bold">Pharmacokinetics</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>Gastrointestinal Absorption</td>
                    <td>{{ selectedChemicalStore.selectedChemical.pharmacokinetics.gastrointestinal_absorption }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://chemistry-europe.onlinelibrary.wiley.com/doi/full/10.1002/cmdc.201600182" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        BOILED-Egg
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>Blood-Brain Barrier Permeation</td>
                    <td>{{ selectedChemicalStore.selectedChemical.pharmacokinetics.blood_brain_barrier_permeation }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.858126/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DeePred-BBB
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="p450_inhibition">
            <h1 class="text-lg md:text-2xl font-bold">P450 Inhibition</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>CYP1A2 Inhibitor</td>
                    <td>{{ selectedChemicalStore.selectedChemical.p450_inhibition.cyp1a2_inhibitor }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DEEPCYP
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>CYP2C9 Inhibitor</td>
                    <td>{{ selectedChemicalStore.selectedChemical.p450_inhibition.cyp2c9_inhibitor }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DEEPCYP
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>CYP2C19 Inhibitor</td>
                    <td>{{ selectedChemicalStore.selectedChemical.p450_inhibition.cyp2c19_inhibitor }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DEEPCYP
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>CYP2D6 Inhibitor</td>
                    <td>{{ selectedChemicalStore.selectedChemical.p450_inhibition.cyp2d6_inhibitor }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DEEPCYP
                      </a>
                    </td>
                  </tr>
                  <tr class="hover">
                    <td>CYP3A4 Inhibitor</td>
                    <td>{{ selectedChemicalStore.selectedChemical.p450_inhibition.cyp3a4_inhibitor }}</td>
                    <td>
                      Computed by
                      <a 
                        href="https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2023.1099093/full" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        class="link-lg link-sm"
                      >
                        DEEPCYP
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="pains_alert">
            <h1 class="text-lg md:text-2xl font-bold">PAINS Alert</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>PAINS Alert Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.undesirable_substructure_alert.count_pains_alert }}</td>
                    <td>
                      Computed by RDKit
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8" id="brenk_alert">
            <h1 class="text-lg md:text-2xl font-bold">BRENK Alert</h1>
            <div class="space-y-4 overflow-x-auto">
              
              <table class="ml-auto table table-auto table-zebra table-pin-rows">
                <!-- head -->
                <thead class="text-sm md:text-lg">
                  <tr>
                    <th>Property Name</th>
                    <th>Property Value</th>
                    <th>Reference</th>
                  </tr>
                </thead>
                <tbody class="text-sm md:text-lg font-normal">
                  <tr class="hover">
                    <td>BRENK Alert Count</td>
                    <td>{{ selectedChemicalStore.selectedChemical.undesirable_substructure_alert.count_brenk_alert }}</td>
                    <td>
                      Computed by RDKit
                    </td>
                  </tr>
                </tbody>
              </table>
              
            </div>
          </section>
          <section data-aos="fade-up" class="space-y-4 w-full pb-8 lg:w-5/6" id="reference">
            <h1 class="text-lg md:text-2xl font-bold">Reference</h1>
            <div class="space-y-4">
              <div class="rounded-box cursor-pointer p-4 transition-transform shadow-md duration-300 ease-in-out hover:scale-105 hover:shadow-xl" v-for="citation in selectedChemicalStore.selectedChemical.literature" :key="citation.api_id">
                <a :href="doiRedirectionSiteHost+citation.doi" target="_blank" rel="noopener noreferrer" >
                  <p class="text-primary font-semibold text-md md:text-lg">
                    {{ citation.doi }}
                  </p>
                  <p class="font-bold text-md md:text-xl">
                    {{ decodeHtml(citation.title) }}
                  </p>
                  <p class="text-slate-400 font-semibold">
                    {{ decodeHtml(citation.publication_name) }}
                  </p>
                  <p class="text-slate-400 font-semibold">
                    <time :datetime="selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', { day: 'numeric', month: 'numeric', year: 'numeric' })">
                      {{ selectedChemicalStore.getFirstPublicationDate().toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) }}
                    </time>
                  </p>
                </a>
                
              </div>
            </div>
          </section>
        </div>
      </div>
      <div class="w-1/4 hidden lg:flex lg:flex-col">
        <div class="mx-auto space-y-4 overflow-y-auto max-h-screen sticky top-0 p-4">
          <p class="text-xl font-bold">Table of Contents</p>
          <scrollspy 
            :sections="sectionsRef" 
            scrollspy-list="text-lg font-semibold" 
            scrollspy-item="py-1 pl-2 text-slate-400 hover:text-primary hover:border-primary hover:font-bold hover:rounded-sm  hover:border-l-4" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSelectedChemicalStore } from '~/stores/selectedChemicalStore';
import { useRoute } from 'vue-router';
import { useNuxtApp } from 'nuxt/app';
import { useRouter } from 'vue-router'
import { usePaginationStore } from '~/stores/paginationStore';
import { useThemeStore } from '~/stores/theme'
import { useFilterStore } from '~/stores/filterStore';
import { useFetchChemicalStore } from '~/stores/fetchChemicalStore';

import NglViewer from '~/components/NglViewer.vue';
import Pagination from '~/components/Pagination.vue';

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()

var nglViewerKey = ref(1)

const paginationStore = usePaginationStore()
const selectedChemicalStore = useSelectedChemicalStore()
const themeStore = useThemeStore()
const filterStore = useFilterStore()
const fetchChemicalStore = useFetchChemicalStore()


var isTableOfContentsOpened = ref(false)

const doiRedirectionSiteHost = "https://www.doi.org/"

const getAllConformationsDownloadLink = () => {
  return `${config.public.apiHost}${config.public.downloadChemicalConformationsEndpoint}${selectedChemicalStore.selectedChemical.api_id}/`
}

const toggleTableOfContents = () => {
  isTableOfContentsOpened.value = !isTableOfContentsOpened.value
}

const fetchSelectedChemicalDetail = async () => {
  selectedChemicalStore.reset()
  await selectedChemicalStore.fetchSelectedChemical(route.params.labsoadbId)
}

const getFileName = (url) => {
  return url.substring(url.lastIndexOf('/') + 1);
};

const similaritySearch = () => {
  const similarity_threshold = .85

  paginationStore.setPage(1);
  filterStore.clearFilter();

  filterStore.setExactFilter('similarity_threshold', similarity_threshold)

  filterStore.setExactFilter('query', selectedChemicalStore.selectedChemical.identifier.smiles)
  filterStore.setExactFilter('representation_type', 'smiles')
  filterStore.setExactFilter('search_type', 'similarity')
  
  fetchChemicalStore.setMode('summary')
  fetchChemicalStore.setType('search')
  fetchChemicalStore.fetchChemicals()

  router.push({
    path: '/chemicals/search'
  })
}

const substructureSearch = () => {
  paginationStore.setPage(1);
  filterStore.clearFilter();

  filterStore.setExactFilter('query', selectedChemicalStore.selectedChemical.identifier.smiles)
  filterStore.setExactFilter('representation_type', 'smiles')
  filterStore.setExactFilter('search_type', 'substructure')
  
  fetchChemicalStore.setMode('summary')
  fetchChemicalStore.setType('search')
  fetchChemicalStore.fetchChemicals()

  router.push({
    path: '/chemicals/search'
  })
}

function decodeHtml(html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}

onMounted(() => {
  fetchSelectedChemicalDetail().then(() => {
    // Verifica se os dados da molécula estão disponíveis e têm conformações
    const totalConformations = selectedChemicalStore.selectedChemical?.conformation?.length || 0;
  
    // Atualiza a paginação com base nos novos dados
    paginationStore.setTotalItems(totalConformations);
    paginationStore.setPageSize(1);
    paginationStore.calcTotalPages();
  
    paginationStore.setPage(1);
  })
})

const sectionsRef = ref([
  {
    id: "2d_depiction",
    label: "2D Depiction"
  },
  {
    id: "3d_conformations",
    label: "3D Conformation"
  },
  {
    id: 'names_and_identifiers',
    label: 'Names and Identifiers'
  },
  {
    id: "physical_property",
    label: "Physical Property"
  },
  {
    id: "partition_coefficient",
    label: "Partition Coefficient (LogPow)"
  },
  {
    id: "solubility",
    label: "Solubility (LogS)"
  },
  {
    id: "physicochemical_property",
    label: "Physicochemical Property"
  },
  {
    id: 'qsar_score',
    label: "QSAR Score"
  },
  {
    id: 'drug_like_rule',
    label: "Drug-like Rule"
  },
  {
    id: 'pharmacokinetics',
    label: "Pharmacokinetics"
  },
  {
    id: 'p450_inhibition',
    label: 'P450 Inhibition'
  },
  {
    id: 'pains_alert',
    label: 'PAINS Alert'
  },
  {
    id: 'brenk_alert',
    label: 'BRENK Alert'
  },
  {
    id: 'reference',
    label: 'Reference'
  }
])

watch(() => [paginationStore.page, themeStore.isDarkMode], () => {
  nglViewerKey.value *= -1 
})
</script>

<style scoped>
.link-sm {
  @apply link link-secondary;
}

.link-lg {
  @apply lg:link-primary duration-200 lg:hover:text-secondary;
}
</style>