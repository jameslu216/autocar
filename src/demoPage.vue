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
    align-items: flex-start;
    /* 使用 flex-start 替代 start */
    gap: 20px;
}

.video-container {
    /* 你可以添加一些特定于视频的样式，如宽度、高度等 */
}

.text-container {
    /* 样式用于格式化旁边的文本 */
    width: 300px;
    /* 或根据需要调整 */
    /* 其他样式，比如字体大小、行高等 */
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
  