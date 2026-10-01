import React, { useState, useEffect, useRef } from 'react';
import { 
  GraduationCap, 
  RotateCcw, 
  BookOpen, 
  Send, 
  Sparkles, 
  Bookmark, 
  HelpCircle,
  Menu,
  X,
  ChevronRight,
  ShieldCheck,
  Cpu,
  Monitor,
  Sun,
  Moon
} from 'lucide-react';

export default function App() {
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [systemStatus, setSystemStatus] = useState({
    offline_ready: true,
    local_ip: '127.0.0.1'
  });

  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('oibtc_theme') || 'dark';
    } catch (e) {
      return 'dark';
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('oibtc_theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } catch (e) {}
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const chatEndRef = useRef(null);

  const quickPrompts = [
    "কম্পিউটার ভাইরাস কী?",
    "কম্পিউটার ভাইরাস কী এবং কীভাবে ছড়ায়?",
    "কম্পিউটার ভাইরাস কীভাবে ছড়ায়?",
    "ভাইরাস থেকে কীভাবে নিরাপদ থাকব?",
    "ভাইরাসের উদাহরণ দাও।"
  ];

  const curriculumChapters = [
    {
      chapter: 1,
      title: "তথ্য ও যোগাযোগ প্রযুক্তি এবং আমাদের বাংলাদেশ",
      icon: <Cpu className="w-4 h-4 text-sky-400" />,
      topics: [
        "একুশ শতক এবং আইসিটি",
        "আইসিটি বিকাশে উল্লেখযোগ্য ব্যক্তিত্ব",
        "ই-লার্নিং ও বাংলাদেশ",
        "ই-গভর্ন্যান্স ও ই-সার্ভিস",
        "ডিজিটাল বাংলাদেশ"
      ]
    },
    {
      chapter: 2,
      title: "কম্পিউটার ও কম্পিউটার ব্যবহারকারীর নিরাপত্তা",
      icon: <ShieldCheck className="w-4 h-4 text-emerald-400" />,
      topics: [
        "কম্পিউটারের সঠিক রক্ষণাবেক্ষণ",
        "সফটওয়্যার ইনস্টলেশন ও আনইনস্টলেশন",
        "পাসওয়ার্ড ও নিরাপত্তা",
        "কম্পিউটার ভাইরাস ও অ্যান্টিভাইরাস",
        "সাধারণ ট্রাবলশুটিং"
      ]
    }
  ];

  useEffect(() => {
    fetchStatus();
    initSession();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/v1/status');
      if (res.ok) {
        const data = await res.json();
        setSystemStatus(data);
      }
    } catch (e) {
      console.log('Status check notice:', e);
    }
  };

  const initSession = async () => {
    try {
      const res = await fetch('/api/v1/chat/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          grade: 9,
          subject: 'ICT',
          subject_bn: 'তথ্য ও যোগাযোগ প্রযুক্তি'
        })
      });
      if (res.ok) {
        const data = await res.json();
        setSessionId(data.session_id);
        setMessages([
          {
            id: 'welcome',
            sender: 'tutor',
            answer: `আসসালামু আলাইকুম! আমি তোমার অফলাইন বাংলা আইসিটি শিক্ষক।\n\nNCTB পাঠ্যবইয়ের অধ্যায় ১ (তথ্য ও যোগাযোগ প্রযুক্তি এবং আমাদের বাংলাদেশ) এবং অধ্যায় ২ (কম্পিউটার ও কম্পিউটার ব্যবহারকারীর নিরাপত্তা) থেকে তোমার যেকোনো প্রশ্ন আমাকে জিজ্ঞাসা করতে পারো। প্রশ্নে যা জানতে চাইবে, আমি পাঠ্যবই থেকে ঠিক সেটুকুই উত্তর দেবো।`,
            sources: [
              {
                book: "তথ্য ও যোগাযোগ প্রযুক্তি (৯ম-১০ম শ্রেণি)",
                chapter: 1,
                topic: "কারিকুলাম অধ্যায় ১ ও ২",
                page: "১-৩২"
              }
            ],
            suggested_followups: [
              "কম্পিউটার ভাইরাস কী?",
              "শক্তিশালী পাসওয়ার্ড কীভাবে তৈরি করব?",
              "ই-লার্নিং বলতে কী বোঝায়?"
            ]
          }
        ]);
      }
    } catch (e) {
      console.error('Session error:', e);
    }
  };

  const handleSend = async (customQuery) => {
    const text = (customQuery || inputQuery).trim();
    if (!text || isLoading) return;

    setInputQuery('');
    setMessages(prev => [...prev, { id: String(Date.now()), sender: 'student', query: text }]);
    setIsLoading(true);
    if (isSidebarOpen) setIsSidebarOpen(false);

    try {
      const res = await fetch('/api/v1/chat/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          query: text,
          grade: 9,
          subject: 'ICT'
        })
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [
          ...prev,
          {
            id: String(Date.now()),
            sender: 'tutor',
            answer: data.answer,
            sources: data.sources || [],
            suggested_followups: data.suggested_followups || [],
            is_out_of_curriculum: data.is_out_of_curriculum,
            intent: data.intent || 'GENERAL',
            intent_label: data.intent_label || 'পাঠ্যবইভিত্তিক উত্তর'
          }
        ]);
      } else {
        setMessages(prev => [
          ...prev,
          {
            id: String(Date.now()),
            sender: 'tutor',
            answer: "দুঃখিত, উত্তর তৈরিতে সাময়িক সমস্যা হয়েছে। পুনরায় চেষ্টা করো।",
            sources: []
          }
        ]);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: String(Date.now()),
          sender: 'tutor',
          answer: "লোকাল সার্ভারের সাথে সংযোগ পাওয়া যায়নি। নিশ্চিত করো ব্যাকএন্ড চালু আছে।",
          sources: []
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const cleanMarkdown = (txt) => {
    if (!txt) return '';
    return txt.replace(/\*\*/g, '').replace(/\*/g, '').trim();
  };

  const renderPedagogicalAnswer = (rawText, intent, intentLabel) => {
    if (!rawText) return null;

    // Check if it's a multi-part answer (e.g. **১. ...** and **২. ...**)
    const multiMatch = rawText.match(/\*\*([১-৯IVX0-9]+)\.\s*(.*?)\*\*\n([\s\S]*?)(?=(?:\*\*([১-৯IVX0-9]+)\.|$))/g);

    if (multiMatch && multiMatch.length > 1) {
      return (
        <div className="pedagogy-container">
          {multiMatch.map((section, sIdx) => {
            const lines = section.trim().split('\n');
            const header = cleanMarkdown(lines[0] || '');
            const body = cleanMarkdown(lines.slice(1).join('\n'));
            const isMech = header.includes('ছড়ায়') || header.includes('পদ্ধতি') || header.includes('নিয়ম');
            return (
              <div key={sIdx} className="pedagogy-section-card">
                <div className="section-badge-row">
                  <span className={`section-badge ${isMech ? 'badge-mech' : 'badge-def'}`}>
                    {header}
                  </span>
                </div>
                <div className="section-body-text" style={{ whiteSpace: 'pre-line' }}>
                  {body}
                </div>
              </div>
            );
          })}
        </div>
      );
    }

    // Determine card badge based on intent
    let badgeClass = 'badge-def';
    let badgeText = intentLabel || 'পাঠ্যবইয়ের তথ্য';

    if (intent === 'DEFINITION') {
      badgeClass = 'badge-def';
      badgeText = 'পাঠ্যবইয়ের অনুমোদিত সংজ্ঞা';
    } else if (intent === 'MECHANISM') {
      badgeClass = 'badge-mech';
      badgeText = 'ছড়ানোর পদ্ধতি ও প্রক্রিয়া';
    } else if (intent === 'PREVENTION') {
      badgeClass = 'badge-prev';
      badgeText = 'নিরাপত্তা ও প্রতিরোধের উপায়';
    } else if (intent === 'EXAMPLES') {
      badgeClass = 'badge-ex';
      badgeText = 'পাঠ্যবইয়ে উল্লেখিত উদাহরণ';
    } else if (intent === 'RULES') {
      badgeClass = 'badge-rules';
      badgeText = 'নিয়মাবলি ও নির্দেশিকা';
    } else if (intent === 'TROUBLESHOOTING') {
      badgeClass = 'badge-trouble';
      badgeText = 'ট্রাবলশুটিং সমাধান';
    } else if (intent === 'SYMPTOMS') {
      badgeClass = 'badge-trouble';
      badgeText = 'আক্রমণের লক্ষণ';
    } else if (intent === 'HISTORY_PERSON') {
      badgeClass = 'badge-def';
      badgeText = 'ঐতিহাসিক ব্যক্তিত্ব ও অবদান';
    }

    return (
      <div className="pedagogy-container">
        <div className="pedagogy-section-card">
          <div className="section-badge-row">
            <span className={`section-badge ${badgeClass}`}>
              {badgeText}
            </span>
          </div>
          <div className="section-body-text" style={{ whiteSpace: 'pre-line' }}>
            {cleanMarkdown(rawText)}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="stitch-app-shell">
      {/* Mobile Backdrop Overlay */}
      <div 
        className={`sidebar-backdrop ${isSidebarOpen ? 'active' : ''}`}
        onClick={() => setIsSidebarOpen(false)}
      />

      {/* 1. Left Sidebar: Curriculum & Station Management */}
      <aside className={`stitch-sidebar ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-brand">
            <div className="sidebar-logo-icon">
              <GraduationCap style={{ width: '22px', height: '22px' }} />
            </div>
            <div className="sidebar-brand-text">
              <span className="sidebar-title">OIBTC</span>
              <span className="sidebar-tagline">AI বাংলা শিক্ষক</span>
            </div>
          </div>
          <button 
            className="btn-sidebar-close"
            onClick={() => setIsSidebarOpen(false)}
            aria-label="Close sidebar"
          >
            <X style={{ width: '20px', height: '20px' }} />
          </button>
        </div>

        <div className="sidebar-content">
          {/* Station Card */}
          <div className="station-card">
            <div className="station-title-row">
              <span>স্টেশন #০৪ (Lab PC)</span>
              <span style={{ fontSize: '0.68rem', background: 'rgba(16,185,129,0.2)', padding: '2px 6px', borderRadius: '4px' }}>Active</span>
            </div>
            <span className="station-desc">৯ম শ্রেণি • তথ্য ও যোগাযোগ প্রযুক্তি</span>
          </div>

          {/* Curriculum Explorer Section */}
          <div>
            <div className="sidebar-section-title">
              <BookOpen style={{ width: '13px', height: '13px', color: '#38bdf8' }} />
              <span>কারিকুলাম অধ্যায় ও বিষয়বস্তু</span>
            </div>

            {curriculumChapters.map((ch) => (
              <div key={ch.chapter} className="curriculum-chapter-box">
                <div className="chapter-header">
                  {ch.icon}
                  <span>অধ্যায় {ch.chapter}: {ch.title}</span>
                </div>
                <div className="chapter-topic-list">
                  {ch.topics.map((tp, tIdx) => (
                    <button
                      key={tIdx}
                      className="topic-link-item"
                      onClick={() => handleSend(`${tp} সম্পর্কে বুঝিয়ে বলো`)}
                      title={`প্রশ্ন করো: ${tp}`}
                    >
                      <ChevronRight style={{ width: '11px', height: '11px', display: 'inline', marginRight: '3px' }} />
                      <span>{tp}</span>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Active Session Info */}
          <div>
            <div className="sidebar-section-title">
              <Monitor style={{ width: '13px', height: '13px', color: '#10b981' }} />
              <span>সেশন আইডি ও ক্লাসরুম নেটওয়ার্ক</span>
            </div>
            <div className="session-network-box">
              <div className="session-network-row">
                <strong>Session:</strong> <span>{sessionId ? sessionId.slice(0, 16) + '...' : 'লোডিং...'}</span>
              </div>
              <div className="session-network-row">
                <strong>Hotspot:</strong> <span>{systemStatus.local_ip}:3000</span>
              </div>
            </div>
          </div>
        </div>

        <div className="sidebar-footer">
          <button onClick={initSession} className="btn-new-session">
            <RotateCcw style={{ width: '15px', height: '15px' }} />
            <span>নতুন সেশন শুরু করো</span>
          </button>
        </div>
      </aside>

      {/* 2. Main Tutoring Stage */}
      <div className="stitch-main">
        {/* Top Navbar */}
        <header className="workspace-topbar">
          <div className="topbar-left">
            <button 
              className="btn-mobile-menu"
              onClick={() => setIsSidebarOpen(true)}
              aria-label="Open sidebar"
            >
              <Menu style={{ width: '18px', height: '18px' }} />
            </button>

            <div className="curriculum-context-badge">
              <span className="badge-grade-pill">৯ম শ্রেণি</span>
              <span className="curriculum-title-text">তথ্য ও যোগাযোগ প্রযুক্তি</span>
              <span className="curriculum-separator">•</span>
              <span className="curriculum-subtitle-text">অধ্যায় ১ ও ২ (NCTB Approved)</span>
            </div>
          </div>

          <div className="topbar-right">
            <div className="offline-status-pill">
              <div className="pulse-circle"></div>
              <span>সম্পূর্ণ অফলাইন (No Internet)</span>
            </div>

            {/* Dark Mode Option Feature */}
            <button
              onClick={toggleTheme}
              className="btn-theme-toggle"
              title={theme === 'dark' ? 'লাইট মোডে পরিবর্তন করো' : 'ডার্ক মোডে পরিবর্তন করো'}
              aria-label="Toggle dark and light mode"
            >
              {theme === 'dark' ? (
                <Sun style={{ width: '18px', height: '18px', color: '#f59e0b' }} />
              ) : (
                <Moon style={{ width: '18px', height: '18px', color: '#0284c7' }} />
              )}
            </button>
          </div>
        </header>

        {/* Chat Stream Canvas */}
        <main className="chat-stage">
          <div className="chat-stage-inner">
            {messages.map((msg, idx) => (
              <div 
                key={msg.id || idx} 
                className={`message-entry ${msg.sender === 'student' ? 'student-entry' : 'tutor-entry'}`}
              >
                {msg.sender === 'student' ? (
                  <div className="student-bubble">
                    {msg.query}
                  </div>
                ) : (
                  <div className="tutor-card">
                    {/* Intent Scope Pill */}
                    {msg.intent_label && (
                      <div className="intent-header-badge">
                        <Sparkles style={{ width: '13px', height: '13px' }} />
                        <span>উদ্দেশ্য: {msg.intent_label}</span>
                      </div>
                    )}

                    {/* Pedagogical Answer Body */}
                    {renderPedagogicalAnswer(msg.answer, msg.intent, msg.intent_label)}

                    {/* Verified NCTB Textbook Citation */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="citation-container">
                        <div className="citation-heading">
                          <Bookmark style={{ width: '13px', height: '13px', color: '#38bdf8' }} />
                          <span>যাচাইকৃত NCTB পাঠ্যবই উৎস (Curriculum Citation):</span>
                        </div>
                        <div className="citation-chips-row">
                          {msg.sources.map((src, sIdx) => (
                            <div key={sIdx} className="citation-card-pill">
                              <span className="citation-ch-tag">অধ্যায় {src.chapter}</span>
                              <span className="citation-topic-text">{src.topic}</span>
                              <span className="citation-page-text">| পৃষ্ঠা: {src.page}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Follow-up Prompts */}
                    {msg.suggested_followups && msg.suggested_followups.length > 0 && (
                      <div className="followups-container">
                        {msg.suggested_followups.map((fQ, fIdx) => (
                          <button
                            key={fIdx}
                            onClick={() => handleSend(fQ)}
                            className="btn-followup"
                          >
                            <Sparkles style={{ width: '12px', height: '12px', color: '#38bdf8' }} />
                            <span>{fQ}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="loading-box">
                <div className="spinner"></div>
                <span>NCTB পাঠ্যবই থেকে শিক্ষকসুলভ উত্তর খোঁজা হচ্ছে...</span>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
        </main>

        {/* Bottom Floating AI Capsule Input Deck */}
        <div className="stitch-bottom-dock">
          {/* Quick Prompts Ribbon */}
          <div className="quick-prompts-ribbon">
            <span className="quick-ribbon-label">
              <HelpCircle style={{ width: '14px', height: '14px' }} />
              <span>কুইক প্রশ্ন:</span>
            </span>
            {quickPrompts.map((qp, qIdx) => (
              <button
                key={qIdx}
                onClick={() => handleSend(qp)}
                className="btn-quick-chip"
              >
                {qp}
              </button>
            ))}
          </div>

          {/* Floating AI Capsule Input */}
          <div className="input-capsule-row">
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="এখানে তোমার আইসিটি প্রশ্নটি বাংলায় লেখো (যেমন: কম্পিউটার ভাইরাস কীভাবে ছড়ায়?)..."
              className="chat-input-field"
            />
            <button
              onClick={() => handleSend()}
              disabled={!inputQuery.trim() || isLoading}
              className="btn-capsule-send"
            >
              <span>প্রশ্ন পাঠাও</span>
              <Send style={{ width: '15px', height: '15px' }} />
            </button>
          </div>

          {/* Classroom Mode Footer */}
          <footer className="dock-footer">
            <span>ল্যাব ক্লাসরুম মোড হটস্পট আইপি: <strong className="hotspot-ip-text">http://{systemStatus.local_ip}:3000</strong></span>
          </footer>
        </div>
      </div>
    </div>
  );
}
