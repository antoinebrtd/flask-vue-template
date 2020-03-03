<template>
    {% raw %}
    <v-hover v-slot:default="{ hover }">
        <v-row align="center" justify="center">
            <v-col align-self="end" cols="3" v-if="!stack.reverse">
                <v-img :src="stack.logo" alt="vue" class="logo"></v-img>
            </v-col>
            <v-col class="text-start" cols="4">
                <span class="subtitle-1 font-weight-bold">{{ stack.caption }}</span>
                <v-divider color="primary" style="width: 30%" class="mt-2 mb-5"></v-divider>
                <span>{{ stack.description }}</span>
                <a :href="stack.link" target="_blank" class="link">
                    <v-row align="center" justify="center" class="mt-5">
                        <v-slide-x-reverse-transition hide-on-leave>
                            <span :class="hover ? 'primary--text ease hover' : 'ease'">discover</span>
                        </v-slide-x-reverse-transition>
                        <v-slide-x-transition hide-on-leave>
                            <v-icon color="primary" v-if="hover">arrow_right_alt</v-icon>
                        </v-slide-x-transition>
                    </v-row>
                </a>
            </v-col>
            <v-col align-self="end" cols="3" v-if="stack.reverse">
                <v-img :src="stack.logo" alt="vue" class="logo"></v-img>
            </v-col>
        </v-row>
    </v-hover>
    {% endraw %}
</template>

<script>
    export default {
        name: "MainStack",
        props: {
            stack: Object
        }
    }
</script>

<style scoped>
    .link {
        text-decoration: none;
    }

    .logo {
        width: 320px;
    }

    .ease {
        transition: transform .3s ease-out;
    }

    .hover {
        transform: translate(-10px, 0);
        transition: transform .3s ease-in-out;
    }
</style>