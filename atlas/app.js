"use strict";
const $ = (id) => document.getElementById(id);
const f = (x, d = 2) => (x == null ? "n/a" : x.toFixed(d));
const J = (u) => fetch(u).then((r) => r.json());
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

Promise.all([J("data/summary.json"), J("data/stations.json"), J("data/value_curve.json"), J("data/reliability.json")])
  .then(([sum, st, vc, rel]) => { cards(sum); seasons(sum); stations(st); revChart(vc); relChart(rel); })
  .catch((e) => { document.querySelector("main").insertAdjacentHTML("afterbegin", `<p class="note">Could not load data (${esc(e)}). Serve this folder over http.</p>`); });

function ci(o) { return `${f(o.est, 3)} [${f(o.lo, 3)}, ${f(o.hi, 3)}]`; }

function cards(s) {
  const names = { mae_diff_persist: "MAE diff vs persistence", mae_diff_clim: "MAE diff vs climatology", mae_diff_official: "MAE diff vs official", brier_diff_persist_4: "Brier(4) diff vs persistence", brier_diff_clim_4: "Brier(4) diff vs climatology" };
  const li = Object.entries(s.H1.criteria).map(([k, v]) => `<li>${names[k]}: ${ci(v)} - ${v.met ? "met" : "not met"}</li>`).join("");
  const c = (ok, t, intro, body) => `<div class="card ${ok ? "yes" : "no"}"><h3>${t}</h3><div class="v">${ok ? "SUPPORTED" : "NOT SUPPORTED"}</div>${intro}${body}</div>`;
  $("cards").innerHTML =
    c(s.H1.supported, "H1 Accuracy", `<p>All five criteria (CI upper bound below 0) are required. Differences are model minus benchmark; negative favours the model.</p>`,
      `<ul>${li}</ul><p>Peirce skill at 4 g/L: model ${f(s.H1.pss4.model, 3)}, official ${f(s.H1.pss4.official, 3)}; difference ${ci(s.H1.pss4.diff)}.</p>`) +
    c(s.H2.H2a_supported, "H2a Coverage", `<p>Forward coverage of the 90% CQR interval must lie in [0.87, 0.93]: ${ci(s.H2.cov_cqr_forward)}.</p>`,
      `<ul><li>Leave-station-out: ${ci(s.H2.cov_cqr_loso)}</li><li>Leave-province-out: ${ci(s.H2.cov_cqr_lopo)}</li></ul><p>H2b (Mondrian fix under leave-out designs) is not supported.</p>`) +
    c(s.H3.supported, "H3 Decision value", `<p>Area under the relative-economic-value curve (C/L 0.1-0.9, 4 g/L), model minus official, CI lower bound above 0: ${ci(s.H3.rev_area_diff_official)}.</p>`,
      `<p>Area: model ${f(s.H3.rev_area.model, 3)}, official ${f(s.H3.rev_area.official, 3)}, persistence ${f(s.H3.rev_area.persist, 3)}.</p>`);
}

function seasons(s) {
  const h = ["Season", "n", "MAE model", "MAE persist.", "MAE official", "Coverage 90%", "Width", "Brier(4)", "Peirce(4) model", "Peirce(4) official"];
  const k = ["season", "n", "mae_model", "mae_persist", "mae_official", "cov_cqr", "width_cqr", "brier_model_4", "pss_model_4", "pss_official_4"];
  $("seasons").innerHTML = `<thead><tr>${h.map((x) => `<th scope="col">${x}</th>`).join("")}</tr></thead><tbody>` +
    s.seasons.map((r) => `<tr>${k.map((c, i) => `<td>${i < 2 ? esc(r[c]) : f(r[c])}</td>`).join("")}</tr>`).join("") + "</tbody>";
}

function stations(data) {
  const cols = [["station", "Station"], ["province_new", "Province"], ["river", "River"], ["n", "n"], ["mae_model", "MAE model"], ["mae_persist", "MAE persist."], ["mae_official", "MAE official"], ["skill_vs_persist", "Skill vs persist."], ["cov_cqr", "Coverage"], ["width_cqr", "Width"], ["cov_cqr_loso", "LOSO coverage"]];
  let key = "station", dir = 1, sel = null;
  const tb = document.createElement("tbody"), th = document.createElement("thead");
  th.innerHTML = "<tr>" + cols.map(([k, t]) => `<th scope="col" tabindex="0" data-k="${k}" aria-sort="none">${t}</th>`).join("") + "</tr>";
  $("stations").append(th, tb);
  const v = (r) => r[key] ?? -1e9;
  const draw = () => {
    data.sort((a, b) => dir * (v(a) > v(b) ? 1 : v(a) < v(b) ? -1 : 0));
    tb.innerHTML = "";
    data.forEach((r) => {
      const tr = document.createElement("tr");
      tr.tabIndex = 0; tr.className = r === sel ? "sel" : "";
      tr.innerHTML = cols.map(([k]) => `<td>${typeof r[k] === "number" ? f(r[k], k === "n" ? 0 : 2) : esc(r[k] ?? "n/a")}</td>`).join("");
      const pick = () => { sel = r; detail(r); draw(); if (r.marker) r.marker.openPopup(); };
      tr.onclick = pick;
      tr.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); } };
      tb.append(tr);
    });
    th.querySelectorAll("th").forEach((h) => h.setAttribute("aria-sort", h.dataset.k === key ? (dir > 0 ? "ascending" : "descending") : "none"));
  };
  th.addEventListener("click", (e) => { const k = e.target.dataset && e.target.dataset.k; if (k) { dir = k === key ? -dir : 1; key = k; draw(); } });
  th.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.dataset.k) e.target.click(); });
  map(data); // before draw so markers exist
  draw();
}

function detail(r) {
  const better = r.skill_vs_persist > 0 ? "better" : "no better";
  $("detail").innerHTML = `<h3>${esc(r.station)}</h3><p>${esc(r.river)} river, ${esc(r.km_from_mouth)} km from mouth; ${esc(r.province_new)} (formerly ${esc(r.province_old)}).</p>
  <ul><li>Forecasts scored: ${r.n}</li><li>MAE (g/L): model ${f(r.mae_model)}, persistence ${f(r.mae_persist)}, official ${f(r.mae_official)}</li>
  <li>Skill vs persistence: ${f(r.skill_vs_persist, 3)}</li><li>90% interval coverage: ${f(r.cov_cqr)}; leave-station-out ${f(r.cov_cqr_loso)}; mean width ${f(r.width_cqr)} g/L</li></ul>
  <p class="note">Model MAE is ${better} than persistence here. With about ${r.n} forecasts per station, single-station scores are noisy.</p>`;
}

function map(data) {
  const withLoc = data.filter((r) => r.lat != null && r.lon != null);
  $("pending").hidden = withLoc.length > 0;
  if (typeof L === "undefined") { $("map").textContent = "Map library unavailable offline."; return; }
  const m = L.map("map").setView([9.9, 105.9], 8);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18, attribution: "&copy; OpenStreetMap contributors" }).addTo(m);
  withLoc.forEach((r) => {
    const col = r.skill_vs_persist > 0 ? "#1f5fa8" : "#b45309";
    r.marker = L.circleMarker([r.lat, r.lon], { radius: 8, color: "#fff", weight: 2, fillColor: col, fillOpacity: 0.9 })
      .bindPopup(`<b>${esc(r.station)}</b><br>skill vs persistence ${f(r.skill_vs_persist, 3)}`).addTo(m);
    r.marker.on("click", () => detail(r));
  });
}

// ---- charts (inline SVG) ----
const W = 480, H = 320, P = { l: 48, r: 90, t: 12, b: 40 };
const X = (v) => P.l + v * (W - P.l - P.r);
const Y = (v, lo, hi) => H - P.b - ((v - lo) / (hi - lo)) * (H - P.t - P.b);
const svg = (el, label, inner) => { el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${esc(label)}">${inner}</svg>`; };

function frame(lo, hi, step, xt, yt) {
  let s = "";
  for (let t = lo; t <= hi + 1e-9; t += step) s += `<line class="gr" x1="${P.l}" x2="${W - P.r}" y1="${Y(t, lo, hi)}" y2="${Y(t, lo, hi)}"/><text class="mute" x="${P.l - 6}" y="${Y(t, lo, hi) + 4}" text-anchor="end">${+t.toFixed(2)}</text>`;
  for (let t = 0; t <= 1.001; t += 0.25) s += `<text class="mute" x="${X(t)}" y="${H - P.b + 16}" text-anchor="middle">${t}</text>`;
  return s + `<line class="ax" x1="${P.l}" x2="${W - P.r}" y1="${H - P.b}" y2="${H - P.b}"/><text x="${(P.l + W - P.r) / 2}" y="${H - 6}" text-anchor="middle">${xt}</text><text transform="translate(12 ${H / 2}) rotate(-90)" text-anchor="middle">${yt}</text>`;
}

function revChart(vc) {
  const series = [["model", "Model", "var(--model)", ""], ["official", "Official", "var(--off)", ""], ["persistence", "Persistence", "var(--per)", "6 4"]];
  const lo = -1, hi = 1, clip = (v) => Math.max(lo, Math.min(hi, v));
  let s = frame(lo, hi, 0.5, "Cost / loss ratio", "Relative economic value");
  series.forEach(([k, , col, dash], i) => {
    const pts = vc.cost_loss.map((c, j) => vc[k][j] == null ? null : `${X(c).toFixed(1)},${Y(clip(vc[k][j]), lo, hi).toFixed(1)}`).filter(Boolean);
    s += `<polyline fill="none" stroke="${col}" stroke-width="2" ${dash ? `stroke-dasharray="${dash}"` : ""} points="${pts.join(" ")}"/>`;
    s += `<line x1="${W - P.r + 8}" x2="${W - P.r + 26}" y1="${30 + i * 18}" y2="${30 + i * 18}" stroke="${col}" stroke-width="2" ${dash ? `stroke-dasharray="${dash}"` : ""}/><text x="${W - P.r + 30}" y="${34 + i * 18}">${series[i][1]}</text>`;
  });
  svg($("chart-rev"), "Relative economic value at 4 g/L versus cost-loss ratio for the model, the official forecast and persistence. Values below -1 are clipped.", s);
}

function relChart(rel) {
  let s = frame(0, 1, 0.25, "Forecast probability", "Observed frequency");
  s += `<line x1="${X(0)}" y1="${Y(0, 0, 1)}" x2="${X(1)}" y2="${Y(1, 0, 1)}" stroke="var(--mute)" stroke-dasharray="4 4"/><text class="mute" x="${W - P.r + 8}" y="${Y(1, 0, 1) + 4}">perfect</text>`;
  const b = rel.bins.filter((r) => r.n > 0 && r.mean_prob != null);
  const mx = Math.max(...b.map((r) => r.n));
  s += `<polyline fill="none" stroke="var(--model)" stroke-width="2" points="${b.map((r) => `${X(r.mean_prob)},${Y(r.obs_freq, 0, 1)}`).join(" ")}"/>`;
  b.forEach((r) => { s += `<circle cx="${X(r.mean_prob)}" cy="${Y(r.obs_freq, 0, 1)}" r="${3 + 7 * Math.sqrt(r.n / mx)}" fill="var(--model)" stroke="var(--bg)" stroke-width="2"><title>${r.bin}: n=${r.n}, forecast ${f(r.mean_prob)}, observed ${f(r.obs_freq)}</title></circle>`; });
  svg($("chart-rel"), "Reliability diagram for exceedance of 4 g/L; points near the diagonal mean well-calibrated probabilities.", s);
}
