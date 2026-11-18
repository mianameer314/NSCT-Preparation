import pypdf
import re
import json

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
# Remove all bullet symbols and artifacts
full_text = re.sub(r'•', ' ', full_text)

subtopic_matches = list(re.finditer(r'Subtopic\s+(\d+):\s*([^\n\(]+)\s*\((\d+)\s*MCQs\)', full_text))
print(f"Total subtopics found: {len(subtopic_matches)}")

parsed_subtopics = []
total_parsed_mcqs = 0

for i, sm in enumerate(subtopic_matches):
    sub_num = int(sm.group(1))
    sub_title = sm.group(2).strip()
    target_count = int(sm.group(3))
    
    start_pos = sm.start()
    end_pos = subtopic_matches[i+1].start() if i+1 < len(subtopic_matches) else len(full_text)
    sub_block = full_text[start_pos:end_pos]
    
    # Locate sections
    m_qn = re.search(r'(?:«/?B»\s*)*Quick Notes(?:«/?B»\s*)*', sub_block)
    m_ct = re.search(r'(?:«/?B»\s*)*Common Traps & Confusions(?:«/?B»\s*)*', sub_block)
    m_mcq = re.search(r'(?:«/?B»\s*)*\n\s*(?:«/?B»\s*)*MCQs(?:\s*\(.*?\))?(?:«/?B»\s*)*\n', sub_block)
    m_dd = re.search(r'(?:«/?B»\s*)*Deep Dive(?:«/?B»\s*)*', sub_block)
    m_res = re.search(r'(?:«/?B»\s*)*Stable Web Resources(?:«/?B»\s*)*', sub_block)
    
    quick_notes = ""
    if m_qn:
        qn_end = m_ct.start() if m_ct else (m_mcq.start() if m_mcq else len(sub_block))
        quick_notes = sub_block[m_qn.end():qn_end].strip()
        quick_notes = re.sub(r'«/?B»', '', quick_notes)
        
    common_traps = ""
    if m_ct:
        ct_end = m_mcq.start() if m_mcq else (m_dd.start() if m_dd else len(sub_block))
        common_traps = sub_block[m_ct.end():ct_end].strip()
        common_traps = re.sub(r'«/?B»', '', common_traps)
        
    deep_dive = ""
    if m_dd:
        dd_end = m_res.start() if m_res else len(sub_block)
        deep_dive = sub_block[m_dd.end():dd_end].strip()
        deep_dive = re.sub(r'«/?B»', '', deep_dive)
        
    mcq_text = ""
    first_q = re.search(r'(?:«/?B»\s*)*Q1\.', sub_block)
    if first_q:
        mcq_end = m_dd.start() if m_dd else (m_res.start() if m_res else len(sub_block))
        mcq_text = sub_block[first_q.start():mcq_end].strip()

    # Parse individual questions inside mcq_text
    q_starts = [m.start() for m in re.finditer(r'(?:«/?B»\s*)*Q\d+\.', mcq_text)]
    q_starts.append(len(mcq_text))
    
    questions = []
    for q_idx in range(len(q_starts)-1):
        q_chunk = mcq_text[q_starts[q_idx]:q_starts[q_idx+1]].strip()
        
        m_num = re.search(r'Q(\d+)\.', q_chunk)
        if not m_num:
            continue
        q_num = int(m_num.group(1))
        
        # Match option positions allowing start of line, newline, or 2+ spaces
        m_a = re.search(r'(?:^|\n|\s{2,})\s*(?:«/?B»\s*)*A\)', q_chunk)
        m_b = re.search(r'(?:^|\n|\s{2,})\s*(?:«/?B»\s*)*B\)', q_chunk)
        m_c = re.search(r'(?:^|\n|\s{2,})\s*(?:«/?B»\s*)*C\)', q_chunk)
        m_d = re.search(r'(?:^|\n|\s{2,})\s*(?:«/?B»\s*)*D\)', q_chunk)
        
        if not (m_a and m_b and m_c and m_d):
            continue
            
        q_statement = q_chunk[m_num.end():m_a.start()].strip()
        q_statement = re.sub(r'«/?B»', '', q_statement)
        q_statement = re.sub(r'\s+', ' ', q_statement)
        
        raw_a = q_chunk[m_a.start():m_b.start()]
        raw_b = q_chunk[m_b.start():m_c.start()]
        raw_c = q_chunk[m_c.start():m_d.start()]
        raw_d = q_chunk[m_d.start():]
        
        # In D, parse option text vs explanation
        d_clean_chunk = raw_d[m_d.end()-m_d.start():].strip()
        d_lines = [l.strip() for l in d_clean_chunk.splitlines() if l.strip()]
        
        opt_d_text = d_lines[0] if d_lines else ""
        explanation = " ".join(d_lines[1:]) if len(d_lines) > 1 else ""
        
        # Detect bold for correct answer
        correct_opt = None
        if '«B»' in raw_a:
            correct_opt = 'A'
        elif '«B»' in raw_b:
            correct_opt = 'B'
        elif '«B»' in raw_c:
            correct_opt = 'C'
        elif '«B»' in raw_d:
            correct_opt = 'D'
                
        def clean_opt(raw_opt, prefix):
            text = re.sub(r'^(?:«/?B»\s*)*' + prefix + r'\)?\s*', '', raw_opt.strip())
            text = re.sub(r'«/?B»', '', text)
            return re.sub(r'\s+', ' ', text).strip()
            
        opt_a = clean_opt(raw_a, 'A')
        opt_b = clean_opt(raw_b, 'B')
        opt_c = clean_opt(raw_c, 'C')
        opt_d = re.sub(r'«/?B»', '', opt_d_text).strip()
        explanation = re.sub(r'«/?B»', '', explanation).strip()
        
        questions.append({
            'q_num': q_num,
            'question': q_statement,
            'options': {
                'A': opt_a,
                'B': opt_b,
                'C': opt_c,
                'D': opt_d
            },
            'correct': correct_opt,
            'explanation': explanation
        })
        
    print(f"Subtopic {sub_num:02d}: {sub_title} -> {len(questions)}/{target_count} MCQs")
    total_parsed_mcqs += len(questions)
    parsed_subtopics.append({
        'id': sub_num,
        'title': sub_title,
        'target_mcqs': target_count,
        'quick_notes': quick_notes,
        'common_traps': common_traps,
        'deep_dive': deep_dive,
        'questions': questions
    })

print(f"\nTOTAL MCQs parsed: {total_parsed_mcqs} / 320")

with open(r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\subject_01_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_subtopics, f, indent=2, ensure_ascii=False)
