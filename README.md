# 地域文化資源デジタルアーカイブ

谷根千エリアの地域文化資源を IIIF Presentation API v2 で公開するデジタルアーカイブ。

## エンドポイント

公開URL prefix: `https://nakamura196.github.io/lda`

- IIIF Collection（全446件）: `/iiif/collection/collection.json`
- IIIF Collection（アノテーション付き14件）: `/iiif/collection/annotated.json`
- IIIF Manifest: `/iiif/2/{id}/manifest.json`（`{id}` は `yanesen_XX_XXX`）
- 画像（オリジナル）: `/files/original/yanesen-XX/yanesen-XX-XXX.jpg`
- 画像（中サイズ）: `/files/medium/yanesen-XX/yanesen-XX-XXX.jpg`

## 構成

```
docs/                       公開コンテンツ（GitHub Pages）
├── assets/
├── files/
│   ├── original/           オリジナル画像
│   └── medium/             中サイズ画像
└── iiif/
    ├── 2/{id}/             IIIF Presentation v2 マニフェスト
    │   ├── manifest.json
    │   ├── curation.json   （アノテーション付きアイテムのみ）
    │   └── list/*.json     （AnnotationList）
    └── collection/         IIIF Collection
        ├── collection.json
        └── annotated.json

src/data/                   元データ
├── metadata.xlsx
└── images.xlsx
```

## ライセンス

[Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
