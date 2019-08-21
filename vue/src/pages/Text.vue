<template>
    <div class="my-5">
        <div class="section">
            <div class="container">
    
                <h3 class="title">『校異源氏物語』の<a :href="url">テキスト</a>からさがす <span class="text-danger">（一部テキストのみ）</span></h3>
    
                <table class="table mt-5">
                    <thead>
                        <th>テキスト</th>
                        <th>画像をみる</th>
                        <th>国立国会図書館デジタルコレクションでみる</th>
                    </thead>
                    <tbody>
                        <tr v-for="line in lines">
                            <td>【{{line.id}}】 {{line.text}}</td>
                            <td>
                                <router-link v-if="line.camera" class="btn btn-round btn-info" v-bind:to="{ path: 'listByPage', query: { page: line.camera}}"><i class="fas fa-search"></i></router-link>
                            </td>
                            <td>
                                <a v-if="line.camera" :href="'http://dl.ndl.go.jp/info:ndljp/pid/3437686/'+(20+Math.floor(line.camera / 2))"><img height="45px" src="https://www.dl.ndl.go.jp/resources/images/dlicon.png"></a>
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
            url: "https://nakamura196.github.io/genji/tei/taisei.xml",
            lines: []
        }
    },
    created: function() {

        axios.get(this.url, {
                responseType: 'document'
            })
            .then(response => {

                let xml = response.data

                const lines = xml.getElementsByTagName('span');

                let arr = []

                for (let i = 0; i < lines.length; i++) {
                    let line = lines[i]


                    let attr = line.attributes[0].value

                    let attrs = attr.slice(1).split("-")
                    let line_index = Number(attrs[1])

                    let obj = {
                        "text": line.innerHTML,
                        "id": Number(attrs[0]) + "頁" + line_index + "行"
                    }

                    if (line_index == 1) {
                        obj["camera"] = Number(attrs[0])
                    }
                    arr.push(obj)
                }

                this.lines = arr



            }).catch(error => { console.log(error); });

    }
};
</script>