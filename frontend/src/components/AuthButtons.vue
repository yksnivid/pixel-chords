<template>
  <v-row align="center" justify="end">
    <v-col cols="auto" v-if="!isLoggedIn">
      <v-btn icon="mdi-account" @click="loginDialog = true" />
    </v-col>
    <template v-else>
      <v-col cols="auto">
        <v-menu v-model="menu" :close-on-content-click="false">
          <template v-slot:activator="{ props }">
            <v-avatar
              image="@/assets/avatar.png"
              size="40"
              v-bind="props"
            ></v-avatar>
          </template>
          <v-card>
            <v-card-title class="text-center">
              <v-avatar
                :class="isAdmin ? 'admin-avatar' : null"
                size="100"
                image="@/assets/avatar.png"
              ></v-avatar>
            </v-card-title>
            <v-card-subtitle class="text-center"> {{ userName }} </v-card-subtitle>

            <v-list density="compact" nav>
              <v-list-item title="Account" prepend-icon="mdi-account" @click="$router.push('/account')" />
              <v-list-item title="Favorites" prepend-icon="mdi-heart" @click="$router.push('/favorites')" />
              <v-list-item title="Sign out" prepend-icon="mdi-logout" @click="logout" />
            </v-list>
          </v-card>
        </v-menu>
      </v-col>
    </template>
    <LoginDialog v-model="loginDialog" />
  </v-row>
</template>

<script>
import LoginDialog from '@/components/LoginDialog.vue';
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'AuthButtons',
  components: {
    LoginDialog
  },
  data() {
    return {
      menu: false,
      loginDialog: false
    };
  },
  methods: {
    ...mapActions(['logout'])
  },
  computed: {
   ...mapGetters(['isLoggedIn', 'userName', 'isAdmin'])
  }
};
</script>

<style scoped>
.admin-avatar {
  box-shadow: 0 0 10px 2px red;
}
</style>
