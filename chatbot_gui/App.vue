<template>
  <v-app>
    <v-app-bar
      app
      color="#392b58"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Laur.ai Logo"
          class="shrink mr-2"
          contain
          src="./assets/ai.png"
          transition="scale-transition"
          width="50"
        />

        <v-img
          alt="Laur.ai Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="./assets/name.png"
          width="120"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/Nathan-Nesbitt/Laur.ai"
        target="_blank"
        text
      >
        <span class="mr-2">GitHub Repository</span>
        <v-icon></v-icon>
         <v-img
          alt="Laur.ai Name"
          contain
          min-width="32"
          src="./assets/GitHub-Mark-Light-32px.png"
          width="32"
        />
      </v-btn>
    </v-app-bar>

    <v-content>
      <chat></chat>
    </v-content>
  </v-app>
</template>

<script>
import chat from './components/chat';

export default {
  name: 'App',

  components: {
    chat,
  },
}
</script>
