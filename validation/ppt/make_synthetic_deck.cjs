// Synthetic evidence only. npm install pptxgenjs@4.0.1, then run with an output path.
const pptxgen = require('pptxgenjs');
const fs = require('node:fs');
const path = require('node:path');
const target = process.argv[2];
if (!target) throw new Error('Usage: node make_synthetic_deck.cjs OUTPUT.pptx');
if (fs.existsSync(target)) throw new Error('Refusing to replace an existing output');
fs.mkdirSync(path.dirname(path.resolve(target)), {recursive: true});
const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.author = 'skill-library validation';
p.subject = 'Synthetic Chinese scientific presentation';
p.title = '合成研究汇报';
p.company = '';
p.lang = 'zh-CN';
p.theme = {headFontFace:'Microsoft YaHei', bodyFontFace:'Microsoft YaHei', lang:'zh-CN'};
const c = {navy:'19344D', teal:'007C83', grey:'586773'};
function text(s, t, x, y, w, h, size=26, color=c.navy, bold=false) {
  s.addText(t,{x,y,w,h,fontSize:size,color,bold,fontFace:'Microsoft YaHei',breakLine:false,margin:0,paraSpaceAfterPt:12,valign:'top'});
}
function footer(s, n) { text(s, `合成数据演示，非真实研究结果  ·  ${n}/3`,.65,6.94,11.9,.26,12,c.grey); }
let s=p.addSlide();
s.background={color:'FFFFFF'};
text(s,'训练过程中的任务完成量',.72,1.42,11.8,.8,42,c.navy,true);
text(s,'三周观察的合成研究汇报',.76,2.48,10.8,.6,28,c.teal);
text(s,'研究问题\n两组任务完成量随训练周次如何变化？',.76,3.55,11.5,1.2,26);
s.addNotes('45秒。介绍研究问题与两个演示组。数据完全合成，不能外推为真实干预效果。没有虚构作者、机构或引文。');
footer(s,1);

s=p.addSlide();
text(s,'第三周两组每分钟完成量相差 9 项',.65,.48,12.05,.7,32,c.navy,true);
text(s,'任务完成量，项/分钟',.82,1.38,7,.4,20,c.grey);
s.addChart(p.ChartType.line,[
  {name:'对照组',labels:['第1周','第2周','第3周'],values:[20,24,30]},
  {name:'训练组',labels:['第1周','第2周','第3周'],values:[22,30,39]}
],{x:.65,y:1.95,w:8.25,h:4.35,showTitle:false,showLegend:true,legendPos:'b',legendFontFace:'Microsoft YaHei',legendFontSize:16,catAxisLabelFontFace:'Microsoft YaHei',catAxisLabelFontSize:18,valAxisLabelFontSize:16,valAxisMinVal:0,valAxisMaxVal:40,valAxisMajorUnit:10,chartColors:[c.navy,c.teal],lineSize:3,showValue:false,showMarker:true,markerSize:6,showCatName:false,showSerName:false,showBorder:false,altText:'合成数据。第1至3周，对照组为20、24、30项/分钟，训练组为22、30、39项/分钟。'});
text(s,'39 − 30 = 9',9.26,2.46,3.25,.64,30,c.teal,true);
text(s,'仅为组间描述性差异\n未提供样本量和变异度\n不能据此判断显著性',9.26,3.42,3.2,2.1,22);
s.addNotes('90秒。先读单位，再描述两组时间走势，最后说明第三周9项的差值。缺少样本量和个体数据，不计算置信区间、p值或因果效应。');
footer(s,2);

s=p.addSlide();
text(s,'观察到差距扩大，仍需验证训练效果',.65,.65,12.05,.9,32,c.navy,true);
text(s,'现有证据',.78,2.03,3.15,.5,27,c.teal,true);
text(s,'两组完成量均随周次增加\n组间差值由 2 项增至 9 项',4.03,2.03,8.25,1.18,26);
text(s,'下一步',.78,3.8,3.15,.5,27,c.teal,true);
text(s,'采集样本量、个体变化与不确定性\n控制基线差异后，再检验研究假设',4.03,3.8,8.25,1.25,26);
s.addNotes('45秒。总结描述结果与证据边界。30秒预留问答，总时长3分30秒。正式研究应补充设计、样本量、误差范围和可追溯数据。');
footer(s,3);
p.writeFile({fileName:target});
