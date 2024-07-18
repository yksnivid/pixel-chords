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
        <v-card
          @click="goToAuthor(author.author)"
        >
          <v-img
              :src="author.image"
              class="align-end"
              gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
              height="200px"
              cover
            >
              <v-card-title class="text-white" v-text="author.author"></v-card-title>
              <v-card-subtitle v-text="'Number of songs: ' + author.numberOfSongs"></v-card-subtitle>
            </v-img>
          <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                color="medium-emphasis"
                icon="mdi-heart"
                size="small"
                @click=""
                disabled
              ></v-btn>

              <v-btn
                color="medium-emphasis"
                icon="mdi-bookmark"
                size="small"
                @click=""
                disabled
              ></v-btn>

              <v-btn
                color="medium-emphasis"
                icon="mdi-share-variant"
                size="small"
                @click=""
                disabled
              ></v-btn>
            </v-card-actions>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
  name: 'Authors',
  components: {
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
    },
    goToAuthor(authorAuthor) {
      this.$router.push(`/author/${authorAuthor}`);
    }
  }
};
</script>

<style scoped>
.v-card {
  cursor: pointer;
}
</style>
