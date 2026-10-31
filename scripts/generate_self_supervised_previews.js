// Original CC BY-SA 4.0; no dependencies. Regenerate: node scripts/generate_self_supervised_previews.js
function generate(kind) {
  const W=480,H=200,P=16;
  const colors=['#f8fbfd','#b9cbd6','#20384b','#3a7fa9','#dfecf3','#399a80','#e4f3eb','#c06647','#8c62a7','#e9eff4','#15856d','#ffffff','#455e72','#c6eee0','#b55d65','#fbe3d2'];
  const glyph={
    A:['01110','10001','10001','11111','10001','10001','10001'],B:['11110','10001','10001','11110','10001','10001','11110'],C:['01111','10000','10000','10000','10000','10000','01111'],D:['11110','10001','10001','10001','10001','10001','11110'],E:['11111','10000','10000','11110','10000','10000','11111'],F:['11111','10000','10000','11110','10000','10000','10000'],G:['01111','10000','10000','10111','10001','10001','01111'],H:['10001','10001','10001','11111','10001','10001','10001'],I:['11111','00100','00100','00100','00100','00100','11111'],J:['00111','00010','00010','00010','10010','10010','01100'],K:['10001','10010','10100','11000','10100','10010','10001'],L:['10000','10000','10000','10000','10000','10000','11111'],M:['10001','11011','10101','10101','10001','10001','10001'],N:['10001','11001','10101','10011','10001','10001','10001'],O:['01110','10001','10001','10001','10001','10001','01110'],P:['11110','10001','10001','11110','10000','10000','10000'],Q:['01110','10001','10001','10001','10101','10010','01101'],R:['11110','10001','10001','11110','10100','10010','10001'],S:['01111','10000','10000','01110','00001','00001','11110'],T:['11111','00100','00100','00100','00100','00100','00100'],U:['10001','10001','10001','10001','10001','10001','01110'],V:['10001','10001','10001','10001','10001','01010','00100'],W:['10001','10001','10001','10101','10101','10101','01010'],X:['10001','10001','01010','00100','01010','10001','10001'],Y:['10001','10001','01010','00100','00100','00100','00100'],Z:['11111','00001','00010','00100','01000','10000','11111'],
    '0':['01110','10011','10101','10101','11001','10001','01110'],'1':['00100','01100','00100','00100','00100','00100','01110'],'2':['01110','10001','00001','00010','00100','01000','11111'],'3':['11110','00001','00001','01110','00001','00001','11110'],'4':['00010','00110','01010','10010','11111','00010','00010'],'5':['11111','10000','10000','11110','00001','00001','11110'],'6':['01110','10000','10000','11110','10001','10001','01110'],'7':['11111','00001','00010','00100','01000','01000','01000'],'8':['01110','10001','10001','01110','10001','10001','01110'],'9':['01110','10001','10001','01111','00001','00001','01110'],
    '.':['00000','00000','00000','00000','00000','00110','00110'],'-':['00000','00000','00000','11111','00000','00000','00000'],' ':['00000','00000','00000','00000','00000','00000','00000']
  };
  const rgb=colors.flatMap(hex=>[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)));
  const frames=[];
  const online=[.70,.85,.78,.91], target=[.30];for(let i=1;i<4;i++)target.push(.9*target[i-1]+.1*online[i]);
  for(let fi=0;fi<36;fi++){
    const pix=new Uint8Array(W*H);pix.fill(0);
    const rect=(x,y,w,h,c)=>{x=Math.round(x);y=Math.round(y);w=Math.round(w);h=Math.round(h);for(let yy=Math.max(0,y);yy<Math.min(H,y+h);yy++)pix.fill(c,yy*W+Math.max(0,x),yy*W+Math.min(W,x+w));};
    const line=(x0,y0,x1,y1,c,width=2)=>{const n=Math.ceil(Math.hypot(x1-x0,y1-y0)*1.3)+1;for(let i=0;i<=n;i++){const t=i/n;rect(x0+(x1-x0)*t-width/2,y0+(y1-y0)*t-width/2,width,width,c);}};
    const circle=(x,y,r,c)=>{const xx=Math.round(x),yy=Math.round(y);for(let j=-r;j<=r;j++){let k=Math.floor(Math.sqrt(r*r-j*j));rect(xx-k,yy+j,2*k+1,1,c);}};
    const text=(str,x,y,c=2,scale=2)=>{let px=x;for(const ch of str.toUpperCase()){const rows=glyph[ch]||glyph[' '];for(let j=0;j<7;j++)for(let i=0;i<5;i++)if(rows[j][i]==='1')rect(px+i*scale,y+j*scale,scale,scale,c);px+=6*scale;}};
    const ease=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t)};
    const turn=Math.floor(fi/12),phase=fi%12;
    const q=online[turn]+(online[turn+1]-online[turn])*ease((phase-5)/3);
    const k=target[turn]+(target[turn+1]-target[turn])*ease((phase-8)/3);
    const stage=phase<3?'ENCODE':phase<6?'LOSS':phase<9?'SGD':phase<11?'EMA':(kind==='moco'?'FIFO':'EMA');
    rect(0,0,W,200,0);rect(0,0,W,2,1);rect(0,198,W,2,1);
    text(kind==='moco'?'MOCO':'BYOL',20,12,2,3);
    text('ITER '+(turn+1),188,17,12,2);
    text(stage,345,17,phase<9?3:10,2);
    line(20,42,460,42,1,2);
    text(kind==='moco'?'QUERY':'ONLINE',20,59,12,2);
    text(kind==='moco'?'KEY':'TARGET',20,102,12,2);
    rect(145,60,255,14,4);rect(145,103,255,14,6);
    rect(145,60,255*q,14,3);rect(145,103,255*k,14,5);
    circle(145+255*q,67,9,2);circle(145+255*k,110,9,10);
    text(q.toFixed(3),408,60,2,2);text(k.toFixed(3),408,103,2,2);
    if(kind==='moco'){
      text('FIFO',20,135,12,2);
      const queue=['A','B','C','D','E','F','G','H','I'];
      const shift=ease((phase-10)/2);
      for(let i=0;i<7;i++){
        if(i===6&&phase<10)continue; // New key is NOT a negative for this loss.
        const item=queue[turn+i];
        const x=102+56*i-56*shift;
        if(x<70||x>460)continue;
        rect(x,145,48,30,i===6?13:9);rect(x,145,48,2,1);
        text(item,x+18,153,2,2);
      }
      if(phase<3)circle(150+(phase/2)*185,124,5,3);
      else if(phase<6)circle(330,119-(phase-3)/2*45,5,8);
      else if(phase<9)circle(145+255*q,67,5,7);
      else if(phase<11)circle(145+255*k,110,5,10);
      else circle(440-42*(phase-10),161,5,10);
    }else{
      text('STOP GRAD',20,144,14,2);
      for(let i=0;i<10;i++)rect(175+i*15,150,8,3,14);
      text('NO NEGATIVES',20,170,12,2);
      if(phase<3)circle(150+(phase/2)*180,132,5,3);
      else if(phase<6)circle(330-(phase-3)/2*130,132,5,8);
      else if(phase<9)circle(145+255*q,67,5,7);
      else circle(145+255*k,110,5,10);
    }
    text('TOY VALUES  M 0.9',280,183,12,1);
    frames.push(pix);
  }
  const out=[];const push=(...a)=>out.push(...a);const u16=n=>push(n&255,n>>8&255);
  for(const ch of 'GIF89a')push(ch.charCodeAt(0));u16(W);u16(H);push(0xF3,0,0);push(...rgb);
  push(0x21,0xFF,11);for(const ch of 'NETSCAPE2.0')push(ch.charCodeAt(0));push(3,1,0,0,0);
  const lzw=arr=>{
    const bytes=[];let bits=0,count=0;const emit=(v,size)=>{bits|=v<<count;count+=size;while(count>=8){bytes.push(bits&255);bits>>>=8;count-=8;}};
    let dict,next,size;
    const reset=()=>{dict=new Map();for(let i=0;i<P;i++)dict.set(String.fromCharCode(i),i);next=P+2;size=5;};
    reset();emit(P,size);let prefix=String.fromCharCode(arr[0]);
    for(let i=1;i<arr.length;i++){
      const ch=String.fromCharCode(arr[i]),pair=prefix+ch;
      if(dict.has(pair)){prefix=pair;continue;}
      emit(dict.get(prefix),size);
      if(next<4096){dict.set(pair,next++);if(next>(1<<size)&&size<12)size++;}
      else{emit(P,size);reset();}
      prefix=ch;
    }
    emit(dict.get(prefix),size);emit(P+1,size);if(count)bytes.push(bits&255);
    return bytes;
  };
  for(const frame of frames){
    push(0x21,0xF9,4,0x08,24,0,0,0);
    push(0x2C);u16(0);u16(0);u16(W);u16(H);push(0);
    push(4);
    const data=lzw(frame);
    for(let i=0;i<data.length;i+=255){const block=data.slice(i,i+255);push(block.length,...block);}push(0);
  }
  push(0x3B);
  return new Uint8Array(out);
}
if (typeof require !== 'undefined' && require.main === module) {
  const fs=require('fs'),path=require('path');
  for(const kind of ['moco','byol']) {
    const file=path.join(__dirname,'../docs/assets/concept-animations',kind+'-momentum-preview.gif');
    fs.writeFileSync(file,generate(kind));
    console.log(file,fs.statSync(file).size);
  }
}
