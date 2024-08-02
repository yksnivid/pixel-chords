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
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          >
            <v-card-title>
              <v-row no-gutters align="center">
                <div v-if="!editMode">
                  {{ author.name }}
                </div>
                <v-text-field
                  v-else
                  v-model="author.name"
                  density="compact"
                  hide-details
                ></v-text-field>
                <AuthorButtons v-if="!editMode" :author="author" />
                <v-spacer></v-spacer>
                <div v-if="user.isAdmin">
                  <v-btn
                    v-if="editMode"
                    icon="mdi-content-save"
                    variant="plain"
                    @click.stop="updateAuthor"
                  ></v-btn>
                  <v-btn
                    :icon="editMode ? 'mdi-close' : 'mdi-pencil'"
                    size="small"
                    variant="plain"
                    @click.stop="editMode = !editMode"
                  ></v-btn>
                </div>

              </v-row>
            </v-card-title>
          </v-img>

          <div v-if="author.about || editMode">
            <v-card-subtitle>About</v-card-subtitle>
            <v-card-text v-if="!editMode">{{ author.about }}</v-card-text>
            <v-textarea v-else v-model="author.about" rows="10"></v-textarea>
          </div>

          <v-card-subtitle v-if="!editMode">
            Number of songs: {{ author.numberOfSongs }}
          </v-card-subtitle>

          <v-list v-if="!editMode">
            <v-list-item
              v-for="song in author.songs"
              :key="song.id"
              :title="song.title"
              @click="$router.push(`/authors/${author.id}/songs/${song.id}`)"
            >
              <template v-slot:append>
                <SongButtons :song="song" />
                <v-btn
                  v-if="user.isAdmin"
                  icon="mdi-delete"
                  size="small"
                  variant="plain"
                  @click.stop="handleSongDelete(song)"
                ></v-btn>
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

    <v-fab
      v-if="user.isLoggedIn"
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
  </v-container>
  <DeleteSongDialog v-model="deleteDialog" :song="songToDelete" />
  <SongEditor v-model="editorDialog" :author="author" />
  <MessageSnackbar v-model="showMessage" :message="message" />
</template>

<script>
import {mapGetters} from "vuex";
import Header from "@/components/Header.vue";
import AuthorButtons from "@/components/AuthorButtons.vue";
import SongButtons from "@/components/SongButtons.vue";
import SongEditor from "@/components/SongEditor.vue";
import MessageSnackbar from "@/components/MessageSnackbar.vue";
import DeleteSongDialog from "@/components/songs/DeleteSongDialog.vue";

export default {
  name: "Author",
  components: {DeleteSongDialog, MessageSnackbar, AuthorButtons},
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
      editMode: false,
      showMessage: false,
      message: '',
      error: null,
      loading: true,

      deleteDialog: false,
      songToDelete: {type: Object, default: undefined}
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
    async updateAuthor() {
      try {
        const response = await fetch(`/api/authors/${this.author.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.author.name,
            about: this.author.about
          })
        })
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.message = 'Author updated successfully';
        console.log('Author updated successfully, author id:', this.author.id);
      } catch (error) {
        this.message = 'Error while editing author';
        console.error('Error while updating author:', error);
      } finally {
        this.showMessage = true;
        this.editMode = false;
      }
    },
    handleSongDelete(song) {
      this.songToDelete = song;
      this.deleteDialog = true;
    }
  }
};
</script>

<style scoped>
</style>
