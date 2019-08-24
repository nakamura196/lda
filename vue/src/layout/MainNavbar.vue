<template>
    <navbar position="fixed" type="info" :transparent="transparent" :color-on-scroll="colorOnScroll" menu-classes="ml-auto">
        <template>
                          <router-link class="navbar-brand" to="/">
                            地域文化資源デジタルアーカイブ
                          </router-link>
</template>

<template slot="navbar-menu">
    <li class="nav-item">
        <a href="https://nakamura196.github.io/isearch/?u=https://nakamura196.github.io/lda/data/items.json" class="nav-link">資料を見る</a>
    </li>
    <drop-down tag="li" title="その他の探し方" class="nav-item">
        <a href="https://view.officeapps.live.com/op/view.aspx?src=https://nakamura196.github.io/lda/data/data.xlsx" class="dropdown-item">EXCELで見る</a>
        <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https://nakamura196.github.io/lda/data/collection.json" class="dropdown-item">画像を一覧する</a>
    </drop-down>
    <drop-down tag="li" title="可視化" class="nav-item">
        <a href="https://archdataset.dl.itc.u-tokyo.ac.jp/html/vis.html?u=https://nakamura196.github.io/lda/data/data.json" class="dropdown-item">データの可視化</a>
        <a href="http://www.kanzaki.com/works/2014/pub/ld-browser?u=https://nakamura196.github.io/lda/data/data.json" class="dropdown-item">RDFの視覚化</a>
    </drop-down>
    <drop-down tag="li" title="活用例" class="nav-item">
        <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https://nakamura196.github.io/lda/data/acollection.json" class="dropdown-item">テキスト検索</a>
    </drop-down>
</template>
  </navbar>
</template>

<script>
import { DropDown, NavbarToggleButton, Navbar, NavLink } from '@/components';
import { Popover } from 'element-ui';
export default {
    name: 'main-navbar',
    props: {
        transparent: Boolean,
        colorOnScroll: Number
    },
    components: {
        DropDown,
        Navbar,
        NavbarToggleButton,
        NavLink,
        [Popover.name]: Popover
    }
};
</script>

<style scoped>

</style>
