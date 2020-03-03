<template>
    {% raw %}
    <v-footer color="transparent" padless style="width: 100%">
        <v-img src="../../assets/grey_background.jpeg" alt="banner" class="banner" v-if="background"></v-img>
        <v-card flat tile class="white--text text-center" color="transparent" style="width: 100%">
            <v-card-text class="white--text" v-if="background">
                Build fast and efficiently
            </v-card-text>
            <v-divider v-if="background" color="grey" style="width: 20%; margin: auto;"></v-divider>
            <v-card-text>
                <a v-for="link in links" :key="link.icon" :href="link.link" target="_blank" class="link">
                    <v-btn class="mx-4 white--text text-center" icon>
                        <v-icon size="24px">{{ link.icon }}</v-icon>
                    </v-btn>
                </a>
            </v-card-text>
        </v-card>
    </v-footer>
    {% endraw %}
</template>

<script>
    export default {
        name: "Footer.vue",
        props: {
            background: Boolean
        },
        data: () => ({
            links: [
                {icon: 'fab fa-vuejs', link: 'https://vuejs.org'},
                {icon: 'fab fa-python', link: 'http://flask.palletsprojects.com/en/1.1.x'},
                {icon: 'fab fa-github-square', link: 'https://github.com/antoinebrtd'},
                {icon: 'fab fa-linkedin', link: 'https://www.linkedin.com/in/antoine-bertrand-5906a5133/'}
            ]
        })
    }
</script>

<style scoped>
    .link {
        text-decoration: none
    }

    .banner {
        width: 100%;
        margin: auto;
        position: absolute;
        height: 100%;
        top: 0
    }
</style>