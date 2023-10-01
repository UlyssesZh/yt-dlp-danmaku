from biliass import Danmaku2ASS
from yt_dlp.postprocessor.common import PostProcessor

from pathlib import Path

class danmakuPP(PostProcessor):
	TRUTH_STRINGS = {'true', 'True', 'yes', '1', 'on'}
	def __init__(self, downloader=None, **kwargs):
		# ⚠ Only kwargs can be passed from the CLI, and all argument values will be string
		# Also, "downloader", "when" and "key" are reserved names
		super().__init__(downloader)
		self._kwargs = kwargs
		self.read_args()

	def read_args(self):
		self.lang = self._kwargs.get('lang', 'danmaku')
		self.delete_original = self._kwargs.get('delete_original', '1') in self.TRUTH_STRINGS
		self.reserve_blank = int(self._kwargs.get('reserve_blank', 0))
		self.font_face = self._kwargs.get('font_face', 'sans-serif')
		self.font_size = float(self._kwargs.get('font_size', 25))
		self.text_opacity = float(self._kwargs.get('text_opacity', 0.8))
		self.duration_marquee = float(self._kwargs.get('duration_marquee', 15))
		self.duration_still = float(self._kwargs.get('duration_still', 10))
		self.comment_filter = self._kwargs.get('comment_filter')
		self.is_reduce_comments = self._kwargs.get('is_reduce_comments') in self.TRUTH_STRINGS

	def get_danmaku_info(self, info):
		subtitles = info.get('requested_subtitles')
		if not subtitles:
			self.to_screen('No subtitles to post-process, skipping')
			return
		danmaku = subtitles.get(self.lang)
		if not danmaku:
			self.to_screen(f'No subtitle with lang being {self.lang}, skipping')
			return
		ext = danmaku.get('ext')
		if ext == 'xml':
			input_format = 'xml'
		elif ext == 'pb':
			input_format = 'protobuf'
		else:
			self.to_screen(f'Unsupported subtitle format {ext}, skipping')
			return
		width = info.get('width')
		height = info.get('height')
		if not width or not height:
			self.to_screen('Width or height information is missing, skipping')
			return
		path = Path(danmaku.get('filepath'))
		if not path.exists():
			self.to_screen(f'File {path} does not exist, skipping')
			return [], info
		return danmaku, path, input_format, width, height

	def run(self, info):
		danmaku_info = self.get_danmaku_info(info)
		if not danmaku_info:
			return [], info
		subtitle, path, input_format, width, height = danmaku_info
		with path.open('rb') as f:
			source = f.read()
		
		ass = Danmaku2ASS(
			source, width, height,
			input_format = input_format,
			reserve_blank = self.reserve_blank,
			font_face = self.font_face,
			font_size = self.font_size,
			text_opacity = self.text_opacity,
			duration_marquee = self.duration_marquee,
			duration_still = self.duration_still,
			comment_filter = self.comment_filter,
			is_reduce_comments = self.is_reduce_comments,
			progress_callback = None # TODO
		)
		new_path = path.with_suffix('.ass')
		subtitle['filepath'] = str(new_path)
		subtitle['ext'] = 'ass'
		del subtitle['url']
		subtitle['data'] = ass
		with new_path.open('w') as f:
			f.write(ass)
		
		to_delete = [path] if self.delete_original else []
		self.to_screen(to_delete)
		return to_delete, info  # return list_of_files_to_delete, info_dict
