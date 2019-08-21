<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">『源氏物語』読解支援システム・プロトタイプ</h3>
    
                <span style="display:none;">{{this.id}}</span>
                <span style="display:none;">{{this.id_modern}}</span>
    
                <div class="row">
    
                    <div class="col">
                        <div class="card">
                            <div class="card-body">
                                <h3>翻刻文（校異源氏物語）</h3>
                                <div class="scroll" id="org">
                                    <div :style="line.selected ? 'background-color : yellow;' : null" v-for="(line, line_id) of lines_org" :id="line_id" v-on:mouseover="mouseover" @click="clickSmoothScroll(line_id)">
    
                                        <router-link v-if="line.page" class="mr-2" v-bind:to="{ path: 'listByPage', query: { page: line.page}}"><img src="https://iiif.dl.itc.u-tokyo.ac.jp/images/iiif.png" /></router-link>
    
                                        <span v-for="(node, index) of line.array">      
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
                    </div>
                    <div class="col">
                        <div class="card">
                            <div class="card-body">
                                <h3>現代語訳（青空文庫）</h3>
                                <div class="scroll" id="modern">
                                    <div :style="line.selected ? 'background-color : yellow;' : null" v-for="(line, line_id) of lines_modern" :id="line_id" v-on:mouseover="mouseover_modern" @click="clickSmoothScrollModern(line_id)">
                                        <span v-for="(node, index) of line.array">{{node.text}}</span>
                                    </div>
                                </div>
                            </div>
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
            org_modern_map: {}
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
                    for (let line_now in modern_org_map) {
                        let org_ids = modern_org_map[line_now]
                        for (let i = 0; i < org_ids.length; i++) {
                            let org_id = org_ids[i]
                            if (!org_modern_map[org_id]) {
                                org_modern_map[org_id] = []
                            }
                            org_modern_map[org_id].push(line_now)
                        }
                    }

                    this.org()
                    this.now()
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
        now: function(data) {

            axios.get(this.url_modern, {
                    //responseType: 'document'
                })
                .then(response => {

                    let parser = new DOMParser();

                    let text = response.data

                    let xml = parser.parseFromString(text, 'text/xml');

                    const div = xml.getElementsByTagName('body')[0];

                    const lines = div.querySelectorAll('[*|id]');

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

                let now_ids = this.org_modern_map[target_id]

                if (!now_ids) {
                    now_ids = []
                }

                let lines_modern = this.lines_modern
                for (let line_id in lines_modern) {
                    let selected = false
                    if (now_ids.indexOf(line_id) != -1) {
                        selected = true
                    }
                    lines_modern[line_id].selected = selected
                }

                this.id = target_id //おまじない
            }
        },
        clickSmoothScroll: function(target_id) {
            let now_ids = this.org_modern_map[target_id]

            if (now_ids != null) {

                //if(document.querySelector('#modern').getBoundingClientRect().y < document.querySelector('#'+now_ids[0]).getBoundingClientRect().y){
                this.$SmoothScroll(
                    document.querySelector('#' + now_ids[0]).getBoundingClientRect().y - document.querySelector('#modern').getBoundingClientRect().y,
                    400,
                    null,
                    document.querySelector('#modern'),
                    'y'
                )
                //}
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
            let modern_ids = this.modern_org_map[target_id]

            if (modern_ids != null) {

                //if(document.querySelector('#org').getBoundingClientRect().y < document.querySelector('#'+modern_ids[0]).getBoundingClientRect().y){
                this.$SmoothScroll(
                    document.querySelector('#' + modern_ids[0]).getBoundingClientRect().y - document.querySelector('#org').getBoundingClientRect().y,
                    400,
                    null,
                    document.querySelector('#org'),
                    'y'
                )
                //}
            }

        },
    }
};
</script>

<style>
.scroll {
    max-height: 600px;
    overflow-y: auto;
}
</style>