<template>
  <q-page class="">
    <!-- <div class="q-pa-md">
      <q-input v-model="applicationNumber" label="Application Number" />
      <q-btn @click="fetchData" label="Fetch Data" />
    </div> -->
    <div class="center q-my-md" style="width: 100%; max-width: 1200px">
      <q-form style="width: 100%; max-width: 1200px" class="row">
        <q-input
          outlined
          v-model="applicationNumber"
          label="Enter Application Number or URL . . ."
          style="width: 100%; max-width: 1600px"
          class="col"
        >
          <!-- <template v-slot:append> </template>
          <template v-slot> </template> -->
        </q-input>
        <q-input
          class="col"
          v-model.number="num"
          min="1"
          type="number"
          label="Depth of Tree"
          outlined
          style="max-width: 200px"
        />
        <q-btn
          outline
          style="height: 55px"
          class="col-1 text-primary"
          icon="chevron_right"
          @click="fetchData"
        />
      </q-form>
    </div>
    <LoadingComponent v-if="loading" />
    <div v-if="data">
      <tree-node
        :tree-data="data"
        :width="900"
        :height="900"
        class=""
      ></tree-node>
      <!-- print the raw data -->
      <pre>{{ data }}</pre>
    </div>
  </q-page>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import TreeNode from "../components/TreeNode.vue";
import LoadingComponent from "../components/LoadingComponent.vue";

export default {
  name: "IndexPage",
  components: {
    TreeNode,
    LoadingComponent,
  },
  setup() {
    const applicationNumber = ref("");
    const num = ref(1);
    const data = ref(null);
    const loading = ref(false);

    const sanitizeApplicationNumber = (input) => {
      // Decode the URI components first to simplify replacements
      // let result = decodeURIComponent(input);
      let result = input;
      console.log(result);
      // Strip URL elements if present
      if (result.startsWith("https://patentcenter.uspto.gov/applications/")) {
        result = result.replace(
          "https://patentcenter.uspto.gov/applications/",
          ""
        );

        // Strip any trailing elements after the application number
        let slashIndex = result.indexOf("/");
        if (slashIndex !== -1) {
          result = result.substring(0, slashIndex);
        }
      }
      else {
        // remove all /
        result = result.replace(/\//g, "");
        // remove all ,
        result = result.replace(/,/g, "");
      }

      // Remove any commas
      // result = result.replace(/,/g, "");

      // Encode the result to make it safe for a URL
      result = encodeURIComponent(result);
      console.log(result);
      return result;
    };

    const fetchData = async () => {
      loading.value = true;

      // Sanitize the application number
      const sanitizedApplicationNumber = sanitizeApplicationNumber(
        applicationNumber.value
      );

      const response = await axios.get(
        `https://8f03-2601-98a-4002-b580-e7ec-3235-8f7e-d30d.ngrok-free.app/get_data/${sanitizedApplicationNumber}?max_depth=${num.value}`
      );
      data.value = {
        id: sanitizedApplicationNumber,
        children: response.data.children,
      };
      loading.value = false;
    };

    return {
      loading,
      num,
      applicationNumber,
      data,
      fetchData,
    };
  },
};
</script>
<style scoped>
.center {
  margin-left: auto;
  margin-right: auto;
}
</style>
