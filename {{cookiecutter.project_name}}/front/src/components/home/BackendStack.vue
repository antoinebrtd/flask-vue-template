<template>
    {% raw %}
    <v-hover v-slot:default="{ hover }">
        <a :href="stack.link" target="_blank" class="link">
            <v-card :class="hover ? 'hover mx-2' : 'ease mx-2'" color="transparent" elevation="0">
                <v-layout justify-center column align-center>
                    <v-card-text class="title font-weight-bold primary--text">{{ stack.name }}</v-card-text>
                    <v-img :src="stack.logo" :alt="stack.name" class="logo"></v-img>
                    <h4 class="subheading white--text font-weight-thin mt-5">{{ stack.description }}</h4>
                    <v-row align="center" justify="center" class="mt-5">
                        <v-slide-x-reverse-transition hide-on-leave>
                            <span :class="hover ? 'tertiary--text ease hover-discover' : 'white--text ease'">discover</span>
                        </v-slide-x-reverse-transition>
                        <v-slide-x-transition hide-on-leave>
                            <v-icon color="tertiary" v-if="hover" class="ml-2">arrow_right_alt</v-icon>
                        </v-slide-x-transition>
                    </v-row>
                </v-layout>
            </v-card>
        </a>
    </v-hover>
    {% endraw %}
</template>

<script>
    export default {
        name: "BackendStack",
        props: {
            stack: Object
        }
    }
</script>

<style scoped>
    .logo {
        width: 40px;
        height: 40px
    }

    .ease {
        transition: transform .3s ease-out;
    }

    .hover {
        transform: translate(0, -20px);
        transition: transform .3s ease-in-out;
    }

    .link {
        text-decoration: none;
    }
</style>