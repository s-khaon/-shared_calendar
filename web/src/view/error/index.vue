<template>
  <div>
    <div class="big">
      <div class="inner">
        <p>页面被神秘力量吸走了</p>
        <div class="button-box">
          <button class="error-button" @click="handleClickGoHome">去首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
export default {
  name: 'Error',
  setup() {
    const router = useRouter()
    const handleClickGoHome = () => {
      router.push({name: "Home"})
    }
    return {
      handleClickGoHome,
    }
  }

}
</script>

<style lang="scss" scoped>
    .big{
        width: 100%;
        height: calc(100vh - 220px);
        background-color: rgb(244,244,244);
        position: relative;
    }
    .inner{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .inner p {
        text-align: center;
        font-size: 24px;
    }
    .inner .leftPic{
        width: 60px;
        height: 60px;
        margin-left: 44%;
        margin-top: 20px;
    }
    .button-box{
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: transparent;
      margin-top: 10px;
      .error-button{
        height: 30px;
        color: #0054b4;
        border: 1px solid #0054b4;
        border-radius: 10px;
        width: 150px;
      }
    }
</style>
