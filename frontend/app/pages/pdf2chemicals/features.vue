<template>
  <Head>
    <Title>Features | PDF2Chemicals</Title>
  </Head>

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

  <div data-aos="fade-up" class="mx-auto w-[90%] flex flex-col py-4 lg:py-16">
    <div class="flex">
      <div class="w-full lg:w-[80%] flex flex-col">
        <div class="space-y-2">
          <h1 class="text-2xl md:text-6xl text-primary font-bold">
            PDF2Chemicals Features
          </h1>
          <h1 class="text-lg md:text-3xl font-semibold">
            Navigate through the many features of PDF2Chemicals
          </h1>
        </div>
        <div class="py-8 flex">
          <div class="w-[90%]">
            <section v-for="section in sectionsRef" data-aos="fade-up" :id="section.id" :key="section.id">
              <h1 class="text-lg md:text-3xl font-bold"> {{ section.label }} </h1>
              <div class="overflow-x-auto pb-16 pt-8">
                <table class="ml-auto table table-auto table-zebra table-pin-rows">
                  <thead class="text-lg">
                    <tr>
                      <th></th>
                      <th>Property</th>
                      <th>In CSV file</th>
                      <th>Data Type</th>
                    </tr>
                  </thead>
                  <tbody class="text-lg font-normal">
                    <tr v-for="row in section.rows" :id="row.id" :key="row.id" class="hover">
                      <th>{{ row.id }}</th>
                      <td>{{ row.property }}</td>
                      <td>{{ row.csv_representation }}</td>
                      <td>{{ row.data_type }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>
          </div>
        </div>
      </div>
      <div class="w-[20%] hidden lg:flex lg:flex-col">
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
import Scrollspy from '~/components/Scrollspy.vue';
import { useThemeStore } from '~/stores/theme';

const themeStore = useThemeStore()
const currTheme = computed(() => themeStore.currentTheme)

var isTableOfContentsOpened = ref(false)

const toggleTableOfContents = () => {
  isTableOfContentsOpened.value = !isTableOfContentsOpened.value
}

const sectionsRef = ref([
  { 
    id: 'identifier',
    label: 'Identifier',
    rows: [
      {
        id: 1,
        property: 'IUPAC Name',
        csv_representation: 'iupac',
        data_type: 'String'
      },
      {
        id: 2,
        property: 'Chemical Formula',
        csv_representation: 'formula',
        data_type: 'String'
      },
      {
        id: 3,
        property: 'PDF2Chemicals Chemical Id',
        csv_representation: 'id',
        data_type: 'String'
      },
      {
        id: 4,
        property: 'Chemical Reference Index',
        csv_representation: 'reference_index',
        data_type: 'String'
      },
      {
        id: 5,
        property: 'InChi',
        csv_representation: 'inchi',
        data_type: 'String'
      },
      {
        id: 6,
        property: 'InChI Key',
        csv_representation: 'inchi_key',
        data_type: 'String'
      },
      {
        id: 7,
        property: 'SMILES',
        csv_representation: 'smiles',
        data_type: 'String'
      }
    ]
  },
  { id: 'physical-property',
    label: 'Physical Property',
    rows: [
      {
        id: 1,
        property: 'Atomic Volume',
        csv_representation: 'volume',
        data_type: 'Float'
      },
      {
        id: 2,
        property: 'Atom Count',
        csv_representation: 'num_atom',
        data_type: 'Integer'
      },
      {
        id: 3,
        property: 'Heavy Atom Count',
        csv_representation: 'num_heavy_atom',
        data_type: 'Integer'
      },
      {
        id: 4,
        property: 'Aromatic Heavy Atom Count',
        csv_representation: 'num_arom_heavy_atom',
        data_type: 'Integer'
      },
      {
        id: 5,
        property: 'Rotatable Bond Count',
        csv_representation: 'num_rotatable_bond',
        data_type: 'Integer'
      },
      {
        id: 6,
        property: 'H-Bond Acceptor Count',
        csv_representation: 'num_h_bond_accept',
        data_type: 'Integer'
      },
      {
        id: 7,
        property: 'H-Bond Donor Count',
        csv_representation: 'num_h_bond_donor',
        data_type: 'Integer'
      },
      {
        id: 8,
        property: 'Ring Count',
        csv_representation: 'num_ring',
        data_type: 'Integer'
      },
      {
        id: 9,
        property: 'Carbon Count',
        csv_representation: 'num_carbon',
        data_type: 'Integer'
      },
      {
        id: 10,
        property: 'Heteroatom Count',
        csv_representation: 'num_heteroatom',
        data_type: 'Integer'
      }
    ] 
  },
  { id: 'physicochemical-property',
    label: 'Physicochemical Property',
    rows: [
      {
        id: 1,
        property: 'Molecular Weight (MW)',
        csv_representation: 'mass_weight',
        data_type: 'Float'
      },
      {
        id: 2,
        property: 'Fraction of SP3 Hybridised Carbon Atoms',
        csv_representation: 'fraction_csp3',
        data_type: 'Float between 0 and 1'
      },
      {
        id: 3,
        property: 'Molar Refractivity (MR)',
        csv_representation: 'molar_refractivity',
        data_type: 'Float'
      },
      {
        id: 4,
        property: 'Topological Polar Surface Area (TPSA)',
        csv_representation: 'tpsa',
        data_type: 'Float'
      }
    ]
  },
  {
    id: 'experimental-melting-point',
    label: 'Experimental Melting Point',
    rows: [
      {
        id: 1,
        property: 'Melting Point Lower Bound',
        csv_representation: 'melting_point_lower_bound',
        data_type: 'Float'
      },
      {
        id: 2,
        property: 'Melting Point Upper Bound',
        csv_representation: 'melting_point_upper_bound',
        data_type: 'Float'
      },
    ]
  },
  {
    id: 'experimental-state-of-matter',
    label: 'Experimental State of Matter',
    rows: [
      {
        id: 1,
        property: 'State of Matter',
        csv_representation: 'state_of_matter',
        data_type: 'String'
      },
      {
        id: 2,
        property: 'Color',
        csv_representation: 'color',
        data_type: 'String'
      },
      {
        id: 3,
        property: 'Color Hexadecimal',
        csv_representation: 'color_hex_value',
        data_type: 'String'
      },
    ]
  },
  {
    id: 'log-pow',
    label: 'Partition Coefficient (LogPow)',
    rows: [
      {
        id: 1,
        property: 'Wildman-Crippen LogP',
        csv_representation: 'wlogp',
        data_type: 'Float'
      },
      {
        id: 2,
        property: 'XLogP v2',
        csv_representation: 'xlogp2',
        data_type: 'Float'
      },
      {
        id: 3,
        property: 'JPLogP',
        csv_representation: 'jplogp',
        data_type: 'Float'
      },
      {
        id: 4,
        property: 'Mouriguchi LogP',
        csv_representation: 'mlogp',
        data_type: 'Float'
      },
      {
        id: 5,
        property: 'Consensus LogP',
        csv_representation: 'consensus_logp',
        data_type: 'Float'
      }
    ]
  },
  {
    id: 'log-s',
    label: 'Solubility (LogS)',
    rows: [
      {
        id: 1,
        property: 'ESOL LogS',
        csv_representation: 'esol_logs',
        data_type: 'Float'
      },
      {
        id: 2,
        property: 'Filter-It LogS',
        csv_representation: 'filter_it_logs',
        data_type: 'Float'
      }
    ]
  },
  { 
    id: 'qsar-score', 
    label: 'QSAR Score',
    rows: [
      {
        id: 1,
        property: 'Quantitative Estimate of Druglikeness (QED)',
        csv_representation: 'qed_score',
        data_type: 'Float between 0 and 1'
      },
      {
        id: 2,
        property: 'Synthetic Accessibility',
        csv_representation: 'synthetic_accessibility_score',
        data_type: 'Float between 1 and 10'
      },
      {
        id: 3,
        property: 'Natural Product',
        csv_representation: 'natural_product_score',
        data_type: 'Float between -5 and 5'
      }
    ]
  },
  { 
    id: 'drug-like-rule',
    label: 'Drug-like Rule',
    rows: [
      {
        id: 1,
        property: 'Lipinski Violation Count',
        csv_representation: 'num_lipinski_violation',
        data_type: 'Integer'
      },
      {
        id: 2,
        property: 'Ghose Violation Count',
        csv_representation: 'num_ghose_violation',
        data_type: 'Integer'
      },
      {
        id: 3,
        property: 'Veber Violation Count',
        csv_representation: 'num_veber_violation',
        data_type: 'Integer'
      },
      {
        id: 4,
        property: 'Egan Violation Count',
        csv_representation: 'num_egan_violation',
        data_type: 'Integer'
      },
      {
        id: 5,
        property: 'Muegge Violation Count',
        csv_representation: 'num_muegge_violation',
        data_type: 'Integer'
      },
    ] 
  },
  { 
    id: 'pharmacokinetics', 
    label: 'Pharmacokinetics',
    rows: [
      {
        id: 1,
        property: 'Gastrointestinal Absorption',
        csv_representation: 'gi_absorption',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 2,
        property: 'Blood-Brain Barrier Permeation',
        csv_representation: 'bbb_permeant',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 3,
        property: 'Skin Permeation (LogKp)',
        csv_representation: 'logkp',
        data_type: 'Float'
      }
    ]
  },
  {
    id:'p450-inhibition',
    label: 'P450 Inhibition',
    rows: [
      {
        id: 1,
        property: 'CYP1A2 Inhibitor',
        csv_representation: 'cyp1a2_inhibitor',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 2,
        property: 'CYP2C9 Inhibitor',
        csv_representation: 'cyp2c9_inhibitor',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 3,
        property: 'CYP2C19 Inhibitor',
        csv_representation: 'cyp2c19_inhibitor',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 4,
        property: 'CYP2D6 Inhibitor',
        csv_representation: 'cyp2d6_inhibitor',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 5,
        property: 'CYP3A4 Inhibitor',
        csv_representation: 'cyp3a4_inhibitor',
        data_type: 'Integer 0 (false) or 1 (true)'
      }
    ]
  },
  {
    id: 'pains-violation',
    label: 'PAINS Violation',
    rows: [
      {
        id: 1,
        property: 'PAINS Violation Count',
        csv_representation: 'num_pains_violation',
        data_type: 'Integer'
      },
    ]
  },
  {
    id: 'brenk-violation',
    label: 'BRENK Violation',
    rows: [
      {
        id: 1,
        property: 'BRENK Violation Count',
        csv_representation: 'num_brenk_violation',
        data_type: 'Integer'
      },
    ]
  },
  { 
    id: 'toxicity', 
    label: 'Toxicity',
    rows: [
      {
        id: 1,
        property: 'Cardiotoxicity Prediction',
        csv_representation: 'cardiotoxicity_prediction',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 2,
        property: 'Hepatotoxicity Prediction',
        csv_representation: 'hepatotoxicity_prediction',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
      {
        id: 3,
        property: 'Ames Mutagenesis Prediction',
        csv_representation: 'ames_mutagenesis_prediction',
        data_type: 'Integer 0 (false) or 1 (true)'
      },
    ]
  },
  {
    id: 'literature',
    label: 'Literature',
    rows: [
      {
        id: 1,
        property: 'Document Id',
        csv_representation: 'document_id',
        data_type: 'String'
      },
      {
        id: 2,
        property: 'DOI',
        csv_representation: 'doi',
        data_type: 'String'
      }
    ]
  },
  { 
    id: 'molecular-conformation', 
    label: 'Molecular Conformation',
    rows: [
      {
        id: 1,
        property: 'Generation of a Given Number of Molecule Conformations',
        csv_representation: '—',
        data_type: '—'
      }
    ]
  },
  {
    id: 'directory-path',
    label: 'Chemical Directory Path',
    rows: [
      {
        id: 1,
        property: 'Directory path where all PDB, MOL2, SDF, etc, files generated for each chemical are located',
        csv_representation: 'compound_path',
        data_type: 'String'
      }
    ]
  }
])

watch(currTheme, (newTheme) => {
  if(process.client) {
    document.documentElement.setAttribute('data-theme', newTheme)
  }
})

</script>
<style scoped>
  .table-of-contents[data-theme='winter'] {
    border-top-width: 1px;
    border-bottom-width: 1px;
    border-top-color: #e2e8f0;
    border-bottom-color: #e2e8f0;
  }

  .table-of-contents[data-theme='night'] {
    border-top-width: 1px;
    border-bottom-width: 1px;
    border-top-color: #1e293b;
    border-bottom-color:#1e293b;
  }
</style>