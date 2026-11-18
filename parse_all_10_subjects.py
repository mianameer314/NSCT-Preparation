import pypdf
import re
import json
import os
import sys

BASE_DIR = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation'

SUBJECTS_CONFIG = [
    {
        "id": 1,
        "code": "01",
        "title": "Problem Solving & Analytical Skills",
        "weight": 20,
        "icon": "🧩",
        "file": "NSCT_File_01_Problem_Solving.pdf"
    },
    {
        "id": 2,
        "code": "02",
        "title": "Programming (C++ / Java / Python)",
        "weight": 10,
        "icon": "💻",
        "file": "NSCT_File_02_Programming.pdf"
    },
    {
        "id": 3,
        "code": "03",
        "title": "Data Structures & Algorithms",
        "weight": 10,
        "icon": "⚡",
        "file": "NSCT_File_03_DSA.pdf"
    },
    {
        "id": 4,
        "code": "04",
        "title": "Databases (SQL & NoSQL)",
        "weight": 10,
        "icon": "🗄️",
        "file": "NSCT_File_04_Databases.pdf"
    },
    {
        "id": 5,
        "code": "05",
        "title": "Software Engineering & Architecture",
        "weight": 10,
        "icon": "📐",
        "file": "NSCT_File_05_Software-Engineering.pdf"
    },
    {
        "id": 6,
        "code": "06",
        "title": "Web Development (Frontend & Backend)",
        "weight": 10,
        "icon": "🌐",
        "file": "NSCT_File_06_Web-Development.pdf"
    },
    {
        "id": 7,
        "code": "07",
        "title": "Computer Networks & Cloud Computing",
        "weight": 10,
        "icon": "☁️",
        "file": "NSCT_File_07_Computer-Networks_&_Cloud-Computing.pdf"
    },
    {
        "id": 8,
        "code": "08",
        "title": "AI / ML & Data Analytics",
        "weight": 10,
        "icon": "🤖",
        "file": "NSCT_File_08_Ai-Ml-Learning_&_Data-Analytics.pdf"
    },
    {
        "id": 9,
        "code": "09",
        "title": "Operating Systems",
        "weight": 5,
        "icon": "⚙️",
        "file": "NSCT_File_09_Operating-Systems.pdf"
    },
    {
        "id": 10,
        "code": "10",
        "title": "Cyber Security & Information Assurance",
        "weight": 5,
        "icon": "🛡️",
        "file": "NSCT_File_10_Cyber-Security.pdf"
    }
]

def format_quick_notes(text):
    if not text:
        return []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    items = []
    current_title = ""
    current_desc = []
    for l in lines:
        if ':' in l and len(l.split(':')[0]) < 45 and not l.startswith('http'):
            if current_title:
                items.append({'title': current_title, 'desc': ' '.join(current_desc)})
            parts = l.split(':', 1)
            current_title = parts[0].strip()
            current_desc = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
        else:
            if current_title:
                current_desc.append(l)
            else:
                items.append({'title': 'Key Concept', 'desc': l})
    if current_title:
        items.append({'title': current_title, 'desc': ' '.join(current_desc)})
    return items

def format_traps(text):
    if not text:
        return []
    items = []
    trap_blocks = re.split(r'\n(?=[A-Z][a-zA-Z\s/&-]+:\s*)', text)
    for tb in trap_blocks:
        tb = tb.strip()
        if not tb:
            continue
        if ':' in tb:
            parts = tb.split(':', 1)
            title = parts[0].strip()
            body = re.sub(r'\s+', ' ', parts[1]).strip()
            items.append({'title': title, 'explanation': body})
        else:
            items.append({'title': 'Trap to Avoid', 'explanation': re.sub(r'\s+', ' ', tb)})
    return items

def format_deep_dive_html(text):
    if not text:
        return ""
    text = text.strip()
    sections = re.split(r'\n(?=\d+\.\s+[A-Z])', text)
    html_parts = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        m_head = re.match(r'^(\d+\.\s+[^\n]+)', sec)
        if m_head:
            heading = m_head.group(1).strip()
            body = sec[len(heading):].strip()
            body_clean = re.sub(r'\n+', '</p><p class="deep-dive-text">', body)
            html_parts.append(f"<h4 class='deep-dive-heading'>{heading}</h4><p class='deep-dive-text'>{body_clean}</p>")
        else:
            sec_clean = re.sub(r'\n+', '</p><p class="deep-dive-text">', sec)
            html_parts.append(f"<p class='deep-dive-text'>{sec_clean}</p>")
    return "".join(html_parts)

def parse_subject_pdf(cfg):
    pdf_path = os.path.join(BASE_DIR, cfg['file'])
    print(f"\n==========================================")
    print(f"Parsing Subject {cfg['code']}: {cfg['title']} ({cfg['file']})...")
    reader = pypdf.PdfReader(pdf_path)
    
    pages_text = []
    for p_no in range(len(reader.pages)):
        spans = []
        def visitor(text, cm, tm, fontDict, fontSize):
            if text:
                bf = str(fontDict.get('/BaseFont', '')) if fontDict else ''
                spans.append((text, 'Bold' in bf or 'bold' in bf))
        reader.pages[p_no].extract_text(visitor_text=visitor)
        merged = ''
        for t, b in spans:
            if b:
                merged += f'«B»{t}«/B»'
            else:
                merged += t
        pages_text.append(merged)
        
    full_text = '\n'.join(pages_text)
    full_text = re.sub(r'•', ' ', full_text)
    
    # Locate all subtopic headers
    # Match Subtopic XX or Topic XX
    # We ignore the table of contents by checking that subtopics have body content
    matches = list(re.finditer(r'(?:«/?B»\s*)*(?:Subtopic|Topic)\s+(\d+):\s*([^\n\(]+)(?:\s*\((\d+)\s*MCQs\))?', full_text))
    
    # Filter matches to only real section headers (not TOC items)
    # A real section header is followed closely by Quick Notes or MCQs or Q1.
    valid_subtopics = []
    for idx, m in enumerate(matches):
        start = m.start()
        peek_window = full_text[start:start+1200]
        if 'Quick Notes' in peek_window or 'MCQs' in peek_window or 'Q1.' in peek_window or 'Q01.' in peek_window:
            valid_subtopics.append(m)
            
    print(f"Found {len(valid_subtopics)} valid subtopic sections in {cfg['title']}.")
    
    parsed_subtopics = []
    total_mcqs = 0
    
    for i, sm in enumerate(valid_subtopics):
        sub_num = int(sm.group(1))
        sub_title = sm.group(2).strip()
        target_count = int(sm.group(3)) if sm.group(3) else 0
        
        start_pos = sm.start()
        end_pos = valid_subtopics[i+1].start() if i+1 < len(valid_subtopics) else len(full_text)
        sub_block = full_text[start_pos:end_pos]
        
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
            
        # Parse MCQs
        first_q = re.search(r'(?:«/?B»\s*)*Q\d+\.', sub_block)
        questions = []
        if first_q:
            mcq_end = m_dd.start() if m_dd else (m_res.start() if m_res else len(sub_block))
            mcq_text = sub_block[first_q.start():mcq_end].strip()
            
            q_starts = [m.start() for m in re.finditer(r'(?:«/?B»\s*)*Q\d+\.', mcq_text)]
            q_starts.append(len(mcq_text))
            
            for q_idx in range(len(q_starts)-1):
                q_chunk = mcq_text[q_starts[q_idx]:q_starts[q_idx+1]].strip()
                m_num = re.search(r'Q(\d+)\.', q_chunk)
                if not m_num:
                    continue
                q_num = int(m_num.group(1))
                
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
                
                d_clean_chunk = raw_d[m_d.end()-m_d.start():].strip()
                d_lines = [l.strip() for l in d_clean_chunk.splitlines() if l.strip()]
                opt_d_text = d_lines[0] if d_lines else ""
                explanation = " ".join(d_lines[1:]) if len(d_lines) > 1 else ""
                
                correct_opt = 'A'
                if '«B»' in raw_a:
                    correct_opt = 'A'
                elif '«B»' in raw_b:
                    correct_opt = 'B'
                elif '«B»' in raw_c:
                    correct_opt = 'C'
                elif '«B»' in raw_d:
                    correct_opt = 'D'
                else:
                    # fallback if bold wasn't caught
                    correct_opt = 'A'
                    
                def clean_opt(raw_opt, prefix):
                    t = re.sub(r'^(?:«/?B»\s*)*' + prefix + r'\)?\s*', '', raw_opt.strip())
                    t = re.sub(r'«/?B»', '', t)
                    return re.sub(r'\s+', ' ', t).strip()
                    
                opt_a = clean_opt(raw_a, 'A')
                opt_b = clean_opt(raw_b, 'B')
                opt_c = clean_opt(raw_c, 'C')
                opt_d = re.sub(r'«/?B»', '', opt_d_text).strip()
                opt_d = re.sub(r'\s+', ' ', opt_d)
                explanation = re.sub(r'«/?B»', '', explanation).strip()
                explanation = re.sub(r'\s+', ' ', explanation)
                
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
                
        total_mcqs += len(questions)
        parsed_subtopics.append({
            'id': sub_num,
            'title': sub_title,
            'target_mcqs': target_count,
            'quick_notes': quick_notes,
            'common_traps': common_traps,
            'deep_dive': deep_dive,
            'formatted_quick_notes': format_quick_notes(quick_notes),
            'formatted_traps': format_traps(common_traps),
            'formatted_deep_dive': format_deep_dive_html(deep_dive),
            'questions': questions
        })
        print(f"  Subtopic {sub_num:02d}: {sub_title} -> {len(questions)} MCQs")
        
    print(f"Total MCQs parsed for Subject {cfg['code']}: {total_mcqs}")
    return {
        **cfg,
        'total_mcqs': total_mcqs,
        'subtopics': parsed_subtopics
    }

def main():
    all_subjects = []
    grand_total_mcqs = 0
    
    # Load Subject 01 with our handcrafted deep dives if available
    for cfg in SUBJECTS_CONFIG:
        subj_data = parse_subject_pdf(cfg)
        
        # If subject 01, attach the curated enhanced deep dives we already perfected
        if cfg['id'] == 1 and os.path.exists(os.path.join(BASE_DIR, 'subject_01_enhanced.json')):
            try:
                with open(os.path.join(BASE_DIR, 'subject_01_enhanced.json'), 'r', encoding='utf-8') as f:
                    s1_enhanced = json.load(f)
                # merge enhanced deep dives
                dd_map = {st['id']: st.get('formatted_deep_dive') for st in s1_enhanced}
                for st in subj_data['subtopics']:
                    if st['id'] in dd_map and dd_map[st['id']]:
                        st['formatted_deep_dive'] = dd_map[st['id']]
            except Exception as e:
                print("Could not merge s1 enhanced:", e)
                
        all_subjects.append(subj_data)
        grand_total_mcqs += subj_data['total_mcqs']
        
    print(f"\n==========================================")
    print(f"ALL 10 SUBJECTS PARSED SUCCESSFULLY!")
    print(f"Grand Total MCQs across all 10 subjects: {grand_total_mcqs}")
    print(f"==========================================\n")
    
    # Save combined database JSON
    out_json = os.path.join(BASE_DIR, 'nsct_all_subjects.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(all_subjects, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_json} ({os.path.getsize(out_json) / 1024 / 1024:.2f} MB)")
    
    # Write to data.js for trainer and root
    js_content = 'window.NSCT_ALL_SUBJECTS = ' + json.dumps(all_subjects, ensure_ascii=False) + ';\n'
    # Also set legacy window.NSCT_SUBJECT_01 for backwards compatibility
    s1_subtopics = all_subjects[0]['subtopics']
    js_content += 'window.NSCT_SUBJECT_01 = ' + json.dumps(s1_subtopics, ensure_ascii=False) + ';\n'
    
    for dest in [os.path.join(BASE_DIR, 'data.js'), os.path.join(BASE_DIR, 'interactive-trainer', 'data.js')]:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"Wrote {dest} ({os.path.getsize(dest) / 1024 / 1024:.2f} MB)")

if __name__ == '__main__':
    main()
