---
title: このサイトについて
layout: about
permalink: /about.html
# include CollectionBuilder info at bottom
credits: false
about-featured-image: yanesen_01_001
position: center
heading: このサイトについて
sub-heading:
padding: 6em
---

## 収録資料

1984年に谷根千工房が創刊した地域雑誌『谷中・根津・千駄木』1〜10号とその関連資料を、[地域文化資源デジタルアーカイブ・プロジェクト](https://tcha.jp/pts/lcrd/)の活動の一環として、谷根千工房・森まゆみ氏の協力のもとデジタルアーカイブ化したものです。
画像・メタデータ・アノテーションをオープンに公開しています。

1 件は 1 本の記事です。
記事の画像は見開きで、1 つの見開きに複数の記事が載っているときは、それぞれの記事に同じ見開きを表示しています。
複数の見開きにまたがる記事は、見開きを順にめくって読めます。

{% include feature/button.html text="目録データ（CSV）" link="/assets/data/metadata.csv" color="outline-dark" %}

## IIIF とデータ

各記事のページの画像は IIIF（画像を共有するための国際的な規格）のマニフェストで表示しています。
同じデータを、ほかの IIIF ビューアでも開けます。

- IIIF コレクション（全件）: [/iiif/collection/3/collection.json]({{ '/iiif/collection/3/collection.json' | relative_url }})（[Theseus Viewer で開く](https://theseusviewer.org/?iiif-content={{ '/iiif/collection/3/collection.json' | absolute_url }})）
- IIIF コレクション（アノテーション付き 14 件）: [/iiif/collection/3/annotated.json]({{ '/iiif/collection/3/annotated.json' | relative_url }})（[Theseus Viewer で開く](https://theseusviewer.org/?iiif-content={{ '/iiif/collection/3/annotated.json' | absolute_url }})）
- IIIF マニフェスト: `/iiif/3/{id}/manifest.json`（`{id}` は `yanesen_XX_XXX`）
- 画像（オリジナル）: `/files/original/yanesen-XX/yanesen-XX-XXX.jpg`
- 画像（中サイズ）: `/files/medium/yanesen-XX/yanesen-XX-XXX.jpg`

## クレジット

- プロジェクト: [地域文化資源デジタルアーカイブ](https://tcha.jp/pts/lcrd/)（[lda.tcha.jp](http://lda.tcha.jp/)）
- 協力: 谷根千工房 / 森 まゆみ 氏
- ライセンス: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- リポジトリ: [github.com/nakamura196/lda](https://github.com/nakamura196/lda)

このサイトは [CollectionBuilder-CSV](https://collectionbuilder.github.io/)（University of Idaho Library, Center for Digital Inquiry and Learning）をもとに作っています。
