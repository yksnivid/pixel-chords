<template>
  <Header />
  <v-container fluid>
    <v-card :title="user.user" :subtitle="user.isAdmin ? 'Admin' : 'User' ">
      <template v-slot:prepend>
        <v-avatar
          color="error"
          size="80"
        >
          <div class="text-h4 font-weight-bold">{{ user.user ? user.user[0].toUpperCase() : null }}</div>
        </v-avatar>
      </template>
      <v-list>
        <v-list-item title="Change email" prepend-icon="mdi-email" />
        <v-list-item title="Change password" prepend-icon="mdi-key" />
        <v-list-item title="Delete account" prepend-icon="mdi-delete" />
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "Account",
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
  watch: {
    'user.user'(state) {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>

</style>
