from argparse import ArgumentParser
import json
import sys

if __name__ == '__main__':
	from yt_dlp import YoutubeDL
	from yt_dlp_danmaku import YoutubeDLDanmaku

	parser = ArgumentParser(
		prog='yt_dlp_danmaku', description='Convert danmaku to ASS according to youtube-dl infojson')
	parser.add_argument('--url', '-u', help='only used when stdin is empty')
	parser.add_argument('--lang', default='danmaku',
	                    help='lang selector of subtitle to be used as danmaku source')
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
			converter.to_screen('invalid json')
			sys.exit(1)
	to_delete, _ = converter.run(info)
	if not args.keep_original:
		for path in to_delete:
			path.unlink()
