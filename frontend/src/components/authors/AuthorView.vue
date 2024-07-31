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
                <div>{{ author.name }}</div>
                <AuthorButtons :author="author" />
                <v-spacer></v-spacer>
                <div v-if="user.isAdmin">
                  <v-btn
                    icon="mdi-pencil"
                    size="small"
                    variant="plain"
                    @click.stop="$emit('edit-mode', true)"
                  ></v-btn>
                </div>
              </v-row>
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
                <SongButtons :song="song" />
                <v-btn
                  v-if="user.isAdmin"
                  icon="mdi-delete"
                  size="small"
                  variant="plain"
                  @click.stop="deleteDialog = true"
                ></v-btn>
                <v-dialog v-model="deleteDialog">
                  <v-card
                    max-width="400"
                    :text='`Are you sure you want to delete song "${song.title}"?`'
                    title="Delete song"
                  >
                    <template v-slot:actions>
                      <v-btn
                        text="Yes, delete"
                        @click="deleteSong(song)"
                        color="error"
                      ></v-btn>
                      <v-btn text="No" @click="deleteDialog = false"></v-btn>
                    </template>
                  </v-card>
                </v-dialog>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

        <v-alert v-else-if="error" type="error">{{ error }}</v-alert>
        <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
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
  </v-container>
  <SongEditor v-model="editorDialog" :author="author" />
  <MessageSnackbar v-model="showMessage" :message="message" />
</template>

<script>
import { mapGetters } from "vuex";
import Header from "@/components/Header.vue";
import AuthorButtons from "@/components/AuthorButtons.vue";
import SongButtons from "@/components/SongButtons.vue";
import SongEditor from "@/components/SongEditor.vue";
import MessageSnackbar from "@/components/MessageSnackbar.vue";

export default {
  name: "AuthorView",
  components: { Header, AuthorButtons, SongButtons, SongEditor, MessageSnackbar },
  props: {
    author: Object,
  },
  emits: ['edit-mode', 'refresh-data'],
  data() {
    return {
      editorDialog: false,
      deleteDialog: false,
      showMessage: false,
      message: '',
      error: null,
      loading: false,
    };
  },
  computed: {
    ...mapGetters(['user']),
  },
  methods: {
    async deleteSong(song) {
      try {
        const response = await fetch(`/api/songs/${song.id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error('Failed to delete song');
        }
        this.deleteDialog = false;
        await this.$emit('refresh-data');
      } catch (error) {
        console.error('Error while deleting song:', error);
      }
    },
  },
};
</script>

<style scoped></style>
