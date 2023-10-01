from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp_danmaku import YoutubeDLDanmaku

class danmakuPP(YoutubeDLDanmaku, PostProcessor):
	def __init__(self, downloader=None, **kwargs):
		super(YoutubeDLDanmaku, self).__init__(downloader)
		self._kwargs = kwargs
		self.read_args()
