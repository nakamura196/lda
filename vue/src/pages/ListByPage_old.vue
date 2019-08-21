<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">源氏物語大成の頁数でさがす：p.{{$route.query.page}}</h3>
    
                <div class="text-right">
                    <router-link class="btn btn-round btn-success" v-bind:to="{ path: 'listByPage2', query: { page: $route.query.page}}">検討中の紐付け方法（行単位）はこちら</router-link>
                    <a :href="comp_url" class="btn btn-round btn-primary ml-2">Miradorで比較する</a>
                </div>
    
                <table class="table mt-5">
                    <thead>
                        <th></th>
                        <th>IIIF viewers &amp; Manifest URI icon</th>
                    </thead>
                    <tbody>
                        <tr v-for="obj in result">
                            <td>{{obj.label}}：{{obj.clabel}}</td>
                            <td>
                                <a :href="'http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest='+obj.manifest.value+'&canvas='+obj.canvas_id.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/mirador.png"></a>
                                <a :href="obj.manifest.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/iiif.png"></a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            result: [],
            comp_url: ""
        }
    },
    created: function() {

        let query = " PREFIX sc: <http://iiif.io/api/presentation/2#> \n";
        query += " SELECT DISTINCT ?manifest ?canvas_id ?label ?clabel WHERE { \n";
        query += "  ?taisei_page rdfs:label \"" + this.$route.query.page + "\"^^xsd:int . \n";
        query += "  ?canvas_id dcterms:subject ?taisei_page . \n";
        query += "  ?canvas_id dcterms:isPartOf ?manifest .  \n";
        query += "  ?manifest rdf:type sc:Manifest .  \n";
        query += "  ?manifest dcterms:isPartOf ?collection .  \n";
        query += "  ?manifest dcterms:subject ?subject .  \n";
        query += "  ?subject rdfs:label ?label .  \n";
        query += "  ?collection rdfs:label ?clabel .  \n";
        query += " } \n";

        console.log(query)

        axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
            .then(response => {

                let result = response.data.results.bindings
                this.result = result

                let manifests = ""
                let canvases = ""

                for (let i = 0; i < result.length; i++) {
                    let obj = result[i]
                    manifests += obj.manifest.value + ";"
                    canvases += obj.canvas_id.value + ";"
                }

                this.comp_url = "https://nakamura196.github.io/genji/mirador2/compare?manifest=" + manifests.slice(0, -1) + "&canvas=" + canvases.slice(0, -1)

            }).catch(error => { console.log(error); });

    }
};
</script>