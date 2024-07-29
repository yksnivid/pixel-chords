<template>
  <v-row align="center" justify="end">
    <v-col cols="auto" v-if="!user.isLoggedIn">
      <v-avatar color="grey-darken-3" icon="mdi-account" @click="loginDialog = true" />
    </v-col>
    <template v-else>
      <v-col cols="auto">
        <v-menu v-model="menu" :close-on-content-click="false">
          <template v-slot:activator="{ props }">
            <v-avatar
              size="40"
              v-bind="props"
              color="error"
            ><div class="text-h6 font-weight-bold">{{ user.user[0].toUpperCase() }}</div></v-avatar>
          </template>
          <v-card>
            <v-card-title class="text-center">
              <v-avatar
                :class="user.isAdmin ? 'admin-avatar' : null"
                size="100"
                color="error"
              ><div class="text-h3 font-weight-bold">{{ user.user[0].toUpperCase() }}</div></v-avatar>
            </v-card-title>
            <v-card-title class="text-center"> {{ user.user }} </v-card-title>

            <v-list density="compact">
              <v-list-item density="compact" title="Light theme">
                <template v-slot:prepend>
                  <v-switch
                    :model-value="theme.global.name.value === 'light'"
                    class="pr-3"
                    hide-details
                    @click="toggleTheme"
                  ></v-switch>
                </template>
              </v-list-item>
              <v-divider></v-divider>
              <v-list-item title="Account" prepend-icon="mdi-account" @click="$router.push('/account')" />
              <v-list-item title="Favorites" prepend-icon="mdi-heart" @click="$router.push('/account/favorites')" />
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
import { mapActions, mapGetters } from "vuex";

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
   ...mapGetters(['user'])
  }
};
</script>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

const savedTheme = localStorage.getItem('theme');

if (savedTheme) {
  theme.global.name.value = savedTheme;
} else {
  theme.global.name.value = theme.global.current.value.dark ? 'dark' : 'light';
}

function toggleTheme () {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  localStorage.setItem('theme', theme.global.name.value);
}
</script>

<style scoped>
</style>
