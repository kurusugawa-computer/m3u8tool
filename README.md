# m3u8tool
HTTP Live Streaming (HLS) フォーマットファイルを取り扱うための CLI ツールです。

## 注意
* **作者または著作権者は、ソフトウェアに関してなんら責任を負いません。**

# Features
* HLS フォーマットファイル (m3u8+ts) を分割 (split) できます。
* HLS フォーマットファイル (m3u8+ts) を結合 (cat) できます。
* HLS フォーマットファイル (m3u8+ts) を別の動画フォーマットと相互変換 (convert) できます。

# Requirements
* python 3.x
* ffmpeg 4.x (動画フォーマット変換する場合のみ)

# Install

For user:
## pip
```shell
pip install git+https://github.com/kurusugawa-computer/m3u8tool
```

## pipenv
```shell
pipenv install -e git+https://github.com/kurusugawa-computer/m3u8tool#egg=m3u8tool
```

# Usage

## HLS フォーマットファイル (m3u8+ts) を分割 (split)

### `input.m3u8` を `{filename}-{index:04}.m3u8` に分割
```shell
m3u8tool split input.m3u8
```

### `input.m3u8` を `3.0` 秒ごとに `output-{index:04}.m3u8` に分割
```shell
m3u8tool split -d 3.0 -m output-{index:04}.m3u8 input.m3u8
```

### `input.m3u8` を `output-{index:04}.m3u8` と `output-{index:04}.ts` に分割
```shell
m3u8tool split -m output-{index:04}.m3u8 -t output-{index:04}.ts input.m3u8
```

## HLS フォーマットファイル (m3u8+ts) を結合
### `input-{index:04}.m3u8` を `output.m3u8` に結合
```shell
m3u8tool cat input-*.m3u8 output.m3u8
```

### `input-{index:04}.m3u8` を `output.m3u8` と `output.ts` に結合
```shell
m3u8tool cat -t output.ts input-*.m3u8 output.m3u8
```

## HLS フォーマットファイル (m3u8+ts) を別の動画フォーマットと相互変換
### `input.mp4` を `output.m3u8` と `output.ts` に変換
```shell
m3u8tool convert input.mp4 output.m3u8
```

### `input.m3u8` を `output.mp4` に変換
```shell
m3u8tool convert input.m3u8 output.mp4
```
