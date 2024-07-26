<template>
  <v-btn
    :color="author.isFavorite ? 'red' : 'medium-emphasis'"
    icon="mdi-heart"
    size="small"
    variant="plain"
    @click.stop="toggleFavorite"
  ></v-btn>
  <v-btn
    icon="mdi-share-variant"
    size="small"
    variant="plain"
    @click.stop="share"
  ></v-btn>
  <LoginDialog v-model="loginDialog" />
</template>

<script>
import LoginDialog from "@/components/LoginDialog.vue";
import {mapGetters} from "vuex";

export default {
  name: "AuthorButtons",
  components: {LoginDialog},
  props: {
    author: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      loginDialog: false
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    share() {
      console.log('Share author, id: ' + this.author.id);
    },
    async toggleFavorite() {
      if (!this.user.isLoggedIn) {
        this.loginDialog = true;
        return;
      }
      try {
        this.author.isFavorite = !this.author.isFavorite;

        const method = this.author.isFavorite ? 'POST' : 'DELETE';

        const response = await fetch(`/api/users/${this.user.id}/favorites`, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ item_type: 'author', item_id: this.author.id })
        });

        if (!response.ok) {
          throw new Error('Failed to toggle favorite');
        }
        const data = await response.json();
        console.log(`${data.message}, author id: ${this.author.id}`);
      } catch (error) {
        console.error('Error toggling favorite:', error);
        // Revert the isFavorite status in case of an error
        this.author.isFavorite = !this.author.isFavorite;
      }
    }
  }
}
</script>

<style scoped>

</style>
