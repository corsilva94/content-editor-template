// One entry point for every npm command. Reads project.json to find the active job and video.
import {spawnSync} from 'node:child_process';
import {readFileSync,existsSync,mkdirSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const cfgPath=path.join(root,'project.json');
const cfg=JSON.parse(readFileSync(cfgPath));
const job=path.join(root,cfg.job);
const videoDir=path.join(job,'work',cfg.video);
const project=path.join('work',cfg.video,cfg.composition);
const compDir=path.join(videoDir,cfg.composition);
const hf=path.join(root,'node_modules','.bin',process.platform==='win32'?'hyperframes.cmd':'hyperframes');
const python=process.env.PYTHON || (process.platform==='win32'?'python':'python3');
const vpy=path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
const cmd=process.argv[2] || 'doctor';

function run(bin,args,cwd=root){const r=spawnSync(bin,args,{cwd,stdio:'inherit'});if(r.error)throw r.error;if(r.status!==0)throw new Error(`${path.basename(bin)} exited ${r.status}`);}
function needFile(p,message){if(!existsSync(p))throw new Error(message);}
function readEdit(){needFile(path.join(videoDir,'edit.json'),`No edit.json in ${videoDir}. See docs/FIRST-VIDEO.md.`);return JSON.parse(readFileSync(path.join(videoDir,'edit.json')));}
function sha(p){return createHash('sha256').update(readFileSync(p)).digest('hex');}
function mediaCheck(){
 const m=JSON.parse(readFileSync(path.join(root,'media-manifest.json')));
 if(m.files&&m.files.length){
  for(const f of m.files){const p=path.join(root,f.path);needFile(p,'Media missing. Run npm run download:media first.');if(sha(p)!==f.sha256)throw new Error(`Media checksum differs: ${f.path}. Keep originals intact; use a new video folder for other footage.`);}
  return;
 }
 const e=readEdit();
 const footage=path.join(compDir,e.footage||'assets/media/footage.mp4');
 needFile(footage,`Footage missing: ${footage}\nPut your prepared clip there (or set "footage" in edit.json). See docs/FIRST-VIDEO.md.`);
 if(e.music)needFile(path.join(compDir,e.music),`Music file named in edit.json is missing: ${e.music}`);
}
function pythonReady(){needFile(vpy,'Run npm run setup before building the composition.');}
function snapshotTimes(duration){const pts=[0,.1,.3,.5,.7,.9].map(f=>+(f*duration).toFixed(2));return pts.join(',');}

try{
 if(Number(process.versions.node.split('.')[0])<22)throw new Error('Node.js 22 or later is required.');
 switch(cmd){
 case 'setup':
  run(python,['-c',"import sys; assert sys.version_info >= (3,12), 'Python 3.12+ is required (set PYTHON=/path/to/python3.12 if your default is older)'"]);
  if(!existsSync(vpy))run(python,['-m','venv',path.join(root,'.venv')]);
  run(vpy,['-m','pip','install','-q','-r',path.join(root,'requirements.txt')]);
  console.log('Python editing tools ready. Next: put footage in place, then npm run build and npm run preview.');break;
 case 'use':{
  const name=process.argv[3];if(!name)throw new Error('Usage: npm run use -- <video-folder>');
  needFile(path.join(job,'work',name,'edit.json'),`No edit.json in ${path.join(job,'work',name)}.`);
  cfg.video=name;writeFileSync(cfgPath,JSON.stringify(cfg,null,2)+'\n');console.log(`Active video: ${name}`);break;
 }
 case 'download':{
  const m=JSON.parse(readFileSync(path.join(root,'media-manifest.json')));
  if(!m.files||!m.files.length)throw new Error('media-manifest.json lists no files. Drop your clip into the composition assets/media folder instead (docs/FIRST-VIDEO.md).');
  const dir=path.join(root,'.downloads');mkdirSync(dir,{recursive:true});
  const local=process.argv[3]?path.resolve(process.argv[3]):null;
  if(!local)run('gh',['release','download',m.release,'--repo',m.repository,'--pattern',m.asset,'--dir',dir,'--clobber']);
  const zip=local||path.join(dir,m.asset);
  if(sha(zip)!==m.sha256)throw new Error('Downloaded media archive failed its checksum.');
  run(python,[path.join(root,'scripts/extract_media.py'),zip]);mediaCheck();console.log('Media downloaded and verified.');break;
 }
 case 'doctor':
  run(python,['--version']);run('ffmpeg',['-version']);needFile(hf,'Run npm ci first.');run(hf,['--version']);
  console.log('Active video:',cfg.video);
  try{mediaCheck();console.log('Footage: ready');}catch(e){console.log('Footage:',e.message.split('\n')[0]);}
  console.log('Python building:',existsSync(vpy)?'ready':'run npm run setup');break;
 case 'transcribe':{
  const input=process.argv[3];if(!input)throw new Error('Usage: npm run transcribe -- <audio-or-video-file>');
  const out=path.join(videoDir,'transcript.json');
  run('node',[path.join(root,'Misc/media-use/scripts/transcribe.mjs'),'--input',path.resolve(input),'--out',out,'--json']);
  console.log(`Word-level transcript saved: ${out}. Build edit.json from it (docs/FIRST-VIDEO.md).`);break;
 }
 case 'build':{
  pythonReady();mediaCheck();run(vpy,[path.join(videoDir,'build.py')],job);
  const grade=path.join(videoDir,'color','selected-payload.json');
  if(existsSync(grade))run(hf,['media-treatment','--project',project,'--file','index.html','--selector','#footage','--grading','../color/selected-payload.json','--apply','--json'],job);
  break;
 }
 case 'preview':
  mediaCheck();run(hf,['preview',project,'--foreground','--no-open','--port',String(process.env.PORT||cfg.port||3002)],job);break;
 case 'check':
  mediaCheck();run(hf,['check',project,'--json'],job);break;
 case 'snapshot':
  mediaCheck();run(hf,['snapshot',project,'--at',snapshotTimes(readEdit().duration),'--json'],job);break;
 case 'render':{
  mediaCheck();run(hf,['check',project,'--json'],job);
  const e=readEdit();const name=(e.title||cfg.video).replace(/[\\/:*?"<>|]/g,'-');
  const dir=path.join(job,'exports',cfg.video);mkdirSync(dir,{recursive:true});
  const r=cfg.render||{};const fps=r.fps||'24000/1001';
  const intermediate=path.join(dir,`${name}-render.mp4`);const final=path.join(dir,`${name}.mp4`);
  run(hf,['render',project,'--fps',fps,'--quality',r.quality||'delivery','--video-frame-format','png','--workers',String(r.workers||2),'-o',intermediate],job);
  if(r.srgb_transfer_fix!==false){
   // Browser captures are sRGB-coded. Tag the H.264 stream and MP4 container to match so colour-managed players (Apple) show what the preview showed.
   run('ffmpeg',['-y','-v','error','-i',intermediate,'-map','0','-c','copy','-bsf:v','h264_metadata=transfer_characteristics=13','-color_trc','iec61966-2-1','-color_primaries','bt709','-colorspace','bt709','-movflags','+faststart',final]);
  }else{
   run('ffmpeg',['-y','-v','error','-i',intermediate,'-map','0','-c','copy','-movflags','+faststart',final]);
  }
  const probe=spawnSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',final],{encoding:'utf8'});if(probe.status!==0)throw new Error('Export metadata verification failed.');
  const data=JSON.parse(probe.stdout);const v=data.streams.find(s=>s.codec_type==='video');
  if(v.width!==1080||v.height!==1920||v.r_frame_rate!==fps)throw new Error(`Unexpected export settings: ${v.width}x${v.height} @ ${v.r_frame_rate}`);
  if(r.srgb_transfer_fix!==false&&v.color_transfer!=='iec61966-2-1')throw new Error('Transfer tag was not applied.');
  writeFileSync(path.join(dir,'export-info.json'),JSON.stringify(data,null,2)+'\n');console.log(`Saved: ${final}`);break;
 }
 default:throw new Error(`Unknown command: ${cmd}`);
 }
}catch(e){console.error(e.message);process.exitCode=1;}
