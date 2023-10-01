# yt-dlp-danmaku

[yt-dlp](https://github.com/yt-dlp/yt-dlp) plugin for converting Bilibili danmaku into ASS format.
Powered by [biliass](https://github.com/yutto-dev/biliass).

## Installation and upgrading

Requires yt-dlp 2023.01.02 or above.

You can install or upgrade this package with pip:

```shell
pip install -U https://github.com/UlyssesZh/yt-dlp-danmaku/archive/refs/heads/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins)
for the other methods this plugin package can be installed.

## Usage

### Download video along with the ASS subtitle

```shell
yt-dlp --write-subs --use-postprocessor danmaku https://www.bilibili.com/video/BV1Sm4y1N78J
```

### Download video embedded with danmaku as a subtitle stream

Bilibili videos are originally mp4 format, but this format does not support ASS subtitle.
Therefore, you need to use another format that supports it, such as mkv:

```shell
yt-dlp -v --embed-subs --use-postprocessor danmaku --remux-video mkv https://www.bilibili.com/video/BV1Sm4y1N78J
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

Because postprocessors are not invoked by yt-dlp when `--skip-download` is on,
here I provided another way of getting the ASS subtitle:

```shell
python -m yt_dlp_danmaku -u https://www.bilibili.com/video/BV1Sm4y1N78J
```

If you want to parse more options to yt-dlp:

```shell
yt-dlp --write-subs --skip-download --no-simulate --dump-single-json https://www.bilibili.com/video/BV1Sm4y1N78J | python -m yt_dlp_danmaku
```

## Development

See the [Plugin Development](https://github.com/yt-dlp/yt-dlp/wiki/Plugin-Development)
section of the yt-dlp wiki.
