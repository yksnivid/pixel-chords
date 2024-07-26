<template>
  <Header />
  <v-container fluid>
    <v-row dense>
      <v-col
        v-for="author in authors"
        :key="author.id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card @click="$router.push(`authors/${author.id}`)">
          <v-img
            :src="author.image"
            class="align-end"
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
            height="200px"
            cover
          >
            <v-card-title class="text-white" v-text="author.name"></v-card-title>
            <v-card-subtitle v-text="'Songs: ' + author.numberOfSongs"></v-card-subtitle>
          </v-img>
          <v-card-actions >
            <v-btn
              class="ms-2"
              size="small"
              text="Go to author"
              variant="outlined"
            ></v-btn>
            <v-spacer></v-spacer>
            <AuthorButtons :author="author" />
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Header from '@/components/Header.vue';
import {mapGetters} from "vuex";
import AuthorButtons from "@/components/AuthorButtons.vue";

export default {
  name: 'Authors',
  components: {
    AuthorButtons,
    Header
  },
  data() {
    return {
      authors: []
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
