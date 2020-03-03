<template>
    {% raw %}
    <v-tooltip right>
        <template v-slot:activator="{ on }">
            <div class="upload-btn">
                <input
                        class="upload"
                        :id="buttonId"
                        type="file"
                        @change="upload($event.target.files[0])"
                />
                <label :class="fab ? applyClass + ` {background-color: ${color} !important}` : applyClass" :for="buttonId" v-on="on">
                    <v-icon
                            v-if="!loading"
                            style="{margin: auto}"
                            :large="large"
                            :small="small"
                            :color="fab ? 'white' : color"
                    >{{icon}}
                    </v-icon>
                    <v-progress-circular indeterminate v-else></v-progress-circular>
                </label>
            </div>
        </template>
        <span>{{tooltip}}</span>
    </v-tooltip>
    {% endraw %}
</template>

<script>
    export default {
        name: "UploadButton",
        props: {
            large: Boolean,
            small: Boolean,
            absolute: Boolean,
            fixed: Boolean,
            text: Boolean,
            fab: Boolean,
            right: Boolean,
            left: Boolean,
            top: Boolean,
            bottom: Boolean,
            loading: Boolean,
            color: String,
            icon: String,
            buttonId: String,
            upload: Function,
            tooltip: String
        },
        data() {
            return {
                style: ['large', 'small', 'absolute', 'fixed', 'text', 'fab', 'right', 'left', 'top', 'bottom'],
                classes: {
                    large: ' v-size--large',
                    small: ' v-size--small',
                    absolute: ' v-btn--absolute',
                    fixed: ' v-btn--fixed',
                    text: ' v-btn--text v-btn--flat',
                    fab: ' v-btn--fab v-btn--contained',
                    right: ' v-btn--right',
                    left: ' v-btn--left',
                    top: ' v-btn--top',
                    bottom: ' v-btn--bottom',
                },
                applyClass: 'v-btn v-btn--icon v-btn--round'
            }
        },
        mounted() {
            for (let i = 0; i < this.style.length; i++) {
                if (this[this.style[i]]) {
                    this.applyClass += this.classes[this.style[i]]
                }
            }
            if (!this.large && !this.small) {
                this.applyClass += ' v-size--default'
            }
        }
    }
</script>

<style scoped>
    .upload {
        opacity: 0;
        position: absolute;
        z-index: -1;
    }

    .v-btn--absolute.v-size--default.v-btn--right {
        right: -10px !important;
    }

    .v-btn--absolute.v-size--default.v-btn--bottom {
        bottom: -10px !important;
    }

    .v-btn--absolute.v-size--large.v-btn--right {
        right: -20px !important;
    }

    .v-btn--absolute.v-size--large.v-btn--bottom {
        bottom: -20px !important;
    }

    .v-btn--absolute.v-size--small.v-btn--right {
        right: -5px !important;
    }

    .v-btn--absolute.v-size--small.v-btn--bottom {
        bottom: -5px !important;
    }

    .v-btn--fixed.v-btn--text, .v-btn--absolute.v-btn--text {
        z-index: 4
    }
</style>
