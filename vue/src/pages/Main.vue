<template>
    <div class="row">
    
        <span style="display:none;">{{this.id}}</span>
        <span style="display:none;">{{this.id_modern}}</span>
    
        <div class="col-md-6 pl-5">
            <iframe :src="mirador_path" seamless width="100%" height="850px" style="border: none;"></iframe>
            <p><a target="_blank" :href="mirador_path"><span class="fa fa-expand fa-lg fa-fw"></span> 全画面表示</a></p>
        </div>
        <div class="col-md-6 pr-5">
    
            <div>
    
                <div class="card scroll mb-2 vertical" id="org">
                    <div class="card-body">
                        <h3>翻刻文（校異源氏物語）</h3>
                        <div>
                            <div v-for="(line, line_id) of lines_org" :id="line_id" v-on:mouseover="mouseover" @click="clickSmoothScroll(line_id)">
    
                                <div v-if="line.page" class="mr-2">
                                    <b class="mb-2">p.{{line.page}}</b>
                                    <el-tooltip class="item" content="東大本" placement="top">
                                        <img @click="changeImage(line.page)" width="30x" src="https://iiif.dl.itc.u-tokyo.ac.jp/images/iiif.png" class="mb-2 btn-tooltip" />
                                    </el-tooltip>
                                    <img @click="changeImage2(line.page)" width="30px" src="https://www.dl.ndl.go.jp/resources/images/dlicon.png" />
                                </div>
    
                                <span :style="line.selected ? 'background-color : yellow;' : null" v-for="(node, index) of line.array">
                                                    <el-tooltip
                                                        class="item"
                                                        :content=node.note
                                                        placement="top"
                                                        v-if="node.note"
                                                    >
                                                    <span class="text-info btn-tooltip">{{node.text}}</span>
                                </el-tooltip>
                                <span v-else>{{node.text}}</span>
                                </span>
    
    
    
                                <br/>
                            </div>
                        </div>
                    </div>
                </div>
    
                <div class="card scroll2 vertical" id="modern">
                    <div class="card-body">
                        <h3>現代語訳（青空文庫・与謝野晶子訳）</h3>
                        <div :style="line.selected ? 'background-color : yellow;' : null" v-for="(line, line_id) of lines_modern" :id="line_id" v-on:mouseover="mouseover_modern" @click="clickSmoothScrollModern(line_id)">
                            <span v-for="(node, index) of line.array">      
                                                                                        <span>{{node.text}}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { Tooltip } from 'element-ui';

export default {
    components: {
        [Tooltip.name]: Tooltip
    },
    data() {
        return {
            url: "https://nakamura196.github.io/genji/tei/taisei.xml",
            url_modern: "https://nakamura196.github.io/genji/tei/yosano_genji_kiritsubo_ids.xml",
            url_map: "https://api.myjson.com/bins/tm2nh",
            lines_org: {},
            lines_modern: {},
            id: "", //重要
            id_modern: "",
            modern_org_map: {},
            org_modern_map: {},
            mirador_path: "https://nakamura196.github.io/genji/mirador2/compare4?params=[{%22annotationlist%22:%22https://nakamura196.github.io/genji/ugm/kyushu2/anno/anno_002_a4017e888caba178255bacd1fdff70fd.json%22},{%22annotationlist%22:%22https://nakamura196.github.io/genji/ugm/kyushu/anno/anno_001_8e84f8aa1978545e9da7a3c9058d0528.json%22},{%22annotationlist%22:%22https://nakamura196.github.io/genji/ugm/utokyo/anno/anno_004_3423f58415e722cdcbe59823c9eb1467.json%22},{%22manifest%22:%22https://www.dl.ndl.go.jp/api/iiif/3437686/manifest.json%22,%22canvas%22:%22https://www.dl.ndl.go.jp/api/iiif/3437686/canvas/22%22}]"
        }
    },
    created: function() {

        this.url = this.$route.query.left ? this.$route.query.left : this.url
        this.url_modern = this.$route.query.right ? this.$route.query.right : this.url_modern
        this.url_map = this.$route.query.map ? this.$route.query.map : this.url_map

        this.map()

    },
    methods: {
        map: function() {
            let vm = this
            axios.get(this.url_map)
                .then(response => {
                    let modern_org_map = response.data
                    this.modern_org_map = modern_org_map
                    let org_modern_map = {}
                    this.org_modern_map = org_modern_map
                    for (let line_modern in modern_org_map) {
                        let org_ids = modern_org_map[line_modern]
                        for (let i = 0; i < org_ids.length; i++) {
                            let org_id = org_ids[i]
                            if (!org_modern_map[org_id]) {
                                org_modern_map[org_id] = []
                            }
                            org_modern_map[org_id].push(line_modern)
                        }
                    }

                    this.org()
                    this.modern()
                })
                .catch(err => {
                    vm.errored = true,
                        vm.error = err
                })
                .finally(() => vm.loading = false)
        },
        org: function(data) {

            axios.get(this.url, {
                    responseType: 'document'
                })
                .then(response => {

                    let xml = response.data

                    const div = xml.getElementsByTagName('div')[0];

                    const lines = div.querySelectorAll('span[*|id]');

                    let lines_org = {}
                    this.lines_org = lines_org

                    for (let i = 0; i < lines.length; i++) {
                        let line = lines[i]

                        let line_id = line.attributes[0].value

                        let nodes = line.childNodes

                        let line_obj = {
                            "array": [],
                            "selected": false
                        }

                        let line_index = Number(line_id.split("-")[1])
                        if (line_index == 1) {
                            line_obj["page"] = Number(line_id.split("-")[0].slice(1))
                        }

                        lines_org[line_id] = line_obj

                        for (let j = 0; j < nodes.length; j++) {
                            let node = nodes[j]

                            let obj = {
                                "text": node.innerText || node.textContent
                            }

                            if (node.nodeType != Node.TEXT_NODE) {

                                let id = node.attributes[0].value.split("#")[1]

                                let stmt = xml.querySelector("note[*|id='" + id + "']")

                                obj["note"] = stmt.innerHTML
                            }

                            line_obj["array"].push(obj)
                        }
                    }
                })

        },
        modern: function(data) {

            axios.get(this.url_modern, {
                    responseType: 'document'
                })
                .then(response => {

                    let xml = response.data

                    const div = xml.getElementsByTagName('body')[0];

                    const lines = div.querySelectorAll('*[*|id]');

                    let lines_modern = {}
                    this.lines_modern = lines_modern

                    for (let i = 0; i < lines.length; i++) {
                        let line = lines[i]

                        let line_id = line.attributes[0].value

                        let nodes = line.childNodes

                        let line_obj = {
                            "array": [],
                            "selected": false
                        }

                        lines_modern[line_id] = line_obj

                        for (let j = 0; j < nodes.length; j++) {
                            let node = nodes[j]

                            let obj = {
                                "text": node.innerText || node.textContent
                            }

                            line_obj["array"].push(obj)
                        }
                    }
                })

        },
        mouseover: function(data) {

            if (data.target.attributes.length > 0 && data.target.attributes[0].name == "id") {



                let lines = this.lines_org
                let target_id = data.target.attributes[0].value
                for (let line_id in lines) {
                    let selected = false
                    if (line_id == target_id) {
                        selected = true
                    }
                    lines[line_id].selected = selected
                }

                let modern_ids = this.org_modern_map[target_id]

                if (!modern_ids) {
                    modern_ids = []
                }

                let lines_modern = this.lines_modern
                for (let line_id in lines_modern) {
                    let selected = false
                    if (modern_ids.indexOf(line_id) != -1) {
                        selected = true
                    }
                    lines_modern[line_id].selected = selected
                }

                this.id = target_id //おまじない
            }
        },
        clickSmoothScroll: function(target_id) {
            let modern_ids = this.org_modern_map[target_id]

            if (modern_ids != null) {
                this.$SmoothScroll(
                    document.querySelector('#' + modern_ids[0]).getBoundingClientRect().x - document.querySelector('#modern').getBoundingClientRect().x,
                    400,
                    null,
                    document.querySelector('#modern'),
                    'x'
                )
            }
        },
        mouseover_modern: function(data) {
            if (data.target.attributes.length > 0 && data.target.attributes[0].name == "id") {

                let lines = this.lines_modern
                let target_id = data.target.attributes[0].value

                for (let line_id in lines) {
                    let selected = false
                    if (line_id == target_id) {
                        selected = true
                    }
                    lines[line_id].selected = selected
                }

                let org_ids = this.modern_org_map[target_id]

                if (!org_ids) {
                    org_ids = []
                }

                let lines_org = this.lines_org
                for (let line_id in lines_org) {
                    let selected = false
                    if (org_ids.indexOf(line_id) != -1) {
                        selected = true
                    }
                    lines_org[line_id].selected = selected
                }

                this.id_modern = target_id //おまじない
            }
        },
        clickSmoothScrollModern: function(target_id) {
            let org_ids = this.modern_org_map[target_id]

            if (org_ids != null) {
                this.$SmoothScroll(
                    document.querySelector('#' + org_ids[0]).getBoundingClientRect().x - document.querySelector('#org').getBoundingClientRect().x,
                    400,
                    null,
                    document.querySelector('#org'),
                    'x'
                )
            }

        },
        changeImage: function(page) {
            //this.mirador_path = ""

            let query = " PREFIX sc: <http://iiif.io/api/presentation/2#> \n";
            query += " SELECT DISTINCT ?anno_id WHERE { \n";
            query += "  ?page rdfs:label \"" + page + "\"^^xsd:int . \n";
            query += "  ?page rdf:type <http://example.org/class/TaiseiPageID> . \n";
            query += "  ?anno_id dcterms:subject ?page . \n";
            query += " } \n";

            axios.get("https://dydra.com/ut-digital-archives/genji/sparql?query=" + encodeURIComponent(query) + "&output=json")
                .then(response => {

                    let result = response.data.results.bindings

                    let params = []
                    for (let i = 0; i < result.length; i++) {
                        params.push({
                            "annotationlist": result[i].anno_id.value
                        })
                    }

                    params.push({
                        "manifest": "https://www.dl.ndl.go.jp/api/iiif/3437686/manifest.json",
                        "canvas": "https://www.dl.ndl.go.jp/api/iiif/3437686/canvas/" + (20 + Math.floor(Number(page) / 2))
                    })

                    this.mirador_path = "https://nakamura196.github.io/genji/mirador2/compare4?params=" + JSON.stringify(params)


                }).catch(error => { console.log(error); });

        },
        changeImage2: function(page) {

            let params = [{
                "manifest": "https://www.dl.ndl.go.jp/api/iiif/3437686/manifest.json",
                "canvas": "https://www.dl.ndl.go.jp/api/iiif/3437686/canvas/" + (20 + Math.floor(Number(page) / 2))
            }]

            this.mirador_path = "https://nakamura196.github.io/genji/mirador2/compare4?params=" + JSON.stringify(params)

        }
    }
};
</script>


<style>
.scroll {
    max-height: 525px;
    overflow-y: auto;
}

.scroll2 {
    max-height: 325px;
    overflow-y: auto;
}

.vertical {
    -webkit-writing-mode: vertical-rl;
    -ms-writing-mode: tb-rl;
    writing-mode: vertical-rl;
}
</style>