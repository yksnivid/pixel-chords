<template>
  <Header />
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card v-if="!loading && !error">
          <v-img
            class="align-end text-white mb-3"
            height="200"
            :src="author.image"
            cover
          >
          <v-fab
            v-if="user.isAdmin"
            icon="mdi-plus"
            class="mb-4"
            color="primary"
            location="bottom end"
            size="40"
            absolute
            offset
            appear
            app
            @click.stop="editorDialog = true"
          ></v-fab>
            <v-card-title>
              {{ author.name }}
              <AuthorButtons :author="author" />
            </v-card-title>
          </v-img>

          <div v-if="author.about">
            <v-card-subtitle>About</v-card-subtitle>
            <v-card-text>{{ author.about }}</v-card-text>
          </div>

          <v-card-subtitle>
            Number of songs: {{ author.numberOfSongs }}
          </v-card-subtitle>

          <v-list>
            <v-list-item
              v-for="song in author.songs"
              :key="song.id"
              :title="song.title"
              @click="$router.push(`/authors/${author.id}/songs/${song.id}`)"
            >
              <template v-slot:append>
                <SongButtons
                  :song="song"
                />
                <div v-if="user.isAdmin">
                  <v-btn
                    icon="mdi-delete"
                    size="small"
                    variant="plain"
                    @click.stop="deleteSong(song)"
                  ></v-btn>
                </div>
              </template>
            </v-list-item>
          </v-list>

        </v-card>

        <v-alert v-else-if="error" type="error">
          {{ error }}
        </v-alert>

        <v-progress-circular
          v-else
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-col>
    </v-row>
  </v-container>
  <SongEditor v-model="editorDialog" :author="author" />
</template>

<script>
import {mapGetters} from "vuex";
import Header from "@/components/Header.vue";
import AuthorButtons from "@/components/AuthorButtons.vue";
import SongButtons from "@/components/SongButtons.vue";
import SongEditor from "@/components/SongEditor.vue";

export default {
  name: "Author",
  components: {AuthorButtons},
  data() {
    return {
      author: {
        id: null,
        name: null,
        about: null,
        image: null,
        numberOfSongs: null,
        isFavorite: false,
        songs: []
      },
      editorDialog: false,
      error: null,
      loading: true
    };
  },
  async created() {
    await this.fetchAuthorData(this.$route.params.author_id);
  },
  beforeRouteUpdate(to, from, next) {
    this.fetchAuthorData(to.params.author_id);
    next();
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    async fetchAuthorData(authorId) {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch(`/api/authors/${authorId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.author = await response.json();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    async deleteSong(song) {
      try {
        const response = await fetch(`/api/songs/${song.id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Failed to delete song');
        }
        console.log('Deleted song:', song.id);
        await this.fetchAuthorData(this.author.id)
      } catch (error) {
        console.error('Error while deleting song:', error);
      }
    }
  }
};
</script>

<style scoped>
</style>
