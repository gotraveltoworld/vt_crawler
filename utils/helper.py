from pyquery import PyQuery as pq

def get_words_meaning(div):
    divs = pq(div)('div').filter('.well-padding').filter('.md-text-size')
    learning_list = []
    for word in divs('div').filter('.group-element').items():
        word_obj = []
        for ele in word('.word-element').items():
            word_obj.append(ele.text().replace('&nbsp', ' '))
        learning_list.append(word_obj)
    return learning_list

"""html example for vocabulary.
    <div class="well-padding md-text-size">
        <div class="clearfix"></div>
        <div class="group-element">
            <div style="font-weight:bold;">1. superficial&nbsp&nbsp表面的 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/superficial.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/superficial?ref=everyday_play" target='_blank'>superficial</a>&nbsp&nbsp[ˋsupɚˋfɪʃəl]&nbsp&nbsp(adj.)&nbsp&nbsp表面的 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/shallow.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/shallow?ref=everyday_play" target='_blank'>shallow</a>&nbsp&nbsp[ˋʃælo]&nbsp&nbsp(adj.)&nbsp&nbsp淺的、膚淺的 </div>
        </div>
        <div class="clearfix"></div>
        <div class="group-element">
            <div style="font-weight:bold;">2. aspect&nbsp&nbsp觀點、方面 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/aspect.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/aspect?ref=everyday_play" target='_blank'>aspect</a>&nbsp&nbsp[ˋæspɛkt]&nbsp&nbsp(v.)&nbsp&nbsp觀點、方面 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/respect.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/respect?ref=everyday_play" target='_blank'>respect</a>&nbsp&nbsp[rɪˋspɛkt]&nbsp&nbsp(v.)&nbsp&nbsp尊敬 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/inspect.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/inspect?ref=everyday_play" target='_blank'>inspect</a>&nbsp&nbsp[ɪnˋspɛkt]&nbsp&nbsp(v.)&nbsp&nbsp檢查 </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/suspect.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/suspect?ref=everyday_play" target='_blank'>suspect</a>&nbsp&nbsp[səˋspɛkt]&nbsp&nbsp(v.)&nbsp&nbsp懷疑、察覺 </div>
        </div>
        <div class="clearfix"></div>
        <div class="group-element">
            <div style="font-weight:bold;">3. go through sth&nbsp&nbsp經歷、仔細或系統地研究或檢查(尤為尋找、發現某事物) </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/go%20through%20sth.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/go through sth?ref=everyday_play" target='_blank'>go through sth</a>&nbsp&nbsp(phr.)&nbsp&nbsp經歷、仔細或系統地研究或檢查(尤為尋找、發現某事物) </div>
            <div class="clearfix"></div>
            <ul class='controls pull-left'>
                <li>
                    <a class="audioButton" href="/player/encounter.mp3"></a>
                </li>
            </ul>
            <div class="pull-left word-element">
                <a href="/definition/encounter?ref=everyday_play" target='_blank'>encounter</a>&nbsp&nbsp[ɪnˋkaʊntɚ]&nbsp&nbsp(v.)&nbsp&nbsp遇到（困難，危險等） </div>
        </div>
    </div>
"""