<template>
    <div v-if="visible" :style="containerStyle">
      {{ message }}{{ dots }}
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoadingDots',
    props: {
      message: {
        type: String,
        default: '加载中，请稍候'
      },
      visible: {
        type: Boolean,
        default: true
      },
      interval: {
        type: Number,
        default: 500
      }
    },
    data() {
      return {
        dots: '',
        timer: null
      }
    },
    computed: {
      containerStyle() {
        return {
          position: 'fixed',
          left: '50%',
          top: "28px",
          transform: 'translate(-50%, -50%)',
          background: '#f0f9eb',
          color: '#67c23a',
          padding: '16px 24px',
          borderRadius: '6px',
          boxShadow: '0 2px 12px rgba(0, 0, 0, 0.1)',
          fontWeight: 'bold',
          zIndex: 9999,
          minWidth: '200px',
          textAlign: 'center',
          fontSize: '16px'
        };
      }
    },
    methods: {
      start() {
        this.dots = '';
        if (this.timer) clearInterval(this.timer);
        this.timer = setInterval(() => {
          if (this.dots.length >= 3) {
            this.dots = '';
          } else {
            this.dots += '.';
          }
        }, this.interval);
      },
      stop() {
        if (this.timer) {
          clearInterval(this.timer);
          this.timer = null;
        }
        this.dots = '';
      }
    },
    watch: {
      visible(newVal) {
        if (newVal) {
          this.start();
        } else {
          this.stop();
        }
      }
    },
    mounted() {
      if (this.visible) {
        this.start();
      }
    },
    beforeDestroy() {
      this.stop();
    }
  }
  </script>
  