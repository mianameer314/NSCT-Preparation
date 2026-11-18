import pypdf
import re
import json
import os

pdf_path = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\NSCT_File_01_Problem_Solving.pdf'
reader = pypdf.PdfReader(pdf_path)

pages_text = []
for p_no in range(len(reader.pages)):
    spans = []
    def visitor(text, cm, tm, fontDict, fontSize):
        if text:
            is_bold = False
            if fontDict:
                bf = str(fontDict.get('/BaseFont', ''))
                if 'Bold' in bf or 'bold' in bf:
                    is_bold = True
            spans.append((text, is_bold))
    reader.pages[p_no].extract_text(visitor_text=visitor)
    merged = ''
    for t, b in spans:
        if b:
            merged += f'«B»{t}«/B»'
        else:
            merged += t
    pages_text.append(merged)

full_text = '\n'.join(pages_text)
# Remove bullet points that appear across page splits
full_text = re.sub(r'(?:«/B»)?\s*•\s*(?:«B»)?', ' ', full_text)

subtopic_matches = list(re.finditer(r'Subtopic\s+(\d+):\s*([^\n\(]+)\s*\((\d+)\s*MCQs\)', full_text))
print(f"Found {len(subtopic_matches)} subtopics.")

subtopics_data = []

for idx, sm in enumerate(subtopic_matches):
    sub_num = int(sm.group(1))
    sub_title = sm.group(2).strip()
    target_count = int(sm.group(3))
    
    start_pos = sm.start()
    end_pos = subtopic_matches[idx + 1].start() if idx + 1 < len(subtopic_matches) else len(full_text)
    
    sub_text = full_text[start_pos:end_pos]
    
    # Extract Quick Notes
    quick_notes = ""
    qn_start = sub_text.find("Quick Notes")
    ct_start = sub_text.find("Common Traps")
    mcq_start = sub_text.find("MCQs")
    dd_start = sub_text.find("Deep Dive")
    res_start = sub_text.find("Stable Web Resources")
    
    if qn_start != -1:
        qn_end = ct_start if ct_start != -1 else (mcq_start if mcq_start != -1 else len(sub_text))
        quick_notes = sub_text[qn_start + len("Quick Notes"):qn_end].strip()
        quick_notes = re.sub(r'«/?B»', '', quick_notes)
        quick_notes = re.sub(r'\n+', '\n', quick_notes)
        
    # Extract Common Traps
    common_traps = ""
    if ct_start != -1:
        ct_end = mcq_start if mcq_start != -1 else len(sub_text)
        common_traps = sub_text[ct_start + len("Common Traps & Confusions"):ct_end].strip()
        common_traps = re.sub(r'«/?B»', '', common_traps)
        common_traps = re.sub(r'\n+', '\n', common_traps)
        
    # Extract Deep Dive
    deep_dive = ""
    if dd_start != -1:
        dd_end = res_start if res_start != -1 else len(sub_text)
        deep_dive = sub_text[dd_start + len("Deep Dive"):dd_end].strip()
        deep_dive = re.sub(r'«/?B»', '', deep_dive)
        deep_dive = re.sub(r'\n+', '\n', deep_dive)
        
    # Extract MCQs
    mcq_section = ""
    if mcq_start != -1:
        mcq_end = dd_start if dd_start != -1 else (res_start if res_start != -1 else len(sub_text))
        mcq_section = sub_text[mcq_start + len("MCQs"):mcq_end].strip()
        
    # Find individual questions
    q_matches = list(re.finditer(r'(?:«B»)?Q(\d+)\.(?:«/B»)?\s*(.*?)(?=(?:«B»)?Q\d+\.(?:«/B»)?|$)', mcq_section, re.DOTALL))
    
    questions = []
    for q in q_matches:
        q_num = int(q.group(1))
        raw = q.group(2).strip()
        
        # Locate option A)
        m_a = re.search(r'(?:^|\n)\s*(?:«B»)?A\)', raw)
        if not m_a:
            continue
        q_text = raw[:m_a.start()].strip()
        q_text = re.sub(r'«/?B»', '', q_text)
        q_text = re.sub(r'\s+', ' ', q_text)
        
        rest = raw[m_a.start():]
        
        opt_a_m = re.search(r'(?:^|\n)\s*(?:«B»)?A\)\s*(.*?)(?=(?:^|\n)\s*(?:«B»)?B\))', rest, re.DOTALL)
        opt_b_m = re.search(r'(?:^|\n)\s*(?:«B»)?B\)\s*(.*?)(?=(?:^|\n)\s*(?:«B»)?C\))', rest, re.DOTALL)
        opt_c_m = re.search(r'(?:^|\n)\s*(?:«B»)?C\)\s*(.*?)(?=(?:^|\n)\s*(?:«B»)?D\))', rest, re.DOTALL)
        opt_d_m = re.search(r'(?:^|\n)\s*(?:«B»)?D\)\s*(.*?)$', rest, re.DOTALL)
        
        if not (opt_a_m and opt_b_m and opt_c_m and opt_d_m):
            continue
            
        opt_a_raw = opt_a_m.group(0)
        opt_b_raw = opt_b_m.group(0)
        opt_c_raw = opt_c_m.group(0)
        opt_d_raw = opt_d_m.group(0)
        
        # Split D into option text and explanation
        d_content = opt_d_m.group(1).strip()
        d_lines = [l.strip() for l in d_content.splitlines() if l.strip()]
        
        opt_d_text = d_lines[0] if d_lines else ''
        explanation = ' '.join(d_lines[1:]) if len(d_lines) > 1 else ''
        
        # Check bold for correct option
        correct = None
        if '«B»' in opt_a_raw:
            correct = 'A'
        elif '«B»' in opt_b_raw:
            correct = 'B'
        elif '«B»' in opt_c_raw:
            correct = 'C'
        elif '«B»' in opt_d_raw[:opt_d_raw.find(d_lines[1]) if len(d_lines) > 1 else len(opt_d_raw)]:
            correct = 'D'
        else:
            # Check entire opt_d_raw
            if '«B»' in opt_d_raw:
                correct = 'D'
                
        opt_a_clean = re.sub(r'«/?B»', '', opt_a_m.group(1)).strip()
        opt_b_clean = re.sub(r'«/?B»', '', opt_b_m.group(1)).strip()
        opt_c_clean = re.sub(r'«/?B»', '', opt_c_m.group(1)).strip()
        opt_d_clean = re.sub(r'«/?B»', '', opt_d_text).strip()
        expl_clean = re.sub(r'«/?B»', '', explanation).strip()
        
        questions.append({
            'q_num': q_num,
            'question': q_text,
            'options': {
                'A': re.sub(r'\s+', ' ', opt_a_clean),
                'B': re.sub(r'\s+', ' ', opt_b_clean),
                'C': re.sub(r'\s+', ' ', opt_c_clean),
                'D': re.sub(r'\s+', ' ', opt_d_clean)
            },
            'correct': correct,
            'explanation': re.sub(r'\s+', ' ', expl_clean)
        })
        
    print(f"Subtopic {sub_num:02d}: {sub_title} -> {len(questions)}/{target_count} MCQs parsed.")
    subtopics_data.append({
        'id': sub_num,
        'title': sub_title,
        'target_mcqs': target_count,
        'quick_notes': quick_notes,
        'common_traps': common_traps,
        'deep_dive': deep_dive,
        'questions': questions
    })

output_path = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\subject_01_parsed.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(subtopics_data, f, indent=2, ensure_ascii=False)

total_qs = sum(len(st['questions']) for st in subtopics_data)
print(f"Extraction complete! Total questions parsed: {total_qs} / 320.")
