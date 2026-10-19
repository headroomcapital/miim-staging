import sys,os,glob; sys.argv=['x']
from fal_gen import call
import base64
from concurrent.futures import ThreadPoolExecutor
def up(f):
    d='data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    out=f.replace('/v-','/up-')
    call('fal-ai/esrgan',{'image_url':d,'scale':2,'model':'RealESRGAN_x4plus','output_format':'png'},out); return out
fs=sorted(glob.glob('fal_out/ii/v-*.png'))
with ThreadPoolExecutor(8) as ex: print(len(list(ex.map(up,fs))))
