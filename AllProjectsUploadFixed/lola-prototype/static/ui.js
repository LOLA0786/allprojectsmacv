window.socket = io();

// Simple SuperConnect modal build + helpers
window.showSuperConnectModal = function(opts){
  opts = opts || {};
  if(document.getElementById('sc-modal')) return;
  const m = document.createElement('div');
  m.id = 'sc-modal';
  m.className = 'modal';
  m.innerHTML = `<div class="modal-panel">
    <h3>SuperConnect</h3>
    <p>Connect 1:1 with someone thinking about: <strong>${(opts.context||'this topic')}</strong></p>
    <div style="display:flex;gap:8px;margin-top:12px">
      <button class="btn" id="sc-yes">Try SuperConnect</button>
      <button class="btn" id="sc-no">Close</button>
    </div>
  </div>`;
  document.body.appendChild(m);
  document.getElementById('sc-no').onclick = ()=> m.remove();
  document.getElementById('sc-yes').onclick = async ()=>{
    // fire a quick fetch to enhanced endpoint (mock user id)
    const uid = 'ui_'+Math.random().toString(36).slice(2,8);
    const payload = {user: uid, text: opts.context || 'superconnect', try_superconnect:true};
    const r = await fetch('/api/stream_intent_enh', {method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(payload)});
    const j = await r.json();
    if(j && j.superconnect && j.room){
      alert('SuperConnect matched! Opening room: ' + j.room);
      window.location.href = '/room/' + j.room;
    } else {
      alert('No immediate match. We will keep looking.');
    }
  };
};

// small helper to toggle modal from elements with data-superconnect
document.addEventListener('click', (e)=>{
  if(e.target && e.target.dataset && e.target.dataset.sc){
    showSuperConnectModal({context:e.target.dataset.sc});
  }
});
