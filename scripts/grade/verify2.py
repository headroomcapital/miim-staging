import sys; sys.path.insert(0,'.'); from common import *
def ld(f): return np.asarray(Image.open(f).convert('RGB'),dtype=np.float32)/255
for n,mats in [('ii',('aluminium','brass')),('i',('steel','brass'))]:
    at,ab,cb=np.load(f'matte_{n.upper()}.npy')
    for c in COLORS:
        a=rgb2lab(ld(f'out/miim-{n}-{c}-{mats[0]}.jpg'))[at>0.95].mean(0); print(f'{n:2s} top {c:7s} L{a[0]:5.1f} a{a[1]:6.1f} b{a[2]:6.1f} {hexs(lab2rgb(a))}')
    for mt in mats:
        a=rgb2lab(ld(f'out/miim-{n}-stone-{mt}.jpg'))[cb>0.5].mean(0); print(f'{n:2s} base {mt:9s} L{a[0]:5.1f} a{a[1]:5.1f} b{a[2]:5.1f} {hexs(lab2rgb(a))}')
    lab=rgb2lab(ld(f'out/miim-{n}-stone-{mats[0]}.jpg')); bg=(at<0.01)&(ab<0.01); ys=np.arange(H)[:,None]/H
    print(f'{n:2s} wall L{lab[bg&(ys<0.32)][:,0].mean():.1f} floor L{lab[bg&(ys>0.85)][:,0].mean():.1f}')
