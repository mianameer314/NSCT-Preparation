import json
import re

with open(r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\subject_01_parsed.json', 'r', encoding='utf-8') as f:
    subtopics = json.load(f)

def format_quick_notes(text):
    if not text:
        return []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    items = []
    current_title = ""
    current_desc = []
    
    for l in lines:
        if ':' in l and len(l.split(':')[0]) < 40 and not l.startswith('http'):
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
    # Match Title: text pattern
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

def format_deep_dive(text):
    if not text:
        return ""
    # Clean up and add HTML structure
    text = text.strip()
    
    # Identify headings like "1. Title" or "2. Title"
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
            
            # Check for truth table in body
            if 'True' in body and 'False' in body and ('AND' in body or 'OR' in body):
                # Build HTML table for truth table
                table_html = """
                <div class="overflow-x-auto my-4">
                  <table class="w-full text-xs text-left border-collapse border border-slate-700 bg-slate-900 rounded-lg">
                    <thead>
                      <tr class="bg-slate-800 text-indigo-300 border-b border-slate-700">
                        <th class="p-2 border border-slate-700">A</th>
                        <th class="p-2 border border-slate-700">B</th>
                        <th class="p-2 border border-slate-700">A AND B</th>
                        <th class="p-2 border border-slate-700">A OR B</th>
                        <th class="p-2 border border-slate-700">A XOR B</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr class="border-b border-slate-800"><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td></tr>
                      <tr class="border-b border-slate-800"><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td></tr>
                      <tr class="border-b border-slate-800"><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td></tr>
                      <tr><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-emerald-400">True</td><td class="p-2 border border-slate-700 font-mono text-rose-400">False</td></tr>
                    </tbody>
                  </table>
                </div>
                """
                # remove raw truth table text from body
                body = re.sub(r'A\s+B\s+A AND B.*?(?=2\.|\Z)', '', body, flags=re.DOTALL)
                html_parts.append(f"<h4 class='deep-dive-heading'>{heading}</h4>{table_html}<p class='deep-dive-text'>{body}</p>")
            elif 'Phase' in body and 'Action Item' in body:
                # Build HTML table for 4 steps
                table_html = """
                <div class="overflow-x-auto my-4">
                  <table class="w-full text-xs text-left border-collapse border border-slate-700 bg-slate-900 rounded-lg">
                    <thead>
                      <tr class="bg-slate-800 text-indigo-300 border-b border-slate-700">
                        <th class="p-2.5 border border-slate-700 font-bold">Phase</th>
                        <th class="p-2.5 border border-slate-700 font-bold">Action Item</th>
                        <th class="p-2.5 border border-slate-700 font-bold">Concrete Example</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr class="border-b border-slate-800"><td class="p-2.5 border border-slate-700 font-bold text-indigo-400">1. Understand</td><td class="p-2.5 border border-slate-700">Identify constraints, inputs, outputs, and edge cases.</td><td class="p-2.5 border border-slate-700 text-slate-300">"The app needs to take two positive integers and return their sum."</td></tr>
                      <tr class="border-b border-slate-800"><td class="p-2.5 border border-slate-700 font-bold text-indigo-400">2. Plan</td><td class="p-2.5 border border-slate-700">Design architecture, draw flowcharts, or write pseudocode.</td><td class="p-2.5 border border-slate-700 text-slate-300">Writing: <code>sum = num1 + num2; print sum</code> on paper.</td></tr>
                      <tr class="border-b border-slate-800"><td class="p-2.5 border border-slate-700 font-bold text-indigo-400">3. Execute</td><td class="p-2.5 border border-slate-700">Translate the plan into a specific programming language.</td><td class="p-2.5 border border-slate-700 text-slate-300">Typing the code into an IDE and compiling.</td></tr>
                      <tr><td class="p-2.5 border border-slate-700 font-bold text-indigo-400">4. Verify</td><td class="p-2.5 border border-slate-700">Test edge cases, boundary values, and performance.</td><td class="p-2.5 border border-slate-700 text-slate-300">Passing inputs: <code>(0, 0)</code>, <code>(-5, 10)</code>, <code>(INT_MAX, 1)</code> to check overflow.</td></tr>
                    </tbody>
                  </table>
                </div>
                """
                html_parts.append(f"<h4 class='deep-dive-heading'>{heading}</h4>{table_html}")
            else:
                body_clean = re.sub(r'\n+', '</p><p class=\"deep-dive-text\">', body)
                html_parts.append(f"<h4 class='deep-dive-heading'>{heading}</h4><p class='deep-dive-text'>{body_clean}</p>")
        else:
            sec_clean = re.sub(r'\n+', '</p><p class=\"deep-dive-text\">', sec)
            html_parts.append(f"<p class='deep-dive-text'>{sec_clean}</p>")
            
    return "".join(html_parts)

enhanced_subtopics = []
for st in subtopics:
    qn_items = format_quick_notes(st['quick_notes'])
    trap_items = format_traps(st['common_traps'])
    dd_html = format_deep_dive(st['deep_dive'])
    
    enhanced_subtopics.append({
        **st,
        'formatted_quick_notes': qn_items,
        'formatted_traps': trap_items,
        'formatted_deep_dive': dd_html
    })

out_json = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\subject_01_enhanced.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(enhanced_subtopics, f, indent=2, ensure_ascii=False)

out_js = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\interactive-trainer\data.js'
with open(out_js, 'w', encoding='utf-8') as f:
    f.write('window.NSCT_SUBJECT_01 = ' + json.dumps(enhanced_subtopics, ensure_ascii=False) + ';')

print(f"Enhanced data generated successfully! Updated data.js")
