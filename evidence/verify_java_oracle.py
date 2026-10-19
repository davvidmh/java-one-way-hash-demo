"""Compila y comprueba el código público en el servidor, sin proveedores de IA."""
from pathlib import Path
import hashlib,json,subprocess,re,platform

BASE=Path(__file__).resolve().parent
BUILD=BASE/'build'
BUILD.mkdir(exist_ok=True)
subprocess.run(['javac','-J-Xmx128m','-encoding','UTF-8','--release','17','-d',str(BUILD),str(BASE/'OneWayHash.java')],check=True,capture_output=True,text=True,timeout=30)
cases=[([], 'hola'),(['hola'],'hola'),([''],''),(['Hola'],'Hola'),(['hola','mundo'],'hola mundo'),(['áéíóú','🔐'],'áéíóú 🔐')]
results=[]
for arguments,text in cases:
    run=subprocess.run(['java','-Xmx64m','-Djava.awt.headless=true','-cp',str(BUILD),'OneWayHash',*arguments],capture_output=True,text=True,encoding='utf-8',check=True,timeout=10)
    expected=hashlib.sha256(text.encode('utf-8')).hexdigest()
    assert run.stdout==expected+'\n' and not run.stderr
    assert re.fullmatch('[0-9a-f]{64}\n',run.stdout)
    results.append({'input':text,'default_invocation':not arguments,'expected':expected,'actual':run.stdout.strip(),'passed':True})
# Una palabra corta puede identificarse por enumeración; no presentar el hash como protección de secretos débiles.
target=hashlib.sha256(b'hola').hexdigest()
candidates=['adios','mundo','hola','casa']
guess=next(s for s in candidates if hashlib.sha256(s.encode()).hexdigest()==target)
assert guess=='hola'
report={'execution':'Oracle Linux ARM64','java_target':17,'tests':results,'dictionary_demonstration':{'candidate_count':len(candidates),'matched':'hola'},'source_sha256':hashlib.sha256((BASE/'OneWayHash.java').read_bytes()).hexdigest(),'passed':True}
(BASE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'execution':report['execution'],'cases_passed':len(results),'dictionary_match':guess,'source_sha256':report['source_sha256']}))
