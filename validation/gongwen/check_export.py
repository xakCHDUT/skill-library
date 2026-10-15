"""Reproduce narrow export checks using synthetic drafts, without external dependencies.

Run from skill-library root:
python -B validation/gongwen/check_export.py --output work/gongwen-checks/results.json
Optionally pass --upstream /path/to/pinned/original/repo to reproduce old overwrite behavior.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
LIB = HERE.parents[1]
SKILL = LIB/'skills/official-document-drafting'
GEN = SKILL/'src/scripts/generate_docx.py'
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--upstream', type=Path)
    args = parser.parse_args()
    checks = []
    def check(name, condition):
        checks.append({'name':name,'passed':bool(condition)})
        if not condition:
            raise AssertionError(name)
    def run(source, out=None, *extra, generator=GEN):
        command = [sys.executable,'-B','-X','utf8',str(generator),str(source)]
        if out is not None: command += ['-o',str(out)]
        return subprocess.run(command+list(extra),capture_output=True,encoding='utf-8',errors='replace')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gongwen-check-',dir=args.output.parent) as temp:
        tmp=Path(temp)
        for name, doc_type in [('request','请示'),('report','报告'),('repair-request','请示'),('school-notice','通知')]:
            out=tmp/(name+'.docx')
            r=run(HERE/'drafts'/f'{name}.md',out,'--doc-type',doc_type,'--title-font','宋体','--body-font','宋体','--title-wrap','off')
            check(name+' export',r.returncode==0 and out.is_file())
            with zipfile.ZipFile(out) as z:
                members=[p for p in z.namelist() if p.endswith(('.xml','.rels'))]
                roots=[ET.fromstring(z.read(p)) for p in members]
                check(name+' ZIP and XML', z.testzip() is None and len(roots)>=8)
                doc=ET.fromstring(z.read('word/document.xml'))
                paragraphs=doc.findall('.//w:body/w:p',NS)
                titles=[p for p in paragraphs if p.find("w:pPr/w:pStyle[@w:val='Title']",NS) is not None]
                title=''.join(titles[0].itertext()) if titles else ''
                expected=(HERE/'drafts'/f'{name}.md').read_text(encoding='utf-8').splitlines()[0][2:]
                check(name+' editable Title',title==expected and not z.namelist().count('word/media/image1.png'))
        source=tmp/'source.md'; source.write_text('# 旧稿\n\n保留原始内容。',encoding='utf-8')
        existing=tmp/'existing.docx'; existing.write_bytes(b'KEEP-OLD-OUTPUT')
        r=run(source,existing)
        check('existing output refused and retained',r.returncode!=0 and existing.read_bytes()==b'KEEP-OLD-OUTPUT')
        r=run(source,existing,'--overwrite')
        check('explicit overwrite produces valid ZIP',r.returncode==0 and zipfile.is_zipfile(existing))
        before=source.read_bytes(); r=run(source,source,'--overwrite')
        check('input path retained',r.returncode!=0 and source.read_bytes()==before)
        odd=tmp/'input.docx'; odd.write_text('# Markdown with misleading extension',encoding='utf-8'); before=odd.read_bytes()
        r=run(odd,odd,'--overwrite')
        check('input same path retained with docx suffix',r.returncode!=0 and odd.read_bytes()==before)
        r=run(source,tmp/'wrong.txt')
        check('wrong output extension rejected',r.returncode!=0 and not (tmp/'wrong.txt').exists())
        missing=tmp/'missing.md'; r=run(missing,tmp/'missing.docx')
        check('missing input creates no output',r.returncode!=0 and not (tmp/'missing.docx').exists())
        empty=tmp/'empty.md'; empty.write_text('',encoding='utf-8'); r=run(empty,tmp/'empty.docx')
        check('empty input creates no output',r.returncode!=0 and not (tmp/'empty.docx').exists())
        r=run(source,tmp/'invalid.docx','--doc-type','不存在的文种')
        check('unknown document type rejected',r.returncode!=0 and not (tmp/'invalid.docx').exists())
        sibling=tmp/'fresh.docx.tmp'; sibling.write_bytes(b'UNRELATED-TEMP')
        r=run(source,tmp/'fresh.docx')
        check('preexisting tmp sibling retained',r.returncode==0 and sibling.read_bytes()==b'UNRELATED-TEMP')
        sys.path.insert(0,str(SKILL/'src'))
        from adapters.doc_types import load_doc_types
        from docgen.package import write_docx_package
        check('all 22 document metadata load',len(load_doc_types())==22)
        old=tmp/'failure.docx'; old.write_bytes(b'KEEP-ON-FAILURE')
        export_args=SimpleNamespace(show_page_number=False,overwrite=True)
        try:
            with patch('docgen.package.build_styles_xml',side_effect=OSError('injected package failure')):
                write_docx_package(old,args=export_args,title='失败检查',document_xml='<document/>',image_assets={})
        except OSError: pass
        check('mid-package failure preserves old output',old.read_bytes()==b'KEEP-ON-FAILURE' and not list(tmp.glob('.official-doc-*.tmp')))
        # Original behavior is evidence, not a test of the adapted package.
        upstream={}
        if args.upstream:
            oldgen=args.upstream/'src/scripts/generate_docx.py'
            baseline=tmp/'baseline.md'; baseline.write_text('# 来源稿\n\n须保留。',encoding='utf-8')
            r=run(baseline,baseline,generator=oldgen)
            upstream['input_overwritten_by_docx']=r.returncode==0 and zipfile.is_zipfile(baseline)
            oldoutput=tmp/'baseline-output.docx'; oldoutput.write_bytes(b'PREEXISTING')
            r=run(source,oldoutput,generator=oldgen)
            upstream['existing_output_replaced_without_opt_in']=r.returncode==0 and zipfile.is_zipfile(oldoutput)
    result={'date':'2026-10-15','scope':'Adapter-author executable regression checks, separate from semantic review and independent agent evaluation','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'upstream_reproduction':upstream,'not_tested':['POSIX no-clobber branch','Windows symlink and hardlink alias paths','all 22 document kinds as authored documents','formal GB/T conformity','digital signatures and seal layout']}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':result['passed'],'total':result['total'],'upstream_reproduction':upstream},ensure_ascii=False))

if __name__=='__main__': main()
