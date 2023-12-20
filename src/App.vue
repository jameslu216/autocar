<template>
  <div>
    <video ref="videoElement" width="720" controls muted></video>
    <div class="direction-buttons">
      <button @click="sendMessage('ENG 1 1')">上</button>
      <div class="horizontal-buttons">
        <button @click="sendMessage('ENG -1 1')">左</button>
        <button @click="sendMessage('ENG -1 -1')">下</button>
        <button @click="sendMessage('ENG 1 -1')">右</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.direction-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.horizontal-buttons {
  display: flex;
}

button {
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* 響應式設計 */
@media (max-width: 600px) {
  button {
    padding: 15px 25px;
    font-size: 20px;
  }
}
</style>


<script>
import AWS from 'aws-sdk';
import Hls from 'hls.js';
// import io from 'socket.io-client';

export default {
  name: 'KinesisVideoPlayer',
  data() {
    return {
      socket: null,
    };
  },
  mounted() {
    this.setupKinesisVideo();
    window.addEventListener('keydown', this.handleKeydown);
  },
  created() {
    this.socket = new WebSocket('ws://localhost:8765');

    this.socket.onopen = () => {
      console.log('连接成功');
    };

    this.socket.onmessage = (event) => {
      console.log('收到消息:', event.data);
      // 处理收到的数据
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket 错误:', error);
    };

    this.socket.onclose = () => {
      console.log('连接已关闭');
    };
  },
  unmounted() {
    this.socket.close();
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    handleKeydown(e) {
      switch (e.key) {
        case 'ArrowLeft':
          this.sendMessage('ENG -1 1')
          break;
        case 'ArrowRight':
          this.sendMessage('ENG 1 -1')
          break;
        case 'ArrowUp':
          this.sendMessage('ENG 1 1')
          break;
        case 'ArrowDown':
          this.sendMessage('ENG -1 -1');
          break;
      }
    },
    sendMessage(message) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(message);
      } else {
        console.error('WebSocket 连接未建立');
      }
    },
    setupKinesisVideo() {
      // 配置 AWS
      AWS.config.update({
        region: 'ap-northeast-1', // AWS 区域
        credentials: new AWS.Credentials(process.env.VUE_APP_PUBLIC, process.env.VUE_APP_SECRET)
      });

      const kinesisVideo = new AWS.KinesisVideo({ apiVersion: '2017-09-30' });

      // 获取数据端点
      kinesisVideo.getDataEndpoint({
        StreamName: 'autocar', // 视频流名称
        APIName: 'GET_HLS_STREAMING_SESSION_URL'
      }, (err, data) => {
        if (err) {
          console.error(err);
          return;
        }

        const kvam = new AWS.KinesisVideoArchivedMedia({
          apiVersion: '2017-09-30',
          endpoint: data.DataEndpoint
        });

        // 获取 HLS Streaming Session URL
        kvam.getHLSStreamingSessionURL({
          StreamName: 'autocar',
          PlaybackMode: 'LIVE', // 播放模式
          // 其他配置项，例如播放模式、时间戳等
        }, (err, urlData) => {
          if (err) {
            console.error(err);
            return;
          }

          // 使用 HLS URL
          const video = this.$refs.videoElement;
          if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(urlData.HLSStreamingSessionURL);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function () {
              video.play();
            });
          } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.addEventListener('canplay', function () {
              video.play();
            });
          }
        });
      });
    }
  }
};
</script>
