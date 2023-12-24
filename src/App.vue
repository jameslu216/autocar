<template>
  <div class="container">
    <video ref="videoElement" width="720" controls muted></video>
    <div class="panel">
      <h3 class="panel-title">Control Panel</h3>
      <button @click="sendMessage('ENG 1 1')" :class="{'arrow': true, 'up-arrow': true, 'active-arrow': activeDirection === 'ArrowUp'}"></button>
      <div class="horizontal-buttons">
        <button @click="sendMessage('ENG -1 1')" :class="{'arrow': true, 'left-arrow': true, 'active-arrow': activeDirection === 'ArrowLeft'}"></button>
        <button @click="sendMessage('ENG 0 0')" :class="{'stop-button': true, 'active-space': activeDirection === ' '}"></button>
        <button @click="sendMessage('ENG 1 -1')" :class="{'arrow': true, 'right-arrow': true, 'active-arrow': activeDirection === 'ArrowRight'}"></button>
      </div>
      <button @click="sendMessage('ENG -1 -1')" :class="{'arrow': true, 'down-arrow': true, 'active-arrow': activeDirection === 'ArrowDown'}"></button>
    </div>
    <div class="panel">
      <h3 class="panel-title">Sensor Data</h3>
      <div class="sensor-data">溫度<span class="temp-icon">&#x1F321;</span>: {{temperature}}</div>
      <div class="sensor-data">濕度<span class="humidity-icon">&#x1F4A7;</span>: {{humidity}}</div>
      <div class="sensor-data">環境煙霧量<span class="smoke-icon">&#x2601;</span>: {{smoke}}</div>
      <div class="sensor-data">GPS定位: {{latitude}} N , {{longitude}} E</div>
      <div class="sensor-data">與前方障礙物的距離: {{distance}}</div>
      <div class="sensor-data">是否偵測到熱源: {{PIR}}</div>
    </div>
  </div>
</template>
<style scoped>
.container {
  width: 720px; /* 视频和控制面板的宽度 */
  margin: auto; /* 居中显示 */
}
.panel-title {
  color: #333; /* 标题颜色 */
  margin-bottom: 20px; /* 在标题和按钮之间添加一些空间 */
  font-size: 1.5em; /* 标题的大小 */
  margin-top: 5px;
}
.panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 3px solid #333; /* 控制面板边框 */
  padding: 20px; /* 控制面板内边距 */
  border-radius: 15px; /* 控制面板圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 控制面板阴影效果 */
  background: #f7f7f7; /* 控制面板背景颜色 */
  margin-top: 20px; /* 和视频元素的间距 */
  box-sizing: border-box; /* 包括padding和border在内的总宽度 */
}

.horizontal-buttons {
  display: flex;
}

button {
  margin: 5px;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.arrow {
  width: 30px;
  height: 30px;
  background-color: transparent;
  border: solid black;
  border-width: 0 5px 5px 0;
  display: inline-block;
  padding: 3px;
  cursor: pointer;
  outline: none;
}

button:focus {
  outline: none;
}

.up-arrow {
  transform: rotate(-135deg);
  -webkit-transform: rotate(-135deg);
}

.down-arrow {
  transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
}

.left-arrow {
  transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
}

.right-arrow {
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}

.stop-button {
  position: relative;
  background-color: #3498db; /* 按钮背景颜色 */
  display: block;
  border-radius: 15%; /* 轻微圆角的正方形 */
}

.sensor-data {
  margin-bottom: 5px; /* 在标题和按钮之间添加一些空间 */
  font-size: 1.2em; /* 标题的大小 */
  font-weight: bold;
}

.sensor-data .temp-icon {
  color: red; /* 溫度計顏色 */
}

.sensor-data .humidity-icon {
  color: blue; /* 水滴图标的颜色 */
}

.sensor-data .smoke-icon {
  color: gray; /* 为烟雾图标设置颜色 */
}

.active-arrow {
  border-color: red; 
}

.active-space {
  background-color: red; 
}

@media (max-width: 600px) {
  button {
    width: 40px;
    height: 40px;
    border-width: 0 6px 6px 0;
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
      controlMap: {
        'ArrowLeft': 'ENG 1 -1',
        'ArrowRight': 'ENG -1 1',
        'ArrowUp': 'ENG 1 1',
        'ArrowDown': 'ENG -1 -1',
        ' ': 'ENG 0 0'
      },
      temperature: 0,
      humidity: 0,
      latitude: 24.9,
      longitude: 121.1,
      PIR: "否",
      distance: 0,
      smoke: 0,
      activeDirection: null,
    };
  },
  mounted() {
    this.setupKinesisVideo();
    window.addEventListener('keydown', this.handleKeydown);
    window.addEventListener('keyup', this.handleKeyup);
  },
  created() {
    this.socket = new WebSocket('ws://'+window.location.hostname+':8765');

    this.socket.onopen = () => {
      console.log('连接成功');
    };

    this.socket.onmessage = (event) => {
      console.log('收到消息:', event.data);
      var datas = event.data.split(' ');
      if(datas[0] == 'TEMP'){
        this.temperature = datas[1];
        this.humidity = datas[3];
      }else if(datas[0] == 'PIR'){
        this.PIR = (datas[1] == 1)? "是":"否";
      }else if(datas[0] == 'GPS'){
        this.latitude = datas[1];
        this.longitude = datas[2];
      }else if(datas[0] == 'DIST'){
        this.distance = datas[1];
      }else if(datas[0] == 'SMOKE'){
        this.smoke = datas[1];
      }
      
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
    window.removeEventListener('keyup', this.handleKeyup);
  },
  methods: {
    handleKeydown(e) {
      this.activeDirection = e.key;
      this.sendMessage(this.controlMap[e.key]);
    },
    handleKeyup() {
    this.activeDirection = null;
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
