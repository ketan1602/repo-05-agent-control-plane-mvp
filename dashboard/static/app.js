// Shared nav helpers
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === location.pathname) a.classList.add('active');
});

function formatStatus(status) {
  const labels = {
    registered: ['muted', 'Registered'],
    policy_pending: ['warning', 'Policy Pending'],
    policy_confirmed: ['success', 'Confirmed'],
  };
  const [cls, label] = labels[status] || ['muted', status];
  return `<span class="status-dot status-${status}"></span><span class="text-${cls}">${label}</span>`;
}
