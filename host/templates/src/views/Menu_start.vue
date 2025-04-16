<template>
  <div class="choose-menu">
    <div class="scale-wrapper">
      <div class="div">
        <div class="overlap">
          <div class="overlap-group">
            <div class="group-2">
              <div class="text-wrapper-2">Browse Watch Lab</div>
              <img class="icon-bootstrap-outline-fingerprint" alt="Icon" :src="iconBootstrap" />
            </div>
            <p class="text-wrapper">Welcome, What You Want To Do?</p>
            <div class="group">
              <div class="rectangle" />
              <div class="rectangle-2" />
            </div>
            <div class="frame">
              <div class="text-wrapper-3">Botnet List</div>
            </div>
            <div class="div-wrapper">
              <div class="text-wrapper-4">About Us</div>
            </div>
          </div>
          <div class="frame-2">
            <div class="text-wrapper-5">User Agent</div>
          </div>
        </div>
        <div class="overlap-2">
          <div class="rectangle-3" />
          <div class="ellipse" />
          <img class="vector" alt="Vector" :src="vector" />
          <div class="text-wrapper-6">NamaAdmin</div>
          <div class="overlap-group-wrapper">
            <div class="overlap-group-2">
              <div class="text-wrapper-7">Logout</div>
            </div>
          </div>
        </div>
        <div class="group-3">
          <img class="ornament" alt="Ornament" :src="ornament2" />
          <img class="img" alt="Ornament" :src="ornament3" />
          <img class="ornament-2" alt="Ornament" :src="ornament4" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import iconBootstrap from "@/assets/Vector.png";
import ornament2 from "@/assets/Ornament_2.png";
import ornament3 from "@/assets/Ornament_3.png";
import ornament4 from "@/assets/Ornament_4.png";
import vector from "@/assets/Vector.svg";

export default {
  name: "ChooseMenu",
  data() {
    return {
      ornament2,
      ornament3,
      ornament4,
      vector,
      iconBootstrap,
    };
  },
};
</script>

<style>
.choose-menu {
  background-color: #0e0d24;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scale-wrapper {
  transform-origin: top left;
  position: absolute;
  top: 0;
  left: 0;
}
@media (max-width: 1920px) {
  .scale-wrapper {
    transform: scale(calc(100vw / 1920));
  }
}

@media (min-width: 1921px) {
  .scale-wrapper {
    transform: scale(1);
  }
}

.choose-menu .div {
  background-color: #0e0d24;
  height: 100vh;
  width: 100vw;
  display: flex;
  position: relative;
}

body {
  margin: 0;
  overflow: hidden;
}

.choose-menu .overlap {
  height: 88.24vh;
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
}

.choose-menu .overlap-group {
  position: relative;
  width: 100%;
  height: 100%;
}

.choose-menu .group {
  position: relative;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.choose-menu .rectangle {
  background-color: #1b1763;
  height: 9.26vh;
  left: -330px;
  position: relative;
  top: 230px;
  transform: rotate(-39.26deg);
  width: 1414px;
}

.choose-menu .rectangle-2 {
  background-color: #1b1763;
  height: 65px;
  left: -435px;
  position: relative;
  top: 500px;
  transform: rotate(59.86deg);
  width: 1414px;
}

.choose-menu .text-wrapper {
  color: #ffffff;
  font-family: "Poppins-SemiBold", Helvetica;
  font-size: 80px;
  font-weight: 600;
  left: 580px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 200px;
  width: 800px;
  z-index: 10;
}

.choose-menu .group-2 {
  height: 84px;
  left: 242px;
  position: absolute;
  top: 210px;
  width: 232px;
}

.choose-menu .text-wrapper-2 {
  color: #ffffff;
  font-family: "Poppins-SemiBold", Helvetica;
  font-size: 28px;
  font-weight: 600;
  left: -150px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  top: -180px;
  width: 161px;
  z-index: 10;
}

.choose-menu .icon-bootstrap-outline-fingerprint {
  top: -180px !important;
  left: -220px;
  position: relative;
  z-index: 10;
  transition: transform 0.3s ease-in-out;
}

.choose-menu .frame {
  background-color: #302a7b;
  border: 1px solid;
  border-color: #000000;
  border-radius: 50px;
  height: 70px;
  left: 673px;
  overflow: hidden;
  position: absolute;
  top: 530px;
  width: 240px;
}

.choose-menu .text-wrapper-3 {
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 30px;
  font-weight: 400;
  left: 50px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 16px;
}

.choose-menu .div-wrapper {
  background-color: #302a7b;
  border: 1px solid;
  border-color: #000000;
  border-radius: 50px;
  height: 70px;
  left: 28px;
  overflow: hidden;
  position: absolute;
  top: 850px;
  width: 262px;
}

.choose-menu .text-wrapper-4 {
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 30px;
  font-weight: 400;
  left: 21px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 15px;
  width: 219px;
}

.choose-menu .frame-2 {
  background-color: #302a7b;
  border: 1px solid;
  border-color: #000000;
  border-radius: 50px;
  height: 70px;
  left: 1030px;
  overflow: hidden;
  position: absolute;
  top: 530px;
  width: 240px;
}

.choose-menu .text-wrapper-5 {
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 30px;
  font-weight: 400;
  left: 36px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 16px;
  width: 173px;
}

.choose-menu .overlap-2 {
  height: 323px;
  left: 1520px;
  position: absolute;
  top: 660px;
  width: 378px;
}

.choose-menu .rectangle-3 {
  background-color: #494391;
  border-radius: 30px;
  height: 263px;
  left: 0;
  position: absolute;
  top: 60px;
  width: 378px;
}

.choose-menu .ellipse {
  background-color: #302A7B;
  border-radius: 100px;
  height: 120px;
  left: 129px;
  position: absolute;
  top: 0;
  width: 120px;
  opacity: 1;
}

.choose-menu .vector {
  height: 100px;
  left: 139px;
  position: absolute;
  top: 10px;
  width: 100px;
}

.choose-menu .text-wrapper-6 {
  color: #ffffff;
  font-family: "Poppins-SemiBold", Helvetica;
  font-size: 36px;
  font-weight: 600;
  left: 40px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 130px;
  width: 298px;
}

.choose-menu .overlap-group-wrapper {
  height: 68px;
  left: 84px;
  position: absolute;
  top: 206px;
  width: 212px;
}

.choose-menu .overlap-group-2 {
  background-color: #0e0949;
  border-radius: 50px;
  height: 60px;
  position: relative;
  width: 210px;
}

.choose-menu .text-wrapper-7 {
  color: #ffffff;
  font-family: "Poppins-Regular", Helvetica;
  font-size: 30px;
  font-weight: 400;
  left: 20px;
  letter-spacing: 0;
  line-height: normal;
  position: absolute;
  text-align: center;
  top: 12px;
  width: 169px;
}

.choose-menu .group-3 {
  height: 222px;
  left: 1604px;
  position: absolute;
  top: 36px;
  width: 260px;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  padding: 36px 20px 0 20px;
}

.choose-menu .ornament {
  height: 150px;
  left: 0;
  position: relative;
  top: 15px;
  width: 150px;
}

.choose-menu .img {
  height: 40px;
  left: 220px;
  position: relative;
  top: 0;
  width: 40px;
}

.choose-menu .ornament-2 {
  height: 60px;
  left: 200px;
  position: relative;
  top: 162px;
  width: 60px;
}

/* Responsiveness */
@media (max-width: 1200px) {
  .choose-menu .text-wrapper {
    font-size: 60px;
  }
  .choose-menu .text-wrapper-2,
  .choose-menu .text-wrapper-3,
  .choose-menu .text-wrapper-4,
  .choose-menu .text-wrapper-5,
  .choose-menu .text-wrapper-6 {
    font-size: 24px;
  }
  .choose-menu .frame,
  .choose-menu .frame-2,
  .choose-menu .div-wrapper {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .choose-menu .text-wrapper {
    font-size: 40px;
  }
  .choose-menu .text-wrapper-2,
  .choose-menu .text-wrapper-3,
  .choose-menu .text-wrapper-4,
  .choose-menu .text-wrapper-5,
  .choose-menu .text-wrapper-6 {
    font-size: 20px;
  }
  .choose-menu .frame,
  .choose-menu .frame-2,
  .choose-menu .div-wrapper {
    width: 150px;
  }
}

</style>