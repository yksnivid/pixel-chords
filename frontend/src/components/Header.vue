<template>
  <v-app-bar>
    <v-container fluid>
      <v-row align="center" justify="space-between" no-gutters>
        <v-col cols="2">
          <Logo />
        </v-col>
        <v-col>
          <Search />
        </v-col>
        <v-col cols="2">
          <AuthButtons />
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script>
import Logo from '@/components/Logo.vue';
import AuthButtons from '@/components/AuthButtons.vue';
import Search from '@/components/Search.vue';

export default {
  name: 'Header',
  components: {
    Logo,
    AuthButtons,
    Search
  }
};
</script>

<style scoped>
</style>
