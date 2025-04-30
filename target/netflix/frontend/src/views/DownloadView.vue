<template>
    <div class="downloads-page">
      <!-- Background -->
      <div class="bg"></div>
  
      <!-- Header -->
      <div class="header">
        <div class="logo-text">NOT</div>
        <img class="logo-img" alt="Logo" :src="image1" />
      </div>
  
      <!-- Judul -->
      <h1 class="title-text">Downloads</h1>
  
      <!-- Kartu OS -->
      <div class="os-cards">
        <div class="card">
          <div class="os-info">
            <img src="@/assets/logo-windows.png" alt="Windows" class="os-icon" />
            <div class="os-name">Windows</div>
          </div>
          <button class="download-btn">Download</button>
        </div>
  
        <div class="card">
          <div class="os-info">
            <img src="@/assets/logo-linux.png" alt="Linux" class="os-icon" />
            <div class="os-name">Linux</div>
          </div>
          <button class="download-btn">Download</button>
        </div>
      </div>
  
      <!-- Tombol Back -->
      <div class="back-container">
        <button class="back-btn" @click="$router.push('/')">Back</button>
      </div>
    </div>
  </template>
  
  <script>
  import image1 from '@/assets/image-1.png';
  
  export default {
    name: 'DownloadView',
    data() {
      return {
        image1,
      };
    }
  };
  </script>
  
  <style scoped>
  .downloads-page {
    position: relative;
    width: 100%;
    min-height: 100vh;
    font-family: "Poppins", Helvetica;
    color: white;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    box-sizing: border-box;
  }
  
  .bg {
    position: absolute;
    inset: 0;
    background-image: url('@/assets/USER-INTERFACE.jpg');
    background-size: cover;
    background-position: center;
    z-index: 0;
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
  
  .title-text {
    position: relative;
    z-index: 2;
    font-size: 44px;
    font-weight: bold;
    margin-top: 150px;
    text-align: center;
  }
  
  .os-cards {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px;
    margin-top: 50px;
    width: 100%;
    max-width: 1000px;
  }
  
  .card {
    background-color: rgba(0, 0, 0, 0.75);
    border-radius: 20px;
    padding: 30px 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 300px;
    height: 250px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s;
  }
  
  .os-info {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 35px;  /* tambah ini untuk turunin */
    margin-bottom: 30px; /* boleh dikurangi juga kalau terlalu jauh dari tombol */
}

  
  .os-icon {
    width: 40px;
    height: 40px;
    object-fit: contain;
  }
  
  .os-name {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    font-family: "Poppins", Helvetica;
  }
  
  .download-btn {
    background-color: red;
    border: none;
    border-radius: 30px;
    color: white;
    font-weight: bold;
    padding: 12px 35px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .download-btn:hover {
    background-color: #cc0000;
  }
  
  .back-container {
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 900px;
    margin-top: 20px;
    display: flex;
    
    margin-left: 260px;
  }
  
  .back-btn {
    background-color: red;
    border: none;
    border-radius: 30px;
    padding: 10px 25px;
    color: white;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-family: "Poppins", Helvetica;
  }
  
  .back-btn:hover {
    background-color: #cc0000;
  }
  
  /* Responsive */
  @media (max-width: 600px) {
    .title-text {
      font-size: 32px;
    }
  
    .os-icon {
      width: 60px;
      height: 60px;
    }
  
    .card {
      width: 90%;
    }
  
    .back-container {
      justify-content: center;
    }
  }
  </style>
  