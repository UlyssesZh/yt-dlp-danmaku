from pathlib import Path
import sys

from biliass import convert_to_ass, BlockOptions

class YoutubeDLDanmaku:

	TRUTH_STRINGS = {'true', 'True', 'yes', '1', 'on'}

	def __init__(self):
		self._kwargs = {}

	def to_screen(self, text):
		sys.stderr.write(text)
		sys.stderr.write('\n')

	def read_args(self):
		self.lang = self._kwargs.get('lang', 'danmaku')
		self.display_region_ratio = float(self._kwargs.get('display_region_ratio', 1.0))
		self.font_face = self._kwargs.get('font_face', 'sans-serif')
		self.font_size = float(self._kwargs.get('font_size', 25))
		self.text_opacity = float(self._kwargs.get('text_opacity', 0.8))
		self.duration_marquee = float(self._kwargs.get('duration_marquee', 15))
		self.duration_still = float(self._kwargs.get('duration_still', 10))
		block_keyword_patterns = self._kwargs.get('block_keyword_patterns', '')
		self.block_options = BlockOptions(
			block_top=self._kwargs.get('block_top') in self.TRUTH_STRINGS or self._kwargs.get('block_fixed') in self.TRUTH_STRINGS,
			block_bottom=self._kwargs.get('block_bottom') in self.TRUTH_STRINGS or self._kwargs.get('block_fixed') in self.TRUTH_STRINGS,
			block_scroll=self._kwargs.get('block_scroll') in self.TRUTH_STRINGS,
			block_reverse=self._kwargs.get('block_reverse') in self.TRUTH_STRINGS,
			block_special=self._kwargs.get('block_special') in self.TRUTH_STRINGS,
			block_colorful=self._kwargs.get('block_colorful') in self.TRUTH_STRINGS,
			block_keyword_patterns=[pattern.strip() for pattern in block_keyword_patterns.split(",")] if block_keyword_patterns != '' else []
		)
		self.reduce_comments = self._kwargs.get('reduce_comments') in self.TRUTH_STRINGS

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
			return
		self.to_screen(f'Processing {path}')
		return danmaku, path, input_format, width, height

	def run(self, info):
		danmaku_info = self.get_danmaku_info(info)
		if not danmaku_info:
			return [], info
		subtitle, path, input_format, width, height = danmaku_info
		with path.open('rb') as f:
			source = f.read()

		print(input_format, width, height, self.display_region_ratio, self.font_face, self.font_size, self.text_opacity, self.duration_marquee, self.duration_still, self.block_options, self.reduce_comments)
		ass = convert_to_ass(
			source, width, height,
			input_format=input_format,
			display_region_ratio=self.display_region_ratio,
			font_face=self.font_face,
			font_size=self.font_size,
			text_opacity=self.text_opacity,
			duration_marquee=self.duration_marquee,
			duration_still=self.duration_still,
			block_options=self.block_options,
			reduce_comments=self.reduce_comments
		)
		new_path = path.with_suffix('.ass')
		subtitle['filepath'] = str(new_path)
		subtitle['ext'] = 'ass'
		del subtitle['url']
		subtitle['data'] = ass
		with new_path.open('w') as f:
			f.write(ass)

		files_to_move = info.get('__files_to_move', {})
		if str(path) in files_to_move:
			files_to_move[str(new_path)] = str(Path(files_to_move[str(path)]).with_suffix('.ass'))
			del files_to_move[str(path)]

		return [path], info
