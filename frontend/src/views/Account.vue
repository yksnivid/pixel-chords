<template>
  <Header />
  <v-container fluid>
    <v-card
      :title="user.username"
      :subtitle="user.isAdmin ? 'Admin' : 'User'"
    >
      <template v-slot:prepend>
        <v-avatar
          color="error"
          size="80"
        >
          <div class="text-h4 font-weight-bold">
            {{ user.username ? user.username[0].toUpperCase() : null }}
          </div>
        </v-avatar>
      </template>
      <v-list>
        <ChangeEmail />
        <ChangePassword />
        <DeleteAccount />
      </v-list>
    </v-card>


  </v-container>
</template>

<script>
import {mapGetters} from "vuex";
import ChangeEmail from "@/components/account/ChangeEmail.vue";
import ChangePassword from "@/components/account/ChangePassword.vue";
import DeleteAccount from "@/components/account/DeleteAccount.vue";

export default {
  name: "Account",
  components: {ChangeEmail, DeleteAccount, ChangePassword},
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters(['user'])
  }
}
</script>

<style scoped>

</style>
