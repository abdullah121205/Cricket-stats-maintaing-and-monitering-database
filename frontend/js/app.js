/**
 * Cricket Statistics Maintaining & Monitoring Database
 * Frontend JavaScript Controller
 */

const API_BASE = "/api";

// ----------------------------------------------------
// Toast Notifications
// ----------------------------------------------------
function showToast(message, type = "success") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "toast-container position-fixed bottom-0 end-0 p-3";
        container.style.zIndex = "1100";
        document.body.appendChild(container);
    }

    const toastId = "toast-" + Date.now();
    const bgClass = type === "success" ? "bg-success" : (type === "danger" ? "bg-danger" : "bg-primary");
    const html = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0 shadow" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    container.insertAdjacentHTML("beforeend", html);
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();
    toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
}

// ----------------------------------------------------
// Badge Helpers
// ----------------------------------------------------
function getRoleBadge(role) {
    switch (role) {
        case "Batter":
        case "Batsman": 
            return '<span class="badge badge-role badge-batsman"><i class="fas fa-baseball-bat-ball me-1"></i>Batter</span>';
        case "Bowler": 
            return '<span class="badge badge-role badge-bowler"><i class="fas fa-volleyball me-1"></i>Bowler</span>';
        case "All-rounder": 
            return '<span class="badge badge-role badge-allrounder"><i class="fas fa-bolt me-1"></i>All-Rounder</span>';
        case "Wicketkeeper": 
            return '<span class="badge badge-role badge-keeper"><i class="fas fa-mitten me-1"></i>Wicketkeeper</span>';
        default: 
            return `<span class="badge bg-secondary">${role}</span>`;
    }
}

function getFormatBadge(format) {
    return `<span class="badge badge-format">${format}</span>`;
}

function getStatusBadge(status) {
    if (status === "Completed") return '<span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50">Completed</span>';
    if (status === "Live" || status === "In Progress") return '<span class="badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-50 d-inline-flex align-items-center"><span class="live-pulse"></span>' + (status === "In Progress" ? "In Progress" : "Live") + '</span>';
    return '<span class="badge bg-primary bg-opacity-25 text-primary border border-primary border-opacity-50">Scheduled</span>';
}

// ----------------------------------------------------
// LIVE SCORES CONTROLLER & SIMULATION ENGINE
// ----------------------------------------------------
let liveScoresData = [];
let liveRefreshTimer = null;

async function loadLiveScores(showFeedback = false) {
    const container = document.getElementById("liveScoresContainer");
    if (!container) return;

    const icon = document.getElementById("refreshLiveIcon");
    if (icon) icon.classList.add("fa-spin");

    try {
        const res = await fetch(`${API_BASE}/live/scores`);
        const json = await res.json();
        if (json.success && json.data) {
            liveScoresData = json.data;
            renderLiveScores(liveScoresData);
            if (showFeedback) showToast("Live scores updated!", "success");
        } else {
            container.innerHTML = `<div class="col-12 text-center text-muted py-3">No live matches available currently.</div>`;
        }
    } catch (err) {
        console.error("Live scores fetch error:", err);
        container.innerHTML = `<div class="col-12 text-center text-danger py-3"><i class="fas fa-triangle-exclamation me-2"></i>Could not connect to live cricket feed.</div>`;
    } finally {
        if (icon) setTimeout(() => icon.classList.remove("fa-spin"), 600);
    }
}

function refreshLiveScoresManually() {
    loadLiveScores(true);
}

function setupLiveAutoRefresh() {
    const sw = document.getElementById("autoRefreshSwitch");
    if (liveRefreshTimer) clearInterval(liveRefreshTimer);

    liveRefreshTimer = setInterval(() => {
        const auto = document.getElementById("autoRefreshSwitch");
        if (auto && auto.checked) {
            loadLiveScores(false);
        }
    }, 15000);

    if (sw) {
        sw.addEventListener("change", () => {
            if (sw.checked) {
                showToast("Auto-refresh enabled (every 15s)");
                loadLiveScores(false);
            } else {
                showToast("Auto-refresh paused");
            }
        });
    }
}

function renderLiveScores(matches) {
    const container = document.getElementById("liveScoresContainer");
    if (!container) return;

    if (!matches || matches.length === 0) {
        container.innerHTML = `<div class="col-12 text-center text-muted py-3">No active live matches found.</div>`;
        return;
    }

    container.innerHTML = matches.map((m, idx) => {
        const t1 = m.team1 || {};
        const t2 = m.team2 || {};
        const batters = m.current_batters || [];
        const bowler = m.current_bowler;

        return `
            <div class="col-lg-4 col-md-6">
                <div class="live-card p-3 h-100 d-flex flex-column">
                    <!-- Top Bar -->
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <div class="d-flex align-items-center gap-1">
                            <span class="live-badge-glow">
                                <span class="live-pulse"></span> ${m.status || 'LIVE'}
                            </span>
                            <span class="badge badge-format ms-1">${m.format}</span>
                        </div>
                        <span class="small text-muted text-truncate ms-2" style="max-width: 140px;" title="${m.venue || ''}">
                            <i class="fas fa-location-dot me-1 text-danger"></i>${(m.venue || '').split(',')[0]}
                        </span>
                    </div>

                    <!-- Match Title & Series -->
                    <div class="mb-2">
                        <div class="fw-bold text-white fs-6 text-truncate" title="${m.title}">
                            ${m.title}
                        </div>
                        ${m.series ? `<div class="small text-muted" style="font-size: 0.76rem;">${m.series}</div>` : ''}
                    </div>

                    <!-- Scorecard Box -->
                    <div class="bg-black bg-opacity-40 rounded p-2 mb-2 border border-secondary border-opacity-25">
                        <div class="live-team-row">
                            <span class="live-team-name d-flex align-items-center gap-1">
                                ${t1.is_batting ? '<i class="fas fa-baseball-bat-ball text-emerald me-1 small"></i>' : ''}
                                ${t1.name}
                            </span>
                            <span class="live-team-score text-white">
                                ${t1.runs !== undefined ? t1.runs : '-'}${t1.wickets !== undefined ? '/' + t1.wickets : ''}
                                ${t1.overs ? `<span class="live-overs">(${t1.overs})</span>` : ''}
                            </span>
                        </div>
                        <div class="live-team-row">
                            <span class="live-team-name d-flex align-items-center gap-1 text-light">
                                ${t2.is_batting ? '<i class="fas fa-baseball-bat-ball text-emerald me-1 small"></i>' : ''}
                                ${t2.name}
                            </span>
                            <span class="live-team-score text-secondary">
                                ${t2.runs !== undefined ? t2.runs : '-'}${t2.wickets !== undefined ? '/' + t2.wickets : ''}
                                ${t2.overs ? `<span class="live-overs text-secondary">(${t2.overs})</span>` : ''}
                            </span>
                        </div>
                    </div>

                    <!-- Situation Summary -->
                    <div class="small fw-semibold text-warning mb-2 d-flex align-items-center gap-1">
                        <i class="fas fa-circle-info text-info small"></i>
                        <span class="text-truncate">${m.summary || 'Match in progress'}</span>
                    </div>

                    <!-- Current Batters & Bowler Box -->
                    ${(batters.length > 0 || bowler) ? `
                    <div class="live-player-box mb-3 mt-auto">
                        ${batters.length > 0 ? `
                        <div class="d-flex justify-content-between text-muted small border-bottom border-secondary border-opacity-25 pb-1 mb-1" style="font-size: 0.75rem;">
                            <span>Batting:</span>
                            <span>R (B)</span>
                        </div>
                        ${batters.map(b => `
                            <div class="d-flex justify-content-between align-items-center small py-0.5">
                                <span class="${b.on_strike ? 'text-emerald fw-bold' : 'text-light'}">
                                    ${b.on_strike ? '▶ ' : '&nbsp;&nbsp;'}${b.name}
                                </span>
                                <span class="fw-semibold text-white">${b.runs} <span class="text-muted small">(${b.balls})</span></span>
                            </div>
                        `).join('')}
                        ` : ''}

                        ${bowler ? `
                        <div class="d-flex justify-content-between align-items-center small pt-1 mt-1 border-top border-secondary border-opacity-25" style="font-size: 0.77rem;">
                            <span class="text-muted">Bowling: <strong class="text-light">${bowler.name}</strong></span>
                            <span class="text-white">${bowler.wickets}/${bowler.runs} <span class="text-muted">(${bowler.overs} ov)</span></span>
                        </div>
                        ` : ''}
                    </div>
                    ` : '<div class="mt-auto"></div>'}

                    <!-- Auto-Sync Status & Scorecard Link -->
                    <div class="mt-2 d-flex gap-2 align-items-center">
                        <span class="badge bg-success bg-opacity-25 text-success border border-success border-opacity-50 py-1.5 px-2 flex-grow-1 text-truncate" title="Automatically synchronized with database">
                            <i class="fas fa-check-circle me-1"></i> Auto-Synced in DB ${m.db_match_id ? '(#' + m.db_match_id + ')' : ''}
                        </span>
                        ${m.db_match_id ? `
                        <a href="/matches?match_id=${m.db_match_id}" class="btn btn-sm btn-outline-info text-nowrap py-1">
                            <i class="fas fa-file-lines me-1"></i> Scorecard
                        </a>
                        ` : `
                        <button class="btn btn-sm btn-outline-emerald text-nowrap py-1" onclick="importLiveMatchToDb(${idx})" id="importBtn-${idx}">
                            <i class="fas fa-database me-1"></i> Sync Now
                        </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

async function importLiveMatchToDb(matchIdx) {
    const match = liveScoresData[matchIdx];
    if (!match) return;

    const btn = document.getElementById(`importBtn-${matchIdx}`);
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i> Saving to Database...`;
    }

    try {
        const res = await fetch(`${API_BASE}/live/import`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ match: match })
        });
        const json = await res.json();
        if (json.success) {
            showToast(json.message || "Match successfully recorded in database!");
            if (btn) {
                btn.className = "btn btn-sm btn-success w-100 py-1.5";
                btn.innerHTML = `<i class="fas fa-check-circle me-1"></i> Tracked (Match #${json.match_id})`;
            }
            // Update Dashboard counter if present
            const statMatchesEl = document.getElementById("stat-matches");
            if (statMatchesEl && statMatchesEl.innerText !== "-" && json.is_new) {
                statMatchesEl.innerText = Number(statMatchesEl.innerText) + 1;
            }
        } else {
            showToast(json.message || "Failed to import match", "danger");
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i class="fas fa-database me-1"></i> Track in Database`;
            }
        }
    } catch (e) {
        showToast("Error connecting to server", "danger");
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = `<i class="fas fa-database me-1"></i> Track in Database`;
        }
    }
}

// ----------------------------------------------------
// 1. DASHBOARD CONTROLLER (index.html)
// ----------------------------------------------------
async function initDashboard() {
    // 1. Initialize Live Scores Feed
    loadLiveScores(false);
    setupLiveAutoRefresh();

    // 2. Fetch KPI & Aggregates
    try {
        const res = await fetch(`${API_BASE}/stats/summary`);
        const json = await res.json();
        if (json.success) {
            const d = json.data;
            document.getElementById("stat-players").innerText = d.total_players;
            document.getElementById("stat-teams").innerText = d.total_teams;
            document.getElementById("stat-matches").innerText = d.total_matches;
            document.getElementById("stat-runs").innerText = Number(d.total_runs).toLocaleString();
            document.getElementById("stat-wickets").innerText = d.total_wickets;
            document.getElementById("stat-boundaries").innerText = `${d.total_fours} / ${d.total_sixes}`;
        }

        const batsmenRes = await fetch(`${API_BASE}/stats/top-batsmen`);
        const batsmenJson = await batsmenRes.json();
        if (batsmenJson.success && batsmenJson.data.length > 0) {
            renderBatsmenChart(batsmenJson.data.slice(0, 5));
        }

        const teamsRes = await fetch(`${API_BASE}/stats/team-rankings`);
        const teamsJson = await teamsRes.json();
        if (teamsJson.success && teamsJson.data.length > 0) {
            renderTeamsChart(teamsJson.data);
        }

        const matchesRes = await fetch(`${API_BASE}/matches`);
        const matchesJson = await matchesRes.json();
        if (matchesJson.success) {
            renderRecentMatches(matchesJson.data.slice(0, 4));
        }
    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

function renderBatsmenChart(batsmen) {
    const ctx = document.getElementById("topBatsmenChart");
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: batsmen.map(b => b.player_name || b.full_name),
            datasets: [{
                label: 'Runs Scored',
                data: batsmen.map(b => b.total_runs),
                backgroundColor: 'rgba(16, 185, 129, 0.75)',
                borderColor: '#10b981',
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.06)' } }
            }
        }
    });
}

function renderTeamsChart(teams) {
    const ctx = document.getElementById("teamsChart");
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: teams.map(t => t.team_name || t.name),
            datasets: [{
                data: teams.map(t => Math.max(t.wins, 0)),
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#f43f5e', '#8b5cf6', '#06b6d4'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94a3b8', boxWidth: 12 } }
            }
        }
    });
}

function renderRecentMatches(matches) {
    const container = document.getElementById("recent-matches-list");
    if (!container) return;

    if (matches.length === 0) {
        container.innerHTML = `<div class="p-4 text-center text-muted">No matches recorded yet.</div>`;
        return;
    }

    container.innerHTML = matches.map(m => `
        <div class="p-3 border-bottom border-secondary border-opacity-25 d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2">
            <div>
                <div class="d-flex align-items-center gap-2 mb-1">
                    ${getFormatBadge(m.format || m.match_format)}
                    <span class="text-muted small"><i class="far fa-calendar me-1"></i>${m.match_date}</span>
                    <span class="text-muted small">• <i class="fas fa-location-dot me-1"></i>${m.venue_name || 'TBD'}</span>
                </div>
                <h6 class="mb-1 fw-bold text-white">
                    ${m.match_title || `${m.team1_name} vs ${m.team2_name}`}
                </h6>
                <div class="small text-emerald fw-semibold">
                    ${m.result_summary || m.result || (m.status === 'Completed' ? 'Completed' : 'Match Scheduled')}
                </div>
            </div>
            <div class="d-flex align-items-center gap-2">
                ${getStatusBadge(m.status)}
                <a href="/matches?match_id=${m.match_id}" class="btn btn-sm btn-outline-custom">Scorecard</a>
            </div>
        </div>
    `).join("");
}

// ----------------------------------------------------
// 2. PLAYERS CONTROLLER (players.html)
// ----------------------------------------------------
let allPlayers = [];
let allTeams = [];

async function initPlayersPage() {
    await loadTeamsDropdowns();
    await fetchPlayers();

    document.getElementById("searchPlayer")?.addEventListener("input", filterPlayers);
    document.getElementById("filterRole")?.addEventListener("change", filterPlayers);
    document.getElementById("filterCountry")?.addEventListener("change", filterPlayers);

    document.getElementById("addPlayerForm")?.addEventListener("submit", handleAddPlayer);
    document.getElementById("editPlayerForm")?.addEventListener("submit", handleUpdatePlayer);
}

async function loadTeamsDropdowns() {
    try {
        const res = await fetch(`${API_BASE}/teams`);
        const json = await res.json();
        if (json.success) {
            allTeams = json.data;
            const filterCountryEl = document.getElementById("filterCountry");
            if (filterCountryEl) {
                const countries = [...new Set(allTeams.map(t => t.country).filter(Boolean))];
                filterCountryEl.innerHTML = `<option value="">All Nationalities</option>` + countries.map(c => `<option value="${c}">${c}</option>`).join("");
            }
        }
    } catch (e) {
        console.error("Teams dropdown error:", e);
    }
}

async function fetchPlayers() {
    try {
        const res = await fetch(`${API_BASE}/players`);
        const json = await res.json();
        if (json.success) {
            allPlayers = json.data;
            renderPlayersTable(allPlayers);
        }
    } catch (e) {
        console.error("Fetch players error:", e);
    }
}

function filterPlayers() {
    const q = document.getElementById("searchPlayer").value.toLowerCase();
    const role = document.getElementById("filterRole").value;
    const country = document.getElementById("filterCountry")?.value || "";

    const filtered = allPlayers.filter(p => {
        const name = (p.full_name || p.name || "").toLowerCase();
        const nat = (p.nationality || p.country || "").toLowerCase();
        const matchesQuery = name.includes(q) || nat.includes(q);
        const matchesRole = !role || p.role === role;
        const matchesCountry = !country || (p.nationality || p.country) === country;
        return matchesQuery && matchesRole && matchesCountry;
    });

    renderPlayersTable(filtered);
}

function renderPlayersTable(players) {
    const tbody = document.getElementById("playersTableBody");
    const countEl = document.getElementById("playerCountBadge");
    if (countEl) countEl.innerText = `${players.length} Players`;
    if (!tbody) return;

    if (players.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No players found matching your criteria.</td></tr>`;
        return;
    }

    tbody.innerHTML = players.map(p => `
        <tr>
            <td>
                <div class="d-flex align-items-center gap-3">
                    <img src="https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=100" class="avatar-img" alt="${p.full_name || p.name}">
                    <div>
                        <div class="fw-bold text-white">${p.full_name || p.name}</div>
                        <div class="small text-muted">${p.is_active ? 'Active' : 'Retired'}</div>
                    </div>
                </div>
            </td>
            <td><span class="fw-semibold text-light">${p.nationality || p.country}</span></td>
            <td>${getRoleBadge(p.role)}</td>
            <td><span class="small text-muted">${p.batting_style || '-'}</span></td>
            <td><span class="small text-muted">${p.bowling_style || '-'}</span></td>
            <td>${p.date_of_birth || '-'}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-info me-1" onclick="viewPlayerProfile(${p.player_id})" title="Career Stats">
                    <i class="fas fa-chart-line"></i>
                </button>
                <button class="btn btn-sm btn-outline-warning me-1" onclick="openEditPlayerModal(${p.player_id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deletePlayer(${p.player_id}, '${p.full_name || p.name}')" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join("");
}

async function handleAddPlayer(e) {
    e.preventDefault();
    const data = {
        full_name: document.getElementById("playerName").value.trim(),
        nationality: document.getElementById("playerCountry").value.trim(),
        role: document.getElementById("playerRole").value,
        date_of_birth: document.getElementById("playerDob").value || null,
        batting_style: document.getElementById("playerBattingStyle").value,
        bowling_style: document.getElementById("playerBowlingStyle").value
    };

    try {
        const res = await fetch(`${API_BASE}/players`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Player added successfully!");
            document.getElementById("addPlayerForm").reset();
            bootstrap.Modal.getInstance(document.getElementById("addPlayerModal")).hide();
            await fetchPlayers();
        } else {
            showToast(json.message || "Failed to add player", "danger");
        }
    } catch (err) {
        showToast("Server error", "danger");
    }
}

async function viewPlayerProfile(playerId) {
    try {
        const res = await fetch(`${API_BASE}/players/${playerId}`);
        const json = await res.json();
        if (!json.success) return showToast("Could not load player profile", "danger");

        const { profile, batting, bowling, recent_batting, recent_bowling } = json.data;

        document.getElementById("profileModalName").innerText = profile.full_name || profile.name;
        document.getElementById("profileModalCountry").innerText = profile.nationality || profile.country;
        document.getElementById("profileModalRoleBadge").innerHTML = getRoleBadge(profile.role);

        // Batting stats
        document.getElementById("prof-bat-innings").innerText = batting.innings || 0;
        document.getElementById("prof-bat-runs").innerText = batting.total_runs || 0;
        document.getElementById("prof-bat-hs").innerText = batting.highest_score || 0;
        document.getElementById("prof-bat-avg").innerText = batting.batting_average || "0.00";
        document.getElementById("prof-bat-sr").innerText = batting.strike_rate || "0.00";
        document.getElementById("prof-bat-100s").innerText = batting.centuries || 0;
        document.getElementById("prof-bat-50s").innerText = batting.half_centuries || 0;
        document.getElementById("prof-bat-fours").innerText = batting.total_fours || 0;
        document.getElementById("prof-bat-sixes").innerText = batting.total_sixes || 0;

        // Bowling stats
        document.getElementById("prof-bowl-innings").innerText = bowling.innings_bowled || 0;
        document.getElementById("prof-bowl-overs").innerText = bowling.total_overs || "0.0";
        document.getElementById("prof-bowl-wickets").innerText = bowling.total_wickets || 0;
        document.getElementById("prof-bowl-avg").innerText = bowling.bowling_average || "0.00";
        document.getElementById("prof-bowl-econ").innerText = bowling.economy_rate || "0.00";
        document.getElementById("prof-bowl-5w").innerText = bowling.five_wicket_hauls || 0;

        // Recent Batting list
        const batListEl = document.getElementById("profileRecentBatting");
        if (recent_batting.length > 0) {
            batListEl.innerHTML = recent_batting.map(b => `
                <div class="d-flex justify-content-between py-1 border-bottom border-secondary border-opacity-25 small">
                    <span>${b.match_title} (${b.format})</span>
                    <span class="fw-bold ${b.runs >= 50 ? 'text-warning' : 'text-white'}">${b.runs} (${b.balls_faced}b)</span>
                </div>
            `).join("");
        } else {
            batListEl.innerHTML = `<span class="text-muted small">No recent batting records</span>`;
        }

        // Recent Bowling list
        const bowlListEl = document.getElementById("profileRecentBowling");
        if (recent_bowling.length > 0) {
            bowlListEl.innerHTML = recent_bowling.map(bw => `
                <div class="d-flex justify-content-between py-1 border-bottom border-secondary border-opacity-25 small">
                    <span>${bw.match_title} (${bw.format})</span>
                    <span class="fw-bold text-emerald">${bw.wickets}/${bw.runs_conceded}</span>
                </div>
            `).join("");
        } else {
            bowlListEl.innerHTML = `<span class="text-muted small">No recent bowling records</span>`;
        }

        const modal = new bootstrap.Modal(document.getElementById("playerProfileModal"));
        modal.show();
    } catch (e) {
        console.error("View player error:", e);
    }
}

function openEditPlayerModal(playerId) {
    const p = allPlayers.find(x => x.player_id === playerId);
    if (!p) return;

    document.getElementById("editPlayerId").value = p.player_id;
    document.getElementById("editPlayerName").value = p.full_name || p.name;
    document.getElementById("editPlayerCountry").value = p.nationality || p.country;
    document.getElementById("editPlayerRole").value = p.role;
    document.getElementById("editPlayerDob").value = p.date_of_birth || "";
    document.getElementById("editPlayerBattingStyle").value = p.batting_style || "Right-hand bat";
    document.getElementById("editPlayerBowlingStyle").value = p.bowling_style || "";

    const modal = new bootstrap.Modal(document.getElementById("editPlayerModal"));
    modal.show();
}

async function handleUpdatePlayer(e) {
    e.preventDefault();
    const id = document.getElementById("editPlayerId").value;
    const data = {
        full_name: document.getElementById("editPlayerName").value.trim(),
        nationality: document.getElementById("editPlayerCountry").value.trim(),
        role: document.getElementById("editPlayerRole").value,
        date_of_birth: document.getElementById("editPlayerDob").value || null,
        batting_style: document.getElementById("editPlayerBattingStyle").value,
        bowling_style: document.getElementById("editPlayerBowlingStyle").value
    };

    try {
        const res = await fetch(`${API_BASE}/players/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Player updated successfully!");
            bootstrap.Modal.getInstance(document.getElementById("editPlayerModal")).hide();
            await fetchPlayers();
        } else {
            showToast(json.message || "Failed to update", "danger");
        }
    } catch (err) {
        showToast("Update error", "danger");
    }
}

async function deletePlayer(playerId, name) {
    if (!confirm(`Are you sure you want to remove player "${name}"?`)) return;
    try {
        const res = await fetch(`${API_BASE}/players/${playerId}`, { method: "DELETE" });
        const json = await res.json();
        if (json.success) {
            showToast("Player deleted successfully");
            await fetchPlayers();
        } else {
            showToast(json.message || "Failed to delete player", "danger");
        }
    } catch (e) {
        showToast("Error deleting player", "danger");
    }
}

// ----------------------------------------------------
// 3. TEAMS CONTROLLER (teams.html)
// ----------------------------------------------------
async function initTeamsPage() {
    await fetchTeams();
    document.getElementById("addTeamForm")?.addEventListener("submit", handleAddTeam);
}

async function fetchTeams() {
    try {
        const res = await fetch(`${API_BASE}/teams`);
        const json = await res.json();
        if (json.success) {
            renderTeamsGrid(json.data);
        }
    } catch (e) {
        console.error("Teams fetch error:", e);
    }
}

function renderTeamsGrid(teams) {
    const grid = document.getElementById("teamsGrid");
    if (!grid) return;

    if (teams.length === 0) {
        grid.innerHTML = `<div class="col-12 text-center text-muted py-5">No teams found. Add your first team!</div>`;
        return;
    }

    grid.innerHTML = teams.map(t => {
        const winPct = Number(t.win_percentage || 0).toFixed(1);
        return `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card card-dark h-100 p-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <div class="d-flex align-items-center gap-3">
                        <div class="kpi-icon bg-success bg-opacity-25 text-success rounded-circle">
                            <i class="fas fa-shield-halved"></i>
                        </div>
                        <div>
                            <h5 class="fw-bold mb-0 text-white">${t.team_name}</h5>
                            <span class="badge bg-secondary">${t.team_type || 'International'}</span>
                        </div>
                    </div>
                    <span class="badge bg-primary bg-opacity-25 text-primary border border-primary border-opacity-50">
                        ${t.country || 'N/A'}
                    </span>
                </div>

                <div class="small text-muted mb-3">
                    <div><i class="fas fa-users text-emerald me-2"></i>Squad Members: <strong class="text-light">${t.squad_count || 0} Players</strong></div>
                </div>

                <div class="bg-black bg-opacity-25 p-3 rounded mb-3">
                    <div class="d-flex justify-content-between text-center small mb-2">
                        <div>
                            <div class="text-muted">Played</div>
                            <div class="fw-bold text-white fs-6">${t.matches_played || 0}</div>
                        </div>
                        <div>
                            <div class="text-muted">Won</div>
                            <div class="fw-bold text-emerald fs-6">${t.wins || 0}</div>
                        </div>
                        <div>
                            <div class="text-muted">Lost</div>
                            <div class="fw-bold text-danger fs-6">${t.losses || 0}</div>
                        </div>
                        <div>
                            <div class="text-muted">Win %</div>
                            <div class="fw-bold text-warning fs-6">${winPct}%</div>
                        </div>
                    </div>
                    <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: ${winPct}%"></div>
                    </div>
                </div>

                <div class="mt-auto d-flex gap-2">
                    <button class="btn btn-sm btn-outline-custom flex-grow-1" onclick="viewTeamSquad(${t.team_id})">
                        <i class="fas fa-users-viewfinder me-1"></i>View Squad
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteTeam(${t.team_id}, '${t.team_name}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
        `;
    }).join("");
}

async function handleAddTeam(e) {
    e.preventDefault();
    const data = {
        team_name: document.getElementById("teamName").value.trim(),
        country: document.getElementById("teamCountry").value.trim(),
        team_type: document.getElementById("teamType").value
    };

    try {
        const res = await fetch(`${API_BASE}/teams`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Team added successfully!");
            document.getElementById("addTeamForm").reset();
            bootstrap.Modal.getInstance(document.getElementById("addTeamModal")).hide();
            await fetchTeams();
        } else {
            showToast(json.message || "Failed to add team", "danger");
        }
    } catch (err) {
        showToast("Server error", "danger");
    }
}

async function viewTeamSquad(teamId) {
    try {
        const res = await fetch(`${API_BASE}/teams/${teamId}`);
        const json = await res.json();
        if (!json.success) return showToast("Could not load squad", "danger");

        const { team, squad } = json.data;
        document.getElementById("squadModalTitle").innerText = `${team.team_name} Squad`;

        const squadList = document.getElementById("teamSquadList");
        if (squad.length === 0) {
            squadList.innerHTML = `<div class="text-muted p-3">No players currently registered under nationality '${team.country}'.</div>`;
        } else {
            squadList.innerHTML = squad.map(p => `
                <div class="d-flex justify-content-between align-items-center py-2 border-bottom border-secondary border-opacity-25">
                    <div>
                        <span class="fw-bold text-white me-2">${p.full_name || p.name}</span>
                        <span class="small text-muted">${p.batting_style || ''}</span>
                    </div>
                    <div>${getRoleBadge(p.role)}</div>
                </div>
            `).join("");
        }

        const modal = new bootstrap.Modal(document.getElementById("teamSquadModal"));
        modal.show();
    } catch (e) {
        console.error("View squad error:", e);
    }
}

async function deleteTeam(teamId, name) {
    if (!confirm(`Are you sure you want to delete team "${name}"?`)) return;
    try {
        const res = await fetch(`${API_BASE}/teams/${teamId}`, { method: "DELETE" });
        const json = await res.json();
        if (json.success) {
            showToast("Team deleted successfully");
            await fetchTeams();
        } else {
            showToast(json.message || "Failed to delete team", "danger");
        }
    } catch (e) {
        showToast("Error deleting team", "danger");
    }
}

// ----------------------------------------------------
// 4. MATCHES CONTROLLER (matches.html)
// ----------------------------------------------------
let allMatches = [];

async function initMatchesPage() {
    await loadMatchDropdowns();
    await fetchMatches();

    document.getElementById("filterFormat")?.addEventListener("change", filterMatches);
    document.getElementById("filterStatus")?.addEventListener("change", filterMatches);
    document.getElementById("scheduleMatchForm")?.addEventListener("submit", handleScheduleMatch);
    document.getElementById("recordBattingForm")?.addEventListener("submit", handleRecordBatting);
    document.getElementById("recordBowlingForm")?.addEventListener("submit", handleRecordBowling);
    document.getElementById("addPlayerToMatchForm")?.addEventListener("submit", handleAddPlayerToMatch);

    const params = new URLSearchParams(window.location.search);
    const mId = params.get("match_id");
    if (mId) viewScorecard(mId);
}

async function loadMatchDropdowns() {
    try {
        const [tRes, vRes] = await Promise.all([
            fetch(`${API_BASE}/teams`),
            fetch(`${API_BASE}/venues`)
        ]);
        const tJson = await tRes.json();
        const vJson = await vRes.json();

        if (tJson.success) {
            allTeams = tJson.data;
            const populate = (id) => {
                const el = document.getElementById(id);
                if (!el) return;
                el.innerHTML = `<option value="">Select Team</option>`;
                allTeams.forEach(t => el.innerHTML += `<option value="${t.team_id}">${t.team_name}</option>`);
            };
            populate("matchTeam1");
            populate("matchTeam2");
            populate("matchWinner");
        }

        if (vJson.success) {
            const vEl = document.getElementById("matchVenue");
            if (vEl) {
                vEl.innerHTML = `<option value="">Select Venue</option>`;
                vJson.data.forEach(v => vEl.innerHTML += `<option value="${v.venue_id}">${v.venue_name}, ${v.city}</option>`);
            }
        }
    } catch (e) {
        console.error("Dropdown error:", e);
    }
}

async function fetchMatches() {
    try {
        const res = await fetch(`${API_BASE}/matches`);
        const json = await res.json();
        if (json.success) {
            allMatches = json.data;
            renderMatchesList(allMatches);
        }
    } catch (e) {
        console.error("Fetch matches error:", e);
    }
}

function filterMatches() {
    const fmt = document.getElementById("filterFormat").value;
    const st = document.getElementById("filterStatus").value;

    const filtered = allMatches.filter(m => {
        const matchesFmt = !fmt || (m.format || m.match_format) === fmt;
        const matchesSt = !st || m.status === st;
        return matchesFmt && matchesSt;
    });

    renderMatchesList(filtered);
}

function renderMatchesList(matches) {
    const container = document.getElementById("matchesContainer");
    if (!container) return;

    if (matches.length === 0) {
        container.innerHTML = `<div class="card card-dark p-5 text-center text-muted">No matches found for the selected filter.</div>`;
        return;
    }

    container.innerHTML = matches.map(m => `
        <div class="card match-card p-4 mb-3">
            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
                <div>
                    <div class="d-flex align-items-center gap-2 mb-2">
                        ${getFormatBadge(m.format || m.match_format)}
                        ${getStatusBadge(m.status)}
                        <span class="text-muted small ms-2"><i class="far fa-calendar me-1"></i>${m.match_date}</span>
                        <span class="text-muted small">• <i class="fas fa-location-dot me-1"></i>${m.venue_name || 'TBD'}</span>
                    </div>

                    <div class="d-flex align-items-center gap-3 my-2">
                        <div class="fs-5 fw-bold text-white">${m.match_title || `${m.team1_name} vs ${m.team2_name}`}</div>
                    </div>

                    <div class="text-emerald fw-semibold">
                        <i class="fas fa-trophy text-warning me-1"></i> ${m.result_summary || m.result || (m.status === 'Completed' ? 'Completed' : 'Match Scheduled')}
                    </div>
                </div>

                <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-sm btn-outline-info" onclick="viewScorecard(${m.match_id})">
                        <i class="fas fa-file-lines me-1"></i>Scorecard
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="openRecordScoreModal(${m.match_id}, ${m.team1_id}, ${m.team2_id}, '${m.team1_name}', '${m.team2_name}')">
                        <i class="fas fa-plus me-1"></i>Add Entry
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteMatch(${m.match_id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join("");
}

async function handleScheduleMatch(e) {
    e.preventDefault();
    const data = {
        match_title: document.getElementById("matchTitle").value.trim(),
        match_date: document.getElementById("matchDate").value,
        format: document.getElementById("matchFormat").value,
        venue_id: document.getElementById("matchVenue").value || null,
        team1_id: document.getElementById("matchTeam1").value,
        team2_id: document.getElementById("matchTeam2").value,
        status: document.getElementById("matchStatus").value,
        winner_team_id: document.getElementById("matchWinner").value || null,
        result_summary: document.getElementById("matchResultText").value.trim()
    };

    try {
        const res = await fetch(`${API_BASE}/matches`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Match created successfully!");
            document.getElementById("scheduleMatchForm").reset();
            bootstrap.Modal.getInstance(document.getElementById("scheduleMatchModal")).hide();
            await fetchMatches();
        } else {
            showToast(json.message || "Failed to schedule match", "danger");
        }
    } catch (err) {
        showToast("Error scheduling match", "danger");
    }
}

let currentScorecardData = null;

async function viewScorecard(matchId) {
    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}`);
        const json = await res.json();
        if (!json.success) return showToast("Could not load scorecard", "danger");

        currentScorecardData = json.data;
        const { match, innings, batting, bowling, players } = json.data;

        document.getElementById("scorecardModalTitle").innerText = match.match_title || `${match.team1_name} vs ${match.team2_name}`;
        document.getElementById("scorecardSubTitle").innerText = `${match.format} • ${match.match_date} • ${match.venue_name || 'TBD'}`;
        
        // Live badge & banner
        const isLive = match.status === 'In Progress';
        const liveBadgeEl = document.getElementById("scorecardLiveBadge");
        if (liveBadgeEl) {
            liveBadgeEl.innerHTML = isLive ? `<span class="badge bg-danger bg-opacity-25 text-danger border border-danger border-opacity-50 px-2 py-1"><i class="fas fa-circle live-pulse me-1"></i> LIVE NOW</span>` : '';
        }
        
        const bannerEl = document.getElementById("scorecardResultBanner");
        if (bannerEl) {
            bannerEl.className = isLive 
                ? "alert alert-warning bg-opacity-10 border border-warning border-opacity-25 text-warning fw-bold mb-4" 
                : "alert alert-success bg-opacity-10 border border-success border-opacity-25 text-emerald fw-bold mb-4";
            bannerEl.innerHTML = `<i class="${isLive ? 'fas fa-satellite-dish' : 'fas fa-trophy'} me-2"></i> ${match.result_summary || 'Status: ' + match.status}`;
        }

        // Innings Overview Summary Cards (Total Runs, Wickets, Overs, Run Rate)
        const innContainer = document.getElementById("scorecardInningsOverview");
        if (innContainer) {
            if (innings && innings.length > 0) {
                innContainer.innerHTML = `
                    <div class="row g-3">
                        ${innings.map((inn, idx) => {
                            const isCurrentInnings = isLive && (idx === innings.length - 1);
                            return `
                            <div class="col-md-6">
                                <div class="innings-card ${isCurrentInnings ? 'active-innings' : ''}">
                                    <div class="d-flex justify-content-between align-items-center mb-1">
                                        <span class="text-muted small fw-semibold text-uppercase tracking-wider">Innings ${inn.innings_number}</span>
                                        ${isCurrentInnings ? '<span class="badge bg-danger text-white small px-2 py-0.5"><i class="fas fa-circle live-pulse me-1"></i> Batting</span>' : ''}
                                    </div>
                                    <div class="d-flex justify-content-between align-items-baseline">
                                        <h5 class="fw-bold text-white mb-0">${inn.batting_team_name}</h5>
                                        <div class="fs-4 fw-extrabold text-emerald">
                                            ${inn.total_runs}<span class="text-muted fs-6">/${inn.wickets_lost}</span>
                                            <span class="fs-6 text-muted fw-normal ms-1">(${inn.overs || 0} ov)</span>
                                        </div>
                                    </div>
                                    <div class="d-flex justify-content-between text-muted small mt-2 pt-2 border-top border-secondary border-opacity-25">
                                        <span>Current Run Rate: <strong class="text-light">${inn.run_rate || '0.00'}</strong></span>
                                        <span>Extras: <strong class="text-light">${(inn.wides || 0) + (inn.no_balls || 0) + (inn.byes || 0) + (inn.leg_byes || 0)}</strong></span>
                                    </div>
                                </div>
                            </div>
                            `;
                        }).join("")}
                    </div>
                `;
            } else {
                innContainer.innerHTML = `
                    <div class="card card-dark p-3 text-center text-muted small">
                        <i class="far fa-clock mb-1"></i> Match scheduled. Team scores and overs will appear once innings begin.
                    </div>
                `;
            }
        }

        // Batting Scorecard Table
        const batTbody = document.getElementById("scorecardBattingBody");
        if (!batting || batting.length === 0) {
            batTbody.innerHTML = `<tr><td colspan="7" class="text-center py-3 text-muted">No batting scorecard entries for this match yet.</td></tr>`;
        } else {
            batTbody.innerHTML = batting.map(b => `
                <tr>
                    <td class="fw-bold text-white">
                        ${b.player_name}
                        ${b.is_out ? '' : ' <span class="badge bg-success bg-opacity-25 text-success small py-0 px-1">*</span>'}
                    </td>
                    <td class="text-muted small">${b.batting_team_name || '-'}</td>
                    <td class="text-muted small">${b.dismissal_kind || (b.is_out ? 'out' : 'not out')}</td>
                    <td class="fw-bold text-warning">${b.runs}</td>
                    <td>${b.balls_faced}</td>
                    <td>${b.fours} / ${b.sixes}</td>
                    <td class="fw-semibold text-light">${b.strike_rate || '0.00'}</td>
                </tr>
            `).join("");
        }

        // Bowling Scorecard Table
        const bowlTbody = document.getElementById("scorecardBowlingBody");
        if (!bowling || bowling.length === 0) {
            bowlTbody.innerHTML = `<tr><td colspan="6" class="text-center py-3 text-muted">No bowling scorecard entries for this match yet.</td></tr>`;
        } else {
            bowlTbody.innerHTML = bowling.map(bw => `
                <tr>
                    <td class="fw-bold text-white">${bw.player_name}</td>
                    <td>${bw.overs}</td>
                    <td>${bw.maidens}</td>
                    <td>${bw.runs_conceded}</td>
                    <td class="fw-bold text-emerald">${bw.wickets}</td>
                    <td class="fw-semibold text-light">${bw.economy_rate || '0.00'}</td>
                </tr>
            `).join("");
        }

        // Match Squads & Playing XI Container
        renderMatchSquads(match, players || []);

        const modalEl = document.getElementById("matchScorecardModal");
        let modal = bootstrap.Modal.getInstance(modalEl);
        if (!modal) {
            modal = new bootstrap.Modal(modalEl);
        }
        modal.show();
    } catch (e) {
        console.error("View scorecard error:", e);
        showToast("Error loading match scorecard", "danger");
    }
}

function renderMatchSquads(match, players) {
    const container = document.getElementById("scorecardSquadsContainer");
    if (!container) return;

    // Filter players per team
    const t1Players = players.filter(p => p.team_id === match.team1_id);
    const t2Players = players.filter(p => p.team_id === match.team2_id);

    const renderTeamSquadCard = (teamName, teamId, squad) => {
        const playingXiCount = squad.filter(p => p.playing_xi).length;
        return `
        <div class="col-md-6">
            <div class="squad-card h-100">
                <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-secondary border-opacity-25">
                    <div>
                        <h6 class="fw-bold text-white mb-0">${teamName}</h6>
                        <span class="small text-muted">${squad.length} Players (${playingXiCount} in Playing XI)</span>
                    </div>
                    <button class="btn btn-sm btn-outline-emerald py-0.5 px-2" onclick="openAddPlayerToMatchModal(${match.match_id}, ${teamId})">
                        <i class="fas fa-plus me-1"></i> Add
                    </button>
                </div>

                <div class="squad-list" style="max-height: 260px; overflow-y: auto;">
                    ${squad.length === 0 ? `
                        <div class="text-center text-muted py-3 small">
                            No players assigned to ${teamName} yet.<br>
                            Click <strong>Add</strong> to select or add new players.
                        </div>
                    ` : squad.map(p => `
                        <div class="squad-player-item">
                            <div>
                                <div class="d-flex align-items-center gap-1">
                                    <span class="text-white fw-semibold small">${p.player_name}</span>
                                    ${p.captain ? '<span class="badge-captain">C</span>' : ''}
                                    ${p.wicketkeeper ? '<span class="badge-keeper">WK</span>' : ''}
                                    ${p.playing_xi ? '<span class="badge-xi">XI</span>' : ''}
                                </div>
                                <span class="text-muted" style="font-size: 0.72rem;">${p.role} • ${p.batting_style || 'Right-hand bat'}</span>
                            </div>
                            <div class="d-flex align-items-center gap-2">
                                ${getRoleBadge(p.role)}
                                <button class="btn btn-sm text-danger p-0 border-0" title="Remove from Match" onclick="removePlayerFromMatch(${match.match_id}, ${p.player_id}, '${p.player_name.replace(/'/g, "\\'")}')">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        </div>
                    `).join("")}
                </div>
            </div>
        </div>
        `;
    };

    container.innerHTML = `
        ${renderTeamSquadCard(match.team1_name, match.team1_id, t1Players)}
        ${renderTeamSquadCard(match.team2_name, match.team2_id, t2Players)}
    `;
}

function openAddPlayerToMatchModalFromScorecard() {
    if (!currentScorecardData || !currentScorecardData.match) return;
    openAddPlayerToMatchModal(currentScorecardData.match.match_id);
}

function openRecordScoreModalFromScorecard() {
    if (!currentScorecardData || !currentScorecardData.match) return;
    const m = currentScorecardData.match;
    openRecordScoreModal(m.match_id, m.team1_id, m.team2_id, m.team1_name, m.team2_name);
}

async function openAddPlayerToMatchModal(matchId, preferredTeamId = null) {
    const match = currentScorecardData ? currentScorecardData.match : allMatches.find(m => m.match_id === matchId);
    if (!match) return;

    document.getElementById("addMatchPlayerMatchId").value = match.match_id;

    // Populate team selector
    const teamSelect = document.getElementById("addMatchPlayerTeam");
    if (teamSelect) {
        teamSelect.innerHTML = `
            <option value="${match.team1_id}">${match.team1_name}</option>
            <option value="${match.team2_id}">${match.team2_name}</option>
        `;
        if (preferredTeamId) teamSelect.value = preferredTeamId;
    }

    // Reset radio and form
    document.getElementById("srcExistingPlayer").checked = true;
    togglePlayerSourceMode();

    // Populate existing players
    try {
        const res = await fetch(`${API_BASE}/players`);
        const json = await res.json();
        if (json.success) {
            const selectEl = document.getElementById("addMatchPlayerExisting");
            selectEl.innerHTML = `<option value="">Select Registered Player</option>` + json.data.map(p => `
                <option value="${p.player_id}">${p.full_name || p.name} (${p.role} - ${p.nationality || p.country})</option>
            `).join("");
        }
    } catch (e) {
        console.error("Failed to load players for modal:", e);
    }

    // Reset new player fields
    document.getElementById("addMatchPlayerFullName").value = "";
    document.getElementById("addMatchPlayerRole").value = "Batter";
    document.getElementById("addMatchPlayerNationality").value = "";
    document.getElementById("addMatchPlayerPlayingXi").checked = true;
    document.getElementById("addMatchPlayerCaptain").checked = false;
    document.getElementById("addMatchPlayerWicketkeeper").checked = false;

    const modal = new bootstrap.Modal(document.getElementById("addPlayerToMatchModal"));
    modal.show();
}

function togglePlayerSourceMode() {
    const isNew = document.getElementById("srcNewPlayer").checked;
    const existingSec = document.getElementById("sectionExistingPlayer");
    const newSec = document.getElementById("sectionNewPlayer");

    if (isNew) {
        existingSec.classList.add("d-none");
        newSec.classList.remove("d-none");
    } else {
        existingSec.classList.remove("d-none");
        newSec.classList.add("d-none");
    }
}

async function handleAddPlayerToMatch(e) {
    e.preventDefault();
    const matchId = document.getElementById("addMatchPlayerMatchId").value;
    const teamId = document.getElementById("addMatchPlayerTeam").value;
    const isNew = document.getElementById("srcNewPlayer").checked;

    let payload = {
        team_id: parseInt(teamId),
        playing_xi: document.getElementById("addMatchPlayerPlayingXi").checked ? 1 : 0,
        captain: document.getElementById("addMatchPlayerCaptain").checked ? 1 : 0,
        wicketkeeper: document.getElementById("addMatchPlayerWicketkeeper").checked ? 1 : 0
    };

    if (isNew) {
        const fullName = document.getElementById("addMatchPlayerFullName").value.trim();
        if (!fullName) return showToast("Player full name is required", "warning");

        payload.full_name = fullName;
        payload.role = document.getElementById("addMatchPlayerRole").value;
        payload.batting_style = document.getElementById("addMatchPlayerBattingStyle").value;
        payload.bowling_style = document.getElementById("addMatchPlayerBowlingStyle").value;
        payload.nationality = document.getElementById("addMatchPlayerNationality").value.trim() || null;
    } else {
        const playerId = document.getElementById("addMatchPlayerExisting").value;
        if (!playerId) return showToast("Please select a player", "warning");
        payload.player_id = parseInt(playerId);
    }

    const submitBtn = document.getElementById("btnAddPlayerToMatchSubmit");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin me-1"></i> Saving...`;
    }

    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}/players`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();
        if (json.success) {
            showToast(json.message || "Player added to match and database!");
            const modalEl = document.getElementById("addPlayerToMatchModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            // Refresh scorecard
            await viewScorecard(matchId);
        } else {
            showToast(json.message || "Failed to add player to match", "danger");
        }
    } catch (err) {
        console.error("Add player to match error:", err);
        showToast("Error adding player to match", "danger");
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="fas fa-check me-1"></i> Add to Match Squad`;
        }
    }
}

async function removePlayerFromMatch(matchId, playerId, playerName) {
    if (!confirm(`Are you sure you want to remove "${playerName}" from this match squad?`)) return;

    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}/players/${playerId}`, {
            method: "DELETE"
        });
        const json = await res.json();
        if (json.success) {
            showToast(json.message || "Player removed from match squad");
            await viewScorecard(matchId);
        } else {
            showToast(json.message || "Could not remove player", "danger");
        }
    } catch (err) {
        console.error("Remove player error:", err);
        showToast("Error removing player", "danger");
    }
}

async function openRecordScoreModal(matchId, team1Id, team2Id, team1Name, team2Name) {
    document.getElementById("entryMatchId").value = matchId;
    
    const teamSelects = [document.getElementById("entryBatTeam"), document.getElementById("entryBowlTeam")];
    teamSelects.forEach(sel => {
        sel.innerHTML = `
            <option value="${team1Id}">${team1Name}</option>
            <option value="${team2Id}">${team2Name}</option>
        `;
    });

    await loadPlayersList();

    const modal = new bootstrap.Modal(document.getElementById("recordScoreModal"));
    modal.show();
}

async function loadPlayersList() {
    try {
        const res = await fetch(`${API_BASE}/players`);
        const json = await res.json();
        if (json.success) {
            const players = json.data;
            const batSelect = document.getElementById("entryBatPlayer");
            const bowlSelect = document.getElementById("entryBowlPlayer");
            const opts = players.map(p => `<option value="${p.player_id}">${p.full_name || p.name} (${p.nationality || p.country})</option>`).join("");
            if (batSelect) batSelect.innerHTML = opts;
            if (bowlSelect) bowlSelect.innerHTML = opts;
        }
    } catch (e) {
        console.error("Load players list error:", e);
    }
}

async function handleRecordBatting(e) {
    e.preventDefault();
    const matchId = document.getElementById("entryMatchId").value;
    const data = {
        player_id: document.getElementById("entryBatPlayer").value,
        team_id: document.getElementById("entryBatTeam").value,
        runs: document.getElementById("entryBatRuns").value,
        balls_faced: document.getElementById("entryBatBalls").value,
        fours: document.getElementById("entryBatFours").value,
        sixes: document.getElementById("entryBatSixes").value,
        is_out: document.getElementById("entryBatOut").checked,
        dismissal_kind: document.getElementById("entryBatDismissal").value
    };

    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}/batting`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Batting score recorded successfully!");
            document.getElementById("recordBattingForm").reset();
            // Automatically refresh scorecard if open
            if (currentScorecardData && currentScorecardData.match && String(currentScorecardData.match.match_id) === String(matchId)) {
                await viewScorecard(matchId);
            }
        } else {
            showToast(json.message || "Failed to record score", "danger");
        }
    } catch (err) {
        showToast("Error recording batting", "danger");
    }
}

async function handleRecordBowling(e) {
    e.preventDefault();
    const matchId = document.getElementById("entryMatchId").value;
    const data = {
        player_id: document.getElementById("entryBowlPlayer").value,
        team_id: document.getElementById("entryBowlTeam").value,
        overs: document.getElementById("entryBowlOvers").value,
        maidens: document.getElementById("entryBowlMaidens").value,
        runs_conceded: document.getElementById("entryBowlRuns").value,
        wickets: document.getElementById("entryBowlWickets").value
    };

    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}/bowling`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast("Bowling spell recorded successfully!");
            document.getElementById("recordBowlingForm").reset();
            // Automatically refresh scorecard if open
            if (currentScorecardData && currentScorecardData.match && String(currentScorecardData.match.match_id) === String(matchId)) {
                await viewScorecard(matchId);
            }
        } else {
            showToast(json.message || "Failed to record bowling", "danger");
        }
    } catch (err) {
        showToast("Error recording bowling", "danger");
    }
}

async function deleteMatch(matchId) {
    if (!confirm("Are you sure you want to delete this match?")) return;
    try {
        const res = await fetch(`${API_BASE}/matches/${matchId}`, { method: "DELETE" });
        const json = await res.json();
        if (json.success) {
            showToast("Match deleted successfully");
            await fetchMatches();
        } else {
            showToast(json.message || "Failed to delete", "danger");
        }
    } catch (e) {
        showToast("Error deleting match", "danger");
    }
}

// ----------------------------------------------------
// 5. STATISTICS CONTROLLER (statistics.html)
// ----------------------------------------------------
async function initStatisticsPage() {
    await Promise.all([
        loadTopBatsmen(),
        loadTopBowlers(),
        loadHighestScores(),
        loadBestStrikeRates(),
        loadTeamStandings()
    ]);
}

function getRankBadge(index) {
    if (index === 0) return `<span class="rank-badge rank-1"><i class="fas fa-crown"></i></span>`;
    if (index === 1) return `<span class="rank-badge rank-2">2</span>`;
    if (index === 2) return `<span class="rank-badge rank-3">3</span>`;
    return `<span class="rank-badge rank-other">${index + 1}</span>`;
}

async function loadTopBatsmen() {
    try {
        const res = await fetch(`${API_BASE}/stats/top-batsmen`);
        const json = await res.json();
        const tbody = document.getElementById("topBatsmenTable");
        if (!tbody || !json.success) return;

        tbody.innerHTML = json.data.map((b, idx) => `
            <tr>
                <td class="text-center">${getRankBadge(idx)}</td>
                <td>
                    <div class="fw-bold text-white">${b.player_name}</div>
                    <span class="small text-muted">${b.country}</span>
                </td>
                <td class="fw-bold text-warning fs-6">${b.total_runs}</td>
                <td>${b.innings}</td>
                <td>${b.highest_score}</td>
                <td>${b.batting_average}</td>
                <td>${b.strike_rate}</td>
                <td>${b.centuries} / ${b.half_centuries}</td>
                <td>${b.total_fours} / ${b.total_sixes}</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Top batsmen error:", e);
    }
}

async function loadTopBowlers() {
    try {
        const res = await fetch(`${API_BASE}/stats/top-bowlers`);
        const json = await res.json();
        const tbody = document.getElementById("topBowlersTable");
        if (!tbody || !json.success) return;

        tbody.innerHTML = json.data.map((bw, idx) => `
            <tr>
                <td class="text-center">${getRankBadge(idx)}</td>
                <td>
                    <div class="fw-bold text-white">${bw.player_name}</div>
                    <span class="small text-muted">${bw.country}</span>
                </td>
                <td class="fw-bold text-emerald fs-6">${bw.total_wickets}</td>
                <td>${bw.total_overs}</td>
                <td>${bw.total_maidens}</td>
                <td>${bw.runs_conceded}</td>
                <td>${bw.bowling_average}</td>
                <td>${bw.economy_rate}</td>
                <td>${bw.five_wicket_hauls}</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Top bowlers error:", e);
    }
}

async function loadHighestScores() {
    try {
        const res = await fetch(`${API_BASE}/stats/highest-scores`);
        const json = await res.json();
        const tbody = document.getElementById("highestScoresTable");
        if (!tbody || !json.success) return;

        tbody.innerHTML = json.data.map((hs, idx) => `
            <tr>
                <td class="text-center">${getRankBadge(idx)}</td>
                <td>
                    <div class="fw-bold text-white">${hs.player_name}</div>
                    <span class="small text-muted">${hs.country}</span>
                </td>
                <td class="fw-bold text-warning fs-6">${hs.runs}</td>
                <td>${hs.balls}</td>
                <td>${hs.strike_rate}</td>
                <td>${hs.fours} / ${hs.sixes}</td>
                <td>${hs.match_format}</td>
                <td class="text-muted small">${hs.venue_name || 'TBD'}</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Highest scores error:", e);
    }
}

async function loadBestStrikeRates() {
    try {
        const res = await fetch(`${API_BASE}/stats/top-strike-rates`);
        const json = await res.json();
        const tbody = document.getElementById("strikeRatesTable");
        if (!tbody || !json.success) return;

        tbody.innerHTML = json.data.map((sr, idx) => `
            <tr>
                <td class="text-center">${getRankBadge(idx)}</td>
                <td class="fw-bold text-white">${sr.player_name} <span class="small text-muted">(${sr.country})</span></td>
                <td class="fw-bold text-info">${sr.strike_rate}</td>
                <td>${sr.total_runs}</td>
                <td>${sr.balls_faced}</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Strike rates error:", e);
    }
}

async function loadTeamStandings() {
    try {
        const res = await fetch(`${API_BASE}/stats/team-rankings`);
        const json = await res.json();
        const tbody = document.getElementById("teamStandingsTable");
        if (!tbody || !json.success) return;

        tbody.innerHTML = json.data.map((t, idx) => `
            <tr>
                <td class="text-center">${getRankBadge(idx)}</td>
                <td class="fw-bold text-white">${t.team_name}</td>
                <td>${t.matches_played}</td>
                <td class="fw-bold text-emerald">${t.wins}</td>
                <td class="text-danger">${t.losses}</td>
                <td class="fw-bold text-warning">${t.win_percentage}%</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Team standings error:", e);
    }
}
