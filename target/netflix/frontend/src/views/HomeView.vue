<template>
    <div class="USER-INTERFACE">
      <div class="container">
        <div class="header">
          <div class="logo-text">NOT</div>
          <img class="logo-img" alt="Image" :src="image1" />
        </div>
  
        <p class="main-title">Free Premium Plan For Netflix!</p>
  
        <div class="benefit-box">
          <div class="benefit-overlay"></div>
          <div class="benefit-title">Benefits:</div>
          <ul class="benefit-list">
            <li>Best video and sound quality</li>
            <li>4K (Ultra HD) + HDR Resolution</li>
            <li>You can download on 6 devices</li>
            <li>Included spatial audio (immersive sound)</li>
            <li>Tv, computer, mobile phone, and tablet is supported</li>
            <li>Your household can watch on 4 devices at the same time</li>
          </ul>
          <div class="ribbon-background"></div>
          <div class="ribbon-text">All For Free!</div>
        </div>
  
        <button class="btn-download" @click="goToDownload">Download Here</button>
      </div>
    </div>
  </template>
  
  <script>
  import image1 from '@/assets/image-1.png';
  
  export default {
    name: 'UserInterface',
    data() {
      return {
        image1,
      };
    },
    methods: {
      goToDownload() {
        this.$router.push('/download')
      }
    }
  };
  </script>
  
  <style scoped>
  .USER-INTERFACE {
    width: 100vw;
    height: 100vh;
    background: url('@/assets/USER-INTERFACE.jpg') center/cover no-repeat;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .container {
    width: 100%;
    max-width: 1920px;
    height: 100%;
    position: relative;
    overflow: hidden;
  }
  
  .header {
    position: absolute;
    top: 2vh;
    left: 2vw;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .logo-text {
    font-size: 3vw;
    font-weight: 700;
    color: #e50914;
    font-family: "Poppins", Helvetica;
  }
  
  .logo-img {
    width: 12vw;
    height: auto;
    margin-top: 0.5vh;
  }
  
  .main-title {
    position: absolute;
    top: 15vh;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 3.5vw;
    font-weight: 700;
    text-align: center;
    text-shadow: 0px 4px 4px #00000040;
    font-family: "Poppins", Helvetica;
  }
  
  .benefit-box {
    position: absolute;
    bottom: 13vh;
    left: 50%;
    transform: translateX(-50%);
    width: 70vw;
    max-width: 1200px;
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 20px;
    padding: 3vh 4vw;
    box-shadow: 0px 4px 4px #00000040;
    color: white;
    font-family: "Poppins", Helvetica;
    text-align: center;
  }
  
  .benefit-title {
    font-size: 2vw;
    font-weight: 700;
    margin-bottom: 2vh;
  }
  
  .benefit-list {
    list-style: none;
    padding: 0;
    font-size: 1.2vw;
    line-height: 1.8;
  }
  
  .ribbon-background {
    position: absolute;
    background-color: #e50914;
    box-shadow: 0px 4px 4px #00000040;
    height: 6vh;
    width: 80vw;
    max-width: 100%;
    top: 90%;
    left: 80%;
    transform: translateX(-50%) rotate(-30deg);
    z-index: 1;
    border-radius: 10px;
  }
  
  .ribbon-text {
    position: absolute;
    color: #ffffff;
    font-family: "Poppins", Helvetica;
    font-size: 2vw;
    font-weight: 700;
    top: 70%;
    left: 90%;
    transform: translateX(-50%) rotate(-30deg);
    z-index: 2;
    width: 100%;
    text-align: center;
  }
  
  .btn-download {
    position: absolute;
    top: 35vh;
    left: 50%;
    transform: translateX(-50%);
    background-color: #e50914;
    color: #ffffff;
    font-family: "Poppins", Helvetica;
    font-size: 2vw;
    font-weight: 700;
    padding: 1vh 5vw;
    border: none;
    border-radius: 50px;
    box-shadow: 0px 4px 8px #00000050;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .btn-download:hover {
    background-color: #bf0810;
    transform: translateX(-50%) scale(1.05);
  }
  </style>