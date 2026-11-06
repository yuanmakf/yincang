import os, re

base = r"F:/软件/自媒体工具/折线~丢丢/折线版独立/YinCangZhe"
out  = r"F:/软件/自媒体工具/折线~丢丢/单文件版/index.html"

def r(p):
    with open(os.path.join(base, p), encoding='utf-8') as f:
        return f.read()

html = r('index.html')
mengban_css = r('../css/mengban.css')
index_css   = r('index.css')
head_js = r('../js/head.js')
jieLiu_js = r('../module/jieLiu.js')
root_js = r('../module/root.js')
zb_js = r('../module/ziyuanBianhao.js')
openurl_js = r('../module/openUrl.js')
td_js = r('../module/tianjiaDandu.js')
index_js = r('index.js')
ym_js = r('../js/yingyongMengban.js')
tongji_js = r('../js/tongji.js')
stop_js = r('../js/stop.js')

# 关键：openUrl.js 模板字符串内含多处 </script>，必须全部转义，否则会截断外层脚本块
openurl_js = re.sub(r'</script>', '<\\/script>', openurl_js)

# ====== #1 放开 F12 / 右键 / 快捷键 / 禁用保存 等保护逻辑 ======
# 原 stop.js 禁用了 F12、Ctrl+Shift+I/J、Ctrl+U、Ctrl+S、Ctrl+/- 与右键菜单。
# 单文件版是本地工具，放开这些方便调试与保存。
stop_js = '/* F12 / 右键 / 快捷键已放开，便于调试与保存 */'

# ====== 条纹 360° 旋转的前提：把平铺范围从"一屏"扩大为"屏幕对角线的正方形" ======
# 原始 index.js 用 window.innerWidth/innerHeight（unicode 转义混淆）决定行列数，只铺满一屏；
# 旋转后四角会露空。这里替换为 window.__stripeW（预置脚本按屏幕对角线计算的正方形边长），
# 条纹在任意旋转角度下都铺满全屏，且条纹粗细不受旋转影响（纯旋转、不缩放）。
_IW = r"window['\u0069\u006E\u006E\u0065\u0072\u0057\u0069\u0064\u0074\u0068']"
_IH = r"window['\u0069\u006E\u006E\u0065\u0072\u0048\u0065\u0069\u0067\u0068\u0074']"
assert _IW in index_js, "innerWidth 转义未匹配"
assert _IH in index_js, "innerHeight 转义未匹配"
index_js = index_js.replace(_IW, 'window.__stripeW').replace(_IH, 'window.__stripeW')

# 条纹缩放：在 newSvg 入口注入缩放因子 _ss（瓷砖宽/高/线宽同乘），配合 __stripeW 的
# 大面积平铺，任意缩放倍数都重新生成、铺满全屏（"无限生成"且永不露空）。
_NSVG = 'function newSvg(w,h){'
assert _NSVG in index_js and index_js.count(_NSVG) == 1, "newSvg 定义未匹配"
index_js = index_js.replace(_NSVG,
    'function newSvg(w,h){var _ss=window.__ss||1;w*=_ss;h*=_ss;b=10*_ss;window.__fineGeo=null;'
    'if(window.__fineTile&&(w<2*b||h<8)){window.__fineTile(w,h,b);return;}')

# ====== #5 手机端可用：去掉 head.js 的移动端跳转 与 QQ 浏览器拦截 ======
# 原逻辑：移动端 UA 会被跳到 /go.html?to=pc（该页面不存在 → 空白），QQ 浏览器被 alert+空白。
# 去掉这两段，手机/QQ 浏览器即可正常打开。
head_js = head_js.replace(
    'if (/MicroMessenger|Wechat|Mobile|Android|iPhone/i.test(window.$head.ua) && !/denglu|houtai/.test(window.$head.href)) {\n  location.href = "/go.html?to=pc";\n}',
    '')
head_js = re.sub(r'if \(/QQ/i\.test\(window\.\$head\.ua\)\) \{.*?\$blank\(\);\s*\}', '', head_js, flags=re.S)

# 1. 删除指定文字
A = '''    <h3>截图保存：</h3>
    <ul>
        <li>截图不会？ （不会别用）</li>

    </ul>
'''
B = '''    <h3>相关：</h3>
    <ul>
        <li><a>内容是扒的网页，别较真</a></li>
        <li><a>作者只是学习研究，别贩卖</a></li>
        <li><a>你卖了也和我没关系啊！！！！</a></li>

    </ul>
'''
assert A in html and B in html
html = html.replace(A, '').replace(B, '')
html = html.replace('<title>隐藏文字【折线版】（改变窗口后 从新刷新浏览器）</title>', '<title>隐藏文字【折线版】</title>')
html = html.replace('<h3>隐藏文字【折线版】 （改变窗口后 从新刷新浏览器）</h3>', '<h3>隐藏文字【折线版】</h3>')
html = html.replace('（自己去下，不会别用）', '')  # 删字体提示里的残留

# 4/5/6（上轮）：文字输入框改 textarea；删除"文字对齐"与"如需换行加符号：|"
# 文字框直接作为底部抽屉 .caozuo 的第一项（不再单独置顶）
html = html.replace('    <label>▶ 输入文字：<input type="text" value="隐藏文字" /></label>',
                    '    <label class="inputRow">输入文字：<textarea id="wenziInput" rows="1" style="width:100%;box-sizing:border-box;font-size:16px;resize:vertical;">隐藏文字</textarea></label>')
html = html.replace('''    <ul>
        <li>
            文字对齐：<select name="textAlign">
            <option value="left">左对齐</option>
            <option value="center">居中</option>
            <option value="right">右对齐</option>
            </select>
        </li>
        <li>如需换行，加符号：|</li>
    </ul>''', '')

# ====== #3 删除：顶部标题 / 副标题（保留浏览器标签标题） ======
html = html.replace('<h3>隐藏文字【折线版】</h3>', '')
html = html.replace('<p>本独立包仅包含【折线版】。</p>', '')
# 删除"面板与导出"标题、"隐藏面板"按钮、"比例"下拉 —— 仅保留 导出 PNG / JPG
gao_label_orig = '    <label>▶ 高(向左变细)：<input name="gao" type="range" min="50" max="300" step="2" value="100" /></label>'
assert gao_label_orig in html
new_controls = gao_label_orig + '''
    <div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;">
      <button id="btnImg" type="button" style="padding:6px 10px;cursor:pointer;background:#555;color:#fff;border:none;">导入图片</button>
      <button id="btnDel" type="button" style="padding:6px 10px;cursor:pointer;background:#933;color:#fff;border:none;">删除图片</button>
      <button id="btnPng" type="button" style="padding:6px 10px;cursor:pointer;background:#0b5;color:#fff;border:none;">导出 PNG</button>
      <button id="btnJpg" type="button" style="padding:6px 10px;cursor:pointer;background:#05b;border:none;color:#fff;">导出 JPG</button>
    </div>
'''
html = html.replace(gao_label_orig, new_controls)
html = html.replace('▶', '')  # 3：删除所有 ▶（含插入的控件与原面板标签、<span>▶</span>）
html = html.replace('<span></span>', '')  # 清掉删 ▶ 后留下的空 span
html = html.replace('<h3>折线设置（可控制线条粗细）：</h3>', '')  # 删除折线设置标题（保留宽/高滑块）

# ====== #3 合并 8 个滑块为 1 个主滑块 + 标签行（原滑块移入隐藏容器，仍驱动原渲染逻辑） =====
slider_block = '''    <label> 文字大小：<input name="fontSize" type="range" min="50" max="700" step="10" value="240" /></label>
    <label> 文字粗细：<input name="fontWeight" type="range" min="100" max="900" step="100" value="700" /></label>
    <label> 文字行距：<input name="lineHeight" type="range" min="1" max="3" step="0.1" value="1" /></label>
    <label> 文字间距：<input name="letterSpacing" type="range" min="0" max="500" step="10" value="0" /></label>
    <label> 文字透明：<input name="opacity" type="range" min="0" max="1" step="0.1" value="1" /></label>
    <section><label for="ziti" >点此：自定义字体</label><input id="ziti" type="file" /><a ></a></section>
    
    <label> 宽(向右变细)：<input name="kuan" type="range" min="50" max="200" step="2" value="100" /></label>
    <label> 高(向左变细)：<input name="gao" type="range" min="50" max="300" step="2" value="100" /></label>'''
master_block = '''    <div id="masterWrap" style="margin:6px 0;">
      <div id="masterRow" style="display:flex;gap:8px;align-items:center;">
        <input id="masterNum" type="number" style="flex:0 0 auto;width:64px;background:#333;color:#fff;border:1px solid #555;border-radius:6px;padding:4px 6px;font-size:14px;box-sizing:border-box;" />
        <input id="masterSlider" type="range" style="flex:1;width:auto;" />
      </div>
      <div id="propLabels" style="display:flex;flex-wrap:wrap;margin-top:6px;">
        <span class="plabel" data-name="kuan">宽(向右变细)</span>
        <span class="plabel" data-name="gao">高(向左变细)</span>
        <span class="plabel" data-name="stripeRot">条纹旋转</span>
        <span class="plabel" data-name="stripeScale">条纹缩放</span>
        <span class="plabel active" data-name="fontSize">文字大小</span>
        <span class="plabel" data-name="imgScale">图片大小</span>
        <span class="plabel" data-name="fontWeight">文字粗细</span>
        <span class="plabel" data-name="letterSpacing">文字间距</span>
        <span class="plabel" data-name="lineHeight">文字行距</span>
        <span class="plabel" data-name="opacity">文字透明</span>
        <span class="plabel" data-name="ziti">替换字体</span>
      </div>
      <div id="presetBar">
        <select id="presetSel" title="选择数值方案"></select>
        <button id="presetSave" type="button">保存</button>
        <button id="presetDel" type="button">删除</button>
      </div>
    </div>
    <div id="hiddenOriginals" style="display:none;">
      <label> 文字大小：<input name="fontSize" type="range" min="50" max="700" step="10" value="240" /></label>
      <label> 文字粗细：<input name="fontWeight" type="range" min="100" max="900" step="100" value="700" /></label>
      <label> 文字行距：<input name="lineHeight" type="range" min="1" max="3" step="0.1" value="1" /></label>
      <label> 文字间距：<input name="letterSpacing" type="range" min="0" max="500" step="10" value="0" /></label>
      <label> 文字透明：<input name="opacity" type="range" min="0" max="1" step="0.1" value="1" /></label>
      <section><label for="ziti" >点此：自定义字体</label><input id="ziti" type="file" /><a ></a></section>
      <label> 宽(向右变细)：<input name="kuan" type="range" min="1" max="200" step="1" value="100" /></label>
      <label> 高(向左变细)：<input name="gao" type="range" min="1" max="300" step="1" value="100" /></label>
    </div>'''
assert slider_block in html, "slider_block 未匹配"
html = html.replace(slider_block, master_block)

# ====== #2 把 .wenzi + .zhexian 包进 #stage（可拖动/缩放） ======
html = html.replace('<div class="wenzi">隐藏文字</div>\n<div class="zhexian"></div>',
                    '<div id="stage">\n<div class="wenzi">隐藏文字</div>\n<div id="zclip"><div class="zhexian"></div></div>\n</div>')

# 注入 #stage 与面板样式：条纹固定整屏可旋转；文字/图片独立图层可拖动；真·屏幕居中
stage_css = '''<style>
#stage{position:absolute;inset:0;}
/* 文字层：只覆盖"工作区"（面板以上区域，bottom=面板高度），并在其中上下左右居中。
   不裁剪（overflow 可见）：文字放大超出屏幕时向左右对称延伸，被条纹/面板底衬自然
   盖住，无边界感；超出工作区下缘的部分被面板(z1001)与底衬(z4)遮住 */
.wenzi{position:fixed!important;top:0!important;bottom:var(--panel-h,0px)!important;left:0!important;right:0!important;width:100%!important;height:auto!important;display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;justify-content:center!important;align-items:center!important;text-align:center!important;white-space:nowrap!important;box-sizing:border-box!important;z-index:1;touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab;}
.wenzi:active{cursor:grabbing;}
/* 工作区裁剪容器：条纹只显示到面板顶端为止（面板以下的折线一律裁掉），
   条纹旋转中心 = 工作区中心；pointer-events:none 让拖动穿透到下面的文字/图片 */
#zclip{position:fixed!important;top:0!important;left:0!important;right:0!important;bottom:var(--panel-h,0px)!important;overflow:hidden!important;pointer-events:none!important;z-index:3;}
/* 条纹层：以工作区（面板以上区域）中心为中心的正方形，rotate 任意角度都被 zclip 裁剪、始终铺满工作区 */
.zhexian{position:absolute!important;top:50%!important;left:50%!important;width:var(--stripe-size,300vmax)!important;height:var(--stripe-size,300vmax)!important;transform:translate(-50%,-50%) rotate(var(--stripe-rot,0deg))!important;overflow:hidden!important;pointer-events:none!important;}
/* 导入的图片：独立图层（与文字共存），可自由拖动，同样藏在条纹下面 */
#userImg{position:fixed;left:50%;top:50%;max-width:80vw;max-height:80vh;object-fit:contain;z-index:2;cursor:grab;touch-action:none;user-select:none;-webkit-user-select:none;-webkit-user-drag:none;}
#userImg:active{cursor:grabbing;}
/* 整个控制面板固定在底部抽屉（手机/电脑统一黑色系） */
.caozuo{position:fixed!important;bottom:0!important;left:0!important;right:0!important;top:auto!important;max-height:62vh;overflow:auto;background:#222;color:#e8e8e8;padding:10px 12px;margin:0!important;max-width:none!important;box-shadow:0 -2px 10px rgba(0,0,0,.35);z-index:1001;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;}
.caozuo label,.caozuo section{color:#e8e8e8;}
.caozuo input[type=text],.caozuo textarea{color:#111;}
/* 面板顶部拖动把手：点击收起 / 拖动展开；上下各留3px，紧凑不占空间 */
#panelHandle{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:center;height:10px;margin:-10px -12px 4px;background:#222;color:#fff;cursor:grab;user-select:none;touch-action:none;}
#panelHandle:active{cursor:grabbing;}
#panelHandle .grip{width:40px;height:4px;border-radius:2px;background:#bbb;}
.caozuo.collapsed{max-height:10px!important;overflow:hidden!important;}
.caozuo.collapsed>#panelHandle{margin-bottom:0;}
.caozuo.collapsed>:not(#panelHandle){display:none!important;}
/* 属性标签：横向一排，左右滑动选择（手机端手指左右滑即可，参考比例选择条样式） */
#propLabels{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:8px!important;margin-top:8px!important;-webkit-overflow-scrolling:touch;scrollbar-width:none;}
#propLabels::-webkit-scrollbar{display:none;}
.plabel{flex:0 0 auto;cursor:pointer;font-size:13px;line-height:1.5;color:#bbb;padding:4px 10px;border:1px solid #555;border-radius:6px;user-select:none;-webkit-user-select:none;white-space:nowrap;}
.plabel.active{color:#fff;border-color:#ff5c8a;background:rgba(255,92,138,.22);}
#masterSlider{width:100%;accent-color:#ff5c8a;height:22px;margin:2px 0 0;}
/* 拉杆左侧数值输入框：可直接输入数值精确修改 */
#masterNum{-moz-appearance:textfield;appearance:textfield;}
#masterNum::-webkit-outer-spin-button,#masterNum::-webkit-inner-spin-button{-webkit-appearance:none;margin:0;}
/* 数值方案栏：下拉选择已保存方案 + 保存 / 删除 */
#presetBar{display:flex;gap:8px;margin-top:8px;align-items:stretch;}
#presetSel{flex:1;min-width:0;background:#333;color:#eee;border:1px solid #555;border-radius:6px;padding:5px 8px;font-size:13px;}
#presetSave,#presetDel{flex:0 0 auto;background:#ff5c8a;color:#fff;border:none;border-radius:6px;padding:5px 14px;font-size:13px;cursor:pointer;}
#presetDel{background:#444;color:#ddd;}
/* 电脑端：面板居中悬浮（宽990，不再通栏贴底）；手机端保持原样 */
@media (min-width:1020px){
  .caozuo{left:50%!important;right:auto!important;transform:translateX(-50%)!important;width:990px;max-width:calc(100vw - 24px);bottom:14px;border-radius:12px;}
  /* 电脑端面板悬浮后，两侧露出的条纹区域用面板同色填充（高度=面板+底部悬空距离） */
  #panelBackdrop{height:calc(var(--panel-h,0px) + 14px);}
}
/* 面板底衬：全宽、与面板同色，盖住面板两侧露出的白色条纹 */
#panelBackdrop{position:fixed;left:0;right:0;bottom:0;height:var(--panel-h,0px);background:#222;z-index:4;pointer-events:none;}
/* 文字输入框：块级布局（标签一行、输入框一行），完整显示不被 flex 压缩裁切；
   高度由 JS 按内容自适应（默认紧贴文字高度） */
.caozuo label.inputRow{display:block!important;line-height:1.8;}
#wenziInput{line-height:1.4;display:block;overflow:hidden;}
/* 恢复面板内（含输入框）的文字选择/复制：画布层为拖动禁了选择，面板必须显式放开 */
.caozuo, .caozuo *{user-select:text!important;-webkit-user-select:text!important;-webkit-touch-callout:default!important;}
html,body{height:100%;overflow:hidden;overscroll-behavior:none;}
</style>
'''
# 安全 localStorage 垫片（强制覆盖，避免 file:// 下访问 localStorage 抛 SecurityError）
localStorage_shim = '<script>try{var __ls={};Object.defineProperty(window,"localStorage",{configurable:true,value:{getItem:function(k){return (k in __ls)?__ls[k]:null},setItem:function(k,v){__ls[k]=String(v)},removeItem:function(k){delete __ls[k]},clear:function(){__ls={}}}});}catch(e){}</script>'
# 预置脚本：计算"屏幕对角线正方形"边长（条纹盒尺寸），供 index.js 平铺与 CSS 旋转共用；
# 并定义点阵版/直线版的备用瓷砖生成器（index.js 的 newSvg 在非折线模式时调用）
stripe_pre = '''<script>(function(){
  var w=window.innerWidth||document.documentElement.clientWidth,h=window.innerHeight||document.documentElement.clientHeight;
  var S=Math.ceil(Math.sqrt(w*w+h*h)*1.02)+40;
  window.__stripeW=S;
  var de=document.documentElement;
  de.style.setProperty('--stripe-size',S+'px');
  de.style.setProperty('--stripe-rot','0deg');
  // 宽/高"归1"支持：kuan/gao 低于原始下限(50)时，原始多边形几何会退化（点坐标交叉、图案崩坏）。
  // 这里接管生成：线宽/缝隙/形状整体等比缩小，图案完整且更细密；同时钳制瓷砖数量防止卡顿。
  window.__fineTile=function(w,h,b){
    var S=window.__stripeW||2000;
    var fw=Math.max(0.05,Math.min(1,w/50));          // 横向缩放比（随 kuan 归1 而缩小）
    var b2=Math.max(b*fw, Math.min(5,b));            // 线宽等比缩，但钳下限保周期≥10px、控元素数
    var g2=2*fw;                                     // 缝隙同比例缩
    var W=Math.max(w, 2*b2-g2+1);                    // 瓷砖宽（不小于图形最小宽度，避免露缝）
    var cols=Math.ceil(S/(2*b2))+Math.ceil(W/(2*b2));
    var rowsMax=Math.max(8, Math.floor(25000/cols)); // 元素总数上限 ≈2.5万，防手机卡顿
    var H=Math.max(h, Math.ceil(S/rowsMax));         // 瓷砖高（纵向周期）钳下限
    var period=2*b2;
    // 与原始几何同构的多边形（b→b2、固定2px缝隙→g2 等比缩放，形状随 W/H 自适应）
    var blk=[[0,0],[b2,0],[W-b2+g2,H/2],[b2,H],[0,H],[W-2*b2+g2,H/2]];
    var wht=[[b2+g2,0],[2*b2-g2,0],[W,H/2],[2*b2-g2,H],[b2+g2,H],[W-b2+g2,H/2]];
    function pts(a){return a.map(function(p){return p[0]+','+p[1];}).join(' ');}
    var tile='<svg width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg">'
      +'<polygon points="'+pts(blk)+'" fill="black"/>'
      +'<polygon points="'+pts(wht)+'" fill="white"/></svg>';
    var rowHtml='';for(var i=0;i<cols;i++)rowHtml+=tile;
    var out='';for(var j=0;j<Math.ceil(S/H);j++)out+='<section>'+rowHtml+'</section>';
    var zx=document.querySelector('.zhexian');
    if(zx){
      zx.innerHTML=out;
      var st=document.createElement('style');
      st.textContent='svg{margin-left:-'+(W-period)+'px;}';
      document.head.appendChild(st);
    }
    window.__fineGeo={b:b2,g:g2};                    // 供导出 canvas 精确复现
  };
})();</script>'''
html = html.replace('</head>', stripe_pre + localStorage_shim + stage_css + '</head>')

# 3. 内联 css / js（核心渲染逻辑原样保留）
html = html.replace('<link rel="stylesheet" href="../css/mengban.css"  type="text/css" />', '<style>\n' + mengban_css + '\n</style>')
html = html.replace('<link rel="stylesheet" href="index.css"  type="text/css" />', '<style>\n' + index_css + '\n</style>')

# 本地单文件版不需要的“部署/统计/授权”脚本：它们会 fetch 远端、读写 localStorage、
# 在 file:// 下直接抛错并拖累页面。这里直接移除（与本地隐藏文字功能无关）。
NEUTRALIZE = {'../module/root.js', '../module/ziyuanBianhao.js', '../module/tianjiaDandu.js',
              '../js/yingyongMengban.js', '../js/tongji.js'}
scripts = [('../js/head.js', head_js), ('../module/jieLiu.js', jieLiu_js), ('../module/root.js', root_js),
           ('../module/ziyuanBianhao.js', zb_js), ('../module/openUrl.js', openurl_js), ('../module/tianjiaDandu.js', td_js),
           ('index.js', index_js), ('../js/yingyongMengban.js', ym_js), ('../js/tongji.js', tongji_js), ('../js/stop.js', stop_js)]
for tag, code in scripts:
    if tag in NEUTRALIZE:
        code = '/* 本地单文件版已移除：原部署/统计脚本（fetch/授权/统计），与本地隐藏文字功能无关 */'
    html = html.replace('<script src="%s"></script>' % tag, '<script>\n' + code + '\n</script>')

# 4. 新增功能脚本 —— 只替换【最后一个】</body>（文档真实结尾，避免命中 openUrl 模板内的 </body>）
feature_script = r'''
<script>
(function(){
  function q(s){return document.querySelector(s);}
  var wzEl=q('.wenzi');
  var rotDeg=0;
  var stripeScale=1;

  // 1) 文字框实时同步到 .wenzi：以输入框排版为准（单行=一行；回车或“|”=换行）
  //    文字与图片共存：输入文字不再清除图片
  function linesHtml(v){
    return v.replace(/\r?\n/g,'\n').replace(/\|/g,'\n').split('\n').map(function(l){ return '<div>'+l+'</div>'; }).join('');
  }
  var wi=q('#wenziInput');
  if(wi) wi.addEventListener('input', function(){
    if(wzEl) wzEl.innerHTML = linesHtml(wi.value);
  });
  // 输入框高度自适应内容：默认紧贴文字高度（不预留多余空白），输入多少行就长多高
  function fitTA(){
    if(!wi) return;
    var saved=wi.style.height;
    wi.style.height='auto';
    var h=wi.scrollHeight;
    wi.style.height=saved;
    if(h>0) wi.style.height=(h+2)+'px';
  }
  if(wi){
    wi.addEventListener('input',fitTA);
    window.addEventListener('resize',fitTA);
    setTimeout(fitTA,60);
  }

  // 2) 通用拖动：文字层 / 图片层各自独立拖动（条纹固定在屏幕上不动）
  //    - Pointer Events 优先；老内核无 PointerEvent 时回退 touch 事件
  //    - 图片禁用原生 HTML5 拖拽（否则 pointer 事件被打断，拖不动）
  //    - 传 opts.onGesture 时支持双指手势：捏合缩放 + 旋转（f=距离倍数, da=角度增量deg）
  function draggable(el, off, apply, opts){
    if(!el) return;
    el.setAttribute('draggable','false');
    el.addEventListener('dragstart',function(e){ try{e.preventDefault();}catch(_){} });
    var pts={}, lastDist=0, lastAng=0;
    function two(){
      var k=Object.keys(pts); if(k.length<2) return null;
      var a=pts[k[0]],c=pts[k[1]];
      return { d:Math.hypot(a.x-c.x,a.y-c.y), ang:Math.atan2(c.y-a.y,c.x-a.x) };
    }
    function start(id,x,y){ pts[id]={x:x,y:y}; }
    function movePt(id,x,y){
      var prev=pts[id]; if(!prev) return;
      if(Object.keys(pts).length>=2&&opts&&opts.onGesture){
        pts[id]={x:x,y:y};
        var t2=two();
        if(lastDist>0&&t2&&t2.d>0){
          var da=t2.ang-lastAng;
          while(da>Math.PI) da-=2*Math.PI;
          while(da<-Math.PI) da+=2*Math.PI;
          opts.onGesture(t2.d/lastDist, da*180/Math.PI);
        }
        if(t2){ lastDist=t2.d; lastAng=t2.ang; }
        return;
      }
      off.x+=x-prev.x; off.y+=y-prev.y; pts[id]={x:x,y:y}; apply();
    }
    function end(id){ delete pts[id]; lastDist=0; lastAng=0; }
    if(window.PointerEvent){
      el.addEventListener('pointerdown',function(e){
        if(e.pointerType==='mouse'&&e.button!==0) return;
        start(e.pointerId,e.clientX,e.clientY);
        try{e.preventDefault();}catch(_){}
        try{el.setPointerCapture(e.pointerId);}catch(_){}
      });
      el.addEventListener('pointermove',function(e){ movePt(e.pointerId,e.clientX,e.clientY); });
      ['pointerup','pointercancel'].forEach(function(t){ el.addEventListener(t,function(e){ end(e.pointerId); }); });
    } else {
      function syncTouches(e){
        var seen={};
        for(var i=0;i<e.touches.length;i++){
          var t=e.touches[i]; seen[t.identifier]=1;
          if(t.identifier in pts) movePt(t.identifier,t.clientX,t.clientY); else start(t.identifier,t.clientX,t.clientY);
        }
        Object.keys(pts).forEach(function(k){ if(!(k in seen)) end(k); });
      }
      el.addEventListener('touchstart',function(e){ syncTouches(e); try{e.preventDefault();}catch(_){} },{passive:false});
      el.addEventListener('touchmove',function(e){ syncTouches(e); try{e.preventDefault();}catch(_){} },{passive:false});
      ['touchend','touchcancel'].forEach(function(t){ el.addEventListener(t,function(e){
        for(var i=0;i<e.changedTouches.length;i++) end(e.changedTouches[i].identifier);
      }); });
    }
    if(opts&&opts.onGesture&&opts.wheel){
      el.addEventListener('wheel',function(e){ e.preventDefault(); opts.onGesture(e.deltaY<0?1.1:0.9, 0); },{passive:false});
    }
  }
  // 文字层：拖动 + 双指捏合缩放 + 双指旋转（手机端手势；电脑端滚轮缩放）
  var textOff={x:0,y:0}, textScale=1, textRot=0;
  function applyWz(){ if(wzEl) wzEl.style.transform='translate('+textOff.x+'px,'+textOff.y+'px) rotate('+textRot+'deg) scale('+textScale+')'; }
  draggable(wzEl, textOff, applyWz, {
    onGesture:function(f2,da){ textScale=Math.max(0.1,Math.min(10,textScale*f2)); textRot+=da; applyWz(); },
    wheel:true
  });

  // 3) 导入图片（与文字共存）：图片为独立图层，可拖动 + 双指捏合缩放/旋转 + 滚轮缩放；删除图片只删图、不清文字
  var userImg=null, imgOff={x:0,y:0}, imgScale=1, imgRot=0, fileInput=document.createElement('input');
  function applyImg(){ if(userImg) userImg.style.transform='translate(-50%,-50%) translate('+imgOff.x+'px,'+imgOff.y+'px) rotate('+imgRot+'deg) scale('+imgScale+')'; }
  fileInput.type='file'; fileInput.accept='image/*'; fileInput.style.display='none'; document.body.appendChild(fileInput);
  var btnImg=q('#btnImg');
  if(btnImg) btnImg.addEventListener('click',function(){ fileInput.click(); });
  fileInput.addEventListener('change',function(){
    var f=fileInput.files&&fileInput.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(){
      var img=new Image();
      img.onload=function(){
        if(userImg&&userImg.parentNode) userImg.parentNode.removeChild(userImg);
        imgOff={x:0,y:0}; imgScale=1; imgRot=0;
        userImg=img; userImg.id='userImg'; applyImg();
        document.body.appendChild(userImg);
        draggable(userImg, imgOff, applyImg, {
          onGesture:function(f2,da){ imgScale=Math.max(0.1,Math.min(10,imgScale*f2)); imgRot+=da; applyImg(); },
          wheel:true
        });
      };
      img.src=rd.result;
    };
    rd.readAsDataURL(f);
  });
  var btnDel=q('#btnDel');
  if(btnDel) btnDel.addEventListener('click',function(){
    if(userImg&&userImg.parentNode) userImg.parentNode.removeChild(userImg);
    userImg=null;
  });

  // 4) 导出 PNG / JPG：白底 → 文字(含拖动偏移) + 图片(含拖动偏移) → 旋转后的人字纹覆盖
  function getText(){
    if(!wzEl) return '';
    var h=wzEl.innerHTML.replace(/<img[^>]*>/gi,'');
    h=h.replace(/<\/div>/gi,'\n').replace(/<br\s*\/?>/gi,'\n').replace(/<[^>]+>/g,'').replace(/\|/g,'\n');
    return h.replace(/\n+/g,'\n').trim();
  }
  // 人字纹/点阵/直线：与 DOM 平铺同相位，覆盖 S×S；调用方先把画布平移到中心并旋转
  // sc=条纹缩放倍数（与 DOM 的 newSvg 缩放一致：瓷砖/线宽同乘，间隙 g 保持 2px）
  function drawPattern(ctx,S,tileW,tileH,sc){
    var b=10*sc, g=2;
    var g=2, step=2*b;
    // 细线模式（宽/高归1）：按屏幕生成时的等比参数在画布上精确复现
    var fg=window.__fineGeo;
    if(fg){
      var b2=fg.b, g2=fg.g, period=2*b2, Wf=tileW, Hf=tileH;
      var blk=[[0,0],[b2,0],[Wf-b2+g2,Hf/2],[b2,Hf],[0,Hf],[Wf-2*b2+g2,Hf/2]];
      var wht=[[b2+g2,0],[2*b2-g2,0],[Wf,Hf/2],[2*b2-g2,Hf],[b2+g2,Hf],[Wf-b2+g2,Hf/2]];
      var colsF=Math.ceil(S/period)+2, rowsF=Math.ceil(S/Hf)+2;
      for(var r3=0;r3<rowsF;r3++)for(var c3=0;c3<colsF;c3++){
        var x3=c3*period-S/2, y3=r3*Hf-S/2;
        ctx.fillStyle='#000'; ctx.beginPath();
        blk.forEach(function(p,i){var X=x3+p[0],Y=y3+p[1]; i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}); ctx.closePath(); ctx.fill();
        ctx.fillStyle='#fff'; ctx.beginPath();
        wht.forEach(function(p,i){var X=x3+p[0],Y=y3+p[1]; i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}); ctx.closePath(); ctx.fill();
      }
      return;
    }
    var offX=S/2, offY=S/2;
    var black=[[0,0],[b,0],[tileW-b+g,tileH/2],[b,tileH],[0,tileH],[tileW-2*b+g,tileH/2]];
    var white=[[b+g,0],[2*b-g,0],[tileW,tileH/2],[2*b-g,tileH],[b+g,tileH],[tileW-b+g,tileH/2]];
    for(var row=0; row*tileH-offY < S/2; row++){
      for(var col=0; col*step - tileW + 2*b - offX < S/2; col++){
        var x0=col*step - tileW + 2*b - offX, y0=row*tileH - offY;
        ctx.fillStyle='#000'; ctx.beginPath();
        black.forEach(function(p,i){ var X=x0+p[0],Y=y0+p[1]; i?ctx.lineTo(X,Y):ctx.moveTo(X,Y); }); ctx.closePath(); ctx.fill();
        ctx.fillStyle='#fff'; ctx.beginPath();
        white.forEach(function(p,i){ var X=x0+p[0],Y=y0+p[1]; i?ctx.lineTo(X,Y):ctx.moveTo(X,Y); }); ctx.closePath(); ctx.fill();
      }
    }
  }
  function exportImage(type){
    try{
      var W=window.innerWidth, H=window.innerHeight;
      var S=window.__stripeW||Math.ceil(Math.sqrt(W*W+H*H)*1.02)+40;
      var tileSvg=q('.zhexian svg');
      var tileW=tileSvg?parseFloat(tileSvg.getAttribute('width')):36;
      var tileH=tileSvg?parseFloat(tileSvg.getAttribute('height')):28;
      function draw(){
        var canvas=document.createElement('canvas'); canvas.width=W; canvas.height=H;
        var ctx=canvas.getContext('2d');
        ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
        // 文字（始终居中 + 拖动偏移 + 双指缩放/旋转；与图片共存时也照常绘制）
        var lines=getText()?getText().split('\n'):[];
        if(lines.length){
          var cs=getComputedStyle(wzEl);
          var fontFamily=cs.fontFamily, fontSize=parseFloat(cs.fontSize)||240, fontWeight=cs.fontWeight,
              lineHeight=parseFloat(cs.lineHeight)||fontSize,
              letterSpacing=parseFloat(cs.letterSpacing)||0, opacity=parseFloat(cs.opacity)||1;
          ctx.save(); ctx.globalAlpha=opacity; ctx.fillStyle='#000'; ctx.textBaseline='middle';
          ctx.textAlign='center';
          // 以"工作区中心"为原点（与屏幕上 .wenzi 的 transform 基准一致）：
          // 平移(拖动偏移) → 旋转(双指) → 缩放(捏合)，行从中心向上下展开
          var panelH=parseFloat((document.documentElement.style.getPropertyValue('--panel-h')||'').replace('px',''))||0;
          var cy=(H-panelH)/2;
          ctx.translate(W/2+textOff.x, cy+textOff.y);
          ctx.rotate((textRot||0)*Math.PI/180);
          ctx.scale(textScale||1, textScale||1);
          if('letterSpacing' in ctx){ try{ ctx.letterSpacing=letterSpacing+'px'; }catch(e){} }
          var lh=lineHeight;
          lines.forEach(function(line,idx){
            var y=(idx-(lines.length-1)/2)*lh;
            ctx.font=fontWeight+' '+fontSize+'px '+fontFamily;
            ctx.fillText(line, 0, y);
          });
          ctx.restore();
        }
        // 图片（居中 + 拖动偏移 + 缩放 + 双指旋转）
        if(userImg){
          var bw=W*0.8, bh=H;
          var ir=Math.min(bw/userImg.width, bh/userImg.height);
          var dw=userImg.width*ir*imgScale, dh=userImg.height*ir*imgScale;
          ctx.save();
          ctx.translate(W/2+imgOff.x, H/2+imgOff.y);
          ctx.rotate((imgRot||0)*Math.PI/180);
          ctx.drawImage(userImg, -dw/2, -dh/2, dw, dh);
          ctx.restore();
        }
        // 条纹：按当前角度、模式与缩放覆盖（与屏幕视觉一致）
        ctx.save(); ctx.translate(W/2,H/2); ctx.rotate(rotDeg*Math.PI/180);
        drawPattern(ctx,S,tileW,tileH,stripeScale);
        ctx.restore();
        var mime=type==='jpg'?'image/jpeg':'image/png';
        var a=document.createElement('a');
        a.href=canvas.toDataURL(mime, type==='jpg'?0.95:undefined);
        a.download=('hidden_'+(userImg?'img':'text')).slice(0,20)+'.'+(type==='jpg'?'jpg':'png'); a.click();
      }
      if(document.fonts && document.fonts.ready) document.fonts.ready.then(draw); else draw();
    }catch(e){ alert('导出失败：'+e.message); }
  }
  if(q('#btnPng')) q('#btnPng').addEventListener('click',function(){ exportImage('png'); });
  if(q('#btnJpg')) q('#btnJpg').addEventListener('click',function(){ exportImage('jpg'); });

  // 5) 单一主滑块驱动多个属性（文字大小/粗细/行距/间距/透明/宽/高/条纹旋转），标签切换
  (function(){
    var master=q('#masterSlider'), labels=document.querySelectorAll('#propLabels .plabel');
    function orig(name){ return document.querySelector('#hiddenOriginals [name="'+name+'"]'); }
    var active='fontSize';
    function setActive(name){ labels.forEach(function(l){ l.classList.toggle('active', l.getAttribute('data-name')===name); }); syncNum(); }
    function activate(name){
      if(name==='ziti'){ var z=document.getElementById('ziti'); if(z) z.click(); return; }
      if(name==='stripeRot'){
        active=name;
        master.min='0'; master.max='360'; master.step='1'; master.value=String(Math.round(rotDeg));
        setActive(name); return;
      }
      if(name==='stripeScale'){
        active=name;
        master.min='0.3'; master.max='5'; master.step='0.05'; master.value=String(stripeScale);
        setActive(name); return;
      }
      if(name==='imgScale'){
        active=name;
        master.min='0.1'; master.max='5'; master.step='0.05'; master.value=String(imgScale);
        setActive(name); return;
      }
      active=name; var inp=orig(name); if(!inp||!master) return;
      master.min=inp.min; master.max=inp.max; master.step=inp.step; master.value=inp.value;
      setActive(name);
    }
    labels.forEach(function(l){ l.addEventListener('click',function(){ activate(l.getAttribute('data-name')); }); });
    // 拉杆左侧数值框：与拉杆双向同步（拖拉杆→数值跟着变；输入数值→立即生效）
    var num=q('#masterNum');
    function syncNum(){ if(num&&master&&num.value!==master.value) num.value=master.value; }
    if(num){
      num.addEventListener('input',function(e){
        e.stopPropagation();  // 防止冒泡到 .caozuo 的委托处理器（数值框无 name → 会抛错）
        if(!master) return;
        var v=parseFloat(num.value); if(isNaN(v)) return;
        var mn=parseFloat(master.min), mx=parseFloat(master.max);
        // 输入过程中的中间值（如刚打个"3"、还没打完"320"）不生效、不回写，避免打字被打断
        if(v<mn||v>mx) return;
        master.value=v;
        master.dispatchEvent(new Event('input'));  // 走主拉杆同一条路由
      });
      num.addEventListener('change',function(){
        // 失焦/回车时收尾：越界钳制到范围，空值恢复当前值
        if(!master) return;
        var v=parseFloat(num.value);
        var mn=parseFloat(master.min), mx=parseFloat(master.max);
        if(isNaN(v)) v=parseFloat(master.value);
        v=Math.max(mn,Math.min(mx,v));
        master.value=v;
        num.value=v;
        master.dispatchEvent(new Event('input'));
      });
      master.addEventListener('input',syncNum);
    }
    if(master) master.addEventListener('input',function(e){
      // 关键：阻止主拉杆自身的 input 冒泡到 .caozuo —— 否则 index.js 的委托处理器会读到
      // zhiXing[master.name]（master 没有 name 属性 → 抛错且节流吞掉渲染事件）。
      e.stopPropagation();
      if(active==='stripeRot'){
        rotDeg=parseFloat(master.value)||0;
        document.documentElement.style.setProperty('--stripe-rot', rotDeg+'deg');
        return;
      }
      if(active==='stripeScale'){
        stripeScale=Math.max(0.3,Math.min(5,parseFloat(master.value)||1));
        window.__ss=stripeScale;
        // 触发 kuan 重新生成条纹（newSvg 会按 __ss 缩放瓷砖），缩放后依然铺满全屏
        var kk=orig('kuan'); if(kk) kk.dispatchEvent(new Event('input',{bubbles:true}));
        return;
      }
      if(active==='imgScale'){
        imgScale=Math.max(0.1,Math.min(5,parseFloat(master.value)||1));
        applyImg();
        return;
      }
      if(active==='ziti') return;
      var inp=orig(active); if(!inp) return;
      inp.value=master.value;
      inp.dispatchEvent(new Event('input',{bubbles:true}));
    });
    activate('fontSize');
    // 手机端默认数值：宽80 高60 文字大小100（其余与默认一致，显式设置保证一致）
    // 注意：必须等 index.js 完全初始化后再派发（载入瞬间同步派发会被内部未就绪状态吞掉）
    try{
      if(window.matchMedia && window.matchMedia('(max-width:1019px)').matches){
        setTimeout(function(){
          var defs={fontSize:'100',fontWeight:'700',lineHeight:'1',letterSpacing:'0',opacity:'1',kuan:'80',gao:'60'};
          Object.keys(defs).forEach(function(n){
            var el=orig(n); if(!el) return;
            el.value=defs[n];
            el.dispatchEvent(new Event('input',{bubbles:true}));
          });
          // 节流器(dingShiQi)会合并16ms内的连续事件只执行最后一个——上批的 fontSize 被吞掉，需延迟重派
          setTimeout(function(){
            var f=orig('fontSize'); if(f) f.dispatchEvent(new Event('input',{bubbles:true}));
            activate('fontSize');  // 刷新主拉杆与数值框显示
          },40);
        },60);
      }
    }catch(_e){}

    // ===== 数值方案（保存/选择/删除）：把当前各属性数值存为一组，随时切换 =====
    var LS_KEY='yz_presets_v1', memStore=null, defaultPreset=null;
    function loadStore(){ try{ var s=localStorage.getItem(LS_KEY); return s?JSON.parse(s):{}; }catch(_e2){ return memStore||{}; } }
    function saveStore(o){ memStore=o; try{ localStorage.setItem(LS_KEY,JSON.stringify(o)); }catch(_e3){} }
    function snapshot(){
      var o={};
      ['fontSize','fontWeight','lineHeight','letterSpacing','opacity','kuan','gao'].forEach(function(n){ var el=orig(n); if(el) o[n]=el.value; });
      o.stripeRot=String(Math.round(rotDeg)); o.stripeScale=String(stripeScale); o.imgScale=String(imgScale);
      return o;
    }
    function applyValues(vals){
      if(!vals) return;
      var seq=[];
      // 条纹缩放先行（条纹缩放决定 __ss，随后 kuan 派发会用新缩放重新生成条纹）
      seq.push(function(){ if('stripeScale' in vals){ stripeScale=Math.max(0.3,Math.min(5,parseFloat(vals.stripeScale)||1)); window.__ss=stripeScale; } });
      ['fontSize','fontWeight','lineHeight','letterSpacing','opacity','kuan','gao'].forEach(function(n){
        if(!(n in vals)) return;
        var el=orig(n); if(!el) return;
        seq.push(function(){ el.value=vals[n]; el.dispatchEvent(new Event('input',{bubbles:true})); });
      });
      if('stripeRot' in vals) seq.push(function(){ rotDeg=parseFloat(vals.stripeRot)||0; document.documentElement.style.setProperty('--stripe-rot', rotDeg+'deg'); });
      if('imgScale' in vals) seq.push(function(){ imgScale=Math.max(0.1,Math.min(5,parseFloat(vals.imgScale)||1)); applyImg(); });
      // 节流器(dingShiQi)会合并16ms内的连续事件 → 逐个错开派发，保证每个都真正渲染
      seq.forEach(function(fn,i){ setTimeout(fn, i*45); });
      setTimeout(function(){ activate('fontSize'); }, seq.length*45+60);
    }
    var sel=q('#presetSel');
    function refreshSel(){
      if(!sel) return;
      var cur=sel.value;
      var store=loadStore();
      sel.innerHTML='<option value="__default">默认</option>';
      Object.keys(store).forEach(function(n){ var op=document.createElement('option'); op.value=n; op.textContent=n; sel.appendChild(op); });
      if(cur && cur!=='__default' && store[cur]) sel.value=cur; else sel.value='__default';
    }
    if(sel){
      // "默认"方案 = 页面初始数值（手机端等 80/60/100 应用完成后再快照；桌面端即 240/100/100）
      setTimeout(function(){ defaultPreset=snapshot(); refreshSel(); },450);
      sel.addEventListener('change',function(){
        if(sel.value==='__default'){ applyValues(defaultPreset); return; }
        applyValues(loadStore()[sel.value]);
      });
      var bs=q('#presetSave');
      if(bs) bs.addEventListener('click',function(e){
        try{e.stopPropagation();}catch(_){}
        var name=prompt('给这组数值起个名字：');
        if(!name) return;
        var store=loadStore(); store[name]=snapshot(); saveStore(store);
        refreshSel(); sel.value=name;
      });
      var bd=q('#presetDel');
      if(bd) bd.addEventListener('click',function(e){
        try{e.stopPropagation();}catch(_){}
        var v=sel.value;
        if(v==='__default'){ alert('默认方案不可删除'); return; }
        var store=loadStore(); delete store[v]; saveStore(store); refreshSel();
      });
      refreshSel();
    }
  })();

  // 7) 图案模式切换已删除（点阵版/直线版下线）

  // 8) 工作区自愈（APK WebView 关键修复）：
  //    __stripeW 在 <head> 解析阶段按 innerWidth/innerHeight 一次性计算。手机浏览器此时
  //    布局已就绪；但 WebView 在 head 脚本执行时视口尚未完成布局，读到 ≈0 →
  //    S=sqrt(0)+40≈40px，条纹只生成屏幕中央一小块。这里在布局就绪后与窗口尺寸
  //    变化时重算 __stripeW，并触发 kuan 重新生成条纹（newSvg 按 __stripeW 平铺）。
  (function(){
    var lastS=-1;
    function refresh(){
      var w=window.innerWidth, h=window.innerHeight;
      if(!w || !h || w<100 || h<100) return;   // 布局未就绪，等下一次时机
      var S=Math.ceil(Math.sqrt(w*w+h*h)*1.02)+40;
      if(lastS>=0 && Math.abs(S-lastS)<10) return;  // 尺寸没变，不重复生成
      lastS=S;
      window.__stripeW=S;
      document.documentElement.style.setProperty('--stripe-size',S+'px');
      var kk=document.querySelector('#hiddenOriginals [name="kuan"]');
      if(kk) kk.dispatchEvent(new Event('input',{bubbles:true}));
    }
    try{ refresh(); }catch(_e0){}
    window.addEventListener('load',refresh);
    document.addEventListener('DOMContentLoaded',refresh);
    window.addEventListener('resize',refresh);
    window.addEventListener('orientationchange',function(){ setTimeout(refresh,200); });
    setTimeout(refresh,150); setTimeout(refresh,400); setTimeout(refresh,900);
  })();

  // 6) 面板收起 / 拖动展开（底部抽屉）：点击把手=收起/展开；在把手上拖动=直接控制高度
  (function(){
    var panel=q('.caozuo'); if(!panel) return;
    // 底衬：面板两侧区域用面板同色填充（高度由 --panel-h 驱动，收起/拖动实时跟随）
    var backdrop=document.createElement('div');
    backdrop.id='panelBackdrop';
    document.body.appendChild(backdrop);
    var handle=document.createElement('div');
    handle.id='panelHandle';
    handle.innerHTML='<span class="grip"></span>';
    panel.insertBefore(handle, panel.firstChild);
    var collapsed=false, dragging=false, startY=0, startH=0, moved=false;
    // 工作区高度变量：条纹与文字只覆盖面板以上区域（面板变高变矮实时跟随）
    function setPanelVar(){ var ph=Math.round(panel.getBoundingClientRect().height); document.documentElement.style.setProperty('--panel-h', ph+'px'); }
    if(window.ResizeObserver){ try{ new ResizeObserver(setPanelVar).observe(panel); }catch(_){ window.addEventListener('resize',setPanelVar); } }
    else { window.addEventListener('resize',setPanelVar); }
    setPanelVar(); setTimeout(setPanelVar,150);
    function setCollapsed(c){ collapsed=c; panel.classList.toggle('collapsed', c); panel.style.maxHeight=''; setPanelVar(); }
    handle.addEventListener('pointerdown',function(e){ try{e.preventDefault();}catch(_){} dragging=true; moved=false; startY=e.clientY; startH=panel.getBoundingClientRect().height; try{handle.setPointerCapture(e.pointerId);}catch(_){} });
    handle.addEventListener('pointermove',function(e){
      if(!dragging) return;
      var dy=startY-e.clientY;            // 向上拖动为正
      if(Math.abs(dy)>4) moved=true;
      if(collapsed && dy>4){ panel.classList.remove('collapsed'); collapsed=false; }
      var nh=Math.max(38, Math.min(window.innerHeight*0.92, startH+dy));
      panel.style.maxHeight=nh+'px';
      setPanelVar();
    });
    function endDrag(){
      if(!dragging) return; dragging=false;
      if(!moved){ setCollapsed(!collapsed); }       // 视为点击：切换收起
      else { var hh=panel.getBoundingClientRect().height; if(hh<=70) setCollapsed(true); else { collapsed=false; panel.classList.remove('collapsed'); } }
    }
    handle.addEventListener('pointerup',endDrag); handle.addEventListener('pointercancel',endDrag);
  })();
})();
</script>
'''

before, _, after = html.rpartition('</body>')
html = before + feature_script + '</body>' + after

with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print("写入完成 字节:", len(html.encode('utf-8')))
print("残留 <script src>:", html.count('<script src'))
print("openUrl 内未转义 </script> 数(应为0):", html.count('</script>') - html.count('<\\/script>'))
print("feature 脚本位置(应在末尾):", html.rfind('exportImage'))
