<template>
  <v-app-bar app>
    <v-toolbar-title>
      <v-avatar
        image="@/assets/logo.png"
        size="80"
      />
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text @click="$router.push('/')">Home</v-btn>
    <v-btn text @click="$router.push({ name: 'authors' })">Authors</v-btn>
    <v-btn v-if="!isLoggedIn" text @click="$router.push('/login')">Login</v-btn>
    <v-btn v-if="isLoggedIn" text @click="logout">Logout</v-btn>
    <v-btn v-if="isAdmin" text @click="$router.push('/admin')">Admin Panel</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'Header',
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
    isAdmin() {
      return this.$store.getters.isAdmin;
    }
  },
  methods: {
    async logout() {
      try {
        await fetch('/api/logout', {
          method: 'POST',
          credentials: 'include' // Включаем куки в запрос
        });
        this.$store.dispatch('logout'); // Диспатчим действие logout
        this.$router.push('/login');
      } catch (error) {
        console.error('Failed to logout:', error);
      }
    }
  },
  created() {
    this.$store.dispatch('login'); // Проверяем статус авторизации при создании компонента
  }
};
</script>

<style scoped>
</style>
