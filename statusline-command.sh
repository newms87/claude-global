#!/usr/bin/env bash
# Claude Code status line script
# Displays: model, context (tokens + %), rate limits, session elapsed, git branch, memory, CPU

input=$(cat)

# --- Model (short name, strip context-window suffix like " (1M context)") ---
model=$(echo "$input" | jq -r '.model.display_name // "Unknown"' | sed 's/ ([0-9.]\+[kKmMbB]\? context)//I')

# --- Working directory relative to project root ---
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // empty')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir // empty')
rel_dir=""
if [ -n "$current_dir" ] && [ -n "$project_dir" ]; then
  project_basename=$(basename "$project_dir")
  if [ "$current_dir" = "$project_dir" ]; then
    rel_dir="$project_basename"
  else
    # Check if current_dir starts with project_dir + /
    case "$current_dir" in
      "$project_dir"/*)
        rel_dir="${project_basename}/${current_dir#$project_dir/}"
        ;;
      *)
        # current_dir is outside project_dir — show absolute path as fallback
        rel_dir="$current_dir"
        ;;
    esac
  fi
fi

# --- Context window usage: tokens + percentage ---
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_window_size=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
# Sum all current_usage fields for true token count
total_tokens=$(echo "$input" | jq -r '
  .context_window.current_usage |
  if . then
    ((.input_tokens // 0) + (.output_tokens // 0) +
     (.cache_creation_input_tokens // 0) + (.cache_read_input_tokens // 0))
  else empty end')
if [ -n "$used_pct" ] && [ -n "$total_tokens" ] && [ "$total_tokens" -gt 0 ] 2>/dev/null; then
  # Format token count: >= 1000000 → X.XM, >= 1000 → Xk
  if [ "$total_tokens" -ge 1000000 ] 2>/dev/null; then
    tok_fmt=$(awk "BEGIN {printf \"%.1fM\", $total_tokens / 1000000}")
  elif [ "$total_tokens" -ge 1000 ] 2>/dev/null; then
    tok_fmt=$(awk "BEGIN {printf \"%.0fk\", $total_tokens / 1000}")
  else
    tok_fmt="$total_tokens"
  fi
  ctx="${tok_fmt}"
elif [ -n "$used_pct" ]; then
  ctx="${used_pct}%"
else
  ctx="--"
fi

# --- Rate limits: 5-hour session and 7-day weekly (with time-until-reset) ---
five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_resets=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
week_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
week_resets=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')

_fmt_reset() {
  local resets_at="$1"
  if [ -z "$resets_at" ] || ! [[ "$resets_at" =~ ^[0-9]+$ ]]; then
    return
  fi
  local now
  now=$(date +%s)
  local secs=$(( resets_at - now ))
  if [ "$secs" -le 0 ]; then
    echo "now"
    return
  fi
  local h=$(( secs / 3600 ))
  local m=$(( (secs % 3600) / 60 ))
  if [ "$h" -gt 0 ]; then
    echo "${h}h${m}m"
  else
    echo "${m}m"
  fi
}

rate_out=""
if [ -n "$five_pct" ]; then
  five_reset_str=$(_fmt_reset "$five_resets")
  if [ -n "$five_reset_str" ]; then
    rate_out="5h:$(printf '%.0f' "$five_pct")% (${five_reset_str})"
  else
    rate_out="5h:$(printf '%.0f' "$five_pct")%"
  fi
fi
if [ -n "$week_pct" ]; then
  [ -n "$rate_out" ] && rate_out="$rate_out "
  week_reset_str=$(_fmt_reset "$week_resets")
  if [ -n "$week_reset_str" ]; then
    rate_out="${rate_out}7d:$(printf '%.0f' "$week_pct")% (${week_reset_str})"
  else
    rate_out="${rate_out}7d:$(printf '%.0f' "$week_pct")%"
  fi
fi

# --- Session elapsed time (keyed by session_id so each new session resets) ---
session_id=$(echo "$input" | jq -r '.session_id // empty')
now_epoch=$(date +%s)
if [ -n "$session_id" ]; then
  session_start_file="$HOME/.claude/.statusline-session-${session_id}"
  if [ ! -f "$session_start_file" ]; then
    # Clean up stale session files (keep last 10)
    ls -t "$HOME/.claude/.statusline-session-"* 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
    echo "$now_epoch" > "$session_start_file"
    session_start=$now_epoch
  else
    session_start=$(cat "$session_start_file" 2>/dev/null)
    if ! [[ "$session_start" =~ ^[0-9]+$ ]]; then
      echo "$now_epoch" > "$session_start_file"
      session_start=$now_epoch
    fi
  fi
else
  # Fallback: no session_id — use legacy single-file approach
  session_start_file="$HOME/.claude/.statusline-session-start"
  if [ ! -f "$session_start_file" ]; then
    echo "$now_epoch" > "$session_start_file"
    session_start=$now_epoch
  else
    session_start=$(cat "$session_start_file" 2>/dev/null)
    if ! [[ "$session_start" =~ ^[0-9]+$ ]]; then
      echo "$now_epoch" > "$session_start_file"
      session_start=$now_epoch
    fi
  fi
fi
elapsed=$(( now_epoch - session_start ))
elapsed_h=$(( elapsed / 3600 ))
elapsed_m=$(( (elapsed % 3600) / 60 ))
if [ "$elapsed_h" -gt 0 ]; then
  session_time="${elapsed_h}h${elapsed_m}m"
else
  session_time="${elapsed_m}m"
fi

# --- Git branch + dirty indicator + line change counts ---
# Use the cwd from JSON if available, otherwise rely on shell cwd
git_cwd=$(echo "$input" | jq -r '.workspace.current_dir // empty')
git_out=""
if [ -n "$git_cwd" ] && [ -d "$git_cwd" ]; then
  git_branch=$(git -C "$git_cwd" symbolic-ref --short HEAD 2>/dev/null)
else
  git_branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  git_cwd="."
fi
if [ -n "$git_branch" ]; then
  # Check dirty (fast — only index + worktree, skip optional locks)
  if git -C "$git_cwd" diff --quiet HEAD 2>/dev/null; then
    dirty=""
  else
    dirty="*"
  fi
  # Line change counts from diff stat (added/removed)
  diff_stat=$(git -C "$git_cwd" diff --shortstat HEAD 2>/dev/null)
  added=$(echo "$diff_stat" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+')
  removed=$(echo "$diff_stat" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+')
  if [ -n "$added" ] || [ -n "$removed" ]; then
    added=${added:-0}
    removed=${removed:-0}
    git_changes="\033[0;32m+${added}\033[0m/\033[0;31m-${removed}\033[0m"
    git_out="${git_branch}${dirty} ${git_changes}"
  else
    git_out="${git_branch}${dirty}"
  fi
fi

# --- Memory usage ---
mem_kb=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
mem_total_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
if [ -n "$mem_kb" ] && [ -n "$mem_total_kb" ]; then
  mem_used_kb=$(( mem_total_kb - mem_kb ))
  mem_used_gb=$(awk "BEGIN {printf \"%.1f\", $mem_used_kb / 1048576}")
  mem_total_gb=$(awk "BEGIN {printf \"%.1f\", $mem_total_kb / 1048576}")
  mem_out="Mem: ${mem_used_gb}/${mem_total_gb}GB"
else
  mem_out="Mem: --"
fi

# --- CPU load average (1-minute) ---
cpu_load=$(awk '{print $1}' /proc/loadavg 2>/dev/null)
if [ -n "$cpu_load" ]; then
  cpu_out="CPU: ${cpu_load}"
else
  cpu_out=""
fi

# --- Assemble output with colors ---
# Colors (will appear dimmed in status line):
#   Cyan for model, Yellow for context, Magenta for rate limits,
#   Blue for session time, Yellow/White for git, Green for memory+CPU
SEP="\033[0;37m | \033[0m"

printf "\033[0;36m%s\033[0m" "$model"
if [ -n "$rel_dir" ]; then
  printf "%b" "$SEP"
  printf "\033[0;37m%s\033[0m" "$rel_dir"
fi
printf "%b" "$SEP"
printf "\033[0;34m%s\033[0m" "$session_time"
printf "%b" "$SEP"
printf "\033[0;33m%s\033[0m" "$ctx"
if [ -n "$rate_out" ]; then
  printf "%b" "$SEP"
  printf "\033[0;35m%s\033[0m" "$rate_out"
fi
if [ -n "$git_out" ]; then
  printf "%b" "$SEP"
  printf "\033[0;33m%b\033[0m" "$git_out"
fi
printf "%b" "$SEP"
printf "\033[0;32m%s\033[0m" "$mem_out"
if [ -n "$cpu_out" ]; then
  printf " \033[0;32m%s\033[0m" "$cpu_out"
fi
