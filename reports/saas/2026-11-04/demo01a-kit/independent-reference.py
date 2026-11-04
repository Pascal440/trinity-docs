"""Independent evaluator reference derived from the three fictional INPUTS, not LLM output."""
from pathlib import Path
from decimal import Decimal
import json,re
from openpyxl import load_workbook
from docx import Document
from pypdf import PdfReader
p=Path('/home/user/runtime01/inputs');rows=list(load_workbook(p/'01_ventes_fictives.xlsx',data_only=True).active.values)[1:]
t1=sum(int(row[1]) for row in rows);t2=sum(int(row[2]) for row in rows)
pdf=' '.join(page.extract_text() for page in PdfReader(p/'03_couts_fictifs.pdf').pages)
cost=lambda period:int(re.search(period+r'\s+2026\s+([0-9 ]+)',pdf)[1].replace(' ',''))
c1=cost('T1');c2=cost('T2');brief=' '.join(x.text for x in Document(p/'02_brief_fictif.docx').paragraphs)
target=int(re.search(r'affaires T2\s*:\s*([0-9 ]+)\s*EUR',brief)[1].replace(' ',''))
print(json.dumps({'derived_from_input_documents':True,'llm_outputs_evaluated':False,'revenue_t1':t1,'revenue_t2':t2,'revenue_delta':t2-t1,'revenue_growth_pct':str((Decimal(t2)/Decimal(t1)-1)*100),'costs_t1':c1,'costs_t2':c2,'margin_t1':t1-c1,'margin_t2':t2-c2,'margin_t2_pct':str(Decimal(t2-c2)/Decimal(t2)*100),'revenue_target_t2':target,'target_gap':t2-target},indent=2))
