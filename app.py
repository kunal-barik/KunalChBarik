import streamlit as st
import time
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
from streamlit.components.v1 import html

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.ensemble_ai import ProfessionalEnsembleAI, PredictionResult
from src.core.knowledge_graph import KnowledgeGraphVerifier
from src.core.multi_source import MultiSourceVerifier
from src.analytics.dashboard import AdvancedDashboard
from src.analytics.explainable_ai import ExplainableAI
from src.data.database import AnalysisDatabase
from src.utils.helpers import clean_text, format_confidence, get_verdict_color
from config import config

# Page configuration
st.set_page_config(
    page_title="NEXUS TRUTH VERIFIER PRO",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS with DiscoveryLandCo-inspired design
st.markdown("""
<style>
/* — DiscoveryLandCo-inspired premium CSS — */

/* VARIABLES / THEME */
:root {
  --clr-bg: #0a0a0c;
  --clr-dark: #0f0f14;
  --clr-light: #f5f5f5;
  --clr-muted: #aaa;
  --clr-accent: #00ffff;
  --clr-accent-secondary: #ff00ff;
  --clr-accent-gold: #ffd700;
  --clr-overlay: rgba(0, 0, 0, 0.7);

  --font-sans: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "SF Mono", Monaco, Inconsolata, monospace;

  --fs-small: 0.875rem;
  --fs-base: 1rem;
  --fs-lg: 1.25rem;
  --fs-xl: 2.5rem;
  --fs-xxl: 4rem;

  --max-width: 1400px;
  --gutter: 40px;

  --transition-base: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --transition-fast: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* RESET / BASES */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.stApp {
  background: linear-gradient(135deg, var(--clr-bg) 0%, var(--clr-dark) 50%, #1a1a2e 100%);
  color: var(--clr-light);
  font-family: var(--font-sans);
  line-height: 1.6;
  overflow-x: hidden;
}

/* ANIMATED GRID BACKGROUND */
.cyber-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(180deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
  pointer-events: none;
  z-index: -2;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* FLOATING PARTICLES */
.floating-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
}

.particle {
  position: absolute;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

/* PREMIUM HEADER - Hero Section */
.premium-header {
  position: relative;
  background: linear-gradient(135deg, 
      rgba(0, 255, 255, 0.1) 0%, 
      rgba(138, 43, 226, 0.1) 50%, 
      rgba(255, 0, 128, 0.1) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0 0 40px 40px;
  padding: 6rem 2rem 4rem;
  margin: 0 0 3rem;
  text-align: center;
  overflow: hidden;
  animation: slideIn 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.premium-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
      transparent, 
      rgba(255, 255, 255, 0.1), 
      transparent);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

.premium-header h1 {
  font-size: var(--fs-xxl);
  font-weight: 800;
  background: linear-gradient(135deg, var(--clr-accent) 0%, var(--clr-accent-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  line-height: 1.1;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  animation: glow 3s ease-in-out infinite alternate;
}

@keyframes glow {
  0% { text-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
  100% { text-shadow: 0 0 40px rgba(255, 0, 255, 0.7); }
}

.premium-header p {
  font-size: var(--fs-lg);
  color: rgba(255, 255, 255, 0.8);
  font-weight: 300;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* CYBER CARDS - Premium Card Design */
.cyber-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem;
  margin: 2rem 0;
  position: relative;
  overflow: hidden;
  transition: var(--transition-base);
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.cyber-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
      transparent, 
      var(--clr-accent), 
      var(--clr-accent-secondary), 
      transparent);
}

.cyber-card:hover {
  transform: translateY(-8px);
  border-color: rgba(0, 255, 255, 0.3);
  box-shadow: 
    0 20px 40px rgba(0, 255, 255, 0.15),
    0 0 80px rgba(0, 255, 255, 0.05);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* PREMIUM BUTTONS */
.premium-button {
  background: linear-gradient(135deg, var(--clr-accent) 0%, var(--clr-accent-secondary) 100%);
  border: none;
  border-radius: 16px;
  padding: 1.2rem 2.5rem;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: var(--transition-base);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: var(--font-mono);
}

.premium-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
      transparent, 
      rgba(255, 255, 255, 0.3), 
      transparent);
  transition: left 0.6s;
}

.premium-button:hover::before {
  left: 100%;
}

.premium-button:hover {
  transform: translateY(-3px);
  box-shadow: 
    0 15px 30px rgba(0, 255, 255, 0.3),
    0 0 40px rgba(255, 0, 255, 0.2);
}

/* DEVELOPER SECTION - Premium Design */
.developer-section {
  background: linear-gradient(135deg, 
      rgba(255, 215, 0, 0.1) 0%, 
      rgba(255, 140, 0, 0.1) 50%, 
      rgba(255, 69, 0, 0.1) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 32px;
  padding: 3rem;
  margin: 3rem 0;
  position: relative;
  overflow: hidden;
  animation: fadeInUp 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.developer-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
      transparent, 
      var(--clr-accent-gold), 
      #ff8c00, 
      transparent);
}

.developer-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(255, 215, 0, 0.2);
  transition: var(--transition-base);
}

/* TECH BADGES */
.tech-badge {
  display: inline-block;
  background: rgba(0, 255, 255, 0.15);
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  margin: 0.3rem;
  color: var(--clr-accent);
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(0, 255, 255, 0.3);
  transition: var(--transition-fast);
  font-family: var(--font-mono);
}

.tech-badge:hover {
  background: rgba(0, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 255, 255, 0.2);
}

/* METRIC CARDS */
[data-testid="metric-container"] {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 20px !important;
  padding: 1.5rem !important;
  transition: var(--transition-base);
}

[data-testid="metric-container"]:hover {
  transform: translateY(-5px);
  border-color: rgba(0, 255, 255, 0.3) !important;
  box-shadow: 0 15px 30px rgba(0, 255, 255, 0.1);
}

/* TEXT AREAS */
.stTextArea textarea {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 16px !important;
  padding: 1.5rem !important;
  color: white !important;
  font-size: 1.1rem;
  transition: var(--transition-base);
  resize: vertical;
  min-height: 150px;
}

.stTextArea textarea:focus {
  border-color: var(--clr-accent) !important;
  box-shadow: 
    0 0 0 2px rgba(0, 255, 255, 0.2),
    0 0 30px rgba(0, 255, 255, 0.1) !important;
  background: rgba(255, 255, 255, 0.08) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 0.5rem;
  gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 12px !important;
  padding: 0.75rem 1.5rem !important;
  transition: var(--transition-fast);
}

.stTabs [data-baseweb="tab"]:hover {
  background: rgba(0, 255, 255, 0.1) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--clr-accent) 0%, var(--clr-accent-secondary) 100%) !important;
  color: white !important;
}

/* PROGRESS BARS */
.stProgress > div > div > div > div {
  background: linear-gradient(135deg, var(--clr-accent) 0%, var(--clr-accent-secondary) 100%) !important;
  border-radius: 10px;
  animation: progressGlow 2s ease-in-out infinite;
}

@keyframes progressGlow {
  0%, 100% { 
    box-shadow: 0 0 10px var(--clr-accent);
  }
  50% { 
    box-shadow: 0 0 20px var(--clr-accent-secondary);
  }
}

/* RESULT STATES */
.result-true {
  background: linear-gradient(135deg, 
      rgba(0, 255, 157, 0.1) 0%, 
      rgba(0, 255, 157, 0.2) 100%) !important;
  border: 1px solid rgba(0, 255, 157, 0.3) !important;
  animation: glow 2s ease-in-out infinite;
}

.result-false {
  background: linear-gradient(135deg, 
      rgba(255, 0, 128, 0.1) 0%, 
      rgba(255, 0, 128, 0.2) 100%) !important;
  border: 1px solid rgba(255, 0, 128, 0.3) !important;
  animation: glow 2s ease-in-out infinite;
}

.result-uncertain {
  background: linear-gradient(135deg, 
      rgba(255, 255, 0, 0.1) 0%, 
      rgba(255, 255, 0, 0.2) 100%) !important;
  border: 1px solid rgba(255, 255, 0, 0.3) !important;
  animation: glow 2s ease-in-out infinite;
}

/* CUSTOM SCROLLBAR */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--clr-accent) 0%, var(--clr-accent-secondary) 100%);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--clr-accent-secondary) 0%, var(--clr-accent) 100%);
}

/* LOADING ANIMATION */
.loading-dots {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
}

.loading-dots div {
  position: absolute;
  top: 33px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--clr-accent);
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
  box-shadow: 0 0 10px var(--clr-accent);
}

.loading-dots div:nth-child(1) {
  left: 8px;
  animation: loading-dots1 0.6s infinite;
}

.loading-dots div:nth-child(2) {
  left: 8px;
  animation: loading-dots2 0.6s infinite;
}

.loading-dots div:nth-child(3) {
  left: 32px;
  animation: loading-dots2 0.6s infinite;
}

.loading-dots div:nth-child(4) {
  left: 56px;
  animation: loading-dots3 0.6s infinite;
}

@keyframes loading-dots1 {
  0% { transform: scale(0); }
  100% { transform: scale(1); }
}

@keyframes loading-dots3 {
  0% { transform: scale(1); }
  100% { transform: scale(0); }
}

@keyframes loading-dots2 {
  0% { transform: translate(0, 0); }
  100% { transform: translate(24px, 0); }
}

/* FEATURE BADGES */
.feature-badge {
  display: inline-block;
  background: rgba(0, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  margin: 0.25rem;
  font-size: 0.8rem;
  color: var(--clr-light);
}

/* RESPONSIVE DESIGN */
@media (max-width: 768px) {
  .premium-header {
    padding: 4rem 1rem 2rem;
    border-radius: 0 0 20px 20px;
  }
  
  .premium-header h1 {
    font-size: 2.5rem;
  }
  
  .premium-header p {
    font-size: 1.1rem;
  }
  
  .cyber-card {
    padding: 1.5rem;
    margin: 1rem 0;
    border-radius: 16px;
  }
  
  .developer-section {
    padding: 2rem;
    margin: 2rem 0;
    border-radius: 20px;
  }
}

/* HIDE STREAMLIT DEFAULTS */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

</style>

<div class="cyber-grid"></div>
<div class="floating-particles" id="particles"></div>
""", unsafe_allow_html=True)

# JavaScript for floating particles
particles_js = """
<script>
// Create floating particles
function createParticles() {
    const container = document.getElementById('particles');
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 6 + 2;
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const delay = Math.random() * 10;
        const duration = Math.random() * 8 + 6;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}vw`;
        particle.style.top = `${posY}vh`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        
        // Random colors
        const colors = ['rgba(0, 255, 255, 0.3)', 'rgba(255, 0, 255, 0.3)', 'rgba(255, 215, 0, 0.3)'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        container.appendChild(particle);
    }
}

// Initialize particles when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createParticles);
} else {
    createParticles();
}
</script>
"""

html(particles_js, height=0)

class EnhancedNexusVerifier:
    def __init__(self):
        self.ai_system = ProfessionalEnsembleAI()
        self.knowledge_graph = KnowledgeGraphVerifier()
        self.multi_source = MultiSourceVerifier()
        self.dashboard = AdvancedDashboard()
        self.explainable_ai = ExplainableAI()
        self.database = AnalysisDatabase()
        
        # Initialize session state
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []
        if 'current_analysis' not in st.session_state:
            st.session_state.current_analysis = None
    
    def render_enhanced_header(self):
        """Render premium header with DiscoveryLandCo-inspired design"""
        st.markdown("""
        <div class="premium-header">
            <h1>🔮 NEXUS TRUTH VERIFIER PRO</h1>
            <p>Advanced AI-Powered Multi-Model Fact Verification System</p>
            <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 12px; height: 12px; background: #00ffff; border-radius: 50%; animation: pulse 2s infinite;"></div>
                    <span style="color: rgba(255,255,255,0.8);">Ensemble AI</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 12px; height: 12px; background: #ff00ff; border-radius: 50%; animation: pulse 2s infinite 0.5s;"></div>
                    <span style="color: rgba(255,255,255,0.8);">Knowledge Graph</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 12px; height: 12px; background: #ffd700; border-radius: 50%; animation: pulse 2s infinite 1s;"></div>
                    <span style="color: rgba(255,255,255,0.8);">Multi-Source</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="width: 12px; height: 12px; background: #00ff9d; border-radius: 50%; animation: pulse 2s infinite 1.5s;"></div>
                    <span style="color: rgba(255,255,255,0.8);">Advanced Analytics</span>
                </div>
            </div>
        </div>
        
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_system_status(self):
        """Render premium system status with real metrics"""
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #00ffff; font-size: 1.5rem; margin-bottom: 2rem;">SYSTEM STATUS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get real metrics from database
        analytics = self.database.get_analytics()
        system_metrics = self.ai_system.get_system_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 TOTAL ANALYSES", 
                value=analytics['total_analyses'], 
                delta="Live"
            )
        with col2:
            st.metric(
                label="🎯 ACCURACY RATE", 
                value=f"{analytics['accuracy_estimate']}%", 
                delta="Professional Grade"
            )
        with col3:
            st.metric(
                label="⚡ AVG CONFIDENCE", 
                value=f"{analytics['avg_confidence']}%", 
                delta="High Precision"
            )
        with col4:
            st.metric(
                label="🔄 SYSTEM UPTIME", 
                value=system_metrics['system_uptime'], 
                delta="Stable"
            )
    
    def render_analysis_interface(self):
        """Render enhanced analysis interface"""
        st.markdown("""
        <div class="cyber-card">
            <h3 style="color: #00ffff; margin-bottom: 1rem;">🔍 ADVANCED TRUTH ANALYSIS</h3>
        """, unsafe_allow_html=True)
        
        # Text input
        text_input = st.text_area(
            "Enter statement for comprehensive verification:",
            height=150,
            placeholder="Paste any claim, news headline, or statement here...\nExamples:\n• 'The Earth is flat'\n• 'Vaccines cause autism'\n• 'AI will achieve consciousness by 2025'\n• 'We never landed on the moon'",
            key="enhanced_input"
        )
        
        # Analysis options
        col1, col2, col3 = st.columns(3)
        with col1:
            enable_knowledge_graph = st.checkbox("🌐 Knowledge Graph", value=True)
        with col2:
            enable_multi_source = st.checkbox("🔗 Multi-Source", value=True)
        with col3:
            enable_deep_analysis = st.checkbox("🧠 Deep Analysis", value=True)
        
        # Action buttons
        col1, col2 = st.columns([3, 1])
        with col1:
            analyze_clicked = st.button(
                "🚀 INITIATE COMPREHENSIVE ANALYSIS",
                use_container_width=True,
                type="primary"
            )
        with col2:
            if st.button("🔄 CLEAR", use_container_width=True):
                st.session_state.current_analysis = None
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        return text_input, analyze_clicked, {
            'knowledge_graph': enable_knowledge_graph,
            'multi_source': enable_multi_source,
            'deep_analysis': enable_deep_analysis
        }
    
    def perform_comprehensive_analysis(self, text: str, options: dict):
        """Perform comprehensive analysis with progress tracking"""
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        steps = [
            "🔮 Initializing Enhanced AI System...",
            "🧠 Loading Advanced Models...",
            "🌐 Connecting to Knowledge Graph...",
            "🔗 Querying Multi-Source Databases...",
            "📊 Analyzing Linguistic Patterns...",
            "🔍 Cross-Referencing Evidence...",
            "⚡ Generating Comprehensive Assessment...",
            "✅ Analysis Complete!"
        ]
        
        results = {}
        
        for i, step in enumerate(steps):
            status_container.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 1.5rem; margin-bottom: 1rem; color: #00ffff;">{step}</div>
                <div class="loading-dots">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            progress = (i + 1) * (100 // len(steps))
            progress_bar.progress(progress)
            
            # Perform actual work at certain steps
            if i == 1:  # After loading models
                results['ai_analysis'] = self.ai_system.ensemble_predict(text)
            
            if i == 2 and options['knowledge_graph']:
                entities = self.knowledge_graph.extract_entities(text)
                results['knowledge_evidence'] = self.knowledge_graph.verify_against_knowledge(text, entities)
            
            if i == 3 and options['multi_source']:
                results['multi_source'] = self.multi_source.verify_claim(text)
            
            time.sleep(0.8)
        
        # Generate explanations
        if options['deep_analysis'] and 'ai_analysis' in results:
            results['explanation'] = self.explainable_ai.generate_explanation(
                results['ai_analysis'], text
            )
        
        status_container.empty()
        return results
    
    def display_enhanced_results(self, results: dict, text: str):
        """Display comprehensive results"""
        if not results.get('ai_analysis'):
            st.error("❌ Analysis failed. Please try again.")
            return
        
        ai_result = results['ai_analysis']
        
        # Main verdict display
        self._display_main_verdict(ai_result)
        
        # Detailed analysis in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Detailed Analysis", 
            "🧠 AI Explanation", 
            "🌐 Evidence", 
            "📈 Analytics"
        ])
        
        with tab1:
            self._display_detailed_analysis(ai_result, results)
        
        with tab2:
            self._display_ai_explanation(results.get('explanation'))
        
        with tab3:
            self._display_evidence(results, text)
        
        with tab4:
            self._display_analytics(ai_result, results)
        
        # Save to history
        self._save_to_history(text, ai_result, results)
    
    def _display_main_verdict(self, ai_result: PredictionResult):
        """Display main verdict with enhanced visualization"""
        verdict_color = get_verdict_color(ai_result.verdict)
        
        st.markdown(f"""
        <div class="cyber-card" style="border-color: {verdict_color}; animation: glow 2s ease-in-out infinite;">
            <div style="text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">
                    {"✅" if ai_result.verdict == 'true' else "❌" if ai_result.verdict == 'false' else "⚠️"}
                </div>
                <h1 style="color: {verdict_color}; margin-bottom: 0.5rem; font-size: 3rem;">
                    {ai_result.verdict.upper()} VERDICT
                </h1>
                <div style="font-size: 2rem; opacity: 0.9;">
                    Confidence: {format_confidence(ai_result.confidence)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence gauge
        fig = self.dashboard.create_verdict_gauge(ai_result.confidence, ai_result.verdict)
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_detailed_analysis(self, ai_result: PredictionResult, results: dict):
        """Display detailed analysis"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🧠 Ensemble Model Probabilities")
            fig = self.dashboard.create_model_comparison(ai_result.probabilities)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Text Feature Analysis")
            fig = self.dashboard.create_feature_analysis(ai_result.features)
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature badges
            st.markdown("#### 🔍 Key Features")
            for feature, value in ai_result.features.items():
                st.markdown(f"""
                <div class="feature-badge">
                    <strong>{feature}:</strong> {value:.2f}
                </div>
                """, unsafe_allow_html=True)
    
    def _display_ai_explanation(self, explanation: dict):
        """Display AI explanation"""
        if not explanation:
            st.info("Deep analysis was not enabled for this verification.")
            return
        
        st.markdown("#### 📖 Verdict Explanation")
        st.write(explanation['verdict_explanation'])
        
        st.markdown("#### 🎯 Confidence Factors")
        for factor in explanation['confidence_breakdown']:
            st.write(f"• {factor}")
        
        st.markdown("#### 💡 Key Decision Factors")
        for factor in explanation['key_factors']:
            st.write(f"• {factor}")
        
        st.markdown("#### 🛠️ Recommendations")
        for recommendation in explanation['recommendations']:
            st.info(f"💡 {recommendation}")
        
        st.markdown("#### 🔄 Counterfactual Analysis")
        for cf in explanation['counterfactuals']:
            with st.expander(f"What if this was {cf['target_verdict']}?"):
                st.write(cf['modification_suggestion'])
    
    def _display_evidence(self, results: dict, text: str):
        """Display evidence from various sources"""
        col1, col2 = st.columns(2)
        
        with col1:
            if results.get('knowledge_evidence'):
                st.markdown("#### 🌐 Knowledge Graph Evidence")
                evidence = results['knowledge_evidence']
                
                st.metric("Knowledge Confidence", format_confidence(evidence.confidence))
                
                if evidence.supporting_facts:
                    st.markdown("**Supporting Facts:**")
                    for fact in evidence.supporting_facts[:3]:
                        st.write(f"• {fact}")
                
                if evidence.related_entities:
                    st.markdown("**Related Entities:**")
                    for entity in evidence.related_entities[:5]:
                        st.write(f"• {entity}")
        
        with col2:
            if results.get('multi_source'):
                st.markdown("#### 🔗 Multi-Source Verification")
                multi_source = results['multi_source']
                
                st.metric("Sources Checked", multi_source['sources_checked'])
                st.metric("Source Consensus", multi_source['final_verdict'])
                
                for source in multi_source['source_breakdown']:
                    with st.expander(f"{source['source'].title()} - {source['verdict']}"):
                        st.write(f"Confidence: {format_confidence(source['confidence'])}")
                        if source['evidence']:
                            st.write("Evidence:", source['evidence'][0])
    
    def _display_analytics(self, ai_result: PredictionResult, results: dict):
        """Display advanced analytics with real data"""
        st.markdown("#### 📊 PERFORMANCE ANALYTICS")
        
        # Get real analytics
        analytics = self.database.get_analytics()
        system_metrics = self.ai_system.get_system_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", analytics['total_analyses'])
        with col2:
            st.metric("Accuracy Rate", f"{analytics['accuracy_estimate']}%")
        with col3:
            st.metric("Avg Confidence", f"{analytics['avg_confidence']}%")
        with col4:
            st.metric("Processing Time", f"{ai_result.processing_time:.2f}s")
        
        # Model performance
        st.markdown("#### 🤖 MODEL PERFORMANCE")
        performance = self.ai_system.get_model_performance()
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            ('DeBERTa', performance['deberta']),
            ('RoBERTa', performance['roberta']),
            ('ELECTRA', performance['electra']),
            ('BERT', performance['bert'])
        ]
        
        for i, (name, data) in enumerate(metrics):
            with [col1, col2, col3, col4][i]:
                st.metric(f"{name} Accuracy", f"{data['accuracy']*100:.1f}%")
                st.metric("Status", data['status'])
        
        # Historical analysis
        st.markdown("#### 📈 SYSTEM ANALYTICS")
        fig = self.dashboard.create_timeline_analysis([])
        st.plotly_chart(fig, use_container_width=True)
    
    def _save_to_history(self, text: str, ai_result: PredictionResult, results: dict):
        """Save analysis to database and session state"""
        analysis_record = {
            'timestamp': datetime.now().isoformat(),
            'text': text,
            'verdict': ai_result.verdict,
            'confidence': ai_result.confidence,
            'features': ai_result.features,
            'processing_time': ai_result.processing_time
        }
        
        # Save to database
        self.database.save_analysis(
            statement=text,
            verdict=ai_result.verdict,
            confidence=ai_result.confidence,
            model_used=ai_result.model_used
        )
        
        # Save to session state
        st.session_state.analysis_history.append(analysis_record)
        st.session_state.current_analysis = analysis_record
    
    def render_developer_section(self):
        """Render premium developer section"""
        st.markdown("""
        <div class="developer-section">
            <h2 style="color: #ffd700; text-align: center; margin-bottom: 3rem; font-size: 2.5rem;">🚀 DEVELOPED BY</h2>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Developer Profile
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h3 style="color: #ffd700; font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 700;">Kunal Chandra Barik</h3>
                <p style="color: rgba(255,255,255,0.8); font-size: 1.3rem; margin-bottom: 2rem; font-weight: 300;">
                    AI Developer & Full Stack Engineer
                </p>
            """, unsafe_allow_html=True)
            
            # Social Links
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.button("💼 LinkedIn Profile", use_container_width=True, key="linkedin_btn"):
                    st.markdown("[Visit LinkedIn](https://www.linkedin.com/in/kunalchandrabarik)")
            with col_s2:
                if st.button("📂 GitHub Portfolio", use_container_width=True, key="github_btn"):
                    st.markdown("[Visit GitHub](https://github.com/kunal-barik/KunalChBarik)")
            
            # Skills & Technologies
            st.markdown("""
            <div style="margin-top: 3rem;">
                <h4 style="color: #ffd700; text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem;">🛠 TECHNOLOGIES USED</h4>
                <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 0.8rem; margin-top: 1.5rem;">
                    <span class="tech-badge">Transformers</span>
                    <span class="tech-badge" style="background: rgba(255,0,255,0.15); color: #ff00ff; border-color: rgba(255,0,255,0.3);">PyTorch</span>
                    <span class="tech-badge" style="background: rgba(255,215,0,0.15); color: #ffd700; border-color: rgba(255,215,0,0.3);">Streamlit</span>
                    <span class="tech-badge" style="background: rgba(0,255,157,0.15); color: #00ff9d; border-color: rgba(0,255,157,0.3);">Plotly</span>
                    <span class="tech-badge" style="background: rgba(255,100,0,0.15); color: #ff6400; border-color: rgba(255,100,0,0.3);">Ensemble AI</span>
                    <span class="tech-badge" style="background: rgba(138,43,226,0.15); color: #8a2be2; border-color: rgba(138,43,226,0.3);">Knowledge Graph</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Project Description
            st.markdown("""
            <div style="margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);">
                <h4 style="color: #ffd700; margin-bottom: 1.5rem; font-size: 1.4rem; text-align: center;">🎯 ABOUT THIS PROJECT</h4>
                <p style="color: rgba(255,255,255,0.8); line-height: 1.7; font-size: 1.1rem; text-align: center;">
                    <strong>Nexus Truth Verifier Pro</strong> is an enterprise-grade AI-powered fact verification system 
                    that combines cutting-edge transformer models with knowledge graph technology and multi-source 
                    analysis to deliver accurate truth assessments with unprecedented precision.
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem;">
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
                        <div style="color: #00ffff; font-weight: 600;">Ensemble AI</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
                        <div style="color: #ff00ff; font-weight: 600;">Knowledge Graph</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
                        <div style="color: #ffd700; font-weight: 600;">Multi-Source</div>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                        <div style="color: #00ff9d; font-weight: 600;">Analytics</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    def run(self):
        """Run the enhanced application"""
        self.render_enhanced_header()
        self.render_system_status()
        
        text_input, analyze_clicked, options = self.render_analysis_interface()
        
        if analyze_clicked and text_input.strip():
            cleaned_text = clean_text(text_input)
            results = self.perform_comprehensive_analysis(cleaned_text, options)
            self.display_enhanced_results(results, cleaned_text)
        
        # Render developer section
        self.render_developer_section()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.5);">
            <p>NEXUS TRUTH VERIFIER PRO | ENTERPRISE AI FACT VERIFICATION SYSTEM</p>
            <p style="font-size: 0.8rem; margin-top: 1rem;">
                🔮 Enhanced Ensemble AI • 🌐 Knowledge Graph • 🔗 Multi-Source • 📊 Advanced Analytics • 🧠 Explainable AI
            </p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    # Initialize the enhanced verifier
    verifier = EnhancedNexusVerifier()
    verifier.run()