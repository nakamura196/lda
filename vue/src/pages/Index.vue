<template>
    <div>
        <div class="page-header page-header-small">
            <parallax class="page-header-image" style="background-image: url('img/bg6.jpg')">
            </parallax>
            <div class="content-center">
                <div class="container">
                    <h1 class="title">地域文化資源デジタルアーカイブ</h1>
                </div>
            </div>
        </div>
        <div class="section section-about-us">
            <div class="container">
                <div class="row">
                    <div class="col-md-8 ml-auto mr-auto text-center">
                        <h2 class="title">About</h2>
                        <h5 class="description">
                            地域文化資源デジタルアーカイブです。
                        </h5>
                    </div>
                </div>
                <div class="separator separator-primary"></div>
                
            </div>
        </div>
        <!-- 
        <div class="section section-team text-center">
            <div class="container">
                <h2 class="title">提供機能</h2>
                <div class="team">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="team-player">
                                <img src="img/ryan.png" alt="Thumbnail Image" class="rounded-circle img-fluid img-raised" />
                                <h4 class="title">源氏物語大成の頁数でさがす</h4>
                                <p class="description">
                                    源氏物語大成の頁数を使って資料を検索します。
                                </p>
                                <router-link to="/searchByPage" class="btn btn-info btn-round"><i class="fas fa-search"></i></router-link>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="team-player">
                                <img src="https://iiif.dl.itc.u-tokyo.ac.jp/iiif/genji/TIFF/A00_6587/07/07_0004.tif/1184,1084,2320,2320/300,/0/default.jpg" alt="Thumbnail Image" class="rounded-circle img-fluid img-raised" />
    
                                <h4 class="title">帖名でさがす</h4>
                                <p class="description">
                                    作品を指定して資料を検索します。
                                </p>
                                <router-link to="/searchByWork" class="btn btn-info btn-round"><i class="fas fa-search"></i></router-link>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="team-player">
                                <img src="https://pbs.twimg.com/profile_images/596366309601845248/2uaPY5NH_400x400.png" alt="Thumbnail Image" class="rounded-circle img-fluid img-raised" />
                                <h4 class="title">IIIFコレクションをみる</h4>
                                <p class="description">
                                    Image Annotator（神崎正英氏作成）を使ってIIIFコレクションを閲覧します。
                                </p>
                                <a href="https://www.kanzaki.com/works/2016/pub/image-annotator?u=https%3A%2F%2Fnakamura196.github.io%2Fgenji%2Fugm%2Fgenji.json" class="btn btn-info btn-round"><i class="fas fa-search"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        -->
    </div>
</template>

<script>
import { Button, FormGroupInput } from '@/components';
export default {
    name: 'landing',
    bodyClass: 'landing-page',
    components: {
        [Button.name]: Button,
        [FormGroupInput.name]: FormGroupInput
    },
    data() {
        return {
            form: {
                firstName: '',
                email: '',
                message: ''
            }
        };
    }
};
</script>

<style>

</style>
