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
            items.append({'title': 'Common Trap', 'explanation': re.sub(r'\s+', ' ', tb)})
    return items

# Curated High-Yield Deep Dive Content formatted with Neumorphic Tables & Callouts
DEEP_DIVES = {
    1: """
    <p class='deep-dive-text'>Problem-solving is the foundational skill required for all IT and software engineering roles. It is language-agnostic, meaning a skilled problem-solver can easily adapt to Python, Java, or C++ once the underlying logic is built.</p>
    
    <h4 class='deep-dive-heading'>1. The Structured 4-Step Approach</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Phase</th>
            <th>Core Objective</th>
            <th>Concrete Example</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1. Understand</strong></td>
            <td>Identify constraints, valid inputs, expected outputs, and edge cases.</td>
            <td><em>"The app takes two positive integers and returns their sum without overflowing."</em></td>
          </tr>
          <tr>
            <td><strong>2. Plan</strong></td>
            <td>Design architecture, draw flowcharts, or write pseudocode.</td>
            <td><em>Writing: <code>sum = num1 + num2; print sum</code> on paper first.</em></td>
          </tr>
          <tr>
            <td><strong>3. Execute</strong></td>
            <td>Translate the plan into syntax of the chosen language.</td>
            <td><em>Typing code into IDE, compiling, and configuring dependencies.</em></td>
          </tr>
          <tr>
            <td><strong>4. Verify</strong></td>
            <td>Test against normal inputs, boundary cases, and bad data.</td>
            <td><em>Passing inputs: <code>(0, 0)</code>, <code>(-5, 10)</code>, and <code>(INT_MAX, 1)</code> to check error handling.</em></td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Computational Thinking Approaches</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card">
        <div class="neu-mini-title">Top-Down vs. Bottom-Up Design</div>
        <p class="deep-dive-text"><strong>Top-Down:</strong> Start with the macro goal (e.g., <em>"Build E-Commerce Platform"</em>) and subdivide into modules (<em>Auth, Cart, Payment</em>).<br>
        <strong>Bottom-Up:</strong> Construct standalone foundational functions first (e.g., <code>connectDB()</code>, <code>validateEmail()</code>), then integrate them into the larger system.</p>
      </div>
      <div class="neu-mini-card">
        <div class="neu-mini-title">Brute Force vs. Heuristics</div>
        <p class="deep-dive-text"><strong>Brute Force:</strong> Exhaustively explores all possible paths. Guarantees finding the global optimum, but runs in exponential time on large datasets.<br>
        <strong>Heuristic:</strong> Uses practical rules of thumb (e.g. A* search heuristic) to reach a good-enough solution rapidly when exact computation is impractical.</p>
      </div>
    </div>
    """,

    2: """
    <p class='deep-dive-text'>Problem understanding bridges business requirements and software implementation. If requirements are misunderstood, you will build the wrong product—regardless of how elegant the code is.</p>

    <h4 class='deep-dive-heading'>1. The Four Pillars of a Well-Defined Problem</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card"><strong>Inputs:</strong> Data formats, data types, protocols (e.g. JSON payloads, CSV streams).</div>
      <div class="neu-mini-card"><strong>Outputs:</strong> Concrete return types, HTTP codes, files, DB schema changes.</div>
      <div class="neu-mini-card"><strong>Constraints:</strong> Hard limits like memory &lt; 256MB, response time &lt; 100ms, budget.</div>
      <div class="neu-mini-card"><strong>Edge Cases:</strong> Null values, extreme values (e.g. -1, INT_MAX), disconnections.</div>
    </div>

    <h4 class='deep-dive-heading'>2. Root Cause Analysis (RCA) Frameworks</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Framework</th>
            <th>How It Works</th>
            <th>Best Applied When</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>The 5 Whys</strong></td>
            <td>Ask <em>"Why?"</em> sequentially until uncovering the systemic human or architectural gap.</td>
            <td>Linear bug regressions, isolated component crashes.</td>
          </tr>
          <tr>
            <td><strong>Fishbone (Ishikawa)</strong></td>
            <td>Categorizes potential failure causes across People, Process, Technology, and Environment.</td>
            <td>Complex distributed outages with multiple concurrent failure modes.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>3. Functional vs. Non-Functional Requirements</h4>
    <p class='deep-dive-text'><strong>Functional:</strong> Specifies <em>what</em> the system does (e.g. <em>"Users can reset their password via SMS"</em>).<br>
    <strong>Non-Functional:</strong> Specifies <em>how well</em> the system behaves (e.g. <em>"SMS OTP must arrive within 5 seconds with 99.99% availability"</em>).</p>
    """,

    3: """
    <p class='deep-dive-text'>Boolean logic and discrete math govern all computer architecture and conditional execution. Mastering truth tables and De Morgan's laws prevents insidious runtime bugs.</p>

    <h4 class='deep-dive-heading'>1. Master Boolean Truth Table</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Input A</th>
            <th>Input B</th>
            <th>A AND B</th>
            <th>A OR B</th>
            <th>A XOR B</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>False</td><td>False</td><td><span class="badge-tag tag-false">False</span></td><td><span class="badge-tag tag-false">False</span></td><td><span class="badge-tag tag-false">False</span></td></tr>
          <tr><td>False</td><td>True</td><td><span class="badge-tag tag-false">False</span></td><td><span class="badge-tag tag-true">True</span></td><td><span class="badge-tag tag-true">True</span></td></tr>
          <tr><td>True</td><td>False</td><td><span class="badge-tag tag-false">False</span></td><td><span class="badge-tag tag-true">True</span></td><td><span class="badge-tag tag-true">True</span></td></tr>
          <tr><td>True</td><td>True</td><td><span class="badge-tag tag-true">True</span></td><td><span class="badge-tag tag-true">True</span></td><td><span class="badge-tag tag-false">False</span></td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. De Morgan's Laws for Code Simplification</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card">
        <strong>Rule 1:</strong> <code>!(A && B) &equiv; (!A || !B)</code><br>
        <em>"Not both" means at least one must be false.</em>
      </div>
      <div class="neu-mini-card">
        <strong>Rule 2:</strong> <code>!(A || B) &equiv; (!A && !B)</code><br>
        <em>"Neither" means both must be false.</em>
      </div>
    </div>

    <h4 class='deep-dive-heading'>3. Short-Circuit Evaluation Guard Pattern</h4>
    <p class='deep-dive-text'>Modern engines abort evaluating logical chains as soon as the result is determined:<br>
    <code>if (user != null && user.isAuthenticated())</code> &mdash; Prevents Null Pointer Exceptions because if <code>user == null</code>, the right side never executes.</p>
    """,

    4: """
    <p class='deep-dive-text'>Algorithms and control flow specify execution order and decision trees within software.</p>

    <h4 class='deep-dive-heading'>1. The Three Pillars of Structured Programming</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Structure</th>
            <th>Execution Semantic</th>
            <th>Core Keywords</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Sequence</strong></td><td>Linear statement execution from top to bottom.</td><td><code>let</code>, <code>=</code>, assignment</td></tr>
          <tr><td><strong>Selection</strong></td><td>Branching based on boolean condition evaluations.</td><td><code>if</code>, <code>else if</code>, <code>switch</code></td></tr>
          <tr><td><strong>Iteration</strong></td><td>Repeated execution while a condition holds true.</td><td><code>for</code>, <code>while</code>, <code>do-while</code></td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Flowchart Reference Standards</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Geometric Symbol</th>
            <th>Programmatic Meaning</th>
            <th>Typical Example</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Oval / Pill</strong></td><td>Start or End terminator</td><td>Begin Program / Return Exit Code</td></tr>
          <tr><td><strong>Parallelogram</strong></td><td>Input or Output operation</td><td>Read User Input, Print Result</td></tr>
          <tr><td><strong>Rectangle</strong></td><td>Internal computational process</td><td><code>total = total + tax;</code></td></tr>
          <tr><td><strong>Diamond</strong></td><td>Conditional decision branch</td><td><code>Is balance &ge; price?</code> (Yes/No)</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>3. Definite vs. Indefinite Iteration</h4>
    <p class='deep-dive-text'><strong>FOR Loops:</strong> Definite iteration used when total iteration count is predetermined (e.g. iterating over 50 items).<br>
    <strong>WHILE Loops:</strong> Indefinite iteration used when loop count depends on a dynamic runtime sentinel condition (e.g. reading until EOF or user quit).</p>
    """,

    5: """
    <p class='deep-dive-text'>Hardware processes only binary states (0 and 1). All high-level types&mdash;integers, floats, strings, and trees&mdash;are abstract layers of conventions.</p>

    <h4 class='deep-dive-heading'>1. Signed Integer Overflow (Two's Complement)</h4>
    <p class='deep-dive-text'>In an 8-bit signed integer (range -128 to +127), binary <code>01111111</code> is 127. Adding 1 yields <code>10000000</code>, where the most significant bit is negative, wrapping unexpectedly to <strong>-128</strong>! This caused the famous Ariane 5 disaster when converting 64-bit float to 16-bit signed integer.</p>

    <h4 class='deep-dive-heading'>2. Why 0.1 + 0.2 != 0.3 in IEEE-754 Floats</h4>
    <p class='deep-dive-text'>Base-10 decimals like 0.1 and 0.2 cannot be represented as finite terminating binary fractions (just as 1/3 cannot be represented as a finite base-10 decimal). IEEE-754 stores 53 bits of precision, causing tiny rounding accumulation: <code>0.30000000000000004</code>.</p>

    <h4 class='deep-dive-heading'>3. Abstract Data Type (ADT) vs. Concrete Implementation</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>ADT (Behavior Contract)</th>
            <th>Operational Guarantee</th>
            <th>Concrete Implementations</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>List</strong></td><td>Ordered elements with positional index</td><td>Dynamic Array, Singly/Doubly Linked List</td></tr>
          <tr><td><strong>Queue</strong></td><td>FIFO (First-In, First-Out)</td><td>Circular Array, Linked List with Tail Pointer</td></tr>
          <tr><td><strong>Stack</strong></td><td>LIFO (Last-In, First-Out)</td><td>Dynamic Array, Linked List Head Pointer</td></tr>
          <tr><td><strong>Map / Dictionary</strong></td><td>Key &rarr; Value retrieval</td><td>Hash Table (O(1)), Red-Black Tree (O(log N))</td></tr>
        </tbody>
      </table>
    </div>
    """,

    6: """
    <p class='deep-dive-text'>Pattern recognition allows software engineers to generalize solutions. Instead of writing bespoke code for 100 individual cases, you craft a single parameterized abstraction.</p>

    <h4 class='deep-dive-heading'>1. Regular Expressions (Regex) Quick Reference</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Token</th>
            <th>Meaning</th>
            <th>Application</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><code>^ / $</code></td><td>Anchors to beginning / end of string</td><td>Strict full-string format validation</td></tr>
          <tr><td><code>\\d+</code></td><td>One or more numeric digits</td><td>Extracting numerical IDs or prices</td></tr>
          <tr><td><code>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}</code></td><td>Email standard matcher</td><td>Sanitizing web form registrations</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Inductive vs. Deductive Reasoning</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Reasoning Mode</th>
            <th>Flow Direction</th>
            <th>Software Engineering Analogy</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Inductive</strong></td><td>Specific Observations &rarr; General Rule</td><td>Observing 5 memory spikes during CSV uploads &rarr; Inferring that CSV parser lacks streaming.</td></tr>
          <tr><td><strong>Deductive</strong></td><td>General Axiom &rarr; Specific Certainty</td><td>Rule: All endpoints require JWT auth. Fact: Endpoint /v1/reports lacks JWT. Deduction: Request is denied.</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>3. Object-Oriented Polymorphism as Generalization</h4>
    <p class='deep-dive-text'>Instead of writing distinct <code>processVisaPayment()</code>, <code>processMastercard()</code>, and <code>processPaypal()</code> methods with massive switch statements, declare a unified <code>PaymentProcessor</code> interface with a generic <code>pay(amount)</code> contract.</p>
    """,

    7: """
    <p class='deep-dive-text'>Discrete mathematics, combinatorics, modular arithmetic, and probability form the bedrock of cryptography, computer graphics, and distributed consensus.</p>

    <h4 class='deep-dive-heading'>1. Real-World Applications of Modular Arithmetic</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card"><strong>Cryptography (RSA):</strong> Uses modular exponentiation on massive primes to create trapdoor one-way mathematical functions.</div>
      <div class="neu-mini-card"><strong>Hash Tables:</strong> Maps potentially infinite key hash codes into fixed bucket array indices using <code>index = hash % capacity</code>.</div>
      <div class="neu-mini-card"><strong>Circular Buffers:</strong> Wraps pointers seamlessly without conditional branches using <code>ptr = (ptr + 1) % size</code>.</div>
    </div>

    <h4 class='deep-dive-heading'>2. Practical Statistics for IT Graduates</h4>
    <p class='deep-dive-text'><strong>Mean vs. Percentiles (P95/P99):</strong> Arithmetic mean hides critical outliers. If 99 requests take 10ms and 1 takes 5,000ms, the mean is ~60ms (looks acceptable), but P99 is 5,000ms (unacceptable SLA breach)!<br>
    <strong>Standard Deviation:</strong> Quantifies jitter and system stability.</p>

    <h4 class='deep-dive-heading'>3. Combinatorics & Cryptographic Entropy</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Concept</th>
            <th>Formula</th>
            <th>Security / IT Application</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Permutations</strong></td><td><code>P(n, r) = n! / (n - r)!</code></td><td>Calculating brute-force password search space when order matters.</td></tr>
          <tr><td><strong>Combinations</strong></td><td><code>C(n, r) = n! / [r!(n - r)!]</code></td><td>Quorum election of 3 out of 5 cluster nodes.</td></tr>
          <tr><td><strong>Availability</strong></td><td><code>1 - &Pi;(1 - A_i)</code></td><td>Calculating total uptime of redundant servers in parallel.</td></tr>
        </tbody>
      </table>
    </div>
    """,

    8: """
    <p class='deep-dive-text'>Algorithmic thinking is evaluating efficiency before coding. It transitions a software developer from "Does it work?" to "How will it scale when traffic increases by 10,000x?"</p>

    <h4 class='deep-dive-heading'>1. Canonical Sorting Hierarchy</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Algorithm</th>
            <th>Best Time</th>
            <th>Average Time</th>
            <th>Worst Time</th>
            <th>Space Complexity</th>
            <th>Best Use Case</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Quick Sort</strong></td><td>O(N log N)</td><td>O(N log N)</td><td>O(N&sup2;)</td><td>O(log N)</td><td>In-place, cache-friendly general sorting.</td></tr>
          <tr><td><strong>Merge Sort</strong></td><td>O(N log N)</td><td>O(N log N)</td><td>O(N log N)</td><td>O(N)</td><td>Guaranteed stability, external sorting on disk.</td></tr>
          <tr><td><strong>Insertion Sort</strong></td><td>O(N)</td><td>O(N&sup2;)</td><td>O(N&sup2;)</td><td>O(1)</td><td>Nearly-sorted streams or tiny arrays (N &le; 16).</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Recursion vs. Dynamic Programming (DP)</h4>
    <p class='deep-dive-text'><strong>Divide & Conquer:</strong> Splits problems into non-overlapping subproblems (e.g. Merge Sort).<br>
    <strong>Dynamic Programming:</strong> Solves problems with <em>Overlapping Subproblems</em> and <em>Optimal Substructure</em> by memoizing previously computed results (e.g. Knapsack, Shortest Path).</p>

    <h4 class='deep-dive-heading'>3. Master Big-O Growth Hierarchy</h4>
    <p class='deep-dive-text'><code>O(1) &lt; O(log N) &lt; O(N) &lt; O(N log N) &lt; O(N&sup2;) &lt; O(2^N) &lt; O(N!)</code></p>
    """,

    9: """
    <p class='deep-dive-text'>Architectural decisions require balancing opposing trade-offs, engineering constraints, and human biases.</p>

    <h4 class='deep-dive-heading'>1. The CAP Theorem in Distributed Systems</h4>
    <p class='deep-dive-text'>A distributed system can guarantee at most <strong>two</strong> out of three properties simultaneously:</p>
    <div class="neu-card-grid">
      <div class="neu-mini-card"><strong>Consistency (C):</strong> Every read gets the most recent write or an error.</div>
      <div class="neu-mini-card"><strong>Availability (A):</strong> Every non-failing node returns a response, without guarantee of freshest data.</div>
      <div class="neu-mini-card"><strong>Partition Tolerance (P):</strong> System operates despite network packet loss. <em>(Mandatory in real networks).</em></div>
    </div>
    <p class='deep-dive-text' style='margin-top:10px;'>Because real-world networks experience partitions, engineering systems must choose between <strong>CP</strong> (Consensus, Banking) and <strong>AP</strong> (Eventual Consistency, Social Feeds).</p>

    <h4 class='deep-dive-heading'>2. Combating Cognitive Biases in Tech</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Cognitive Bias</th>
            <th>Common Developer Rationalization</th>
            <th>Remediation Strategy</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>IKEA Effect</strong></td><td><em>"We built our own custom ORM, so it must be better than Hibernate."</em></td><td>Perform objective latency and vulnerability benchmarks against industry standards.</td></tr>
          <tr><td><strong>Status Quo Bias</strong></td><td><em>"It has run on PHP 5.6 for 8 years without breaking, so don't upgrade."</em></td><td>Enforce automated security audit pipelines highlighting unpatched vulnerabilities.</td></tr>
          <tr><td><strong>Anchoring Bias</strong></td><td><em>"The initial guess was 2 days, so all higher estimates are rejected."</em></td><td>Implement Planning Poker with blind multi-point estimation.</td></tr>
        </tbody>
      </table>
    </div>
    """,

    10: """
    <p class='deep-dive-text'>Debugging is the scientific method applied to malfunctioning software: formulate a hypothesis, construct a minimal reproduction test, observe logs, and verify the patch.</p>

    <h4 class='deep-dive-heading'>1. The Three Primary Defect Categories</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Bug Class</th>
            <th>Detection Mechanism</th>
            <th>Primary Prevention Control</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Syntax</strong></td><td>Compiler / Linter throws error immediately before execution.</td><td>Static analysis, IDE syntax highlighting.</td></tr>
          <tr><td><strong>Runtime</strong></td><td>Program terminates abnormally on edge inputs (e.g. division by zero).</td><td>Defensive assertions, boundary checks, try/catch.</td></tr>
          <tr><td><strong>Logical</strong></td><td>Code compiles and runs, but produces incorrect outputs.</td><td>Automated unit tests, code reviews, property-based tests.</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Professional Logging Hierarchy</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Level</th>
            <th>Usage Context</th>
            <th>Production Destination</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><code>DEBUG</code></td><td>Step-by-step local tracing, variable states.</td><td>Disabled in production to protect disk I/O.</td></tr>
          <tr><td><code>INFO</code></td><td>High-level business transactions (e.g. order placed).</td><td>Indexed in ELK / Datadog.</td></tr>
          <tr><td><code>WARN</code></td><td>Recoverable anomalies (e.g. retry 2/3 on payment).</td><td>Aggregated for performance trends.</td></tr>
          <tr><td><code>ERROR</code></td><td>Operation failed (e.g. database connection dropped).</td><td>Triggers team alert notifications.</td></tr>
          <tr><td><code>FATAL</code></td><td>System unrecoverable; process terminating.</td><td>Pagers / immediate on-call incident paging.</td></tr>
        </tbody>
      </table>
    </div>
    """,

    11: """
    <p class='deep-dive-text'>Algorithmic efficiency determines server scalability and cloud operating costs. An O(N&sup2;) algorithm can cost 100x more to host than an O(N log N) alternative.</p>

    <h4 class='deep-dive-heading'>1. Asymptotic Complexity Reference</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Big-O</th>
            <th>Name</th>
            <th>Operations for N=100</th>
            <th>Real-World Example</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><code>O(1)</code></td><td>Constant</td><td>1</td><td>Array index lookup, Hash table lookup</td></tr>
          <tr><td><code>O(log N)</code></td><td>Logarithmic</td><td>~7</td><td>Binary Search in sorted array</td></tr>
          <tr><td><code>O(N)</code></td><td>Linear</td><td>100</td><td>Single loop traversal through array</td></tr>
          <tr><td><code>O(N log N)</code></td><td>Linearithmic</td><td>~664</td><td>Efficient divide-and-conquer sorting (Merge Sort)</td></tr>
          <tr><td><code>O(N&sup2;)</code></td><td>Quadratic</td><td>10,000</td><td>Nested loops, naive bubble sort</td></tr>
          <tr><td><code>O(2^N)</code></td><td>Exponential</td><td>1.26 &times; 10&sup3;&sup0;</td><td>Naive recursive Fibonacci, Power Set</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Space-Time Trade-off Decisions</h4>
    <p class='deep-dive-text'>When solving problems, engineers trade RAM for CPU cycles:<br>
    <strong>Memory-Saver:</strong> Nested loops to detect duplicates &rarr; <code>Time: O(N&sup2;), Space: O(1)</code>.<br>
    <strong>Speed-Saver:</strong> Hash Set lookup for duplicates &rarr; <code>Time: O(N), Space: O(N)</code>.</p>
    """,

    12: """
    <p class='deep-dive-text'>Writing maintainable code requires applying proven architectural design principles to ensure scalability and ease of refactoring.</p>

    <h4 class='deep-dive-heading'>1. The Core Software Design Principles</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Principle</th>
            <th>Acronym Meaning</th>
            <th>Engineering Benefit</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>DRY</strong></td><td>Don't Repeat Yourself</td><td>Centralize business logic into reusable single sources of truth.</td></tr>
          <tr><td><strong>KISS</strong></td><td>Keep It Simple, Stupid</td><td>Avoid speculative over-engineering; choose the simplest working pattern.</td></tr>
          <tr><td><strong>YAGNI</strong></td><td>You Aren't Gonna Need It</td><td>Do not implement speculative features until there is a verified need.</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Cohesion vs. Coupling</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card">
        <strong>High Cohesion (Goal):</strong> A module focuses exclusively on a single well-defined responsibility (e.g. an <code>AuthenticationService</code> handles only token verification).
      </div>
      <div class="neu-mini-card">
        <strong>Low Coupling (Goal):</strong> Modules interact through minimal abstract interfaces, allowing internal DB changes without impacting the presentation layer.
      </div>
    </div>
    """,

    13: """
    <p class='deep-dive-text'>Data-driven decision making replaces subjective intuition with verifiable empirical metrics.</p>

    <h4 class='deep-dive-heading'>1. The Clean Data Quality Checklist</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card"><strong>Completeness:</strong> No unexpected nulls or missing fields across key dimensions.</div>
      <div class="neu-mini-card"><strong>Consistency:</strong> Uniform datetime standards (ISO 8601 UTC) and unit measurements.</div>
      <div class="neu-mini-card"><strong>Accuracy:</strong> No physically impossible values (e.g. user age = 300 years).</div>
      <div class="neu-mini-card"><strong>Freshness:</strong> Metrics reflect real-time telemetry rather than stale caches.</div>
    </div>

    <h4 class='deep-dive-heading'>2. Operational Telemetry Metrics</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Metric</th>
            <th>Definition</th>
            <th>Primary Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Throughput (RPS)</strong></td><td>Requests served per second</td><td>Measures maximum concurrency capacity.</td></tr>
          <tr><td><strong>P99 Latency</strong></td><td>Maximum time taken by fastest 99% of requests</td><td>Catches tail latency regressions affecting power users.</td></tr>
          <tr><td><strong>Error Budget</strong></td><td>Allowed percentage of 5xx server errors</td><td>Determines whether to ship new features or freeze for stability.</td></tr>
        </tbody>
      </table>
    </div>
    """,

    14: """
    <p class='deep-dive-text'>Innovation in technology often stems from reframing problems or reasoning from fundamental physical truths rather than by analogy.</p>

    <h4 class='deep-dive-heading'>1. Reasoning by First Principles</h4>
    <p class='deep-dive-text'>Rather than accepting conventional industry wisdom (<em>"Enterprise cloud hosting costs $50,000/month because everyone pays that"</em>), first-principles thinking breaks down the problem to raw costs: CPU hours, gigabytes of RAM, and actual bandwidth, identifying 10x cost reductions.</p>

    <h4 class='deep-dive-heading'>2. The Problem Reframing Matrix</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card"><strong>The User Frame:</strong> How does this bottleneck physically feel to someone on a slow 3G network?</div>
      <div class="neu-mini-card"><strong>The Financial Frame:</strong> Does rewriting this query save enough cloud server instances to justify 2 weeks of engineering time?</div>
      <div class="neu-mini-card"><strong>The Inversion Frame:</strong> What would happen if we did the exact opposite of our current architecture?</div>
    </div>
    """,

    15: """
    <p class='deep-dive-text'>Real-world software engineering is managing trade-offs under constraints of time, staffing, hardware limits, and changing market conditions.</p>

    <h4 class='deep-dive-heading'>1. The Iron Triangle of Project Management</h4>
    <p class='deep-dive-text'>You can optimize at most <strong>two</strong>: <strong>Speed, Cost, and Scope/Quality</strong>.<br>
    &bull; Fast &amp; Cheap &rarr; Low quality / High technical debt.<br>
    &bull; High Quality &amp; Fast &rarr; Expensive (requires senior headcount).<br>
    &bull; High Quality &amp; Cheap &rarr; Slow delivery schedule.</p>

    <h4 class='deep-dive-heading'>2. Vertical vs. Horizontal Scaling</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Dimension</th>
            <th>Vertical Scaling (Scale-Up)</th>
            <th>Horizontal Scaling (Scale-Out)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>Method</strong></td><td>Upgrade CPU/RAM on existing single server.</td><td>Add more commodity nodes behind a load balancer.</td></tr>
          <tr><td><strong>Downtime</strong></td><td>Usually requires scheduled maintenance reboot.</td><td>Zero downtime; rolling container updates.</td></tr>
          <tr><td><strong>Cost Curve</strong></td><td>Exponentially expensive at high tiers.</td><td>Linear cost scaling with commodity hardware.</td></tr>
          <tr><td><strong>Ceiling</strong></td><td>Physical limit of hardware motherboard.</td><td>Virtually limitless distributed scalability.</td></tr>
        </tbody>
      </table>
    </div>
    """,

    16: """
    <p class='deep-dive-text'>In modern software development, code without documentation is technical debt. Clear communication ensures solutions remain maintainable when team members change.</p>

    <h4 class='deep-dive-heading'>1. The Three Tiers of Technical Documentation</h4>
    <div class="neu-table-wrap">
      <table class="neu-table">
        <thead>
          <tr>
            <th>Tier</th>
            <th>Target Audience</th>
            <th>Artifacts Produced</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>User Level</strong></td><td>End users and non-technical staff</td><td>Quick Start Guides, FAQs, UI tooltips, Release Notes</td></tr>
          <tr><td><strong>System Level</strong></td><td>Engineers, DevOps, and Architects</td><td>README.md, Architecture Decision Records (ADR), OpenAPI / Swagger specs</td></tr>
          <tr><td><strong>Code Level</strong></td><td>Developers reading individual files</td><td>Docstrings, inline explanations for non-obvious algorithms</td></tr>
        </tbody>
      </table>
    </div>

    <h4 class='deep-dive-heading'>2. Translating Technical Jargon for Stakeholders</h4>
    <div class="neu-card-grid">
      <div class="neu-mini-card">
        <strong>Avoid saying:</strong> <em>"We need 2 sprints to normalize third normal form tables and migrate to PostgreSQL B-Tree indices."</em>
      </div>
      <div class="neu-mini-card">
        <strong>Say instead:</strong> <em>"We need 2 sprints to optimize our search database so page loads stay under 1 second during Black Friday sales."</em>
      </div>
    </div>
    """
}

enhanced_subtopics = []
for st in subtopics:
    sid = st['id']
    qn_items = format_quick_notes(st['quick_notes'])
    trap_items = format_traps(st['common_traps'])
    
    # Use our curated clean deep dive HTML or fallback to clean formatted text
    dd_html = DEEP_DIVES.get(sid)
    if not dd_html:
        raw_dd = st.get('deep_dive', '')
        dd_clean = re.sub(r'\n+', '</p><p class="deep-dive-text">', raw_dd.strip())
        dd_html = f"<p class='deep-dive-text'>{dd_clean}</p>"
        
    enhanced_subtopics.append({
        **st,
        'formatted_quick_notes': qn_items,
        'formatted_traps': trap_items,
        'formatted_deep_dive': dd_html.strip()
    })

out_json = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\subject_01_enhanced.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(enhanced_subtopics, f, indent=2, ensure_ascii=False)

out_js_trainer = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\interactive-trainer\data.js'
with open(out_js_trainer, 'w', encoding='utf-8') as f:
    f.write('window.NSCT_SUBJECT_01 = ' + json.dumps(enhanced_subtopics, ensure_ascii=False) + ';')

out_js_root = r'C:\Users\NAC\.gemini\antigravity\scratch\NSCT-Preparation\data.js'
with open(out_js_root, 'w', encoding='utf-8') as f:
    f.write('window.NSCT_SUBJECT_01 = ' + json.dumps(enhanced_subtopics, ensure_ascii=False) + ';')

print(f"Successfully generated clean enhanced data for all 16 subtopics!")
