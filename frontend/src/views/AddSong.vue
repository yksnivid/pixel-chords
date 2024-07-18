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
          <v-card-text class="card-text">
            <!-- Используем div с v-html для отображения экранированных аккордов как ссылок -->
            <div v-html="escapedText"></div>
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
    escapedText() {
  // Регулярное выражение для поиска аккордов и составных аккордов
  const chordRegex = /\b([A-GH](?:[#b]?(?:m|maj|aug|dim|sus(?:2|4)?|m?sus(?:2|4)?|6|7|9|11|13)?)?)\b/g;

  // Заменяем найденные аккорды на [аккорд]
  let result = this.lyrics.replace(chordRegex, '[$1]');

  // Регулярное выражение для поиска и обработки составных аккордов
  const compositeChordRegex = /\[([A-GH](?:[#b]?(?:m|maj|aug|dim|sus(?:2|4)?|m?sus(?:2|4)?|6|7|9|11|13)?)?)\/([A-GH](?:[#b]?)?)\]/g;

  // Заменяем составные аккорды на их экранированные версии
  result = result.replace(compositeChordRegex, '[$1]/[$2]');

  return result;
},

    // Вычисляемое свойство для отображения текста с экранированными аккордами как ссылками
    escapedTextWithLinks() {
      // Регулярное выражение для поиска экранированных аккордов
      const chordRegex = /\[(.*?)\]/g;

      // Заменяем найденные экранированные аккорды на HTML-ссылки
      return this.escapedText.replace(chordRegex, '<a class="chord-link" href="#" @click.prevent="showChord">$1</a>');
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
          lyrics: this.escapedText
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
