// Start a new video from the starter: npm run new -- <slug> ["Video Title"]
import {cpSync,existsSync,readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const cfgPath=path.join(root,'project.json');
const cfg=JSON.parse(readFileSync(cfgPath));
const slug=process.argv[2];const title=process.argv[3]||slug;
if(!slug||!/^[a-z0-9][a-z0-9-]*$/.test(slug))throw new Error('Usage: npm run new -- <slug> ["Video Title"]  (slug: lowercase letters, digits, dashes)');
const src=path.join(root,cfg.job,'work','starter');
const dest=path.join(root,cfg.job,'work',slug);
if(existsSync(dest))throw new Error(`${dest} already exists.`);
cpSync(src,dest,{recursive:true,filter:p=>!/assets[\\/]media[\\/].+|\.hyperframes|__pycache__|compositions[\\/].+\.html$|composition[\\/]index\.html$|captions\.json$|check\.json$|transcript\.json$/.test(p)});
mkdirSync(path.join(dest,cfg.composition,'assets','media'),{recursive:true});
const editPath=path.join(dest,'edit.json');const edit=JSON.parse(readFileSync(editPath));
edit.title=title;writeFileSync(editPath,JSON.stringify(edit,null,2)+'\n');
cfg.video=slug;writeFileSync(cfgPath,JSON.stringify(cfg,null,2)+'\n');
console.log(`Created ${dest} and made it the active video.
Next:
  1. Put your prepared clip at ${path.join(dest,cfg.composition,'assets/media/footage.mp4')}
  2. npm run transcribe -- <that clip>   (word timings)
  3. Fill in edit.json cuts/words and camera-plan.json (docs/FIRST-VIDEO.md)
  4. npm run build && npm run check && npm run preview`);
