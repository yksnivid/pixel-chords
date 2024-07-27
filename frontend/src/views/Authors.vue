<template>
  <Header />
  <v-container fluid>
    <v-fab
      v-if="user.isAdmin"
      icon="mdi-plus"
      class="mb-10"
      color="primary"
      location="bottom end"
      size="40"
      offset
      appear
      app
      @click.stop="editorDialog = true"
    ></v-fab>
    <AuthorsList :authors="authors" />
    <AuthorEditor v-model="editorDialog" />
  </v-container>
</template>

<script>
import Header from '@/components/Header.vue';
import {mapGetters} from "vuex";
import AuthorButtons from "@/components/AuthorButtons.vue";
import AuthorsList from "@/components/AuthorsList.vue";
import AuthorEditor from "@/components/AuthorEditor.vue";

export default {
  name: 'Authors',
  components: {
    AuthorEditor,
    AuthorsList,
    AuthorButtons,
    Header
  },
  data() {
    return {
      authors: [],
      editorDialog: false
    };
  },
  async created() {
    await this.fetchAuthors();
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    async fetchAuthors() {
      try {
        const response = await fetch('/api/authors');
        if (!response.ok) {
          throw new Error('Failed to fetch authors');
        }
        this.authors = await response.json();
      } catch (error) {
        console.error('Error fetching authors:', error);
      }
    }
  }
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
}
</style>
