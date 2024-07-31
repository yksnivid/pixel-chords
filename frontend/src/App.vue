<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Footer from './components/Footer.vue';
import {mapGetters} from "vuex";

export default {
  name: 'App',
  components: {
    Footer
  },
  computed: {
    ...mapGetters(['user'])
  },
  watch: {
    'user.id'() {
      console.log('RUNNING')
      this.$router.go()
    }
  }
};
</script>
