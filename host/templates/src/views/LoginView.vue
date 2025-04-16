<template>
  <div class="LOGIN-ADMIN">
    <div class="scale-wrapper">
      <div class="div">
        <div class="login-left">
          <div class="text-wrapper">Please Login</div>

          <div class="overlap-2">
            <input
              v-model="username"
              class="input"
              type="text"
              placeholder="Username"
            />
          </div>

          <div class="password-wrapper">
            <input
              v-model="password"
              class="input"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password"
            />
            <img
              class="toggle-password-img"
              :src="showPassword ? eye_slash : eye"
              alt="toggle password"
              @click="showPassword = !showPassword"
            />
          </div>

          <div class="overlap-3">
            <button class="login-button" @click="handleLogin">Login</button>
          </div>
        </div>

        <div class="group">
          <div class="overlap-group">
            <div class="ellipse" />
            <div class="ellipse-2" />
            <div class="ellipse-3" />
            <div class="ellipse-4" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import eye_slash from "@/assets/eye_slash.svg"
import eye from "@/assets/eye.svg"
const router = useRouter() 

const username = ref('')
const password = ref('')
const showPassword = ref(false)

const handleLogin = () => {
  if (username.value && password.value) {
    
    router.push('/menu') 
  } else {
    alert('Username dan Password tidak boleh kosong!')
  }
}
</script>

<style>
.LOGIN-ADMIN {
  background-color: #0f0d25;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scale-wrapper {
  width: 100%;
  height: 100%;
}

.LOGIN-ADMIN .div {
  background-color: #0f0d25;
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;
}

body {
  margin: 0;
  overflow: hidden;
}

.login-left {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 25px;
  z-index: 2;
}

.text-wrapper {
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 36px;
  font-weight: 400;
  text-align: center;
}

.overlap-2 {
  position: relative;
  width: 320px;
  height: 50px;
  border-radius: 50px;
}

.password-wrapper {
  position: relative;
  width: 320px;
  height: 50px;
  border-radius: 50px;
}

.input {
  background-color: #090360;
  border-radius: 50px;
  height: 100%;
  width: 100%;
  opacity: 0.75;
  padding-left: 20px;
  color: white;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 16px;
  border: none;
  outline: none;
}

.input::placeholder {
  color: #ffffff;
  opacity: 0.5;
}

.toggle-password-img {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  cursor: pointer;
  opacity: 0.75;
  user-select: none;
}

.toggle-password-img:hover {
  opacity: 1;
}

.overlap-3 {
  position: relative;
  width: 100px;
  height: 40px;
  border-radius: 50px;
  cursor: pointer;
}

.login-button {
  background-color: #090460;
  border-radius: 50px;
  height: 100%;
  width: 100%;
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 16px;
  border: none;
  cursor: pointer;
  opacity: 0.75;
  transition: 0.3s;
}

.login-button:hover {
  opacity: 1;
}

.group {
  position: absolute;
  right: 0;
  top: 0;
  width: 60%;
  height: 100%;
  z-index: 1;
}

.overlap-group {
  position: relative;
  width: 100%;
  height: 100%;
}

.ellipse,
.ellipse-2,
.ellipse-3,
.ellipse-4 {
  position: absolute;
  background-color: #0d0588;
  border-radius: 50%;
}

.ellipse {
  width: 1200px;
  height: 1200px;
  right: -350px;
  top: -30px;
  opacity: 0.1;
}

.ellipse-2 {
  width: 1000px;
  height: 1000px;
  right: -280px;
  top: 80px;
  opacity: 0.25;
}

.ellipse-3 {
  width: 800px;
  height: 800px;
  right: -210px;
  top: 210px;
  opacity: 0.5;
}

.ellipse-4 {
  width: 600px;
  height: 600px;
  right: -150px;
  top: 350px;
  opacity: 0.75;
}
</style>
