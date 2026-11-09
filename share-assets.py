"""Render the share card from NPCI CSVs and the page's Fraunces/Inter fonts."""
import base64,csv,json,os,pathlib,subprocess,urllib.request
ROOT=pathlib.Path(__file__).parent

def font(url):
 return 'data:font/ttf;base64,'+base64.b64encode(urllib.request.urlopen(url,timeout=30).read()).decode()

def rows(file):
 with (ROOT/'data'/file).open() as f:return list(csv.DictReader(f))

def main():
 district=next(r for r in rows('upi_top_districts_sep2026.csv') if r['district']=='BENGALURU (URBAN)')
 count=float(district['volume_mn'])
 states=rows('upi_states_sep2026.csv')
 fewer=sum(float(r['volume_mn'])<count for r in states if r['state']!='Unclassified')
 selected=[('Bengaluru Urban',count,True)]+[(name.title(),float(next(r for r in states if r['state']==name)['volume_mn']),False) for name in ['ANDHRA PRADESH','GUJARAT','KERALA','BIHAR']]
 bars=''.join(f'<div class="row"><span>{name}</span><div class="track"><i style="width:{value/count*100:.4f}%;background:{"#d2501c" if district else "#c4bcab"}"></i></div><b>{value:.0f}</b></div>' for name,value,district in selected)
 fraunces=font('https://fonts.gstatic.com/s/fraunces/v38/6NUh8FyLNQOQZAnv9bYEvDiIdE9Ea92uemAk_WBq8U_9v0c2Wa0K7iN7hzFUPJH58njr1a03gg7S2nfgRYIcaRyjDg.ttf')
 inter=font('https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf')
 html=f'''<style>@font-face{{font-family:Fraunces;src:url('{fraunces}');font-weight:600}}@font-face{{font-family:Inter;src:url('{inter}')}}
 *{{box-sizing:border-box}}body{{margin:0;width:1200px;height:630px;background:#f3eee4;color:#15120e;padding:42px 52px;font-family:Inter}}.top{{display:flex;justify-content:space-between;font-size:18px;border-bottom:1px solid #d9d2c3;padding-bottom:19px}}.top b{{font:600 24px Fraunces}}.main{{display:grid;grid-template-columns:575px 1fr;gap:44px;margin-top:33px}}h1{{font:600 63px/1.02 Fraunces;letter-spacing:-1.9px;margin:0}}h1 em{{font-style:normal;color:#d2501c}}.number{{font:600 95px/1 Fraunces;margin-top:27px;letter-spacing:-3px}}.number small{{font:20px Inter;letter-spacing:0;margin-left:8px}}.label{{margin:8px 0 0;font:20px/1.35 Inter;max-width:475px;color:#4a443b}}.chart{{padding-top:8px}}.chart-head{{font-size:16px;line-height:1.5;border-bottom:1px solid #d9d2c3;padding-bottom:15px;margin-bottom:20px}}.row{{display:grid;grid-template-columns:144px 1fr 42px;align-items:center;gap:12px;margin:23px 0;font-size:18px}}.row span{{font-size:17px}}.row b{{font-weight:400;text-align:right;font-variant-numeric:tabular-nums}}.track{{height:24px}}.track i{{display:block;height:100%}}.foot{{position:absolute;left:52px;right:52px;bottom:30px;border-top:1px solid #d9d2c3;padding-top:17px;display:flex;justify-content:space-between;font-size:15px;color:#6b6357}}</style>
 <div class="top"><b>UPI study</b><span>Ten years of NPCI's public numbers</span></div><div class="main"><div><h1>Bengaluru does<br>more UPI than<br><em>{fewer} states.</em></h1><div class="number">{count:.0f}<small>million payments</small></div><p class="label">One district. One month.<br>More than 31 states and union territories.</p></div><div class="chart"><div class="chart-head">UPI payments · September 2026<br>Millions · Bengaluru Urban vs. selected states</div>{bars}</div></div><div class="foot"><span>Source: NPCI · state and district data, Sep 2026</span><span>A study by Harssha Vardan</span></div>'''
 # The orange and green arrow shapes from assets/upi.svg, cropped to the mark.
 svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#f3eee4"/><g transform="translate(12 4) scale(.24 .24)"><path d="m 0,0 24.414,48.553 -51.322,48.54 z" transform="translate(35 0)" fill="#27803b"/><path d="m 0,0 24.396,48.553 -51.343,48.54 z" transform="translate(18 0)" fill="#e9661c"/></g></svg>'''
 (ROOT/'assets/favicon.svg').write_text(svg)
 code = r"""
const fs=require('node:fs'),path=require('node:path');
const puppeteer=require(process.env.PUPPETEER_MODULE || 'puppeteer-core');
let input='';process.stdin.on('data',s=>input+=s);process.stdin.on('end',async()=>{
 const {html,svg,root}=JSON.parse(input);const browser=await puppeteer.launch({executablePath:process.env.CHROMIUM_PATH || '/snap/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{const page=await browser.newPage();await page.setViewport({width:1200,height:630,deviceScaleFactor:1});await page.setContent(html);await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:path.join(root,'assets/og.png')});for(const [size,file] of [[180,'apple-touch-icon.png'],[32,'favicon-32.png']]){await page.setViewport({width:size,height:size,deviceScaleFactor:1});await page.setContent(`<style>body{margin:0}svg{width:${size}px;height:${size}px}</style>${svg}`);await page.screenshot({path:path.join(root,'assets',file)});}}finally{await browser.close();}
});
"""
 subprocess.run(['node','-e',code],input=json.dumps({'html':html,'svg':svg,'root':str(ROOT)}),text=True,check=True)
 from PIL import Image
 Image.open(ROOT/'assets/favicon-32.png').save(ROOT/'assets/favicon.ico',sizes=[(32,32)])
 print('Card generated from NPCI CSVs:',count,'million; larger than',fewer,'states/UTs')
main()
