<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">帖名でさがす</h3>
    
                <div class="form-group">
                    <input type="text" class="form-control" v-model="q" placeholder="ex. 桐壺">
                </div>
    
                <table class="table mt-5">
                    <thead>
                        <tr>
                            <th scope="col">帖名</th>
                            <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="obj in filteredUsers">
                            <th scope="row">{{obj.label}}</th>
                            <td>
                                <router-link class="btn btn-round btn-info" v-bind:to="{ path: 'listByWork', query: { subject: obj.subject.value}}"><i class="fas fa-search"></i></router-link>
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
        query += " SELECT DISTINCT ?label ?subject WHERE { \n";
        query += "  ?manifest rdf:type sc:Manifest  .  \n";
        query += "  ?manifest dcterms:subject ?subject .  \n";
        query += "  ?subject rdfs:label ?label .  \n";
        query += " } order by ?manifest \n";

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

                if (result.label.indexOf(this.q) != -1) {

                    results.push(result);

                }

            }

            return results;

        }
    }
};
</script>