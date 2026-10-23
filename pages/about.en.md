---
title: About
permalink: /about.html
lang: en
heading: About
---

## The collection

Issues 1–10 of *Yanaka, Nezu, Sendagi* (Yanesen), the community magazine founded by Yanesen Kobo in 1984, and related materials, digitized by the [Local Cultural Resources Digital Archive Project](https://tcha.jp/pts/lcrd/) with the cooperation of Yanesen Kobo and Mayumi Mori.
Images, metadata and annotations are openly available. The records are in Japanese.

Each item is one article.
The images are two-page spreads. When several articles share a spread, each of them shows the same spread.
An article printed across several spreads shows them in order in the viewer.

{% include feature/button.html text="Catalogue data (CSV)" link="/assets/data/metadata.csv" color="outline-dark" %}

## IIIF and data

The images on each article page are shown from IIIF manifests (IIIF is an international standard for sharing images), so the same data opens in any IIIF viewer.
The English and Japanese pages use the same manifests and images.

- IIIF collection (all articles): [/lda/iiif/collection/3/collection.json]({{ site.url }}/lda/iiif/collection/3/collection.json) ([open in Theseus Viewer](https://theseusviewer.org/?iiif-content={{ site.url }}/lda/iiif/collection/3/collection.json))
- IIIF collection (14 annotated articles): [/lda/iiif/collection/3/annotated.json]({{ site.url }}/lda/iiif/collection/3/annotated.json) ([open in Theseus Viewer](https://theseusviewer.org/?iiif-content={{ site.url }}/lda/iiif/collection/3/annotated.json))
- IIIF manifests: `/lda/iiif/3/{id}/manifest.json` (`{id}` is `yanesen_XX_XXX`)
- Images (original): `/lda/files/original/yanesen-XX/yanesen-XX-XXX.jpg`

## Credits

- Project: [Local Cultural Resources Digital Archive](https://tcha.jp/pts/lcrd/) ([lda.tcha.jp](http://lda.tcha.jp/))
- Cooperation: Yanesen Kobo / Mayumi Mori
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Repository: [github.com/nakamura196/lda](https://github.com/nakamura196/lda)

This site is built with [CollectionBuilder-CSV](https://collectionbuilder.github.io/) (University of Idaho Library, Center for Digital Inquiry and Learning).
