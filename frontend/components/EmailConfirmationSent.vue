<template>
    <div class="space-y-6 text-center p-4 hidden md:flex md:flex-col">
        <svg 
            class="mx-auto size-28" 
            fill="currentColor" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 490 490" 
            xml:space="preserve"
        >
            <path 
                d="M245 0C109.69 0 0 109.689 0 245c0 135.31 109.69 245 245 245s245-109.69 245-245C490 109.689 380.31 0 245 0m0 459.375c-118.206 
                0-214.375-96.169-214.375-214.375S126.794 30.625 245 30.625 459.375 126.793 459.375 245 363.207 459.375 245 459.375"
            />
            <path 
                d="M99.576 348.484h291.162V136.411H99.576zm216.808-116.142 43.729-27.361v83.02zm-26.112 16.338 54.35 69.178H146.039l54.152-68.912 
                45.004 27.939zm-160.071 39.765v-82.949l43.809 27.198zm229.912-121.409v1.822l-114.978 71.929-114.934-71.337v-2.414z"
            />
        </svg>
        <h2 class="text-4xl font-semibold">Verify Your Email</h2>
        <div class="text-xl">
            <p>
                We have sent an email to <a class="text-primary">{{ props.confirmationEmail }}</a> in order to verify your provided email address.
            </p>
            <p>
                Please, <b>check your email</b> and <b>click in the sent link</b> to activate your account.
            </p>
        </div>
        <div class="divider w-3/4 mx-auto"></div>
        <p class="font-normal text-lg text-gray-400">If you not got any mail, <a @click="resendConfirmationEmail" class="text-primary cursor-pointer font-bold duration-200 hover:text-secondary">Resend Confirmation Email</a></p>
    </div>

    <div class="space-y-6 text-center p-4 flex flex-col md:hidden">
        <svg 
            class="mx-auto size-20" 
            fill="currentColor" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 490 490" 
            xml:space="preserve"
        >
            <path 
                d="M245 0C109.69 0 0 109.689 0 245c0 135.31 109.69 245 245 245s245-109.69 245-245C490 109.689 380.31 0 245 0m0 459.375c-118.206 
                0-214.375-96.169-214.375-214.375S126.794 30.625 245 30.625 459.375 126.793 459.375 245 363.207 459.375 245 459.375"
            />
            <path 
                d="M99.576 348.484h291.162V136.411H99.576zm216.808-116.142 43.729-27.361v83.02zm-26.112 16.338 54.35 69.178H146.039l54.152-68.912 
                45.004 27.939zm-160.071 39.765v-82.949l43.809 27.198zm229.912-121.409v1.822l-114.978 71.929-114.934-71.337v-2.414z"
            />
        </svg>
        <h2 class="text-3xl font-semibold">Verify Your Email</h2>
        <div class="text-lg space-y-4">
            <p>
                We have sent an email to <a class="text-primary">{{ props.confirmationEmail }}</a> in order to verify your provided email address.
            </p>
            <p>
                Please, check your email and click in the sent link to activate your account.
            </p>
        </div>
        <div class="divider w-5/6 mx-auto"></div>
        <div>
            <p class="font-normal text-gray-400">If you not got any mail</p> 
            <a @click="resendConfirmationEmail" class="text-primary cursor-pointer font-bold duration-200 hover:text-secondary">Resend Confirmation Email</a>
        </div>
        
    </div>
</template>

<script setup>
    import { useUserStore } from '~/stores/user';
    import { useToast } from 'vue-toastification';

    const userStore = useUserStore()

    const toast = useToast();

    const props = defineProps({
        confirmationEmail:  {
            type: String,
            required: true
        },
    })

    async function resendConfirmationEmail() {
        await userStore.resendEmail(props.confirmationEmail)
        toast.info("Confirmation email resent")
    }

</script>