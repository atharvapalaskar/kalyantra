 
const util = require('util');
const exec = util.promisify(require('child_process').exec);

export interface EspeakOptions {
    speak : string, 
    a?: number,//ampltitue :: max 200
    g?: number,//gap between words :: unit in ms 
    s?: number //speed: words-per-minute :: 80-500
}

export const espeak = async(opt:EspeakOptions) =>{ 
   try{ await exec(`espeak -a ${opt.a?? 130} -g ${opt.g?? 10} -s ${opt.s?? 175} '${opt.speak}'`)
    //console.log('data:', data);
   } catch(err) { console.log('err:', err); };
}

export default espeak;