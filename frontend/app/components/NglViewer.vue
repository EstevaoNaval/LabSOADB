<template>
  <div id="viewport" ref="viewport"></div>
</template>

<script>
import * as NGL from 'ngl';
import { useThemeStore } from '~/stores/theme.js'

export default {
  name: 'NglViewer',
  
  data() {
    return {
      theme: useThemeStore()
    }
  },
  methods: {
    initNGL() {
      this.stage = new NGL.Stage(this.$refs.viewport, { backgroundColor: this.theme.isDarkMode ? "black" : "white" });

      window.addEventListener('resize', () => {
        this.stage.handleResize();
      });
    },
    loadMolecule() {
      this.stage.removeAllComponents();

      this.stage.loadFile(this.file, { ext: 'sdf' }).then((o) => {
        o.addRepresentation('ball+stick', {
          aspectRatio: 2.0,
          multipleBond: 'symmetric',
          lineWidth: 2,
          roughness: 0.2,
          metalness: 0,
          radius: 0.15,
          scale: 0.1,
          radiusType: 'vdw',
          bondScale: 0.75,
          bondSpacing: 2,
          clipNear: 0
        });
        o.autoView();
      });
    },
    toggleSpin() {
      this.stage.toggleSpin()
    },
    toggleRock() {
      this.stage.toggleRock()
    }
  },
  props: {
    file: {
      type: String,
      required: true
    }
  },
  mounted() {
    this.initNGL();
    this.loadMolecule();
  }
};
</script>

<style scoped>
</style>
