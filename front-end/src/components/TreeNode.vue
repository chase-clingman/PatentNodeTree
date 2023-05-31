<template>
  <div class="tree-container">
    <svg
      ref="svg"
      width="100%"
      height="100%"
      :viewBox="`0 0 ${calculatedWidth} ${calculatedHeight}`"
    >
      <g ref="g">
        <!-- :transform="`translate(${width / 2}, ${height / 2})`" -->
        <!-- Loop for links -->
        <template v-for="(d, index) in root.descendants()" :key="'link-' + index">
          <line
            class="link"
            v-if="d.parent"
            :x1="d.x"
            :y1="d.y + nodeRadius"
            :x2="d.parent.x"
            :y2="d.parent.y + nodeRadius"
            stroke="#000080"
          ></line>
        </template>
        <!-- Loop for nodes -->
        <template v-for="(d, index) in root.descendants()" :key="'node-' + index">
          <rect
            class="node"
            :x="d.x - 1.5 * nodeRadius"
            :y="d.y - 0.1 * nodeRadius"
            :width="3 * nodeRadius"
            :height="3 * nodeRadius"
            rx="0"
            ry="0"
            fill="#ccc"
          ></rect>

          <foreignObject
            :x="d.x - 1.5 * nodeRadius"
            :y="d.y - 0.1 * nodeRadius"
            :width="3 * nodeRadius"
            :height="3 * nodeRadius"
          >
            <div xmlns="http://www.w3.org/1999/xhtml" class="node-content">
              <h4>{{ d.data.id }}</h4>
              <!-- <p>{{ d.data.details }}</p> -->
              <!-- grab each item in data.details array -->
              <p v-for="(item, index) in d.data.details" :key="index">
                {{ item }}
              </p>
            </div>
          </foreignObject>
        </template>
      </g>
    </svg>
  </div>
</template>


<script>
import { hierarchy } from "d3-hierarchy";
import { tree } from "d3";
import { zoom as d3Zoom } from "d3-zoom";
import { select as d3Select } from "d3-selection";

export default {
  name: "TreeNode",
  props: {
    nodeRadius: {
      type: Number,
      default: 50,
    },
    treeData: {
      type: Object,
      required: true,
    },
    width: {
      type: Number,
      default: 2000, // This is now your "logical" width, not CSS pixels
    },
    height: {
      type: Number,
      default: 2000, // This is now your "logical" height, not CSS pixels
    },
  },
  methods: {
    applyZoom() {
      const svg = d3Select(this.$refs.svg);
      const g = d3Select(this.$refs.g);
      const zoom = d3Zoom()
        .scaleExtent([0.5, 5]) // Limit zoom out and zoom in
        .translateExtent([
          [0, 0],
          [this.calculatedWidth + 10 * this.nodeRadius, this.calculatedHeight], // Update here
        ]) // Limit panning
        .on("zoom", (event) => {
          g.attr("transform", event.transform);
        });

      svg.call(zoom);
    },
  },

  mounted() {
    this.applyZoom();
  },

  computed: {
    numNodes() {
      let numNodes = 0;
      hierarchy(this.treeData).each(() => {
        numNodes++;
      });
      return numNodes;
    },
    calculatedWidth() {
      return Math.max(2000, 200 * Math.sqrt(this.numNodes));
    },
    calculatedHeight() {
      return this.calculatedWidth;
    },
    root() {
      const hierarchicalData = hierarchy(this.treeData);
      const treeLayout = tree().size([
      this.calculatedWidth + 10 * this.nodeRadius,
        this.calculatedHeight - 2.2 * this.nodeRadius,
      ]);
      return treeLayout(hierarchicalData);
    },
  },
};
</script>

<style scoped>
.tree-container {
  width: 60%;
  height: 80vh;
  margin: 0 auto;
  border: 1px solid #ccc;
}

.link {
  fill: none;
}

.node {
  stroke: #fff;
  stroke-width: 3px;
}
.node-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: #ccc;
}

.node-content h4 {
  margin: 0;
  padding: 0;
  font-size: 14px;
  color: #000;
}

.node-content p {
  margin: 0;
  padding: 0;
  font-size: 10px;
  color: #000;
}
</style>
