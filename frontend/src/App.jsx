import React, {useEffect, useState} from 'react'
import {FileText, UploadCloud, ShieldCheck, ChartColumn, Info, CheckCircle2, AlertCircle, ArrowRight, Database, ScanText, Download, Github, Layers} from 'lucide-react'

const SAMPLE = 'Quarterly Operations Report\n\nThis quarterly business report summarizes service delivery performance and operational risk. The operations team completed scheduled tasks and documented delays during the reporting period. Management reviewed project milestones, customer feedback and departmental performance.\n\nThe report recommends a weekly risk review and stronger ownership of blocked tasks. The next reporting period will focus on service quality, task completion trends and reducing recurring operational constraints. This demonstration uses fabricated narrative and does not represent a real company.'
const API = import.meta.env.VITE_API_URL || ''
const fmt = (v) => Number(v || 0).toLocaleString('en-US')
function Metric({icon:Icon, label,value,detail}){return <div className="metric"><div className="metric-label"><Icon size={15}/>{label}</div><strong>{value}</strong><small>{detail}</small></div>}
function Bars({items}){const highest=Math.max(...items.map(x=>x.count),1);return <div className="bars">{items.length ? items.map(x=><div className="bar-row" key={x.label}><span>{x.label}</span><div className="bar-track"><div className="bar-fill" style={{width:(100*x.count/highest)+'%'}}/></div><b>{x.count}</b></div>):<div className="empty-small">No analysis events yet. Upload a sample to generate demo analytics.</div>}</div>}
function App(){
 const [file,setFile]=useState(null),[result,setResult]=useState(null),[analytics,setAnalytics]=useState(null)
 const [error,setError]=useState(''),[loading,setLoading]=useState(false),[tab,setTab]=useState('analysis'),[drag,setDrag]=useState(false)
 const [pdfPreviewUrl,setPdfPreviewUrl]=useState(null)
 useEffect(()=>{
  if(!file || !/\.pdf$/i.test(file.name)){setPdfPreviewUrl(null);return}
  const url=URL.createObjectURL(file)
  setPdfPreviewUrl(url)
  return ()=>URL.revokeObjectURL(url)
 },[file])
 async function loadMetrics(){try{const response=await fetch(API+'/api/v1/analytics');if(response.ok)setAnalytics(await response.json())}catch{}}
 useEffect(()=>{loadMetrics()},[])
 function pick(f){if(!f)return;setFile(f);setResult(null);setError('');setTab('analysis')}
 async function run(selected){
  const chosen=selected||file;if(!chosen){setError('Choose a PDF or UTF-8 text document first.');return}
  setLoading(true);setError('');setResult(null)
  try{
   const form=new FormData();form.append('file',chosen,chosen.name)
   const response=await fetch(API+'/api/v1/analyze',{method:'POST',body:form})
   const body=await response.json()
   if(!response.ok)throw new Error(typeof body.detail==='string'?body.detail:'Analysis could not be completed.')
   setResult(body);setTab('analysis');loadMetrics()
  }catch(e){setError(e.message||'API unavailable. Start the backend and try again.')}finally{setLoading(false)}
 }
 function download(){if(!result)return;const blob=new Blob([JSON.stringify(result,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const anchor=document.createElement('a');anchor.href=url;anchor.download='docsight-analysis.json';anchor.click();URL.revokeObjectURL(url)}
 const modelCategories=analytics?.categories||[]
 return <div className="shell">
  <aside className="sidebar"><a className="brand" href="#"><span className="mark"><Layers size={22}/></span><span>DOCSIGHT <b>AI</b><small>DOCUMENT INTELLIGENCE</small></span></a>
   <div className="side-label">WORKSPACE</div>
   <button className={'navitem '+(tab==='analysis'?'active':'')} onClick={()=>setTab('analysis')}><ScanText size={18}/>Document Lab</button>
   <button className={'navitem '+(tab==='analytics'?'active':'')} onClick={()=>{setTab('analytics');loadMetrics()}}><ChartColumn size={18}/>Usage Analytics</button>
   <div className="side-label mt">ENGINEERING</div><a className="navitem" href="https://github.com/harshakavali81-collab/Smart-Document-Classifier-Summarizer" target="_blank" rel="noreferrer"><Github size={18}/>Source repository</a>
   <div className="bottom-box"><ShieldCheck size={20}/><h4>Local-first privacy</h4><p>Documents are processed in memory. The API records category and timing metadata only.</p><small>Demo only · no authentication</small></div>
  </aside>
  <main className="main"><div className="topline"><span className="breadcrumb">WORKSPACE <span>/</span> {tab==='analysis'?'DOCUMENT LAB':'USAGE ANALYTICS'}</span><span className="top-pill"><span className="dot"/>EXTRACTIVE · SOURCE-LINKED</span></div>
   {tab==='analysis'?<><section className="hero"><div><div className="eyebrow">DOCUMENT AI / EXPLAINABLE ML</div><h1>Turn complex documents into <em>clear, verifiable insights.</em></h1><p>Upload a document to classify its content and get an extractive summary with page-level evidence. No hallucinated sentences, external AI services, or hidden reference links.</p></div><div className="hero-decoration"><div className="halo"><FileText size={66}/><span className="mini-card a">PDF → TEXT</span><span className="mini-card b">PAGE 01 ✓</span></div></div></section>
    <section className="workspace-grid"><div className="panel upload-panel"><div className="panel-head"><div><div className="eyebrow">01 · INGESTION</div><h2>Analyze a document</h2></div><div className="muted-tag">PDF / TXT</div></div>
     <label className={'drop '+(drag?'drag':'')} onDragOver={e=>{e.preventDefault();setDrag(true)}} onDragLeave={()=>setDrag(false)} onDrop={e=>{e.preventDefault();setDrag(false);pick(e.dataTransfer.files[0])}}><input aria-label="Choose a PDF or text document" type="file" accept=".pdf,.txt,application/pdf,text/plain" onChange={e=>pick(e.target.files?.[0])}/><span className="upload-icon"><UploadCloud size={27}/></span><strong>{file?file.name:'Drop your document here'}</strong><span>{file?'Ready for local analysis':'or click to browse files from your device'}</span><small>Max 6 MiB · 50 pages · selectable PDF text only</small></label>
     <div className="upload-actions"><button className="primary" disabled={loading} onClick={()=>run()}>{loading?'Analyzing document…':'Run analysis'}<ArrowRight size={17}/></button><button className="secondary" disabled={loading} onClick={()=>{const sample=new File([SAMPLE],'synthetic-operations-report.txt',{type:'text/plain'});pick(sample);run(sample)}}>Try sample</button></div>
     {error&&<div className="message error" role="alert"><AlertCircle size={17}/>{error}</div>}
     <div className="info-line"><Info size={16}/>Privacy: uploaded content is not saved to the analytics database.</div>
    </div>
    <div className="panel workflow"><div className="panel-head"><div><div className="eyebrow">02 · PIPELINE</div><h2>How DocSight works</h2></div></div>
     {[[FileText,'Extract & validate','Read text and preserve page numbers.'],[Database,'Classify document','TF-IDF + logistic regression over six demo classes.'],[ScanText,'Summarize with evidence','Selected sentences linked to their original pages.'],[ChartColumn,'Track operational metrics','Aggregate classification and request timing only.']].map(([Icon,title,description],i)=><div className="step" key={title}><span className="step-num">0{i+1}</span><div className="step-icon"><Icon size={20}/></div><div><b>{title}</b><p>{description}</p></div></div>)}
    </div></section>
    {result?<section className="result" aria-live="polite"><div className="result-title"><div><div className="eyebrow">03 · ANALYSIS RESULT</div><h2>Evidence-backed output</h2><p>{result.filename}</p></div><button className="secondary" onClick={download}><Download size={16}/>Export JSON</button></div>
     <div className="metrics"><Metric icon={CheckCircle2} label="Category" value={result.category} detail="Synthetic-trained demo model"/><Metric icon={ChartColumn} label="Model score" value={(result.confidence*100).toFixed(1)+'%'} detail="Not calibrated accuracy"/><Metric icon={FileText} label="Pages" value={fmt(result.page_count)} detail={fmt(result.word_count)+' extracted words'}/><Metric icon={ScanText} label="Processing" value={fmt(result.latency_ms)+' ms'} detail="Backend analysis elapsed time"/></div>
     <div className="panel evidence"><div className="panel-head"><div><div className="eyebrow">SOURCE-TRACEABLE SUMMARY</div><h2>Highlights & citations</h2></div><span className="muted-tag">{result.summary.length} excerpts</span></div>
      {result.summary.length ? result.summary.map((item,i)=><div className="excerpt" key={i}>{pdfPreviewUrl?<a className="citation" href={pdfPreviewUrl+'#page='+item.page} target="_blank" rel="noopener noreferrer" title="Open the uploaded PDF at this page in your browser">PAGE {String(item.page).padStart(2,'0')} ↗</a>:<span className="citation">PAGE {String(item.page).padStart(2,'0')}</span>}<p>{item.text}</p></div>):<p>No sentences met the summary selection criteria.</p>}
      <div className="message note"><Info size={17}/>{result.note} PDF page labels open the original locally uploaded PDF where supported by your browser. Citations trace the source, not the truth of its contents.</div>
     </div></section>:<div className="placeholder"><FileText size={20}/>Your classification and page-linked summary will appear here after analysis.</div>}
    </>:<><section className="page-heading"><div className="eyebrow">DEMO OPERATIONS / AGGREGATES</div><h1>Usage analytics</h1><p>Observability for a small prototype. Counts below reflect this server's real requests, not training or validation quality.</p></section>
    <div className="metrics analytics-metrics"><Metric icon={FileText} label="Analyses" value={fmt(analytics?.total_analyses)} detail="Analyzed uploads"/><Metric icon={Layers} label="Pages processed" value={fmt(analytics?.pages_processed)} detail="Total across uploads"/><Metric icon={ChartColumn} label="Mean duration" value={fmt(analytics?.average_latency_ms)+' ms'} detail="End-to-end backend latency"/></div>
    <div className="panel insight-panel"><div className="panel-head"><div><div className="eyebrow">CATEGORY DISTRIBUTION</div><h2>Documents by predicted class</h2></div></div><Bars items={modelCategories}/><p className="muted">Includes uncertain predictions. Counts are not model accuracy or quality scores.</p></div>
    <div className="panel insight-panel"><div className="eyebrow">DAILY REQUEST COUNTS</div><h2>Recent analysis activity</h2><Bars items={(analytics?.days||[]).map(x=>({label:x.day,count:x.count}))}/></div>
    <div className="message note"><Info size={16}/>No user accounts, access control or retention automation are included. Do not expose a public production API without authentication, rate limits and additional hardening.</div>
   </>}
   <footer><span>DOCSIGHT AI • 2026 • PORTFOLIO PROTOTYPE</span><span>Evidence first. Claims second.</span></footer>
  </main></div>
}
export default App
