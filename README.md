# 地域文化資源デジタルアーカイブ

1984年に谷根千工房が創刊した地域雑誌『谷中・根津・千駄木』1〜10号とその関連資料を、[地域文化資源デジタルアーカイブ・プロジェクト](https://tcha.jp/pts/lcrd/)の活動の一環として、谷根千工房・森まゆみ氏の協力のもとデジタルアーカイブ化したものです。画像・メタデータ・アノテーションをオープンに公開しています。

- 公開サイト: <https://nakamura196.github.io/lda/>
- プロジェクトサイト: <http://lda.tcha.jp/>

## エンドポイント

公開URL prefix: `https://nakamura196.github.io/lda`

- IIIF Collection（全446件）: `/iiif/collection/3/collection.json`
- IIIF Collection（アノテーション付き14件）: `/iiif/collection/3/annotated.json`
- IIIF Manifest: `/iiif/3/{id}/manifest.json`（`{id}` は `yanesen_XX_XXX`）
- 画像（オリジナル）: `/files/original/yanesen-XX/yanesen-XX-XXX.jpg`
- 画像（中サイズ）: `/files/medium/yanesen-XX/yanesen-XX-XXX.jpg`

## 構成

[CollectionBuilder-CSV](https://github.com/CollectionBuilder/collectionbuilder-csv) のサイトです。
GitHub Actions で Jekyll を実行し、GitHub Pages に公開します（`.github/workflows/pages.yml`）。

```
_data/yanesen.csv           目録（1 行 1 記事。複数の見開きにまたがる記事は、見開きを子の行に持つ）
iiif/annotations/<id>.csv   画像上のアノテーション（canvas, xywh, text）
iiif/collection/3/          IIIF Collection（静的ファイル）
iiif/3/<id>/curation.json   IIIF Curation（アノテーション付きの 14 件）
files/original/, medium/    画像
src/data/*.xlsx             元の Excel（変換は src/scripts/xlsx_to_cb_csv.py で 1 回だけ行った）
```

IIIF マニフェスト（`/iiif/3/<id>/manifest.json`）は、ビルドのときに gem
[static_iiif](https://github.com/nakamura196/static_iiif) が目録とアノテーションから作ります（`_config.yml` の `static_iiif:`）。

```
bundle install
bundle exec jekyll serve
```

## クレジット

- プロジェクト: [地域文化資源デジタルアーカイブ](https://tcha.jp/pts/lcrd/)
- 協力: 谷根千工房 / 森 まゆみ 氏
- 規格: [IIIF Presentation API 3.0](https://iiif.io/api/presentation/3.0/)

## ライセンス

[Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
