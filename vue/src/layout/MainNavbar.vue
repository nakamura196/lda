<template>
    <navbar position="fixed" type="info" :transparent="transparent" :color-on-scroll="colorOnScroll" menu-classes="ml-auto">
        <template>
                  <router-link class="navbar-brand" to="/">
                    地域文化資源デジタルアーカイブ
                  </router-link>
</template>

<template slot="navbar-menu">
    <li class="nav-item">
        <a href="https://view.officeapps.live.com/op/view.aspx?src=https://nakamura196.github.io/lda/data/metadata.xlsx" class="nav-link">メタデータ一覧</a>
    </li>
    <li class="nav-item">
        <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https://nakamura196.github.io/lda/data/collection.json" class="nav-link">画像一覧</a>
    </li>
    <li class="nav-item">
        <a href="https://nakamura196.github.io/isearch/?u=https://nakamura196.github.io/lda/data/items.json" class="nav-link">メタデータ検索</a>
    </li>
    <li class="nav-item">
        <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https://nakamura196.github.io/lda/data/acollection.json" class="nav-link">テキスト検索</a>
    </li>
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
