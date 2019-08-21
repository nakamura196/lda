<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">『校異源氏物語』の頁数でさがす</h3>
    
                <div class="form-group">
                    <input type="text" class="form-control" v-model="q" placeholder="ex. 5">
                </div>
    
                <table class="table mt-5">
                    <thead>
                        <tr>
                            <th scope="col">頁数</th>
                            <th scope="col">画像をみる</th>
                            <th scope="col">国立国会図書館デジタルコレクションでみる</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="obj in filteredUsers">
                            <th scope="row">{{obj.plabel.value}}（{{obj.label}}）</th>
                            <td>
                                <router-link class="btn btn-round btn-info" v-bind:to="{ path: 'listByPage', query: { page: obj.plabel.value}}"><i class="fas fa-search"></i></router-link>
                            </td>
                            <td>
                                <a :href="'http://dl.ndl.go.jp/info:ndljp/pid/3437686/'+(20+Math.floor(Number(obj.plabel.value) / 2))"><img height="45px" src="https://www.dl.ndl.go.jp/resources/images/dlicon.png"></a>
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
            q: "",
            result: []
        }
    },
    created: function() {

        let query = " PREFIX sc: <http://iiif.io/api/presentation/2#> \n";
        query += " SELECT DISTINCT ?plabel ?label ?page WHERE { \n";
        query += "  ?page rdfs:label ?plabel .  \n";
        query += "  ?page rdf:type <http://example.org/class/TaiseiPageID> . \n";
        query += "  ?anno dcterms:subject ?page .  \n";
        query += "  ?anno dcterms:isPartOf ?canvas .  \n";
        query += "  ?canvas dcterms:isPartOf ?manifest  .  \n";
        query += "  ?manifest rdf:type sc:Manifest  .  \n";
        query += "  ?manifest dcterms:subject ?subject .  \n";
        query += "  ?subject rdfs:label ?label .  \n";
        query += " } order by ?plabel \n";

        axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
            .then(response => {

                let result = response.data.results.bindings
                this.result = result

            }).catch(error => { console.log(error); });

    },
    computed: {
        filteredUsers: function() {

            var results = [];

            if (this.q == "") {
                return this.result
            }

            for (var i in this.result) {

                var result = this.result[i];

                if (result.plabel.value == this.q) {

                    results.push(result);

                }

            }

            return results;

        }
    }
};
</script>