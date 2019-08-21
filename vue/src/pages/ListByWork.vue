<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">帖名でさがす：{{$route.query.subject.split("/resource/")[1]}}</h3>
    
                <div class="text-right">
                    <a :href="comp_url" class="btn btn-round btn-primary">Miradorで比較する</a>
                </div>
    
                <table class="table mt-5">
                    <thead>
                        <th></th>
                        <th>IIIF viewers &amp; Manifest URI icon</th>
                    </thead>
                    <tbody>
                        <tr v-for="obj in result">
                            <td>{{obj.clabel}}</td>
                            <td>
                                <a :href="'http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest='+obj.manifest.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/mirador.png"></a>
                                <a :href="'http://da.dl.itc.u-tokyo.ac.jp/uv/?manifest='+obj.manifest.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/uv.png"></a>
                                <a :href="'http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?manifest='+obj.manifest.value"><img class="m-2" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/icp.png"></a>
                                <a :href="'http://tify.sub.uni-goettingen.de/demo.html?manifest='+obj.manifest.value"><img height="32px" class="m-2" src="https://camo.githubusercontent.com/d9ad46d53a7f00feab7a2fbad3262eb6f9739d29/68747470733a2f2f73756275676f652e6769746875622e696f2f746966792f7374617469632f746966792d6c6f676f2e737667"></a>&nbsp;&nbsp;
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
        query += " SELECT DISTINCT ?manifest ?clabel WHERE { \n";
        query += "  ?manifest rdf:type sc:Manifest .  \n";
        query += "  ?manifest dcterms:isPartOf ?collection .  \n";
        query += "  ?manifest dcterms:subject ?subject .  \n";
        query += " filter (?subject = <" + this.$route.query.subject + "> )"
        //query += "  ?subject rdfs:label ?label .  \n";
        query += "  ?collection rdfs:label ?clabel .  \n";
        query += " } \n";

        axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
            .then(response => {

                let result = response.data.results.bindings
                this.result = result

                let manifests = ""

                for (let i = 0; i < result.length; i++) {
                    let obj = result[i]
                    manifests += obj.manifest.value + ";"
                }

                this.comp_url = "https://nakamura196.github.io/genji/mirador2/compare?manifest=" + manifests.slice(0, -1)

            }).catch(error => { console.log(error); });

    }
};
</script>