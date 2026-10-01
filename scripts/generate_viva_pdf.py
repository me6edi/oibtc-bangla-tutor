"""
Generate the Viva Short Questions PDF for OIBTC project.
Ensures perfect page distribution:
- Page 1: Header + Questions 1 to 10
- Page 2: Questions 11 to 20
- Page 3: Part 2 (Complete Project Flow) + Part 3 ("Sir পুরো Project বুঝাও" Answer)
"""

import os
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<title>OIBTC - Viva Short Questions & Answers</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  @page {
    size: A4;
    margin: 10mm 12mm 10mm 12mm;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: 'Hind Siliguri', 'SolaimanLipi', 'Kalpurush', 'Vrinda', 'Inter', -apple-system, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.45;
    font-size: 13px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .header-card {
    border: 1.5px solid #0284c7;
    border-radius: 9px;
    padding: 10px 16px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    margin-bottom: 10px;
  }
  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #bae6fd;
    padding-bottom: 6px;
    margin-bottom: 6px;
  }
  .univ-title {
    font-size: 12px;
    font-weight: 700;
    color: #0369a1;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .guide-badge {
    background: #0284c7;
    color: #ffffff;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 10.5px;
    font-weight: 600;
  }
  .project-title {
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 3px;
    line-height: 1.25;
  }
  .project-sub {
    font-size: 11.5px;
    color: #475569;
    font-weight: 500;
  }
  .meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 6px;
    background: #ffffff;
    padding: 6px 10px;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
    font-size: 11px;
  }
  .meta-item strong {
    color: #0284c7;
  }

  .section-heading {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
    background: #f1f5f9;
    padding: 5px 10px;
    border-left: 4px solid #0284c7;
    border-radius: 0 6px 6px 0;
    margin-top: 6px;
    margin-bottom: 8px;
  }
  .section-badge {
    background: #0f172a;
    color: #ffffff;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
  }

  .qa-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 10px;
    margin-bottom: 5px;
    page-break-inside: avoid;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  }
  .qa-card:nth-child(even) {
    background: #f8fafc;
  }
  .qa-q {
    font-size: 12.5px;
    font-weight: 700;
    color: #0369a1;
    margin-bottom: 2px;
    display: flex;
    align-items: baseline;
    gap: 6px;
  }
  .q-num {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 10.5px;
    font-weight: 700;
    padding: 0px 5px;
    border-radius: 3px;
    border: 1px solid #bae6fd;
    flex-shrink: 0;
  }
  .qa-a {
    font-size: 12px;
    color: #1e293b;
    padding-left: 26px;
    line-height: 1.4;
  }
  .tech-kw {
    font-weight: 600;
    color: #0f172a;
    background: #f1f5f9;
    padding: 0px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }

  .page-2-start {
    page-break-before: always;
  }
  .page-3-start {
    page-break-before: always;
  }

  .flow-box {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border: 1.5px solid #22c55e;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
    margin-bottom: 16px;
  }
  .flow-title {
    font-size: 14px;
    font-weight: 700;
    color: #15803d;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .flow-line {
    font-family: 'Inter', 'Hind Siliguri', sans-serif;
    font-size: 12.5px;
    font-weight: 600;
    color: #0f172a;
    background: #ffffff;
    padding: 12px 14px;
    border-radius: 6px;
    border: 1px solid #bbf7d0;
    line-height: 1.7;
    word-spacing: 1px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .flow-arrow {
    color: #16a34a;
    font-weight: 700;
    margin: 0 4px;
  }

  .overview-box {
    background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
    border: 1.5px solid #eab308;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
    margin-bottom: 16px;
  }
  .overview-title {
    font-size: 14px;
    font-weight: 700;
    color: #a16207;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .overview-lines {
    background: #ffffff;
    border: 1px solid #fef08a;
    border-radius: 6px;
    padding: 14px 16px;
    font-size: 13px;
    line-height: 1.6;
    color: #1e293b;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }
  .overview-line {
    margin-bottom: 10px;
    display: flex;
    gap: 10px;
  }
  .overview-line:last-child {
    margin-bottom: 0;
  }
  .line-badge {
    background: #fef08a;
    color: #854d0e;
    font-size: 11px;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 4px;
    height: fit-content;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .footer-note {
    text-align: center;
    font-size: 11px;
    color: #64748b;
    border-top: 1px dashed #cbd5e1;
    padding-top: 8px;
    margin-top: 20px;
  }
</style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="header-card">
    <div class="header-top">
      <span class="univ-title">Department of Computer Science & Engineering | World University of Bangladesh</span>
      <span class="guide-badge">Viva Voce & Defense Guide</span>
    </div>
    <div class="project-title">OIBTC: Offline Intelligent Bangla Tutoring Chatbot</div>
    <div class="project-sub">For Students of Secondary Education in Bangladesh (Class 9-10 ICT Pilot)</div>
    <div class="meta-grid">
      <div class="meta-item"><strong>Supervisor:</strong> Kazi H. Robin Sir</div>
      <div class="meta-item"><strong>Students:</strong> Mehedi Amin (3920), Azad Hossain (3915), Jannatul Ferdous (3916)</div>
    </div>
  </div>

  <div class="section-heading">
    <span class="section-badge">Part 1</span>
    <span>২০টি গুরুত্বপূর্ণ Short Viva Questions & Answers (প্রশ্ন ১ – ১০)</span>
  </div>

  <!-- Q1 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১</span> OIBTC প্রজেক্টের পূর্ণরূপ এবং এর মূল লক্ষ্য কী?</div>
    <div class="qa-a"><strong>উত্তর:</strong> OIBTC হলো <span class="tech-kw">Offline Intelligent Bangla Tutoring Chatbot</span>; এর মূল লক্ষ্য ইন্টারনেটবিহীন প্রত্যন্ত অঞ্চলের ৯ম-১০ম শ্রেণির শিক্ষার্থীদের বাংলায় আইসিটি পাঠ্যবইভিত্তিক অফলাইন টিউটরিং সেবা দেওয়া।</div>
  </div>

  <!-- Q2 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">২</span> প্রজেক্টটিতে কোন কোন প্রযুক্তি ও ফ্রেমওয়ার্ক (Tech Stack) ব্যবহার করা হয়েছে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> ব্যাকএন্ডে <span class="tech-kw">FastAPI</span> ও <span class="tech-kw">Python</span>, ডেটাবেজে <span class="tech-kw">SQLite</span>, ভেক্টর সার্চে <span class="tech-kw">FAISS</span> ও <span class="tech-kw">TF-IDF</span>, এবং ফ্রন্টএন্ডে <span class="tech-kw">React (Vite)</span> ও <span class="tech-kw">Lucide Icons</span> ব্যবহৃত হয়েছে।</div>
  </div>

  <!-- Q3 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৩</span> সিস্টেমটি কীভাবে কোনো ইন্টারনেট ছাড়া সম্পূর্ণ অফলাইনে (100% Offline) কাজ করে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> আমাদের NCTB ডেটাসেট, FAISS ভেক্টর ইনডেক্স, SQLite ডেটাবেজ ও সিন্থেসাইজার ইঞ্জিন সবই লোকাল পিসিতে সংরক্ষিত ও রান হয়; কোনো ক্লাউড এপিআই কি লাগে না।</div>
  </div>

  <!-- Q4 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৪</span> প্রজেক্টে RAG (Retrieval-Augmented Generation) আর্কিটেকচার কেন ব্যবহার করেছেন?</div>
    <div class="qa-a"><strong>উত্তর:</strong> সাধারণ এলএলএম-এর মনগড়া ভুল তথ্য (<span class="tech-kw">Hallucination</span>) দূর করে শুধুমাত্র NCTB পাঠ্যবইয়ের নির্ভরযোগ্য তথ্য ও সুনির্দিষ্ট পৃষ্ঠা নম্বরের রেফারেন্সসহ উত্তর নিশ্চিত করার জন্য।</div>
  </div>

  <!-- Q5 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৫</span> প্রজেক্টের ডেটাসেটে কী কী তথ্য রয়েছে এবং এটি কীভাবে সাজানো হয়েছে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> ৯ম-১০ম শ্রেণির NCTB আইসিটি বইয়ের ১ম ও ২য় অধ্যায়কে <span class="tech-kw">৪৩টি পেডাগজিক্যাল চাঙ্কে</span> (JSON ফরম্যাটে) অধ্যায়, বিষয় ও পৃষ্ঠা নম্বরসহ ভাগ করে ডেটাসেট তৈরি করা হয়েছে।</div>
  </div>

  <!-- Q6 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৬</span> প্রাসঙ্গিক তথ্য খোঁজার জন্য (Retrieval) কোন কোন অ্যালগরিদম ব্যবহৃত হয়েছে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> সেমান্টিক ভেক্টর সার্চের জন্য <span class="tech-kw">FAISS (Inner Product / Cosine Similarity)</span> এবং বাংলা মরফোলজির জন্য ক্যারেক্টার n-gram ভিত্তিক <span class="tech-kw">TF-IDF</span> ও টপিক-লেভেল ফ্রেজ বুস্টিং ব্যবহৃত হয়েছে।</div>
  </div>

  <!-- Q7 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৭</span> শিক্ষার্থী Banglish বা ভুল বানানে প্রশ্ন করলে সিস্টেম কীভাবে তা হ্যান্ডেল করে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">transliteration.py</span>-এর কাস্টম অফলাইন আইসিটি লেক্সিকন দিয়ে বাংলিশ ও ভুল বানানকে তাৎক্ষণিকভাবে স্ট্যান্ডার্ড বাংলা পাঠ্যবইয়ের শব্দে রূপান্তর (Normalize) করা হয়।</div>
  </div>

  <!-- Q8 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৮</span> "এটি কীভাবে কাজ করে?"-এর মতো ফলো-আপ প্রশ্ন সিস্টেম কীভাবে সমাধান করে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">pipeline.py</span>-এর হিস্ট্রি রেজোলিউশন লজিক পূর্ববর্তী চ্যাট হিস্ট্রি (SQLite) থেকে মূল বিষয়টি শনাক্ত করে সর্বনামের (Pronoun) স্থানে প্রতিস্থাপন করে কোয়েরি রিরাইট করে।</div>
  </div>

  <!-- Q9 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">৯</span> Intent Classification কীভাবে করা হয়েছে এবং এর ধরনগুলো কী কী?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">intent.py</span> মডিউলটি শূন্য লেটেন্সিতে রুল-বেসড প্যাটার্ন দিয়ে <span class="tech-kw">১১টি Intent</span> (যেমন: DEFINITION, MECHANISM, PREVENTION, TROUBLESHOOTING ইত্যাদি) ও গ্র্যানুলারিটি শনাক্ত করে।</div>
  </div>

  <!-- Q10 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১০</span> তথ্যের নির্ভরযোগ্যতা রক্ষায় অ্যান্টি-হ্যালুসিনেশন গার্ডরেইল কীভাবে কাজ করে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">_verify_chunk_evidence</span> গেটের মাধ্যমে কোয়েরির মূল প্রমাণ চাঙ্কে না থাকলে বা সিলেবাস বহির্ভূত অপারেশন (যেমন: Excel SUM, Photoshop) হলে সিস্টেম উত্তর বাতিল করে দেয়।</div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page-2-start"></div>

  <div class="section-heading">
    <span class="section-badge">Part 1 (চলমান)</span>
    <span>২০টি গুরুত্বপূর্ণ Short Viva Questions & Answers (প্রশ্ন ১১ – ২০)</span>
  </div>

  <!-- Q11 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১১</span> সিলেবাসের বাইরের প্রশ্ন (Out-of-curriculum) করলে চ্যাটবট কী প্রতিক্রিয়া দেখায়?</div>
    <div class="qa-a"><strong>উত্তর:</strong> সিস্টেম বানিয়ে উত্তর না দিয়ে সরাসরি জানায় যে প্রশ্নটি অধ্যায় ১ ও ২-এর আওতাভুক্ত নয় এবং একই সাথে সিলেবাসের <span class="tech-kw">৩টি প্রাসঙ্গিক প্রশ্ন সাজেস্ট</span> করে।</div>
  </div>

  <!-- Q12 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১২</span> ফাইনাল উত্তর সিন্থেসিস (Answer Generation) কীভাবে সম্পন্ন হয়?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">llm.py</span>-তে থাকা অফলাইন ডিটারমিনিস্টিক টেক্সটবুক ইঞ্জিন শিক্ষার্থীর ইনটেন্ট অনুযায়ী সরাসরি এনসিটিবি পাঠ্যবই থেকে পয়েন্ট ও প্যারা আকারে পরিমিত উত্তর তৈরি করে।</div>
  </div>

  <!-- Q13 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৩</span> উত্তরের সাথে সাইটেশন (Citation) কীভাবে দেখানো হয়?</div>
    <div class="qa-a"><strong>উত্তর:</strong> প্রতিটি উত্তরের নিচে রিট্রিভ করা চাঙ্ক থেকে স্বয়ংক্রিয়ভাবে বইয়ের নাম, শ্রেণি, অধ্যায় নম্বর, অধ্যায়ের শিরোনাম এবং সুনির্দিষ্ট <span class="tech-kw">পৃষ্ঠা নম্বর</span> কার্ড আকারে প্রদর্শন করা হয়।</div>
  </div>

  <!-- Q14 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৪</span> ডেটাবেজ হিসেবে SQLite কেন বেছে নেওয়া হয়েছে এবং এতে কী ডেটা থাকে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> SQLite সম্পূর্ণ সার্ভারলেস ও লোকাল হওয়ায় ব্যবহৃত হয়েছে; এতে <span class="tech-kw">sessions</span> (শ্রেণি, বিষয়) এবং <span class="tech-kw">chat_messages</span> (প্রশ্ন, উত্তর, সাইটেশন ও টাইম) সংরক্ষিত থাকে।</div>
  </div>

  <!-- Q15 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৫</span> "Classroom Hotspot Mode" কী এবং এর সুবিধা কী?</div>
    <div class="qa-a"><strong>উত্তর:</strong> ব্যাকএন্ড <span class="tech-kw">0.0.0.0:8000</span>-এ হোস্ট করায় শিক্ষক পিসিতে লোকাল হটস্পট চালু করলে ইন্টারনেট ছাড়াই ক্লাসের সব শিক্ষার্থী মোবাইল ব্রাউজারে লোকাল আইপি দিয়ে যুক্ত হতে পারে।</div>
  </div>

  <!-- Q16 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৬</span> পুরো প্রজেক্টটি চালু করার নিয়ম (Execution/Startup) কী?</div>
    <div class="qa-a"><strong>উত্তর:</strong> প্রজেক্টের রুট ফোল্ডারে থাকা <span class="tech-kw">start_oibtc.bat</span> ফাইলে ডাবল-ক্লিক করলেই স্বয়ংক্রিয়ভাবে FAISS চেকিং, FastAPI ব্যাকএন্ড এবং React ফ্রন্টএন্ড এক ক্লিকে চালু হয়ে যায়।</div>
  </div>

  <!-- Q17 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৭</span> ব্যাকএন্ডের প্রধান এপিআই এন্ডপয়েন্ট (API Endpoints) কোনগুলো?</div>
    <div class="qa-a"><strong>উত্তর:</strong> <span class="tech-kw">/api/v1/status</span> (অফলাইন অবস্থা ও আইপি), <span class="tech-kw">/api/v1/chat/session</span> (সেশন শুরু), এবং <span class="tech-kw">/api/v1/chat/query</span> (প্রশ্নের উত্তর, সাইটেশন ও ফলো-আপ ডেলিভারি)।</div>
  </div>

  <!-- Q18 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৮</span> ফ্রন্টএন্ডে শিক্ষার্থীদের শেখার সুবিধার জন্য কী কী ফিচার রাখা হয়েছে?</div>
    <div class="qa-a"><strong>উত্তর:</strong> অফলাইন স্ট্যাটাস ব্যাজ, রেডিমেড কুইক প্রম্পট বাটন, অধ্যায় ও টপিক লিস্ট ব্রাউজার, ইন্টারঅ্যাক্টিভ সাইটেশন কার্ড এবং ফলো-আপ সাজেশন বাটন রাখা হয়েছে।</div>
  </div>

  <!-- Q19 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">১৯</span> সিস্টেমটির হার্ডওয়্যার প্রয়োজনীয়তা এবং রেসপন্স টাইম (Performance) কেমন?</div>
    <div class="qa-a"><strong>উত্তর:</strong> কোনো জিপিইউ (GPU) ছাড়াই সাধারণ ল্যাব পিসিতে (Core i3/i5, 8GB RAM, CPU-Only) চলে এবং প্রতিটি প্রশ্নের উত্তর গড়ে মাত্র <span class="tech-kw">১.৮৯ সেকেন্ডে</span> ডেলিভার করে।</div>
  </div>

  <!-- Q20 -->
  <div class="qa-card">
    <div class="qa-q"><span class="q-num">২০</span> এই প্রজেক্টের ভবিষ্যৎ রোডম্যাপ বা সম্প্রসারণ পরিকল্পনা কী?</div>
    <div class="qa-a"><strong>উত্তর:</strong> বর্তমান রিইউজেবল ইনজেশন পাইপলাইন বজায় রেখে দ্রুত আইসিটি বইয়ের বাকি অধ্যায়গুলো (৩ থেকে ৬) এবং পরবর্তীতে সাধারণ বিজ্ঞান ও গণিত পাঠ্যবই অন্তর্ভুক্ত করা।</div>
  </div>

  <!-- ==================== PAGE 3 ==================== -->
  <div class="page-3-start"></div>

  <!-- SECTION 2 -->
  <div class="section-heading">
    <span class="section-badge">Part 2</span>
    <span>Complete Project Flow (এক লাইনে মূল পাইপলাইন)</span>
  </div>

  <div class="flow-box">
    <div class="flow-title">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      বাস্তব কোড অনুযায়ী সম্পূর্ণ প্রজেক্টের এক লাইনের এক্সিকিউশন ফ্লো:
    </div>
    <div class="flow-line">
      User (React UI) <span class="flow-arrow">→</span> Banglish/Typo Normalization <span class="flow-arrow">→</span> Context Resolution <span class="flow-arrow">→</span> Intent & Scope Detection <span class="flow-arrow">→</span> NCTB Retrieval (FAISS/TF-IDF) <span class="flow-arrow">→</span> Semantic Predicate & Evidence Verification Gate <span class="flow-arrow">→</span> Scoped Textbook Synthesis <span class="flow-arrow">→</span> Citation & Follow-up Generation <span class="flow-arrow">→</span> Final Answer (with Page Ref & SQLite Persistence)
    </div>
  </div>

  <!-- SECTION 3 -->
  <div class="section-heading">
    <span class="section-badge">Part 3</span>
    <span>“Sir পুরো Project বুঝাও” — মাত্র ৪–৫ লাইনের সহজ ও নিখুঁত উত্তর</span>
  </div>

  <div class="overview-box">
    <div class="overview-title">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
      স্যারের সামনে বলার মতো ৫ লাইনের সহজ বাংলা উত্তর:
    </div>
    <div class="overview-lines">
      <div class="overview-line">
        <span class="line-badge">১</span>
        <div><strong>"স্যার, আমাদের প্রজেক্ট OIBTC হলো একটি ১০০% অফলাইন বাংলা ইন্টেলিজেন্ট টিউটরিং চ্যাটবট,</strong> যা ইন্টারনেটবিহীন প্রত্যন্ত স্কুলের ৯ম-১০ম শ্রেণির শিক্ষার্থীদের আইসিটি শেখার জন্য তৈরি।"</div>
      </div>
      <div class="overview-line">
        <span class="line-badge">২</span>
        <div><strong>"শিক্ষার্থী যখন বাংলায় বা বাংলিশে কোনো প্রশ্ন করে,</strong> আমাদের পাইপলাইন প্রশ্নটিকে নরমালাইজ করে এবং ইনটেন্ট শনাক্ত করে এনসিটিবি পাঠ্যবইয়ের ৪৩টি ভেক্টর চাঙ্ক থেকে নিখুঁত তথ্য রিট্রিভ করে।"</div>
      </div>
      <div class="overview-line">
        <span class="line-badge">৩</span>
        <div><strong>"এরপর আমাদের অ্যান্টি-হ্যালুসিনেশন গার্ডরেইল তথ্যের সত্যতা যাচাই করে সুনির্দিষ্ট উত্তর তৈরি করে</strong> এবং সাথে পাঠ্যবইয়ের নির্দিষ্ট অধ্যায় ও পৃষ্ঠা নম্বরের সাইটেশন প্রদর্শন করে।"</div>
      </div>
      <div class="overview-line">
        <span class="line-badge">৪</span>
        <div><strong>"ব্যাকএন্ডে FastAPI ও SQLite এবং ফ্রন্টএন্ডে React ব্যবহার করা হয়েছে,</strong> যা কোনো ক্লাউড এপিআই বা ইন্টারনেট সংযোগ ছাড়াই সাধারণ ল্যাব কম্পিউটারে সম্পূর্ণ অফলাইনে চলতে সক্ষম।"</div>
      </div>
      <div class="overview-line">
        <span class="line-badge">৫</span>
        <div><strong>"এছাড়া আমাদের 'ক্লাসরুম হটস্পট মোড'-এর মাধ্যমে</strong> পুরো কম্পিউটার ল্যাবে মাত্র একটি হোস্টে সফটওয়্যারটি চালু রেখে কোনো ইন্টারনেট খরচ ছাড়াই ক্লাসের সব শিক্ষার্থী নিজেদের ডিভাইস থেকে একসাথে শিখতে পারে।"</div>
      </div>
    </div>
  </div>

  <div class="footer-note">
    OIBTC • Department of CSE, World University of Bangladesh • 100% Offline RAG Tutoring System
  </div>

</body>
</html>
"""

def generate_pdf():
    output_dir = "Viva Short Questions"
    os.makedirs(output_dir, exist_ok=True)
    
    html_path = os.path.join(output_dir, "temp_viva.html")
    pdf_path = os.path.join(output_dir, "Viva Short Questions.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote temporary HTML to {html_path}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_path)}")
        page.wait_for_load_state("networkidle")
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
        )
        browser.close()
        print(f"Successfully generated PDF at: {pdf_path}")
        
    if os.path.exists(html_path):
        os.remove(html_path)
        print("Cleaned up temporary HTML file.")

if __name__ == "__main__":
    generate_pdf()
