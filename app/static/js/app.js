/* ===== HealthAI Frontend Application ===== */

// ---- Character counter ----
const symptomsTextarea = document.getElementById('symptoms');
const charCount = document.getElementById('charCount');

if (symptomsTextarea) {
  symptomsTextarea.addEventListener('input', () => {
    const len = symptomsTextarea.value.length;
    charCount.textContent = len;
    charCount.style.color = len > 900 ? '#f5576c' : len > 700 ? '#f6d365' : '#a0aec0';
  });
}

// ---- Quick tag injection ----
function addTag(tag) {
  if (!symptomsTextarea) return;
  const current = symptomsTextarea.value.trim();
  symptomsTextarea.value = current ? `${current}, ${tag}` : tag;
  symptomsTextarea.dispatchEvent(new Event('input'));
  symptomsTextarea.focus();
}

// ---- Simple markdown renderer ----
function renderMarkdown(text) {
  if (!text) return '';
  return text
    // Headers
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Inline code
    .replace(/`(.+?)`/g, '<code>$1</code>')
    // Unordered lists
    .replace(/^\s*[-*•] (.+)$/gm, '<li>$1</li>')
    // Ordered lists
    .replace(/^\s*\d+\. (.+)$/gm, '<li>$1</li>')
    // Wrap consecutive <li> in <ul>
    .replace(/(<li>.*<\/li>\n?)+/g, match => `<ul>${match}</ul>`)
    // Line breaks to paragraphs
    .replace(/\n\n+/g, '</p><p>')
    .replace(/^(?!<[hul])(.+)$/gm, (m) => m.startsWith('<') ? m : `<p>${m}</p>`)
    // Clean up empty paragraphs
    .replace(/<p><\/p>/g, '')
    .replace(/<p>(<[hul])/g, '$1')
    .replace(/(<\/[hul][^>]*>)<\/p>/g, '$1');
}

// ---- Agent progress animation ----
const agentOrder = ['researcher', 'planner', 'scheduler', 'summarizer'];
let progressInterval = null;
let currentStep = 0;

function startProgressAnimation() {
  currentStep = 0;
  agentOrder.forEach(agent => {
    const step = document.getElementById(`step-${agent}`);
    if (step) {
      step.classList.remove('active', 'done');
      const statusEl = step.querySelector('.step-status');
      statusEl.classList.add('waiting');
      statusEl.innerHTML = '<i class="fas fa-clock"></i>';
    }
  });

  // Activate first step immediately
  activateStep(0);

  // Simulate progress (real progress comes from API response)
  progressInterval = setInterval(() => {
    currentStep++;
    if (currentStep < agentOrder.length) {
      markStepDone(currentStep - 1);
      activateStep(currentStep);
    } else {
      clearInterval(progressInterval);
    }
  }, 4000);
}

function activateStep(index) {
  if (index >= agentOrder.length) return;
  const step = document.getElementById(`step-${agentOrder[index]}`);
  if (!step) return;
  step.classList.add('active');
  const statusEl = step.querySelector('.step-status');
  statusEl.classList.remove('waiting');
  statusEl.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';
}

function markStepDone(index) {
  if (index < 0 || index >= agentOrder.length) return;
  const step = document.getElementById(`step-${agentOrder[index]}`);
  if (!step) return;
  step.classList.remove('active');
  step.classList.add('done');
  const statusEl = step.querySelector('.step-status');
  statusEl.classList.remove('waiting');
  statusEl.classList.add('done-icon');
  statusEl.innerHTML = '<i class="fas fa-check-circle"></i>';
}

function completeAllSteps() {
  clearInterval(progressInterval);
  agentOrder.forEach((_, i) => markStepDone(i));
}

// ---- Tab switching ----
function showTab(tabName, btn) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  document.getElementById(`tab-${tabName}`).classList.add('active');
  btn.classList.add('active');
}

// ---- Scroll to section ----
function scrollToResults() {
  const el = document.getElementById('resultsSection');
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ---- Print report ----
function printReport() {
  const content = document.getElementById('summaryContent').innerText;
  const win = window.open('', '_blank');
  win.document.write(`
    <html><head><title>HealthAI Report</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; }
      h1, h2, h3 { color: #333; }
      p { line-height: 1.7; }
      ul { padding-left: 20px; }
    </style></head>
    <body><pre style="white-space:pre-wrap; font-family:Arial;">${content}</pre></body></html>
  `);
  win.document.close();
  win.print();
}

// ---- Copy report ----
function copyReport() {
  const content = document.getElementById('summaryContent').innerText;
  navigator.clipboard.writeText(content).then(() => {
    showToast('Report copied to clipboard!', 'success');
  }).catch(() => {
    showToast('Copy failed. Please select and copy manually.', 'error');
  });
}

// ---- Reset form ----
function resetForm() {
  document.getElementById('healthForm').reset();
  document.getElementById('resultsSection').style.display = 'none';
  document.getElementById('progressSection').style.display = 'none';
  if (charCount) charCount.textContent = '0';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ---- Toast notification ----
function showToast(message, type = 'info') {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
    <span>${message}</span>
  `;
  toast.style.cssText = `
    position: fixed; bottom: 32px; right: 32px; z-index: 9999;
    background: ${type === 'success' ? 'rgba(67,233,123,0.15)' : type === 'error' ? 'rgba(245,87,108,0.15)' : 'rgba(102,126,234,0.15)'};
    border: 1px solid ${type === 'success' ? 'rgba(67,233,123,0.4)' : type === 'error' ? 'rgba(245,87,108,0.4)' : 'rgba(102,126,234,0.4)'};
    color: #f0f4ff; padding: 14px 20px; border-radius: 12px;
    display: flex; align-items: center; gap: 10px;
    font-family: Inter, sans-serif; font-size: 0.9rem;
    backdrop-filter: blur(20px);
    animation: slideIn 0.3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ---- Main form submission ----
const healthForm = document.getElementById('healthForm');

if (healthForm) {
  healthForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const symptoms = document.getElementById('symptoms').value.trim();
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const medicalHistory = document.getElementById('medical_history').value.trim();

    if (!symptoms) {
      showToast('Please describe your symptoms.', 'error');
      return;
    }

    // Build patient info string
    const patientParts = [];
    if (age) patientParts.push(`Age: ${age}`);
    if (gender) patientParts.push(`Gender: ${gender}`);
    if (medicalHistory) patientParts.push(`Medical History: ${medicalHistory}`);
    const patientInfo = patientParts.join(' | ');

    // UI state: loading
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').style.display = 'none';
    submitBtn.querySelector('.btn-loading').style.display = 'flex';

    // Show progress section
    const progressSection = document.getElementById('progressSection');
    progressSection.style.display = 'block';
    progressSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Hide previous results
    document.getElementById('resultsSection').style.display = 'none';

    // Start progress animation
    startProgressAnimation();

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms, patient_info: patientInfo }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || 'Analysis failed. Please try again.');
      }

      // Complete all steps
      completeAllSteps();

      // Populate results
      const { research, plan, schedule, summary } = result.data;

      document.getElementById('summaryContent').innerHTML = renderMarkdown(summary);
      document.getElementById('researchContent').innerHTML = renderMarkdown(research);
      document.getElementById('planContent').innerHTML = renderMarkdown(plan);
      document.getElementById('scheduleContent').innerHTML = renderMarkdown(schedule);

      // Show results after short delay
      setTimeout(() => {
        progressSection.style.display = 'none';
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        showToast('Analysis complete! Your health report is ready.', 'success');
      }, 1200);

    } catch (err) {
      clearInterval(progressInterval);
      progressSection.style.display = 'none';
      showToast(err.message || 'Something went wrong. Please try again.', 'error');
      console.error('Analysis error:', err);
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-text').style.display = 'flex';
      submitBtn.querySelector('.btn-loading').style.display = 'none';
    }
  });
}

// ---- Smooth scroll for nav links ----
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ---- Intersection observer for animations ----
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .how-step, .agent-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// ---- CSS animation for toast ----
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
`;
document.head.appendChild(style);
