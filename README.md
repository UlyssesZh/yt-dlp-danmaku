# yt-dlp-danmaku

[yt-dlp](https://github.com/yt-dlp/yt-dlp) plugin for converting Bilibili danmaku into ASS format.
Powered by [biliass](https://github.com/yutto-dev/biliass).

## Installation and upgrading

Requires yt-dlp 2023.01.02 or above.

You can install or upgrade this package with pip:

```shell
pip install -U yt-dlp-danmaku
```

## Usage

### Download video along with the ASS subtitle

```shell
yt-dlp --write-subs --use-postprocessor danmaku https://www.bilibili.com/video/BV1Sm4y1N78J
```

### Download video embedded with danmaku as a subtitle stream

Bilibili videos are originally mp4 format, but this format does not support ASS subtitle.
Therefore, you need to use another format that supports it, such as mkv:

```shell
yt-dlp --embed-subs --use-postprocessor danmaku --remux-video mkv https://www.bilibili.com/video/BV1Sm4y1N78J
```

You can then try playing this video with players that support ASS subtitles,
such as mpv and VLC.

### Download video and "burn" the danmaku onto it

You need to run FFmpeg yourself to do this.
Here is an example how you can do that:

```shell
yt-dlp --write-subs --use-postprocessor danmaku --output input https://www.bilibili.com/video/BV1Sm4y1N78J
ffmpeg -i input.mp4 -vf subtitles=input.danmaku.ass output.mp4
rm input.mp4 input.danmaku.ass
```

### Get ASS subtitle without downloading the video

```shell
yt-dlp --write-subs --use-postprocessor danmaku:when=before_dl --skip-download https://www.bilibili.com/video/BV1Sm4y1N78J
```

### Use with mpv

```shell
mpv --script-opts=ytdl_hook-ytdl_path=yt-dlp --ytdl-raw-options=use-postprocessor=danmaku:when=before_dl,write-subs=,no-simulate=,skip-download= https://www.bilibili.com/video/BV1Sm4y1N78J
```

You can turn on and off danmaku by using <kbd>j</kbd> (by default).
Add `--sid=1` to turn on danmaku on start.
You can add these options to your mpv config file.

*Notice*: this will leave an ASS file in the current directory.
Delete it afterwards if you do not want it.

## Configuration

You can pass options to this plugin.
For example, to set the opacity of danmaku texts to 0.1 and reserve the bottom half, use
`--use-postprocessor danmaku:text_opacity=0.1;display_region_ratio=0.5`.
All available options:

| Option | Default | Meaning |
|-|-|-|
| `lang` | danmaku | Language selector; you do not normally need to set this |
| `display_region_ratio` | 1.0 | |
| `font_face` | sans-serif | |
| `font_size` | 25 | |
| `text_opacity` | 0.8 | |
| `duration_marquee` | 15 | |
| `duration_still` | 10 | |
| `block_top` | false | |
| `block_bottom` | false | |
| `block_scroll` | false | |
| `block_reverse` | false | |
| `block_fixed` | false | |
| `block_special` | false | |
| `block_colorful` | false | |
| `block_keyword_patterns` | | |
| `reduce_comments` | false | |

Run `biliass -h` for more information about these options.

## Development

See the [Plugin Development](https://github.com/yt-dlp/yt-dlp/wiki/Plugin-Development)
section of the yt-dlp wiki.

## License

MIT.
