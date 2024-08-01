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
    'user.id'(id) {
      console.log('Current user:', id)
      this.$router.go()
    }
  }
};
</script>
