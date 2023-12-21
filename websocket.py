import asyncio
import websockets

# 存储已连接的客户端
connected = set()

async def handler(websocket, path):
    # 将新的 WebSocket 连接添加到已连接集合
    connected.add(websocket)
    try:
        async for message in websocket:
            # 收到来自任一客户端的消息
            print(f"收到消息: {message}")
            # 转发给其他所有客户端
            for client in connected:
                if client != websocket:
                    await client.send(message)
    finally:
        # 当客户端断开连接时
        connected.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # 运行直到被中断

# 启动服务器
        
asyncio.run(main())