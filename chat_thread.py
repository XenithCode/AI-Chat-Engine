import json
import asyncio
import aiohttp
from PyQt5.QtCore import QThread, pyqtSignal


class ChatThread(QThread):
    response_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finalize_signal = pyqtSignal()
    start_signal = pyqtSignal()

    def __init__(self, api_key, messages):
        super().__init__()
        self.api_key = api_key
        self.messages = messages
        self.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    async def fetch_response(self):
        try:
            self.start_signal.emit()
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                data = {
                    "model": "qwen-plus",
                    "messages": self.messages,
                    "stream": True
                }
                async with session.post(self.url, json=data, headers=headers) as response:
                    if response.status == 200:
                        async for line in response.content:
                            chunk = line.decode('utf-8').strip()
                            if chunk.startswith('data:'):
                                chunk = chunk[5:].strip()
                                try:
                                    delta_content = json.loads(chunk)["choices"][0]["delta"].get("content", "")
                                    self.response_signal.emit(delta_content)
                                except (json.JSONDecodeError, KeyError):
                                    continue
                        self.finalize_signal.emit()
                    else:
                        self.error_signal.emit(f"错误: HTTP状态码 {response.status}")
        except Exception as e:
            self.error_signal.emit(f"错误: {str(e)}")
        finally:
            self.finalize_signal.emit()

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.fetch_response())
        except Exception as e:
            self.error_signal.emit(f"错误: {str(e)}")
        finally:
            loop.close()