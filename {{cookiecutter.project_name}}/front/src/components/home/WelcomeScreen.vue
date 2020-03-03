<template>
    {% raw %}
    <v-parallax dark src="../../assets/grey_background.jpeg" class="mb-5 bottom-slant" height="500">
        <v-row align="center" justify="center">
            <v-col class="text-center" cols="12">
                <v-row justify="center" align="center" :class="!build && translateUp ? 'translate-up' : ''">
                    <v-fade-transition>
                        <div
                                v-if="greetings"
                                :class="greetings && !translateLeft ? 'appear' : (!welcome && translateLeft ? 'translate-left' : '')"
                                style="width: 180px"
                        >
                  <span class="display-1 font-weight-thin mb-4 primary--text">
                    Hi <span class="font-weight-bold">{{ username }}</span>,
                  </span>
                        </div>
                    </v-fade-transition>
                    <v-fade-transition>
                        <div v-if="welcome" class="appear" style="width: 320px">
                            <span class="display-1 font-weight-thin mb-4 primary--text">welcome to your app!</span>
                        </div>
                    </v-fade-transition>
                </v-row>
                <v-fade-transition>
                    <h4 class="subheading appear mt-4" style="width: 100%" v-if="build">
                        Now the fun begins, develop your first feature!
                    </h4>
                </v-fade-transition>
            </v-col>
        </v-row>
    </v-parallax>
    {% endraw %}
</template>

<script>
    import auth from "@/modules/auth";

    export default {
        name: "WelcomeScreen",
        data() {
            return {
                username: auth.user.profile.first_name,
                greetings: false,
                translateLeft: false,
                translateUp: false,
                welcome: false,
                build: false
            }
        },
        mounted() {
            setTimeout(() => {
                this.greetings = true
            }, 500);
            setTimeout(() => {
                this.translateLeft = true
            }, 1200);
            setTimeout(() => {
                this.welcome = true
            }, 2000);
            setTimeout(() => {
                this.translateUp = true
            }, 3200);
            setTimeout(() => {
                this.build = true
            }, 3500)
        }
    }
</script>

<style scoped>
    .bottom-slant {
        position: relative;
        overflow: hidden;
        z-index: 0;
        -webkit-clip-path: polygon(0 0, 100% 0, 100% 75%, 0 100%);
        clip-path: polygon(0 0, 100% 0, 100% 75%, 0 100%);
    }

    .translate-left {
        transform: translate(-160px, 0);
        transition: transform 0.8s ease-in;
    }

    .translate-up {
        transform: translate(0, -20px);
        transition: transform .3s ease-in-out;
    }

    .appear {
        transition: visibility 0s, opacity 0.4s linear;
    }
</style>