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
                <v-text-field
                  v-model="author.name"
                  density="compact"
                  hide-details
                ></v-text-field>
                <v-spacer></v-spacer>
                <v-btn
                  icon="mdi-content-save"
                  variant="plain"
                  @click.stop="updateAuthor"
                ></v-btn>
                <v-btn
                  icon="mdi-close"
                  size="small"
                  variant="plain"
                  @click.stop="$emit('edit-mode', false)"
                ></v-btn>
              </v-row>
            </v-card-title>
          </v-img>

          <div>
            <v-card-subtitle>About</v-card-subtitle>
            <v-textarea v-model="author.about" rows="10"></v-textarea>
          </div>

          <v-card-subtitle>
            Number of songs: {{ author.numberOfSongs }}
          </v-card-subtitle>
        </v-card>

        <v-alert v-else-if="error" type="error">{{ error }}</v-alert>
        <v-progress-circular v-else indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>
  </v-container>
  <MessageSnackbar v-model="showMessage" :message="message" />
</template>

<script>
import { mapGetters } from "vuex";
import Header from "@/components/Header.vue";
import MessageSnackbar from "@/components/MessageSnackbar.vue";

export default {
  name: "AuthorEdit",
  components: { Header, MessageSnackbar },
  props: {
    author: Object,
  },
  emits: ['edit-mode', 'refresh-data'],
  data() {
    return {
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
    async updateAuthor() {
      try {
        const response = await fetch(`/api/authors/${this.author.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.author.name,
            about: this.author.about,
          }),
        });
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
        this.$emit('edit-mode', false);
        this.$emit('refresh-data');
      }
    },
  },
};
</script>

<style scoped></style>
