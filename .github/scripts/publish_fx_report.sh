#!/usr/bin/env bash

# Copyright (c) 2026 s0llarr
# Licensed under the MIT License.


set -Eeuo pipefail

BASE="${BASE:-EUR}"
QUOTES="${QUOTES:-USD,GBP,CHF}"
DAYS="${DAYS:-1}"

OUTPUT="${OUTPUT:-output/fx_report.md}"
ERROR_OUTPUT="${ERROR_OUTPUT:-output/fx_report_error.md}"
HISTORY_BRANCH="${HISTORY_BRANCH:-report-history}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"
PUBLISH_MAIN="${PUBLISH_MAIN:-false}"
COMMIT_KIND="${COMMIT_KIND:-report}"

FX_REPORT_PYTHON="${FX_REPORT_PYTHON:-python}"
FX_REPORT_MODULE="${FX_REPORT_MODULE:-fx_report}"

GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-github-actions[bot]}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-41898282+github-actions[bot]@users.noreply.github.com}"

log() {
  printf '[fx-report] %s\n' "$*"
}

is_ci() {
  [[ "${GITHUB_ACTIONS:-false}" == "true" ]]
}

ensure_git_repo() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    || { echo "Not a git repository" >&2; exit 1; }
}

git_identity() {
  git config user.name "$GIT_AUTHOR_NAME"
  git config user.email "$GIT_AUTHOR_EMAIL"
}

checkout_main_branch() {
  git fetch origin "$MAIN_BRANCH" >/dev/null

  if is_ci; then
    git switch -C "$MAIN_BRANCH" "origin/$MAIN_BRANCH"
    git reset --hard "origin/$MAIN_BRANCH"
  else
    git switch "$MAIN_BRANCH" 2>/dev/null || true
  fi
}

prepare_output_dir() {
  mkdir -p "$(dirname "$OUTPUT")" "$(dirname "$ERROR_OUTPUT")"
}

# Conventional Commit builder

build_commit_message() {
  local status="$1"

  local type subject

  case "$status" in
    success)
      type="chore"
      if [[ "$DAYS" == "5" ]]; then
        subject="publish weekend FX report"
      else
        subject="publish daily FX report"
      fi
      ;;
    error)
      type="fix"
      subject="record FX report generation failure"
      ;;
  esac

  printf '%s(fx-report): %s' "$type" "$subject"
}

report_timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

report_body() {
  local status="$1"
  local artifact_path="$2"

  cat <<EOF
FX Report Metadata
------------------
base: ${BASE}
quotes: ${QUOTES}
days: ${DAYS}
status: ${status}
timestamp: $(report_timestamp)
artifact: ${artifact_path}
EOF
}

# Report generation

generate_report() {
  log "Generating report (base=$BASE quotes=$QUOTES days=$DAYS)"

  "$FX_REPORT_PYTHON" -m "$FX_REPORT_MODULE" \
    --base "$BASE" \
    --quotes "$QUOTES" \
    --days "$DAYS" \
    --output "$OUTPUT" \
    --error-output "$ERROR_OUTPUT"
}

# History branch publishing

push_history_artifact() {
  local artifact_path="$1"
  local commit_header="$2"
  local commit_body="$3"

  local history_worktree
  history_worktree="$(mktemp -d "${RUNNER_TEMP:-/tmp}/fx-report-history.XXXXXX")"

  cleanup_history_worktree() {
    if [[ -n "${history_worktree:-}" && -d "${history_worktree:-}" ]]; then
      git worktree remove --force "$history_worktree" >/dev/null 2>&1 || true
      rm -rf "$history_worktree" || true
    fi
  }

  trap cleanup_history_worktree RETURN

  if git ls-remote --exit-code --heads origin "$HISTORY_BRANCH" >/dev/null 2>&1; then
    git fetch origin "$HISTORY_BRANCH":"refs/heads/$HISTORY_BRANCH"
    git worktree add "$history_worktree" "$HISTORY_BRANCH"
  else
    git worktree add -b "$HISTORY_BRANCH" "$history_worktree" "$MAIN_BRANCH"
  fi

  mkdir -p "$history_worktree/$(dirname "$artifact_path")"
  cp -a "$artifact_path" "$history_worktree/$artifact_path"

  git -C "$history_worktree" add "$artifact_path"

  if git -C "$history_worktree" diff --cached --quiet -- "$artifact_path"; then
    log "No changes detected for $HISTORY_BRANCH"
    return 0
  fi

  git -C "$history_worktree" commit -m "$commit_header" -m "$commit_body"
  git -C "$history_worktree" push origin "$HISTORY_BRANCH"
}

# Main branch publishing

push_main_artifact() {
  local commit_header="$1"
  local commit_body="$2"

  git add "$OUTPUT"

  if git diff --cached --quiet -- "$OUTPUT"; then
    log "No changes detected for $MAIN_BRANCH"
    return 0
  fi

  git commit -m "$commit_header" -m "$commit_body"
  git push origin "$MAIN_BRANCH"
}

# Main

main() {
  ensure_git_repo
  git_identity
  checkout_main_branch
  prepare_output_dir

  local artifact_path report_status exit_code

  if generate_report; then
    artifact_path="$OUTPUT"
    report_status="success"
    exit_code=0
  else
    artifact_path="$ERROR_OUTPUT"
    report_status="error"
    exit_code=1
  fi

  [[ -e "$artifact_path" ]] || {
    echo "Expected artifact not found: $artifact_path" >&2
    exit 1
  }

  local commit_header
  commit_header="$(build_commit_message "$report_status")"

  local commit_body
  commit_body="$(report_body "$report_status" "$artifact_path")"

  push_history_artifact "$artifact_path" "$commit_header" "$commit_body"

  if [[ "$PUBLISH_MAIN" == "true" && "$report_status" == "success" ]]; then
    push_main_artifact "$commit_header" "$commit_body"
  fi

  log "Done."
  return "$exit_code"
}

main "$@"
