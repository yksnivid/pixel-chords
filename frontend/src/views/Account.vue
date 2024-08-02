<template>
  <Header />
  <v-container fluid>
    <v-card
      v-if="!loading && !error"
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
      <v-list v-if="isCurrentUser">
        <ChangeEmail />
        <ChangePassword />
        <DeleteAccount />
      </v-list>
    </v-card>
    <v-progress-circular v-else-if="loading" indeterminate color="primary" />
    <v-alert v-else-if="error" type="error">{{ message }}</v-alert>


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
  props: {
    userId: {
      type: String,
      default: null,
      required: false
    }
  },
  data() {
    return {
      user: {
        type: Object,
        default: undefined
      },
      loading: false,
      error: null,
      message: ''
    }
  },
  async created() {
    if (!this.userId) {
      this.user = this.currentUser;
    } else {
      this.getUserInfo(this.userId).then(result => {
        this.user = result;
      })
    }
  },
  computed: {
    ...mapGetters({
      currentUser: 'user'
    }),
    isCurrentUser() {
      return this.currentUser.id === parseInt(this.userId) || !this.userId
    }
  },
  methods: {
    async getUserInfo(userId) {
      try {
        this.loading = true;
        this.error = false;
        const response = await fetch(`/api/users/${userId}`);
        if (response.status === 404) {
          this.error = true;
          this.message = 'User not found';
        }
        return response.json();
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>

</style>
