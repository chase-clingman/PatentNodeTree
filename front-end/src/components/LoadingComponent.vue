<template>
  <div class="q-pa-md center">
    <transition-group name="fade" tag="div">
      <div :key="currentSpinner.type">
        <component
          :is="currentSpinner.type"
          color="primary"
          class=""
          size="6em"
        ></component>
        <q-tooltip v-model="showing" :offset="[0, 8]">{{ currentSpinner.message }}</q-tooltip>
      </div>
    </transition-group>
  </div>
</template>

<script>
import {
  QSpinnerOrbit,
  QSpinnerOval,
  QSpinnerPie,
  QSpinnerPuff,
  // import other spinners here
} from "quasar";

export default {
  name: "LoadingComponent",
  components: {
    "q-spinner-orbit": QSpinnerOrbit,
    "q-spinner-oval": QSpinnerOval,
    "q-spinner-pie": QSpinnerPie,
    "q-spinner-puff": QSpinnerPuff,
    // register other spinners here
  },
  data() {
    return {
      showing: true,
      spinners: [
        { type: "q-spinner-orbit", message: "This will take several minutes..." },
        { type: "q-spinner-oval", message: "Please be patient..." },
        { type: "q-spinner-pie", message: "Still working on it..." },
        { type: "q-spinner-puff", message: "Collecting Data..." },
        // Add the rest of your spinners and messages here...
      ],
      currentSpinnerIndex: 0,
    };
  },
  mounted() {
    setInterval(() => {
      this.currentSpinnerIndex =
        (this.currentSpinnerIndex + 1) % this.spinners.length;
        this.showing = true;
    }, 5000); // change spinner every 5 seconds
  },
  computed: {
    currentSpinner() {
      return this.spinners[this.currentSpinnerIndex];
    },
  },
};
</script>

<style scoped>
.center {
  position: absolute;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
  width: 100px; /* Need a specific value to work */
}
.fade-enter-active,
.fade-leave-active {
  position: absolute;
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
