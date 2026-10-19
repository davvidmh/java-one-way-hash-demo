"""Comprobación reproducible; registra el sistema donde realmente se ejecute."""
from pathlib import Path
import hashlib,json,platform,subprocess

base=Path(__file__).resolve().parent
build=base/'build';build.mkdir(exist_ok=True)
subprocess.run(['javac','-J-Xmx128m','-encoding','UTF-8','--release','17','-d',str(build),str(base/'OneWayHash.java')],check=True)
cases=[([], 'hola'),(['hola'],'hola'),([''],''),(['Hola'],'Hola'),(['hola','mundo'],'hola mundo'),(['áéíóú','🔐'],'áéíóú 🔐')]
for arguments,text in cases:
    run=subprocess.run(['java','-Xmx64m','-Djava.awt.headless=true','-cp',str(build),'OneWayHash',*arguments],capture_output=True,text=True,encoding='utf-8',check=True)
    assert run.stdout==hashlib.sha256(text.encode()).hexdigest()+'\n'
    assert not run.stderr
target=hashlib.sha256(b'hola').hexdigest()
assert next(s for s in ['adios','mundo','hola','casa'] if hashlib.sha256(s.encode()).hexdigest()==target)=='hola'
print(json.dumps({'os':platform.system(),'architecture':platform.machine(),'cases_passed':len(cases),'dictionary_match':'hola'}))
