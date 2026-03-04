/* ═══════════════════════════════════════════════════
   Cortex KB · Client Application
   ═══════════════════════════════════════════════════ */
(function () {
  "use strict";

  /* ── DOM refs ── */
  const $  = (s, p) => (p || document).querySelector(s);
  const $$ = (s, p) => [...(p || document).querySelectorAll(s)];

  const navBtns      = $$(".nav-btn");
  const views        = $$(".view");
  const libraryGrid  = $("#library-grid");
  const libraryEmpty = $("#library-empty");
  const filterBar    = $(".filter-bar");
  const searchInput  = $("#search-input");
  const searchGo     = $("#search-go");
  const searchResults= $("#search-results");
  const searchEmpty  = $("#search-empty");
  const modalOverlay = $("#modal-overlay");
  const modalCard    = $("#modal-card");
  const toastBox     = $("#toast-container");

  /* ── State ── */
  let allDocs = [];
  let categories = new Set();
  let activeCategory = "all";

  /* ═══════════════════════════════════════════════
     API helpers
     ═══════════════════════════════════════════════ */
  async function api(path, opts) {
    const res = await fetch(path, opts);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  /* ═══════════════════════════════════════════════
     NAVIGATION
     ═══════════════════════════════════════════════ */
  navBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.view;
      navBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      views.forEach((v) => {
        v.classList.toggle("active", v.id === `view-${target}`);
      });
      if (target === "graph") drawGraph();
    });
  });

  /* ═══════════════════════════════════════════════
     STATS
     ═══════════════════════════════════════════════ */
  async function loadStats() {
    try {
      const s = await api("/api/stats");
      $("#stat-nodes").textContent      = s.total_nodes;
      $("#stat-edges").textContent      = s.total_edges;
      $("#stat-categories").textContent = Object.keys(s.node_types).length;
      $("#stat-types").textContent      = Object.keys(s.relationship_types).length;
    } catch { /* silent */ }
  }

  /* ═══════════════════════════════════════════════
     LIBRARY
     ═══════════════════════════════════════════════ */
  async function loadLibrary() {
    try {
      allDocs = await api("/api/documents");
    } catch {
      allDocs = [];
    }
    categories = new Set(allDocs.map((d) => d.category || "general"));
    renderFilterChips();
    renderCards();
  }

  function renderFilterChips() {
    filterBar.innerHTML = "";
    const all = chip("All", "all");
    if (activeCategory === "all") all.classList.add("active");
    filterBar.appendChild(all);
    [...categories].sort().forEach((c) => {
      const el = chip(c, c);
      if (activeCategory === c) el.classList.add("active");
      filterBar.appendChild(el);
    });
  }

  function chip(label, value) {
    const b = document.createElement("button");
    b.className = "filter-chip";
    b.textContent = label;
    b.dataset.category = value;
    b.addEventListener("click", () => {
      activeCategory = value;
      $$(".filter-chip").forEach((c) => c.classList.remove("active"));
      b.classList.add("active");
      renderCards();
    });
    return b;
  }

  function renderCards() {
    const filtered = activeCategory === "all"
      ? allDocs
      : allDocs.filter((d) => (d.category || "general") === activeCategory);

    libraryGrid.innerHTML = "";
    libraryEmpty.style.display = filtered.length ? "none" : "block";

    filtered.forEach((doc) => {
      const card = document.createElement("div");
      card.className = "doc-card";
      const preview = (doc.content || "").slice(0, 180);
      const concepts = (doc.concepts || []).slice(0, 4);
      const created = doc.created_at
        ? new Date(doc.created_at).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
        : "";
      card.innerHTML = `
        <span class="card-category">${escHtml(doc.category || "general")}</span>
        <div class="card-title">${escHtml(doc.name || "Untitled")}</div>
        <div class="card-preview">${escHtml(preview)}</div>
        <div class="card-concepts">
          ${concepts.map((c) => `<span class="concept-tag">${escHtml(c)}</span>`).join("")}
        </div>
        <div class="card-footer">
          <span>${escHtml(doc.type || "")}</span>
          <span>${created}</span>
        </div>`;
      card.addEventListener("click", () => openModal(doc));
      libraryGrid.appendChild(card);
    });
  }

  /* ═══════════════════════════════════════════════
     SEARCH
     ═══════════════════════════════════════════════ */
  async function doSearch() {
    const q = searchInput.value.trim();
    if (!q) return;
    searchResults.innerHTML = '<div class="shimmer" style="height:60px;margin-bottom:.8rem"></div>'.repeat(3);
    searchEmpty.style.display = "none";
    try {
      const results = await api(`/api/search?q=${encodeURIComponent(q)}`);
      searchResults.innerHTML = "";
      if (!results.length) {
        searchEmpty.style.display = "block";
        return;
      }
      results.forEach((r) => {
        const el = document.createElement("div");
        el.className = "result-item";
        const preview = (r.content || "").slice(0, 200);
        el.innerHTML = `
          <span class="result-score">${(r.similarity * 100).toFixed(0)}% match</span>
          <div class="result-title">${escHtml(r.name || "Untitled")}</div>
          <div class="result-preview">${escHtml(preview)}</div>`;
        el.addEventListener("click", () => openModal(r));
        searchResults.appendChild(el);
      });
    } catch (e) {
      toast("Search failed: " + e.message, true);
    }
  }
  searchGo.addEventListener("click", doSearch);
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });

  /* ═══════════════════════════════════════════════
     ADD TEXT / FILE
     ═══════════════════════════════════════════════ */
  // Tab switching
  $$(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      $$(".tab-btn").forEach((b) => b.classList.remove("active"));
      $$(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      $(`#tab-${btn.dataset.tab}`).classList.add("active");
    });
  });

  // Add text
  $("#btn-add-text").addEventListener("click", async () => {
    const text = $("#add-content").value.trim();
    if (!text) return toast("Please write some text first.", true);
    try {
      const body = {
        text,
        name: $("#add-title").value.trim() || undefined,
        discover: $("#add-discover").checked,
      };
      const res = await api("/api/add-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      toast(`✓ Added — ID ${res.id.slice(0, 8)}…`);
      $("#add-content").value = "";
      $("#add-title").value = "";
      loadStats();
      loadLibrary();
    } catch (e) {
      toast("Error: " + e.message, true);
    }
  });

  // File upload
  const fileDrop  = $("#file-drop");
  const fileInput = $("#file-input");
  const btnFile   = $("#btn-add-file");
  let selectedFile = null;

  fileDrop.addEventListener("dragover",  (e) => { e.preventDefault(); fileDrop.classList.add("dragover"); });
  fileDrop.addEventListener("dragleave", ()  => fileDrop.classList.remove("dragover"));
  fileDrop.addEventListener("drop", (e) => {
    e.preventDefault(); fileDrop.classList.remove("dragover");
    if (e.dataTransfer.files.length) pickFile(e.dataTransfer.files[0]);
  });
  fileDrop.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => { if (fileInput.files.length) pickFile(fileInput.files[0]); });

  function pickFile(f) {
    selectedFile = f;
    $(".file-drop p", fileDrop.parentElement).textContent = f.name;
    btnFile.disabled = false;
  }

  btnFile.addEventListener("click", async () => {
    if (!selectedFile) return;
    const fd = new FormData();
    fd.append("file", selectedFile);
    fd.append("discover", $("#file-discover").checked);
    try {
      const res = await api("/api/add-file", { method: "POST", body: fd });
      toast(`✓ Uploaded — ID ${res.id.slice(0, 8)}…`);
      selectedFile = null;
      btnFile.disabled = true;
      $(".file-drop p", fileDrop.parentElement).textContent = 'Drop a file here, or browse';
      loadStats();
      loadLibrary();
    } catch (e) {
      toast("Upload failed: " + e.message, true);
    }
  });

  /* ═══════════════════════════════════════════════
     MODAL
     ═══════════════════════════════════════════════ */
  function openModal(doc) {
    $("#modal-category").textContent = doc.category || "general";
    $("#modal-title").textContent    = doc.name || "Untitled";
    const created = doc.created_at ? new Date(doc.created_at).toLocaleString() : "";
    $("#modal-meta").textContent     = `ID: ${doc.id || "—"}  ·  ${doc.type || ""}  ·  ${created}`;
    $("#modal-content").textContent  = doc.content || "";

    const conceptsEl = $("#modal-concepts");
    conceptsEl.innerHTML = (doc.concepts || [])
      .map((c) => `<span class="concept-tag">${escHtml(c)}</span>`).join("");

    // Load related docs
    const relEl = $("#modal-related");
    relEl.innerHTML = '<span class="shimmer" style="display:inline-block;width:120px;height:24px"></span>';
    if (doc.id) {
      api(`/api/related/${doc.id}`).then((list) => {
        relEl.innerHTML = list.length
          ? list.map((r) => `<span class="related-chip" data-id="${r.id}">${escHtml(r.name || "Untitled")}</span>`).join("")
          : '<span style="color:var(--muted-dim);font-size:.82rem">No related documents yet.</span>';
      }).catch(() => {
        relEl.innerHTML = '<span style="color:var(--muted-dim);font-size:.82rem">—</span>';
      });
    }

    modalOverlay.classList.add("open");
  }

  $("#modal-close").addEventListener("click", () => modalOverlay.classList.remove("open"));
  modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) modalOverlay.classList.remove("open");
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") modalOverlay.classList.remove("open");
  });

  /* ═══════════════════════════════════════════════
     GRAPH (simple force‑directed canvas)
     ═══════════════════════════════════════════════ */
  async function drawGraph() {
    const canvas = $("#graph-canvas");
    const ctx    = canvas.getContext("2d");
    const wrap   = $("#graph-container");
    canvas.width  = wrap.clientWidth  * devicePixelRatio;
    canvas.height = wrap.clientHeight * devicePixelRatio;
    ctx.scale(devicePixelRatio, devicePixelRatio);
    const W = wrap.clientWidth, H = wrap.clientHeight;

    let graphData;
    try { graphData = await api("/api/graph"); } catch { return; }
    if (!graphData.nodes.length) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = "#6e6558";
      ctx.font = "16px Lora, Georgia, serif";
      ctx.textAlign = "center";
      ctx.fillText("Add documents to see your knowledge graph.", W / 2, H / 2);
      return;
    }

    // Build positions
    const nodes = graphData.nodes.map((n, i) => ({
      ...n,
      x: W / 2 + (Math.random() - .5) * W * .6,
      y: H / 2 + (Math.random() - .5) * H * .6,
      vx: 0, vy: 0,
    }));
    const nodeMap = {};
    nodes.forEach((n) => (nodeMap[n.id] = n));
    const edges = graphData.edges.filter((e) => nodeMap[e.source] && nodeMap[e.target]);

    // Simple force sim
    function tick() {
      // Repulsion
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          let dx = nodes[j].x - nodes[i].x;
          let dy = nodes[j].y - nodes[i].y;
          let d  = Math.sqrt(dx * dx + dy * dy) || 1;
          let f  = 3000 / (d * d);
          nodes[i].vx -= (dx / d) * f;
          nodes[i].vy -= (dy / d) * f;
          nodes[j].vx += (dx / d) * f;
          nodes[j].vy += (dy / d) * f;
        }
      }
      // Attraction (edges)
      edges.forEach((e) => {
        const a = nodeMap[e.source], b = nodeMap[e.target];
        let dx = b.x - a.x, dy = b.y - a.y;
        let d = Math.sqrt(dx * dx + dy * dy) || 1;
        let f = (d - 120) * 0.01;
        a.vx += (dx / d) * f;
        a.vy += (dy / d) * f;
        b.vx -= (dx / d) * f;
        b.vy -= (dy / d) * f;
      });
      // Center gravity
      nodes.forEach((n) => {
        n.vx += (W / 2 - n.x) * 0.0008;
        n.vy += (H / 2 - n.y) * 0.0008;
        n.vx *= 0.88; n.vy *= 0.88;
        n.x += n.vx; n.y += n.vy;
        n.x = Math.max(30, Math.min(W - 30, n.x));
        n.y = Math.max(30, Math.min(H - 30, n.y));
      });
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);

      // edges
      edges.forEach((e) => {
        const a = nodeMap[e.source], b = nodeMap[e.target];
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = "rgba(201,168,76,.15)";
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // nodes
      nodes.forEach((n) => {
        // glow
        const grad = ctx.createRadialGradient(n.x, n.y, 2, n.x, n.y, 18);
        grad.addColorStop(0, "rgba(201,168,76,.35)");
        grad.addColorStop(1, "rgba(201,168,76,0)");
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(n.x, n.y, 18, 0, Math.PI * 2);
        ctx.fill();

        // dot
        ctx.beginPath();
        ctx.arc(n.x, n.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = "#c9a84c";
        ctx.fill();

        // label
        ctx.fillStyle = "#e8dcc8";
        ctx.font = "11px Inter, sans-serif";
        ctx.textAlign = "center";
        const label = (n.name || "").slice(0, 22) || n.id.slice(0, 8);
        ctx.fillText(label, n.x, n.y + 18);
      });
    }

    let frame = 0;
    function animate() {
      tick();
      draw();
      frame++;
      if (frame < 250) requestAnimationFrame(animate);
    }
    animate();
  }

  /* ═══════════════════════════════════════════════
     TOAST
     ═══════════════════════════════════════════════ */
  function toast(msg, isError) {
    const el = document.createElement("div");
    el.className = "toast" + (isError ? " error" : "");
    el.textContent = msg;
    toastBox.appendChild(el);
    setTimeout(() => el.remove(), 3600);
  }

  /* ═══════════════════════════════════════════════
     UTIL
     ═══════════════════════════════════════════════ */
  function escHtml(s) {
    const d = document.createElement("div");
    d.textContent = s || "";
    return d.innerHTML;
  }

  /* ═══════════════════════════════════════════════
     BOOT
     ═══════════════════════════════════════════════ */
  loadStats();
  loadLibrary();
})();
