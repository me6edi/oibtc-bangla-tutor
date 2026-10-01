# OIBTC: Online Demonstration Guide for Supervisor & Evaluators

Welcome to the **Offline Intelligent Bangla Tutoring Chatbot (OIBTC)** online evaluation guide. This guide explains how to demonstrate the system to academic supervisors, examiners, and evaluators anywhere in the world over a secure HTTPS link.

---

## 🌟 1. System Overview & Core Highlights

| Feature | Description |
| :--- | :--- |
| **Domain** | NCTB Class 9-10 ICT Curriculum (তথ্য ও যোগাযোগ প্রযুক্তি) |
| **Architecture** | 100% Offline-First Architecture (Classroom Hotspot ready) |
| **RAG Retrieval** | Hybrid Vector Search (FAISS IP index + Character N-gram TF-IDF) |
| **Language Support** | Pure Bengali and Phonetic Romanized Bengali (Banglish) |
| **Pedagogy** | Intent-aware tutoring (Definitions, Steps, Rules, Explanations, Out-of-curriculum guardrails) |

---

## 🚀 2. Live Demo Test Queries (For Supervisor / Evaluator)

Ask your supervisor or evaluator to test these sample queries on the live demo link:

### 📖 Category 1: Definitions & Concepts (সংজ্ঞা ও মূল ধারণা)
1. **"কম্পিউটার ভাইরাস কী?"**  
   *Expected Response:* VIRUS (Vital Information Resources Under Siege) এর পূর্ণরূপ ও সংজ্ঞা, ফ্রেড কোহেন এর নামকরণ, এবং পাঠ্যবইয়ের পৃষ্ঠা নং ২৩-২৫ এর রেফারেন্স।
2. **"ই-লার্নিং বলতে কী বোঝায়?"**  
   *Expected Response:* ইলেকট্রনিক লার্নিং বা দূরশিক্ষণের ধারণা এবং এটি সনাতন পদ্ধতির বিকল্প নয় বরং পরিপূরক।

### 🛠️ Category 2: Practical Steps & Troubleshooting (ব্যবহারিক ও ট্রাবলশুটিং)
1. **"কম্পিউটার ঘন ঘন রিস্টার্ট হলে কী করতে হবে?"**  
   *Expected Response:* কুলিং ফ্যান চেক, প্রসেসরে থার্মাল পেস্ট ও ডাস্ট ক্লিনিংয়ের পাঠ্যবই নির্দেশিত ধাপসমূহ।
2. **"পাসওয়ার্ড কীভাবে শক্তিশালী করতে হয়?"**  
   *Expected Response:* ছোট ও বড় হাতের অক্ষর, সংখ্যা ও বিশেষ চিহ্নের মিশ্রণ ব্যবহারের পরামর্শ।

### 🔤 Category 3: Banglish / Romanized Bengali (বাংলিশ ইনপুট)
1. **"computer virus ki?"**  
   *Expected Response:* সিস্টেম স্বয়ংক্রিয়ভাবে ফোনেটিক ট্রান্সলিটারেশন করে সঠিক বাংলায় উত্তর ও রেফারেন্স উপস্থাপন করবে।

### 🛡️ Category 4: Curriculum Boundary Guardrail (পাঠ্যক্রমের বাইরের প্রশ্ন)
1. **"পাইথন প্রোগ্রামিং কীভাবে শিখব?"**  
   *Expected Response:* পাঠ্যক্রমের সীমানা বজায় রেখে বিনয়ের সাথে জানাবে যে এটি ৯ম-১০ম শ্রেণির আইসিটি সিলেবাসের অধ্যায় ১ ও ২ বহির্ভূত এবং প্রাসঙ্গিক অধ্যায়ের প্রশ্ন করার পরামর্শ দেবে।

---

## 🔒 3. Clean-up & Security: How to Remove

When your demonstration is complete:
1. Simply press `Ctrl + C` or close the tunnel window (`start_quick_demo_tunnel.bat`).
2. The public link immediately expires and terminates worldwide.
3. Your local server remains 100% offline and secure.
