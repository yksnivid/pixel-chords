<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card>
          <v-textarea
            v-model="lyrics"
            auto-grow
          ></v-textarea>
        </v-card>
      </v-col>
      <v-col cols="12" md="8" lg="6">
        <v-card>
          <v-card-text>
            <div v-html="parsedLyrics"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4" lg="3">
        <v-select
          v-model="author"
          :items="authors"
          label="Author"
        ></v-select>
      </v-col>
      <v-col cols="12" md="4" lg="3">
        <v-text-field
          v-model="title"
          label="Title"
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="4" lg="3">
        <v-btn @click="addSong">Add Song</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ChordSheetJS from 'chordsheetjs';

const formatter = new ChordSheetJS.ChordProFormatter();
const parser = new ChordSheetJS.ChordsOverWordsParser();

export default {
  name: "AddSong",
  data() {
    return {
      authors: [],
      author: '',
      title: '',
      lyrics: ''
    }
  },
  async created() {
    await this.fetchAuthors();
  },
  computed: {
    parsedLyrics() {
      return formatter.format(parser.parse(this.lyrics));
    }
  },
  methods: {
    async fetchAuthors() {
      try {
        const response = await fetch('/api/authors');
        if (!response.ok) {
          throw new Error('Failed to fetch authors');
        }
        const authorsData = await response.json();
        this.authors = authorsData.map(author => author.author);
      } catch (error) {
        console.error('Error fetching authors:', error);
      }
    },
    addSong() {
      // Отправляем текст песни на сервер
      fetch(`/api/songs/add/${this.author}/${this.title}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          lyrics: this.lyrics
        })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Song added successfully:', data);
        // Опционально: добавить обработку успешного добавления
        // например, очистка формы или редирект после успешного добавления
      })
      .catch(error => {
        console.error('Error adding song:', error);
        // Опционально: добавить обработку ошибок
      });
    },
    showChord(linkElement) {
      const chord = linkElement.textContent.trim(); // Получаем текст аккорда

      // Здесь можно выполнить действия для показа аппликатуры аккорда
      console.log('Showing chord:', chord);

      // Например, можно показать модальное окно с аппликатурой
      // Или вызвать другие функции для обработки аккорда
    }
  }
};
</script>

<style scoped>
.chord-link {
  text-decoration: none;
  color: blue;
  cursor: pointer;
}
.card-text {
  white-space: pre-wrap; /* Это свойство сохраняет переносы строк и пробелы */
}
</style>
