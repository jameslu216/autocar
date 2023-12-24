<template>
    <div class="video-text-container">
        <div class="video-container">
            <!-- 这里放置你的视频 -->
            <video ref="videoElement" width="720" controls>
                <source :src="require(`@/assets/autocar.mp4`)" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="text-container">
            <!-- 这里放置你的文字 -->
            <p>{{ videoText }}</p>
            <!-- 你可以继续添加更多的文本或其他内容 -->
        </div>
    </div>
</template>
  
<style>
.video-text-container {
    display: flex;
    flex-direction: column; /* 子元素垂直堆叠 */
    justify-content: center; /* 垂直居中 */
    align-items: center; /* 水平居中子元素 */
    gap: 20px;
    margin: auto;
}

.text-container {
    width: 300px;
    text-align: center; /* 文本居中 */
    font-size: 50px;
}
</style>
  
  
<script>
export default {
    data() {
        return {
            videoText: '', // 添加一个用于显示文字的状态变量
        };
    },
    mounted() {
        const video = this.$refs.videoElement;
        video.addEventListener('timeupdate', this.updateVideoText);
    },
    methods: {
        updateVideoText() {
            const currentTime = this.$refs.videoElement.currentTime;
            if (currentTime >= 0 && currentTime < 2) {
                this.videoText = 'BKQ-1838';
            } else if (currentTime >= 7.2 && currentTime < 8.2) {
                this.videoText = '3U-7913';
            } else {
                this.videoText = '';
            }
        },
    },
    beforeUnmount() {
        // 清理事件监听器
        const video = this.$refs.videoElement;
        if (video) {
            video.removeEventListener('timeupdate', this.updateVideoText);
        }
    },
};
</script>
  