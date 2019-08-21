<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">『校異源氏物語』の頁数でさがす：p.{{$route.query.page}}</h3>
    
                <div class="text-right">
                    <a :href="comp_url" class="btn btn-round btn-primary">Miradorで比較する</a>
    
                    <a :href="'http://dl.ndl.go.jp/info:ndljp/pid/3437686/'+(20+Math.floor(Number($route.query.page) / 2))"><img height="45px" class="mx-2"　src="https://www.dl.ndl.go.jp/resources/images/dlicon.png"></a>
    
                </div>
    
                <table class="table mt-5">
                    <thead>
                        <th></th>
                        <th>IIIF viewers
                            <!--  &amp; Manifest URI icon-->
                        </th>
                    </thead>
                    <tbody>
                        <tr v-for="obj in result">
                            <td>{{obj.label}}：{{obj.clabel}}</td>
                            <td>
                                <a :href="'https://nakamura196.github.io/genji/mirador2/compare3?annotationlist='+obj.anno_id.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/mirador.png"></a>
                                <!-- <a :href="obj.manifest.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/iiif.png"></a> -->
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
        query += " SELECT DISTINCT ?anno_id ?label ?clabel WHERE { \n";
        query += "  ?taisei_page rdfs:label \"" + this.$route.query.page + "\"^^xsd:int . \n";
        query += "  ?taisei_page rdf:type <http://example.org/class/TaiseiPageID> . \n";
        query += "  ?anno_id dcterms:subject ?taisei_page . \n";
        query += "  ?anno_id dcterms:isPartOf ?canvas_id . \n";
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

                console.log(result)

                let annotationlists = ""

                for (let i = 0; i < result.length; i++) {
                    let obj = result[i]
                    annotationlists += obj.anno_id.value + ";"
                }

                /*
                let manifests = ""
                let canvases = ""

                for (let i = 0; i < result.length; i++) {
                    let obj = result[i]
                    manifests += obj.manifest.value + ";"
                    canvases += obj.canvas_id.value + ";"
                }
                */

                this.comp_url = "https://nakamura196.github.io/genji/mirador2/compare3?annotationlist=" + annotationlists.slice(0, -1)

            }).catch(error => { console.log(error); });

    }
};
</script>