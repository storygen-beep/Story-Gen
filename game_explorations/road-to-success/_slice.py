import re,sys
src=open('_storyjs_dump.js').read()
heads=[(m.group(1), m.start()) for m in re.finditer(r'twine-user-script #\d+: "([^"]+)"', src)]
def mod(name):
    for i,(n,s) in enumerate(heads):
        if n==name:
            e=heads[i+1][1] if i+1<len(heads) else len(src)
            return src[s:e]
    return None
name=sys.argv[1]; start=int(sys.argv[2]) if len(sys.argv)>2 else 0; end=int(sys.argv[3]) if len(sys.argv)>3 else 99999
b=mod(name)
print('### %s  total_len=%d ###'%(name,len(b)))
print(b[start:end])
