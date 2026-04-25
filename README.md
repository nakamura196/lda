# 地域文化資源デジタルアーカイブ

1984年に谷根千工房が創刊した地域雑誌『谷中・根津・千駄木』1〜10号とその関連資料を、[地域文化資源デジタルアーカイブ・プロジェクト](https://tcha.jp/pts/lcrd/)の活動の一環として、谷根千工房・森まゆみ氏の協力のもとデジタルアーカイブ化したものです。画像・メタデータ・アノテーションをオープンに公開しています。

- 公開サイト: <https://nakamura196.github.io/lda/>
- プロジェクトサイト: <http://lda.tcha.jp/>

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
    ├── 2/{id}/             IIIF Presentation v3 マニフェスト（パスは互換性のため /2/ のまま）
    │   ├── manifest.json
    │   ├── curation.json   （アノテーション付きアイテムのみ。Curation 拡張のため v2 形式を保持）
    │   └── list/*.json     （AnnotationPage）
    └── collection/         IIIF Collection
        ├── collection.json
        └── annotated.json

src/data/                   元データ
├── metadata.xlsx
└── images.xlsx
```

## クレジット

- プロジェクト: [地域文化資源デジタルアーカイブ](https://tcha.jp/pts/lcrd/)
- 協力: 谷根千工房 / 森 まゆみ 氏
- 規格: [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/)

## ライセンス

[Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
