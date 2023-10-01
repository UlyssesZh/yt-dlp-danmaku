import sys
import json
from pathlib import Path

from biliass import Danmaku2ASS

class YoutubeDLDanmaku:

	TRUTH_STRINGS = {'true', 'True', 'yes', '1', 'on'}

	def __init__(self):
		self._kwargs = {}

	def to_screen(self, text):
		print(text)

	def read_args(self):
		self.lang = self._kwargs.get('lang', 'danmaku')
		self.keep_original = self._kwargs.get('keep_original') in self.TRUTH_STRINGS
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
		self.to_screen(f'Processing {path}')
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
			input_format=input_format,
			reserve_blank=self.reserve_blank,
			font_face=self.font_face,
			font_size=self.font_size,
			text_opacity=self.text_opacity,
			duration_marquee=self.duration_marquee,
			duration_still=self.duration_still,
			comment_filter=self.comment_filter,
			is_reduce_comments=self.is_reduce_comments,
			progress_callback=None  # TODO
		)
		new_path = path.with_suffix('.ass')
		subtitle['filepath'] = str(new_path)
		subtitle['ext'] = 'ass'
		del subtitle['url']
		subtitle['data'] = ass
		with new_path.open('w') as f:
			f.write(ass)

		to_delete = [] if self.keep_original else [path]
		return to_delete, info  # return list_of_files_to_delete, info_dict

if __name__ == '__main__':
	from argparse import ArgumentParser
	from yt_dlp import YoutubeDL

	parser = ArgumentParser(prog='yt_dlp_danmaku', description='Convert danmaku to ASS according to youtube-dl infojson')
	parser.add_argument('--url', '-u', help='only used when stdin is empty')
	parser.add_argument('--lang', default='danmaku', help='lang selector of subtitle to be used as danmaku source')
	parser.add_argument('--keep-original', '-k', action='store_true')
	parser.add_argument('--reserve-blank', type=int, default=0)
	parser.add_argument('--font-face', default='sans-serif')
	parser.add_argument('--font-size', type=float, default=25.0)
	parser.add_argument('--text-opacity', type=float, default=0.8)
	parser.add_argument('--duration-marquee', type=float, default=15.0)
	parser.add_argument('--duration-still', type=float, default=10.0)
	parser.add_argument('--comment-filter')
	parser.add_argument('--is-reduce-comments', action='store_true')
	args = parser.parse_args()
	converter = YoutubeDLDanmaku()
	converter.lang = args.lang
	converter.reserve_blank = args.reserve_blank
	converter.keep_original = args.keep_original
	converter.font_face = args.font_face
	converter.font_size = args.font_size
	converter.text_opacity = args.text_opacity
	converter.duration_marquee = args.duration_marquee
	converter.duration_still = args.duration_still
	converter.comment_filter = args.comment_filter
	converter.is_reduce_comments = args.is_reduce_comments
	if args.url:
		dl = YoutubeDL({
			'writesubtitles': True,
			'skip_download': True,
			'quiet': True
		})
		info = dl.extract_info(args.url, download=True)
	else:
		try:
			info = json.load(sys.stdin)
		except json.decoder.JSONDecodeError:
			raise 'invalid json'
	to_delete, _ = converter.run(info)
	for path in to_delete:
		path.unlink()
