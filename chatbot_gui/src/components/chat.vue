<template>
  <div style="margin:0px; background-color: rgb(108, 150, 157, 0.08);">
    <!-- TODO: Make in flex --> 
    <v-row class="">
      <v-col cols="9" >
        <!-- TODO: Edit styling to flex -->
          <v-row id="chatbox" style="height: 530px; width: 1050px; overflow: auto; margin-top: 20px;">
            <v-col cols="12">
              <div id="responses">
                  <!-- MESSAGING AS LIST -->
                    <ul></ul>
              </div>
            </v-col>
          </v-row>

        <!-- USER INPUT -->
         <v-container style=" width: 120%; position: relative; left: 5px; top: 50px;">
          <v-row class="">
            <v-col cols="10">
              <v-text-field
              label = "Send a message"
              filled
              class="ml-8"
              color="#2d0320"
              background-color="rgb(108, 150, 157, 0.4)"
              placeholder=" "
              v-model="message"  
              v-on:keyup.enter="chatMessage"
              ></v-text-field> 
            </v-col>
            <v-col cols="2">
              <v-btn v-on:click="chatMessage" text large color="#2d0320">SEND</v-btn>
            </v-col>
          </v-row>
        </v-container>
     </v-col>
  </v-row>
  </div>

<!-- TODO: Add footer or sidebar with general description, ref repo README--> 

</template>


<script>
  export default {
    name: 'Chatbot',
    
    data() {
      return {
        message: '',         

      } 
    },
    methods: {

    // TODO: Connect with current data
        
    chatMessage: function() {
        if(this.message != '') {
            let chatRespond = '';
            // User Input
            this.createNewElement('responses','right','60%', this.message);

            chatRespond = this.process();
    
            // New chatbot response
            this.createNewElement('responses','left', '60%' , chatRespond);
            
            // Make chat scrollable 
            this.scrollable(); 
            this.message = '';
        }
    },

    // Messages as list elements, styled based on sender
    createNewElement: function(id, align, width, msg) {   
            let listElement = document.createElement('li');
            listElement.textContent = msg;
            listElement.style.textAlign = align;

        // USER STYLING
            if(align == 'right'){ 
            listElement.style.backgroundColor = "rgb(100, 94, 157, 0.4)" ; 
            }

        // BOT STYLING
            if(align == 'left'){ 
            listElement.style.backgroundColor = "rgb(153, 213, 201, 0.4)" ; 
            }

            listElement.style.borderRadius = "10px" ;
            listElement.style.padding="14px"; 
            listElement.style.margin="10px 0";
            listElement.style.left="310px";
            listElement.style.zIndex = "2";
            listElement.style.maxWidth = width;
            listElement.style.fontSize = "16px";
            listElement.style.fontFamily = "Raleway, bold"
            let dest = document.getElementById(id).getElementsByTagName('ul')[0];
            dest.appendChild(listElement);

          // BOT CHAT
            if(align == "left"){ 
            var imgBot = document.createElement("img");
            imgBot.setAttribute("src", "https://i.imgur.com/FQmzcMP.png");
            imgBot.setAttribute("height", "65px");
            imgBot.setAttribute("width", "65px");
            imgBot.style.borderRadius= "50%" ; 
            imgBot.style.position="relative";
            imgBot.style.top="55px";
            imgBot.style.left="-48px";
            listElement.style.position= "relative";
            listElement.style.left="80px";
            dest.appendChild(imgBot);
            dest.appendChild(listElement);
            }

          // USER CHAT
            if(align == "right"){ 
            var imgChat = document.createElement("img");
            imgChat.setAttribute("src", "https://i.imgur.com/RObojid.png");
            imgChat.setAttribute("height", "60px");
            imgChat.setAttribute("width", "60px");
            imgChat.style.position="relative";
            imgChat.style.top="-60px";
            listElement.style.position= "relative";
            imgChat.style.left="915px";
            dest.appendChild(listElement);
            dest.appendChild(imgChat);}
    },

    scrollable: function() {      
      let chatbox = document.getElementById('chatbox');
      chatbox.scrollTop = chatbox.scrollHeight;
    },         
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@500&family=Roboto+Slab:wght@100&display=swap');

ul {
  list-style: none;
}

</style>