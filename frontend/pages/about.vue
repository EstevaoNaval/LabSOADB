<template>
  <Head>
    <Title>About | LabSOADB</Title>
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
            About LabSOADB
          </h1>
        </div>
        <div class="py-8 flex">
          <div class="w-[90%]">
            <section data-aos="fade-up" id="introduction">
              <h1 class="text-lg md:text-3xl font-bold">Introduction</h1>
              <div class="overflow-x-auto pb-16 pt-8 text-lg md:text-xl space-y-4">
                <p>
                  LabSOADB is a <b>open database</b> of chemicals gathered solely from <b>automated chemical extraction</b> from literature. 
                  Using <b>data mining techniques</b>, enhanced with <b>NLP</b>, <b>Machine Learning</b> and <b>Deep Learning</b>, all chemicals that compose LabSOADB were exctracted
                  from manuscripts, msc dissertations, thesis, etc, in a automated way.
                </p>
                <p>
                  LabSOADB exists with the purpose of leading a <b>family of databases composed by chemical data, automatically, mined from several unstructured data sources</b>. 
                  Using <NuxtLink to="/pdf2chemicals/about" class="link-sm link-lg">PDF2Chemicals</NuxtLink> to be this mining tool, LabSOADB become a 
                  proof of concept (PoC) to demonstrate that <b>is possible to populate chemical databases, requiring minimal human interference</b>.
                </p>
              </div>
            </section>
            <section data-aos="fade-up" id="uff-labsoa-project">
              <h1 class="text-lg md:text-3xl font-bold">The UFF-LabSOA project</h1>
              <div class="overflow-x-auto pb-16 pt-8 text-lg md:text-xl space-y-4">
                <p>
                  One of the core problems faced by cheminformatics nowadays is the limited amount of structured experimental data. 
                  Chemoinformatics, primarily, works with the use of <i>in silico</i> data processing in order to generate chemical attributes 
                  that, previously, could only be generated through laboratory experiments.
                </p>
                <p>
                  With the advent of the information age, accompanied by machine and deep learning techniques, 
                  the priority of more structured data went from an optional status to an extremely urgent need, 
                  considering that machine and deep learning models, to generate good results, need a large amount of structured data.
                </p>
                <p>
                  With the purpose of solve this problem, the project UFF-LabSOA born, dividing itself in two steps. 
                  The first step was creating a tool, called <NuxtLink to="/pdf2chemicals/about" class="link-sm link-lg">PDF2Chemicals</NuxtLink>, 
                  to extract those experimental data scattered through manuscripts, thesis, books, etc. As an initial test, 
                  we use <NuxtLink to="/pdf2chemicals/about" class="link-sm link-lg">PDF2Chemicals</NuxtLink> to extract the organic compounds 
                  synthetized by brazilian <a href="https://en.wikipedia.org/wiki/Fluminense_Federal_University" class="link-sm link-lg">Federal Fluminense University's</a> 
                  <a class="link-sm link-lg" href="https://international.uff.br/project/laboratory-of-applied-organic-synthesis/" >Organic Synthesis Lab (UFF-LabSOA)</a>, therefore, the name of the project.
                </p>
                <p>
                  The next step was create a database, called <NuxtLink to="/home" class="link-sm link-lg">LabSOADB</NuxtLink>, populated with those extracted data,
                  to <b>democratize the access of those data for the scientific community</b>. Also, to <b>ease the search and download of <NuxtLink to="/home" class="link-sm link-lg">LabSOADB</NuxtLink></b>, 
                  this website created, <b>allowing any non-technical user to access the gathered experimental data inserted in our database</b>.
                </p>
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

var isTableOfContentsOpened = ref(false)

const toggleTableOfContents = () => {
  isTableOfContentsOpened.value = !isTableOfContentsOpened.value
}

const sectionsRef = ref([
  {
    id: 'introduction',
    label: 'Introduction',
  },
  {
    id: 'uff-labsoa-project',
    label: 'The UFF-LabSOA project'
  }
])
</script>

<style scoped>
.link-sm {
  @apply link link-secondary;
}

.link-lg {
  @apply lg:link-primary duration-200 lg:hover:text-secondary;
}
</style>